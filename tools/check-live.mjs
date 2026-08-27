/* Acceptance run against the LIVE url in real Chrome. The in-app pane freezes
   scroll clocks and had already fired load, so it cannot judge a deep link. */
import { spawn } from 'node:child_process';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9225;
const BASE = 'https://businessboosterlk.github.io/shwoah/';

const chrome = spawn(CHROME, ['--headless=new','--disable-gpu',
  `--remote-debugging-port=${PORT}`,'--no-first-run',
  '--user-data-dir=/tmp/shwoah-live-profile','about:blank'], { stdio:'ignore' });
process.on('exit', () => chrome.kill());
const wait = ms => new Promise(r => setTimeout(r, ms));
async function ready(){ const end = Date.now.call(null)+30000;
  for(;;){ try{ if((await fetch(`http://localhost:${PORT}/json/version`)).ok) return; }catch{}
    if(Date.now.call(null)>end) throw new Error('no chrome'); await wait(300);} }
async function cdp(ws,m,p={}){ const id=++ws._id; ws.send(JSON.stringify({id,method:m,params:p}));
  return new Promise((res,rej)=>ws._p.set(id,{res,rej})); }
async function open(url){
  const t = await (await fetch(`http://localhost:${PORT}/json/new?${encodeURIComponent(url)}`,{method:'PUT'})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); ws._id=0; ws._p=new Map();
  ws.addEventListener('message',ev=>{const m=JSON.parse(ev.data);
    if(m.id&&ws._p.has(m.id)){const p=ws._p.get(m.id);ws._p.delete(m.id);
      m.error?p.rej(new Error(m.error.message)):p.res(m.result);}});
  await new Promise(r=>ws.addEventListener('open',r,{once:true}));
  return {ws,tabId:t.id};
}
async function evaluate(ws, expr){
  const r = await cdp(ws,'Runtime.evaluate',{returnByValue:true,expression:expr,awaitPromise:true});
  return r.result.value;
}

await ready();
const cases = [
  ['#salon','salon'], ['#bridal','bridal'], ['#concept-store','concept-store']
];
for (const [hash,id] of cases) {
  const { ws, tabId } = await open(BASE + hash);
  await cdp(ws,'Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await wait(3200);
  const v = await evaluate(ws, `(() => {
    const el = document.getElementById(${JSON.stringify(id)});
    return JSON.stringify({ top: Math.round(el.getBoundingClientRect().top),
      y: Math.round(scrollY), hash: location.hash,
      focus: document.activeElement.tagName + ':' + document.activeElement.textContent.trim().slice(0,24),
      hero: document.querySelector('.hero-frame img').naturalWidth });
  })()`);
  console.log(hash.padEnd(16), v);
  ws.close(); await fetch(`http://localhost:${PORT}/json/close/${tabId}`);
}
// keyboard: tab order reaches the three doors early and focus is visible
{
  const { ws, tabId } = await open(BASE);
  await cdp(ws,'Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await wait(2500);
  const order = [];
  for (let i=0;i<7;i++){
    await cdp(ws,'Input.dispatchKeyEvent',{type:'rawKeyDown',windowsVirtualKeyCode:9,key:'Tab',code:'Tab'});
    await cdp(ws,'Input.dispatchKeyEvent',{type:'keyUp',windowsVirtualKeyCode:9,key:'Tab',code:'Tab'});
    order.push(await evaluate(ws,`(()=>{const a=document.activeElement;
      const cs=getComputedStyle(a);
      return (a.getAttribute('href')||a.className||a.tagName).toString().slice(0,26)
        + (cs.outlineStyle!=='none'||cs.boxShadow!=='none' ? ' [focus visible]' : ' [NO RING]');})()`));
  }
  console.log('tab order:', order.join(' | '));
  ws.close(); await fetch(`http://localhost:${PORT}/json/close/${tabId}`);
}
chrome.kill();
console.log('live acceptance done');
