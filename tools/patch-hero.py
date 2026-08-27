"""Rebuild the opening as the real building, and convert the site from swapped
modes to one page with anchored sections (#salon, #bridal, #concept-store).

Door coordinates were measured off the original 1551x1014 photograph by cropping
each storefront and reading its edges, not estimated by eye:
  Bridal        sign+door  x 545-595   y 435-695
  Concept store sign+door  x 720-825   y 350-745
  Nails & Hair  sign+door  x 1080-1330 y 255-825
Expressed below as percentages of the frame, so they stay locked to the doors at
every viewport width."""
import re, pathlib, sys

p = pathlib.Path('index.html')
s = p.read_text()
orig = s

def once(pattern, repl, flags=0, label=''):
    global s
    new, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit('FAILED to patch: ' + (label or pattern[:60]))
    s = new

# ---------------------------------------------------------------- 1. preload
once(r'(<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>)',
     r'''<link rel="preload" as="image" type="image/avif"
  imagesrcset="assets/hero/exterior-480.avif 480w, assets/hero/exterior-640.avif 640w, assets/hero/exterior-900.avif 900w, assets/hero/exterior-1200.avif 1200w, assets/hero/exterior-1551.avif 1551w"
  imagesizes="100vw" fetchpriority="high">
\1''', 0, 'preload')

