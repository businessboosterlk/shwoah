/* Deep-link acceptance: opening /#bridal must OPEN AT bridal, not at the hero.
   The in-app pane freezes the smooth-scroll clock, so this is the surface that
   can actually answer it. */
import { spawn } from 'node:child_process';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9225, BASE = 'http://localhost:4641/';
const chrome = spawn(CHROME, ['--headless=new','--disable-gpu',
  `--remote-debugging-port=${PORT}`,'--no-first-run',
  '--user-data-dir=/tmp/shwoah-anchor-profile','about:blank'], { stdio:'ignore' });
process.on('exit', () => chrome.kill());
const wait = ms => new Promise(r => setTimeout(r, ms));
for (let i = 0; i < 100; i++) {
  try { if ((await fetch(`http://localhost:${PORT}/json/version`)).ok) break; } catch {}
  await wait(300);
}
async function cdp(ws, method, params = {}) {
  const id = ++ws._id; ws.send(JSON.stringify({ id, method, params }));
  return new Promise((res, rej) => ws._p.set(id, { res, rej }));
}
for (const hash of ['#salon', '#bridal', '#concept-store']) {
  const tab = await (await fetch(`http://localhost:${PORT}/json/new?${encodeURIComponent(BASE + hash)}`, { method:'PUT' })).json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  ws._id = 0; ws._p = new Map();
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data);
    if (m.id && ws._p.has(m.id)) { const p = ws._p.get(m.id); ws._p.delete(m.id);
      m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); } });
  await new Promise(r => ws.addEventListener('open', r, { once:true }));
  await cdp(ws, 'Emulation.setDeviceMetricsOverride', { width:1280, height:900, deviceScaleFactor:1, mobile:false });
  await wait(2600);
  const v = (await cdp(ws, 'Runtime.evaluate', { returnByValue:true, expression:`(() => {
    const el = document.querySelector('${hash}');
    const top = Math.round(el.getBoundingClientRect().top);
    return { hash: location.hash, sectionTopInViewport: top,
             openedAtSection: Math.abs(top) < 120, scrollY: Math.round(scrollY),
             focused: (document.activeElement.textContent||'').trim().slice(0,30) };
  })()` })).result.value;
  console.log(hash, JSON.stringify(v));
  ws.close();
  await fetch(`http://localhost:${PORT}/json/close/${tab.id}`);
}
chrome.kill();
