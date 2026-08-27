"""One-off patch: rebuild the first-screen mosaic as three equal salon squares
over two door tiles, with a hover panel carrying real information.
Run once from the repo root, then delete."""
import re, pathlib, sys

p = pathlib.Path('index.html')
s = p.read_text()
before = s

# ---------------------------------------------------------------- CSS: grid
old_grid_start = ".mosaic{display:grid;gap:10px;grid-template-columns:1.05fr"
i = s.index(old_grid_start)
j = s.index(".tile-b2{grid-area:b2;background:linear-gradient(150deg,#efe6da,var(--brand-soft) 85%)}")
j = s.index("\n", j)

new_css = """.mosaic{display:grid;gap:10px;grid-template-columns:repeat(6,1fr);
  grid-template-areas:"h h n n k k" "c c c b b b"}
.tile{position:relative;border:0;border-radius:var(--r-md);overflow:hidden;text-align:left;
  padding:var(--s-5);display:flex;flex-direction:column;justify-content:flex-end;gap:6px;
  background:var(--surface-2);transition:transform var(--t) var(--ease),box-shadow var(--t)}
.tile:hover{transform:translateY(-3px);box-shadow:var(--shadow-md)}
.tile:focus-visible{outline:2px solid var(--brand);outline-offset:3px;box-shadow:none}
.tile[aria-pressed="true"]{box-shadow:inset 0 0 0 2px var(--brand)}
.tile .t-door{font-size:10.5px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.tile .t-line{font-family:var(--font-display);font-weight:600;font-size:clamp(18px,1.9vw,25px);line-height:1.15;color:var(--ink)}
.tile .t-ico{position:absolute;top:var(--s-5);left:var(--s-5);width:26px;height:26px;color:var(--brand);z-index:2}
/* row one: three equal squares, all of them the salon door */
.tile-sq{aspect-ratio:1}
.tile-h{grid-area:h}
.tile-n{grid-area:n}
.tile-k{grid-area:k}
/* row two: the other two doors, together the same width as the three above */
.tile-c{grid-area:c;background:var(--brand-ink);min-height:200px}
.tile-c .t-door{color:#968d7c}
.tile-c .t-line{color:#f4efe4}
.tile-c .t-ico{color:#c8a878}
.tile-b{grid-area:b;background:linear-gradient(150deg,#efe6da,var(--brand-soft) 85%);min-height:200px}
/* The hover panel. Information only. The offer line renders ONLY when OFFERS
   in the script is filled in, which needs Harini's written approval: BB never
   publishes an offer the salon has not agreed, and the consultancy report's own
   advice was that a salon this good does not need a discount every month. */
.t-over{position:absolute;inset:0;z-index:4;background:rgba(24,18,10,.93);color:#f4efe4;
  padding:var(--s-5);display:flex;flex-direction:column;justify-content:center;gap:9px;
  opacity:0;transform:translateY(10px);pointer-events:none;
  transition:opacity var(--t) var(--ease),transform var(--t) var(--ease)}
.t-over .to-t{font-family:var(--font-display);font-weight:600;font-size:var(--fs-md)}
.t-over .to-b{font-size:var(--fs-sm);color:#d9d0bf;line-height:1.5}
.t-over .to-offer{font-size:var(--fs-xs);font-weight:500;color:#e6c893;
  border-top:1px solid rgba(244,239,228,.22);padding-top:9px}
.t-over .to-cta{font-size:var(--fs-xs);font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:#e6d3ae;display:flex;align-items:center;gap:8px;margin-top:2px}
.t-over .to-cta svg{width:15px;height:15px}
.t-sub{font-size:var(--fs-xs);color:#e6dcc6;line-height:1.45;display:none}
@media(hover:hover) and (pointer:fine){
  .tile-sq:hover .t-over,.tile-sq:focus-visible .t-over{opacity:1;transform:none}
}
/* A phone has no hover, so the same information simply sits on the tile. */
@media(hover:none),(pointer:coarse){
  .t-over{display:none}
  .t-sub{display:block}
}
"""
s = s[:i] + new_css + s[j+1:]

# ------------------------------------------------------- CSS: mobile block
old_mobile = re.search(
    r"@media\(max-width:720px\)\{\s*\.mosaic\{.*?\n\}", s, re.S)
if not old_mobile:
    sys.exit("mobile mosaic block not found")