# ------------------------------------------------------------------- 2. CSS
hero_css = '''
/* ======= HERO: the real building is the navigation =======
   The photograph carries three actual storefronts. Each one is a link. The frame
   below reproduces object-fit:cover while keeping a coordinate box locked to the
   image, so a hotspot placed at 33% stays on the Bridal door at every width.
   Phones crop far too hard for three doors to read, so under 900px the hotspots
   step aside for a bottom treatment, which is the same three choices. */
.hero{position:relative;height:100svh;min-height:540px;overflow:hidden;background:var(--brand-ink)}
.hero-frame{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  aspect-ratio:1551/1014;width:max(100%,calc(100svh * 1.5296))}
.hero-frame img{width:100%;height:100%;object-fit:cover;display:block}
/* Readability only. The building must stay legible, so this stays light. */
.hero-wash{position:absolute;inset:0;z-index:2;pointer-events:none;
  background:linear-gradient(180deg,rgba(20,14,8,.46) 0,rgba(20,14,8,.10) 24%,rgba(20,14,8,0) 46%)}
.hero-ask{position:absolute;z-index:5;left:0;right:0;text-align:center;
  top:calc(var(--nav-h) + env(safe-area-inset-top) + 14px);
  font-size:var(--fs-xs);font-weight:500;letter-spacing:.22em;text-transform:uppercase;
  color:rgba(248,244,236,.9);text-shadow:0 1px 14px rgba(18,12,6,.5);padding:0 var(--gutter)}

.hot{position:absolute;z-index:6;border-radius:12px;display:block;
  -webkit-tap-highlight-color:transparent}
.hot::before{content:"";position:absolute;inset:-2% -6%;border-radius:16px;
  background:radial-gradient(120% 92% at 50% 62%,rgba(255,246,229,.34),rgba(255,246,229,0) 72%);
  opacity:0;transition:opacity .24s var(--ease)}
.hot::after{content:"";position:absolute;inset:0;border-radius:12px;
  box-shadow:inset 0 0 0 1px rgba(255,247,233,.5);
  opacity:0;transition:opacity .24s var(--ease)}
.hot:hover::before,.hot:focus-visible::before,.hot:hover::after,.hot:focus-visible::after{opacity:1}
.hot:focus-visible{outline:2px solid #fff;outline-offset:4px}
.hot-salon{left:68.5%;top:24%;width:18%;height:58%}
.hot-concept{left:45%;top:32%;width:9.5%;height:43%}
.hot-bridal{left:33%;top:41%;width:7.5%;height:30%}
.hot-label{position:absolute;left:50%;top:calc(100% + 14px);transform:translateX(-50%);
  display:flex;flex-direction:column;align-items:center;gap:3px;white-space:nowrap;
  min-width:44px;min-height:44px;justify-content:center}
.hot-label .hl-n{font-family:var(--font-display);font-weight:600;
  font-size:clamp(17px,1.5vw,23px);color:#fdfaf3;
  text-shadow:0 1px 16px rgba(16,11,5,.72),0 0 3px rgba(16,11,5,.4)}
.hot-label .hl-s{font-size:10.5px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;
  color:rgba(250,245,236,.74);text-shadow:0 1px 12px rgba(16,11,5,.8);
  opacity:0;transform:translateY(-3px);transition:opacity .26s var(--ease),transform .26s var(--ease)}
.hot-label .hl-r{width:0;height:1px;background:rgba(252,247,238,.85);
  transition:width .28s var(--ease);margin-top:1px}
.hot:hover .hl-s,.hot:focus-visible .hl-s{opacity:1;transform:none}
.hot:hover .hl-r,.hot:focus-visible .hl-r{width:30px}

/* Phone and small tablet: the same three choices, thumb height, over the photo. */
.hero-choices{display:none;position:absolute;left:0;right:0;bottom:0;z-index:6;
  padding:var(--s-16) var(--gutter) calc(var(--s-5) + env(safe-area-inset-bottom));
  background:linear-gradient(180deg,rgba(20,14,8,0),rgba(20,14,8,.74) 42%,rgba(20,14,8,.93));
  gap:8px}
.hero-choices a{display:flex;align-items:center;justify-content:space-between;gap:14px;
  min-height:58px;padding:13px 18px;border-radius:12px;color:#f8f4ec;
  background:rgba(32,23,14,.62);border:1px solid rgba(248,244,236,.24)}
.hero-choices a:active{background:rgba(32,23,14,.85)}
.hero-choices .hc-n{font-family:var(--font-display);font-weight:600;font-size:var(--fs-md)}
.hero-choices .hc-s{display:block;font-size:var(--fs-2xs);letter-spacing:.14em;
  text-transform:uppercase;color:rgba(248,244,236,.66);margin-top:2px}
.hero-choices svg{width:18px;height:18px;flex:none;color:rgba(248,244,236,.8)}
@media(max-width:900px){
  .hot{display:none}
  .hero-choices{display:grid}
  .hero-frame{position:absolute;inset:0;top:0;left:0;transform:none;width:100%;height:100%;aspect-ratio:auto}
  .hero-frame img{object-position:64% center}
  .hero-ask{top:calc(var(--nav-h) + env(safe-area-inset-top) + 8px)}
}
/* transparent header while the photograph is behind it */
.nav.onhero{background:transparent;backdrop-filter:none;border-color:transparent;box-shadow:none}
.nav.onhero .brand .bt,.nav.onhero .nav-links a,.nav.onhero .nav-links button{color:#f8f4ec}
.nav.onhero .brand .bt small{color:rgba(248,244,236,.7)}
.nav.onhero .hamb{color:#f8f4ec}
.nav.onhero .brand .bm{background:rgba(248,244,236,.16);color:#f8f4ec}
.nav.onhero .nav-links a:hover,.nav.onhero .nav-links button:hover{color:#fff}

/* Entrance: photograph, then the words, then the doors. Under 1.2s, and it never
   gates interaction because every element is clickable from the first frame. */
@keyframes heroIn{from{opacity:0}to{opacity:1}}
@keyframes heroRise{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}
.hero-frame{animation:heroIn .62s var(--ease) both}
.hero-ask{animation:heroRise .5s var(--ease) .42s both}
.hot-label{animation:heroRise .46s var(--ease) both}
.hot-salon .hot-label{animation-delay:.62s}
.hot-concept .hot-label{animation-delay:.72s}
.hot-bridal .hot-label{animation-delay:.82s}
.hero-choices a:nth-child(1){animation:heroRise .46s var(--ease) .6s both}
.hero-choices a:nth-child(2){animation:heroRise .46s var(--ease) .7s both}
.hero-choices a:nth-child(3){animation:heroRise .46s var(--ease) .8s both}
@media(prefers-reduced-motion:reduce){
  .hero-frame,.hero-ask,.hot-label,.hero-choices a{animation:none}
  .hot-label .hl-s{opacity:1;transform:none}
}
'''
once(r'(/\* ======= FIRST SCREEN ======= \*/)', hero_css.replace('\\', '\\\\') + r'\n\1', 0, 'hero css')

