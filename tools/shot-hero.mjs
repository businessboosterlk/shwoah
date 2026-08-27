/* Viewport-only hero shots at several widths, through real Chrome over CDP.
   The full-page capture is useless for judging a 100svh hero, and the in-app
   pane has its own paint quirks, so this is the surface that decides. */
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9224;
const BASE = 'http://localhost:4641/';
const OUT = new URL('./shots/', import.meta.url).pathname;
mkdirSync(OUT, { recursive: true });

const SIZES = [
  { name: 'hero-1440', w: 1440, h: 900 },
  { name: 'hero-1280', w: 1280, h: 800 },
  { name: 'hero-768',  w: 768,  h: 1024 },
  { name: 'hero-390',  w: 390,  h: 844 },
  { name: 'hero-320',  w: 320,  h: 700 },
];

const chrome = spawn(CHROME, ['--headless=new','--disable-gpu',
  `--remote-debugging-port=${PORT}`,'--no-first-run',
  '--user-data-dir=/tmp/shwoah-hero-profile','about:blank'], { stdio:'ignore' });
process.on('exit', () => chrome.kill());
const wait = ms => new Promise(r => setTimeout(r, ms));

async function ready(t = 30000) {
  const end = Date.now.call(null) + t;
  for (;;) {
    try { const r = await fetch(`http://localhost:${PORT}/json/version`); if (r.ok) return; } catch {}
    if (Date.now.call(null) > end) throw new Error('chrome never bound');
    await wait(300);
  }
}
async function cdp(ws, method, params = {}) {
  const id = ++ws._id;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((res, rej) => ws._p.set(id, { res, rej }));
}
async function open(url) {
  const tab = await (await fetch(`http://localhost:${PORT}/json/new?${encodeURIComponent(url)}`, { method:'PUT' })).json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  ws._id = 0; ws._p = new Map();
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && ws._p.has(m.id)) { const p = ws._p.get(m.id); ws._p.delete(m.id);
      m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); }
  });
  await new Promise(r => ws.addEventListener('open', r, { once:true }));
  return { ws, tabId: tab.id };
}

await ready();
for (const s of SIZES) {
  const { ws, tabId } = await open(BASE);
  await cdp(ws, 'Emulation.setDeviceMetricsOverride',
    { width:s.w, height:s.h, deviceScaleFactor:1, mobile:s.w < 768 });
  await wait(1800);
  const probe = await cdp(ws, 'Runtime.evaluate', { returnByValue:true, expression:`(() => {
    const i = document.querySelector('.hero-frame img');
    const widest = [...document.querySelectorAll('body *')]
      .map(e => ({ w: Math.round(e.getBoundingClientRect().right), t: e.className || e.tagName }))
      .filter(x => x.w > innerWidth + 1).sort((a,b) => b.w - a.w).slice(0,3);
    return { src: i && i.currentSrc.split('/').pop(), nat: i && i.naturalWidth,
             layout: innerWidth, scrollW: document.documentElement.scrollWidth,
             over: JSON.stringify(widest) };
  })()` });
  console.log(s.name, JSON.stringify(probe.result.value));
  const png = await cdp(ws, 'Page.captureScreenshot', { format:'png' });
  writeFileSync(OUT + s.name + '.png', Buffer.from(png.data, 'base64'));
  ws.close();
  await fetch(`http://localhost:${PORT}/json/close/${tabId}`);
}
chrome.kill();
console.log('done');