s = s[:old_mobile.start()] + """@media(max-width:720px){
  .mosaic{gap:8px}
  .tile{padding:var(--s-4)}
  .tile .t-line{font-size:clamp(15px,4.2vw,20px)}
  .tile-c,.tile-b{min-height:150px}
}
@media(max-width:560px){
  /* three squares across a phone leave no room for a second line, and the
     salon door carries the same information one tap away */
  .t-sub{display:none}
}""" + s[old_mobile.end():]

# ------------------------------------------------------------- HTML: tiles
m = re.search(r'<div class="mosaic".*?</div>\s*(?=<div class="notsure">)', s, re.S)
if not m:
    sys.exit("mosaic markup not found")

arrow = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14m0 0-6-6m6 6-6 6"/></svg>')

new_html = f'''<div class="mosaic" role="group" aria-label="Choose what you came for">
      <button type="button" class="tile tile-sq tile-h tile-photo" data-door="salon" onclick="pickDoor('salon')">
        <img src="assets/hair-result.jpg" width="900" height="880" alt="A finished blow dry at sh-WOAH, layered and lifted">
        <span class="t-door">The salon</span>
        <span class="t-line">Hair</span>
        <span class="t-sub">Cuts, colour and styling</span>
        <span class="t-over" data-over="hair"></span>
      </button>
      <button type="button" class="tile tile-sq tile-n tile-photo" data-door="salon" onclick="pickDoor('salon')">
        <img src="assets/nails-work.jpg" width="900" height="1093" alt="Nail work done at sh-WOAH, a French manicure with fine gold detail">
        <span class="t-door">The salon</span>
        <span class="t-line">Nails</span>
        <span class="t-sub">Manicure, pedicure and nail art</span>
        <span class="t-over" data-over="nails"></span>
      </button>
      <button type="button" class="tile tile-sq tile-k tile-photo" data-door="salon" onclick="pickDoor('salon')">
        <img src="assets/lash-work.jpg" width="900" height="1170" alt="Lash work in progress at sh-WOAH">
        <span class="t-door">The salon</span>
        <span class="t-line">Skin</span>
        <span class="t-sub">Skin treatments and lashes</span>
        <span class="t-over" data-over="skin"></span>
      </button>
      <button type="button" class="tile tile-c" data-door="concept" onclick="pickDoor('concept')">
        <svg class="t-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        <span class="t-door">The concept store</span>
        <span class="t-line">Take the result home.</span>
      </button>
      <button type="button" class="tile tile-b" data-door="bridal" onclick="pickDoor('bridal')">
        <svg class="t-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="14" r="6"/><circle cx="15" cy="14" r="6"/><path d="M9 8l1.5-4h3L15 8"/></svg>
        <span class="t-door">Bridal</span>
        <span class="t-line">The one photographed day.</span>
      </button>
    </div>
    '''
s = s[:m.start()] + new_html + s[m.end():]

# --------------------------------------------------------------- JS: panels
anchor = "renderReviews();"
js = '''/* What each salon square says when someone hovers it. Information only.
   OFFERS is deliberately EMPTY: BB never publishes an offer the salon has not
   approved in writing. Put a line in here (for example
   hair: 'First visit includes a consultation') and it appears on that square
   and nowhere else. Never invent one. */
const SQUARES = {
  hair:  { title:'Hair', body:'Cuts, colour, blow dry and styling. Tell the desk what you are after and they will confirm a time.', cta:'Book hair' },
  nails: { title:'Nails', body:'Manicure, pedicure and nail art. The fine gold detail in the picture was done here.', cta:'Book nails' },
  skin:  { title:'Skin', body:'Skin treatments and lash work. Ask the desk what suits you.', cta:'Book skin' }
};
const OFFERS = { hair:'', nails:'', skin:'' };
Object.keys(SQUARES).forEach(k => {
  const host = document.querySelector('[data-over="' + k + '"]');
  if (!host) return;
  const v = SQUARES[k];
  host.innerHTML =
    '<span class="to-t">' + v.title + '</span>' +
    '<span class="to-b">' + v.body + '</span>' +
    (OFFERS[k] ? '<span class="to-offer">' + OFFERS[k] + '</span>' : '') +
    '<span class="to-cta">' + v.cta + ' ARROW</span>';
});

'''.replace('ARROW', arrow)
s = s.replace(anchor, js + anchor, 1)

assert s != before
p.write_text(s)
print("patched: grid, mobile, markup, panels")