# ------------------------------------------------------------------ 3. HTML
hero_html = '''<!-- ======= HERO: the three real doors ======= -->
<section class="hero" id="top">
  <div class="hero-frame">
    <picture>
      <source type="image/avif" sizes="100vw" srcset="assets/hero/exterior-480.avif 480w, assets/hero/exterior-640.avif 640w, assets/hero/exterior-900.avif 900w, assets/hero/exterior-1200.avif 1200w, assets/hero/exterior-1551.avif 1551w">
      <source type="image/webp" sizes="100vw" srcset="assets/hero/exterior-480.webp 480w, assets/hero/exterior-640.webp 640w, assets/hero/exterior-900.webp 900w, assets/hero/exterior-1200.webp 1200w, assets/hero/exterior-1551.webp 1551w">
      <img src="assets/hero/exterior-1200.jpg" width="1551" height="1014" fetchpriority="high" decoding="async"
           sizes="100vw"
           srcset="assets/hero/exterior-480.jpg 480w, assets/hero/exterior-640.jpg 640w, assets/hero/exterior-900.jpg 900w, assets/hero/exterior-1200.jpg 1200w, assets/hero/exterior-1551.jpg 1551w"
           alt="The sh-WOAH arcade in Negombo. Three signed entrances along one colonnade: Bridal, Concept Store and Nails and Hair.">
    </picture>
    <div class="hero-wash"></div>
    <a class="hot hot-salon" href="#salon" data-door="salon">
      <span class="hot-label"><span class="hl-n">Salon</span><span class="hl-s">Hair, skin and nails</span><span class="hl-r"></span></span>
    </a>
    <a class="hot hot-concept" href="#concept-store" data-door="concept">
      <span class="hot-label"><span class="hl-n">Concept store</span><span class="hl-s">Take the result home</span><span class="hl-r"></span></span>
    </a>
    <a class="hot hot-bridal" href="#bridal" data-door="bridal">
      <span class="hot-label"><span class="hl-n">Bridal</span><span class="hl-s">The photographed day</span><span class="hl-r"></span></span>
    </a>
  </div>
  <p class="hero-ask">Choose your sh-WOAH experience</p>
  <nav class="hero-choices" aria-label="Choose a service">
    <a href="#salon" data-door="salon"><span><span class="hc-n">Salon</span><span class="hc-s">Hair, skin and nails</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m0 0-6-6m6 6-6 6"/></svg></a>
    <a href="#bridal" data-door="bridal"><span><span class="hc-n">Bridal</span><span class="hc-s">The photographed day</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m0 0-6-6m6 6-6 6"/></svg></a>
    <a href="#concept-store" data-door="concept"><span><span class="hc-n">Concept store</span><span class="hc-s">Take the result home</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m0 0-6-6m6 6-6 6"/></svg></a>
  </nav>
</section>
'''
once(r'<!-- ======= FIRST SCREEN ======= -->.*?</section>\s*', hero_html, re.S, 'hero html')

# ------------------------------------------- 4. one page: un-gate + rename ids
s = re.sub(r'\s+data-modes="[^"]*"', '', s)
once(r'<section class="section scene-dark" id="salon-head">',
     '<section class="section scene-dark" id="salon">', 0, 'salon id')
once(r'<section class="section scene-dark" id="bridal-head">',
     '<section class="section scene-dark" id="bridal">', 0, 'bridal id')
once(r'<section class="section scene-dark" id="concept-head">',
     '<section class="section scene-dark" id="concept-store">', 0, 'concept id')

# headings become focus targets for keyboard users arriving via a door
for sid in ('salon', 'bridal', 'concept-store'):
    once(r'(<section class="section scene-dark" id="' + sid + r'">.*?<h2)(?![^>]*tabindex)',
         r'\1 tabindex="-1"', re.S, sid + ' heading tabindex')

# nav, drawer and footer become real anchors
s = s.replace('''<button type="button" data-door="salon" onclick="pickDoor('salon')">The salon</button>
      <button type="button" data-door="bridal" onclick="pickDoor('bridal')">Bridal</button>
      <button type="button" data-door="concept" onclick="pickDoor('concept')">The store</button>''',
'''<a href="#salon" data-door="salon">The salon</a>
      <a href="#bridal" data-door="bridal">Bridal</a>
      <a href="#concept-store" data-door="concept">The store</a>''')
s = s.replace('''<button type="button" class="dlink" onclick="closeDrawer();pickDoor('salon')">The salon</button>
    <button type="button" class="dlink" onclick="closeDrawer();pickDoor('bridal')">Bridal</button>
    <button type="button" class="dlink" onclick="closeDrawer();pickDoor('concept')">The store</button>''',
'''<a class="dlink" href="#salon" onclick="closeDrawer()">The salon</a>
    <a class="dlink" href="#bridal" onclick="closeDrawer()">Bridal</a>
    <a class="dlink" href="#concept-store" onclick="closeDrawer()">The store</a>''')
