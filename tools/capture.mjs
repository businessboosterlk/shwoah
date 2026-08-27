/* Full-page capture over CDP. Node 22, no dependencies.
   Usage: node tools/capture.mjs
   Chrome must NOT already hold the port. Writes PNGs to tools/shots/. */
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9223;
const BASE = 'http://localhost:4641/';
const OUT = new URL('./shots/', import.meta.url).pathname;
mkdirSync(OUT, { recursive: true });

const SHOTS = [
  { name: 'all-1440',        url: '?capture=1',                    w: 1440, h: 1000 },
  { name: 'all-390',         url: '?capture=1',                    w: 390,  h: 844  },
  { name: 'all-768',         url: '?capture=1',                    w: 768,  h: 1024 },
  { name: 'salon-1440',      url: '?service=salon&capture=1',      w: 1440, h: 1000 },
  { name: 'salon-390',       url: '?service=salon&capture=1',      w: 390,  h: 844  },
  { name: 'bridal-1440',     url: '?service=bridal&capture=1',     w: 1440, h: 1000 },
  { name: 'bridal-390',      url: '?service=bridal&capture=1',     w: 390,  h: 844  },
  { name: 'concept-1440',    url: '?service=concept&capture=1',    w: 1440, h: 1000 },
  { name: 'salon-dev-1440',  url: '?service=salon&capture=1&preview=dev', w: 1440, h: 1000 },
  { name: 'all-320',         url: '?capture=1',                    w: 320,  h: 700  },
];

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', `--remote-debugging-port=${PORT}`,
  '--no-first-run', '--user-data-dir=/tmp/shwoah-cap-83309', 'about:blank'
], { stdio: 'ignore' });
process.on('exit', () => chrome.kill());

const wait = ms => new Promise(r => setTimeout(r, ms));

async function cdp(ws, method, params = {}) {
  const id = ++ws._id;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => {
    ws._pending.set(id, { resolve, reject });
  });
}

async function connect(url) {
  const res = await fetch(`http://localhost:${PORT}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
  const tab = await res.json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  ws._id = 0; ws._pending = new Map();
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && ws._pending.has(m.id)) {
      const p = ws._pending.get(m.id); ws._pending.delete(m.id);
      m.error ? p.reject(new Error(m.error.message)) : p.resolve(m.result);
    }
  });
  await new Promise(r => ws.addEventListener('open', r, { once: true }));
  return { ws, tabId: tab.id };
}

async function shot({ name, url, w, h }) {
  const { ws, tabId } = await connect(BASE + url);
  await cdp(ws, 'Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: w < 768 });
  await cdp(ws, 'Page.enable');
  await wait(1200);
  /* lazy images never decode inside captureBeyondViewport: force them eager and
     wait for every one to finish, or the shot lies about a working page */
  await cdp(ws, 'Runtime.evaluate', {
    expression: `(async () => {
      document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
      await Promise.all([...document.images].map(i => i.complete ? null :
        new Promise(r => { i.addEventListener('load', r, {once:true});
                           i.addEventListener('error', r, {once:true}); })));
      if (document.fonts) await document.fonts.ready;
    })()`, awaitPromise: true
  });
  await wait(900);
  const metrics = await cdp(ws, 'Page.getLayoutMetrics');
  const full = Math.min(Math.ceil(metrics.cssContentSize.height), 12000);
  const png = await cdp(ws, 'Page.captureScreenshot', {
    format: 'png',
    clip: { x: 0, y: 0, width: w, height: full, scale: 1 },
    captureBeyondViewport: true
  });
  writeFileSync(OUT + name + '.png', Buffer.from(png.data, 'base64'));
  const overflow = await cdp(ws, 'Runtime.evaluate', {
    expression: 'document.documentElement.scrollWidth + "/" + window.innerWidth', returnByValue: true
  });
  console.log(name, 'h=' + full, 'scrollW/innerW=' + overflow.result.value);
  ws.close();
  await fetch(`http://localhost:${PORT}/json/close/${tabId}`);
}

/* Poll until Chrome answers on the debug port. A fixed sleep raced a cold start and
   failed with ECONNREFUSED; how long Chrome takes to bind is not ours to guess. */
async function waitForChrome(timeoutMs = 30000) {
  const deadline = Date.now.call(null) + timeoutMs;
  for (;;) {
    try {
      const r = await fetch(`http://localhost:${PORT}/json/version`);
      if (r.ok) return;
    } catch {}
    if (Date.now.call(null) > deadline) throw new Error('Chrome never bound port ' + PORT);
    await wait(300);
  }
}
await waitForChrome();
for (const s of SHOTS) await shot(s);
chrome.kill();
console.log('done');