s = s.replace('''<button type="button" class="flink" onclick="pickDoor('salon')">The salon</button>
        <button type="button" class="flink" onclick="pickDoor('bridal')">Bridal</button>
        <button type="button" class="flink" onclick="pickDoor('concept')">The concept store</button>''',
'''<a href="#salon">The salon</a>
        <a href="#bridal">Bridal</a>
        <a href="#concept-store">The concept store</a>''')
s = s.replace("onclick=\"pickDoor('salon')\"", 'href="#salon"')
s = s.replace("onclick=\"pickDoor('bridal')\"", 'href="#bridal"')
s = s.replace("onclick=\"pickDoor('concept')\"", 'href="#concept-store"')
s = s.replace("onclick=\"pickDoor('all')\"", 'href="#overview"')
s = s.replace("goTool('salon','book')", "goSection('#book')")
s = s.replace("goTool('bridal','bridal-date')", "goSection('#bridal-date')")
s = s.replace("goTool('salon','leaving')", "goSection('#leaving')")
s = s.replace("goTool('all','about')", "goSection('#about')")

# ------------------------------------------------------------------- 5. JS
new_js = '''/* ONE PAGE, THREE ANCHORS. Every section is always in the document; a door is a
   real link to it, so a pasted #bridal opens at bridal and the back button works.
   MODE is now only used to label a WhatsApp enquiry, and is set by whichever
   section the reader is actually looking at. */
const VALID = ['salon','bridal','concept'];
const DOOR_LABEL = { salon:'Salon', bridal:'Bridal', concept:'Concept', all:'General' };
const SECTION_OF = { salon:'salon', bridal:'bridal', concept:'concept-store' };
let MODE = 'all';

function goSection(hash, push){
  const el = document.querySelector(hash);
  if (!el) return;
  el.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block:'start' });
  if (push !== false && location.hash !== hash) history.pushState(null, '', hash);
  const h = el.querySelector('h2, h3');
  if (h) { if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex','-1'); h.focus({ preventScroll:true }); }
}
/* Doors are anchors, so a middle click or a copied link still behaves. We only
   intercept the plain left click, to add smooth scroll and move focus. */
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#"]');
  if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
  const hash = a.getAttribute('href');
  if (hash === '#' || !document.querySelector(hash)) return;
  e.preventDefault();
  goSection(hash);
});
window.addEventListener('popstate', () => { if (location.hash) goSection(location.hash, false); });

/* which door the reader is in, for the enquiry tag and the sticky button */
if ('IntersectionObserver' in window) {
  const watch = new IntersectionObserver(es => {
    es.forEach(en => {
      if (!en.isIntersecting) return;
      const found = VALID.find(v => SECTION_OF[v] === en.target.id);
      MODE = found || 'all';
      const stick = document.getElementById('stickCta');
      if (stick) stick.textContent = MODE === 'bridal' ? 'Check my date' : 'WhatsApp';
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  ['salon','bridal','concept-store','overview','about','reviews','find']
    .forEach(id => { const el = document.getElementById(id); if (el) watch.observe(el); });
}
function stickAction(btn){
  if (MODE === 'bridal') { goSection('#bridal-date'); return; }
  waSend(DOOR_LABEL[MODE], 'Quick message', [], btn);
}
/* transparent header only while the photograph is behind it */
const heroEl = document.getElementById('top');
function navSkin(){
  if (!heroEl) return;
  nav.classList.toggle('onhero', scrollY < heroEl.offsetHeight - 90);
}
addEventListener('scroll', () => requestAnimationFrame(navSkin), { passive:true });
addEventListener('resize', navSkin);
'''

# replace the old mode plumbing (VALID .. setMode call) wholesale
once(r"const VALID = \['salon','bridal','concept'\];.*?setMode\(Q\.get\('service'\) \|\| 'all', false\);",
     new_js.replace('\\', '\\\\'), re.S, 'mode plumbing')

# remaining references to the retired helpers
s = s.replace("function pickDoor(m){ setMode(m, true); }\n", "")
s = re.sub(r"function goTool\(mode, id\)\{.*?\n\}\n", "", s, flags=re.S)
s = s.replace("  revealVisible();\n}\n", "  revealVisible();\n}\n", 1)

# boot: honour an incoming hash, and paint the header state once
once(r'(renderReviews\(\);)',
     r'''navSkin();
if (location.hash && document.querySelector(location.hash)) {
  requestAnimationFrame(() => goSection(location.hash, false));
}
\1''', 0, 'boot')

assert s != orig
p.write_text(s)
print('patched hero + one-page anchors')
