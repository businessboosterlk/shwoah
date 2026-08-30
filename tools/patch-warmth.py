"""Warm the copy and put real photography down the page.

Three faults Thulaib named, all correct:
  1. the words read like a business writing to a customer, not a salon,
  2. too many headings are questions,
  3. below the booking form the page is 8,500px of text on flat colour.

The biggest single tell was "the desk". It is agency vocabulary. A salon says we.
"""
import pathlib, sys

p = pathlib.Path('index.html')
s = p.read_text()
n_ok = 0

def swap(old, new, label):
    global s, n_ok
    if old not in s:
        sys.exit('NOT FOUND [' + label + ']: ' + old[:80])
    s = s.replace(old, new, 1)
    n_ok += 1

# ---------------------------------------------------------------- hero
swap('Choose your sh-WOAH experience', 'Choose a door', 'hero instruction')

# ---------------------------------------------------------- overview
swap('<span class="eyebrow">The house</span>', '<span class="eyebrow">Under one roof</span>', 'overview eyebrow')
swap('<h2>Three ways in.</h2>', '<h2>Three doors, one house.</h2>', 'overview h2')
swap('Most people come for the chairs. Some come for a date months away. A few just want the shelf.',
     'Skin, hair and nails on an ordinary week. A wedding morning booked a year ahead. And a small shelf of things worth taking home.',
     'overview p')

# ------------------------------------------------------------- doors
swap("The weekly habit and the visitor's hour. Book a chair on WhatsApp.",
     'Colour, cuts, facials, lashes and nail work, taken slowly.', 'salon card')
swap('Bridal runs on one date. Send yours first and plan the rest with the salon.',
     'One morning, photographed for the rest of your life. Send us the date first.', 'bridal card')
swap('The one part of sh-WOAH that leaves with you.',
     'The one part of sh-WOAH you can take away with you.', 'concept card')

# ----------------------------------------------------------- shortcuts
swap('<span class="eyebrow">Shortcuts</span>', '<span class="eyebrow">Straight there</span>', 'tools eyebrow')
swap('<h2>Know what you need already?</h2>', '<h2>If you already know what you want.</h2>', 'tools h2')
swap('Hair, nails or skin, on WhatsApp in two minutes', 'Hair, nails or skin, whenever suits you', 'tool row 1')
swap('Send the date first. The salon confirms it', 'Send the date first and we build around it', 'tool row 2')
swap('Flying out and want something done before you go', 'Here on holiday and short on time', 'tool row 3')

# --------------------------------------------------------------- salon
swap('Tell the desk what you need on WhatsApp. They answer in opening hours, daily 10:00 to 20:00.',
     'Colour, cuts, facials, lashes and nail work. Open every day, ten in the morning until eight at night.',
     'salon p')
swap('The full treatment menu is being written up with prices. Until it is published here, the desk will send it to you.',
     'The full treatment menu is being written up with prices. Until it is here, ask us and we will send it over.',
     'salon note')

# ---------------------------------------------------------------- book
swap('<h2>Two minutes, then it is with the desk.</h2>', '<h2>Tell us what you would like.</h2>', 'book h2')
swap('A time is confirmed once the desk replies.', 'A time is confirmed once we reply.', 'book note')

# -------------------------------------------------------------- prices
swap('<h2>What things cost.</h2>', '<h2>What it costs.</h2>', 'prices h2')
swap('The price list is coming to this page. Ask on WhatsApp and the desk will send it to you.',
     'The full list is being finished. Ask us and we will send it to you.', 'prices p')

# ------------------------------------------------------------- leaving
swap('<span class="eyebrow">Flying out</span>', '<span class="eyebrow">Passing through</span>', 'leaving eyebrow')
swap('<h2>Leaving Negombo soon?</h2>', '<h2>Here for a few days, and short on time.</h2>', 'leaving h2')
swap('Tell the desk when you leave and when you could come in. They will tell you what is possible.',
     'Tell us when you fly and when you are free. We will say honestly what we can fit in before you go.',
     'leaving p')
swap('Send it to the desk', 'Send it to us', 'leaving button')
swap('We will not guess what fits before a flight. The desk replies in opening hours with what is genuinely possible.',
     'We will not guess what fits before a flight. We reply in opening hours with what is genuinely possible.',
     'leaving note')

# -------------------------------------------------------------- bridal
swap('Bridal runs on one date. Send yours first, before anything else is decided.',
     'Every photograph from that morning outlives the day. Send us the date first and the rest is built around it.',
     'bridal p')
swap('<h2>Check my date.</h2>', '<h2>Start with the date.</h2>', 'bridal-date h2')
swap('<h2>What a bridal booking includes.</h2>', '<h2>What the morning includes.</h2>', 'packages h2')
swap('The bridal packages are being written up for this page. Ask and the desk will talk you through them.',
     'The bridal packages are being written up. Ask and we will talk you through them properly.', 'packages p')
swap('The form below takes two minutes and goes straight to the salon.',
     'A few lines below and it comes straight to us.', 'bridal step 1')
swap('A date is held only once they confirm it. Sending the form does not book the day.',
     'A date is held only once we confirm it. Sending the form does not book the day.', 'bridal step 2')

# ------------------------------------------------------------- concept
swap('The store is the part of sh-WOAH that leaves with you. What is on the shelf changes, so ask.',
     'The one part of sh-WOAH you can take away with you. What sits on the shelf changes, so do ask.',
     'concept p')

# ----------------------------------------------------------------- ask
swap('<h2>Not a form person? Just ask.</h2>', '<h2>Or simply say hello.</h2>', 'ask h2')
swap('One message. The desk answers in opening hours.',
     'One message, answered while the doors are open.', 'ask sub')

# ------------------------------------------------------ CSS for figures
css = """/* Real photography down the page. Below the booking form the site was 8,500px
   of text on flat colour, which reads as unfinished however good the words are. */
.sec-shot{margin:var(--s-10) 0 0;border-radius:var(--r-lg);overflow:hidden}
.sec-shot img{width:100%;display:block;object-fit:cover;aspect-ratio:16/6.5}
.sec-shot figcaption{padding:var(--s-3) var(--s-1) 0;color:var(--faint);font-size:var(--fs-xs)}
.scene-dark .sec-shot figcaption{color:var(--faint)}
.split{display:grid;grid-template-columns:.85fr 1.15fr;gap:var(--s-12);align-items:center;margin-top:var(--s-10)}
.split figure{margin:0;border-radius:var(--r-lg);overflow:hidden}
.split img{width:100%;display:block}
@media(max-width:820px){
  .split{grid-template-columns:1fr;gap:var(--s-6)}
  .sec-shot img{aspect-ratio:4/3}
}
"""
swap('.work-grid{display:grid;', css + '.work-grid{display:grid;', 'figure css')

# --------------------------------------------------- the images themselves
swap('''    <p class="tool-note" data-sr>The full treatment menu is being written up with prices.''',
'''    <figure class="sec-shot" data-sr>
      <img src="assets/salon-floor.jpg" width="1100" height="1438" loading="lazy" alt="The salon floor at sh-WOAH, styling chairs, pedicure seats and the nail bar under warm light">
    </figure>
    <p class="tool-note" data-sr>The full treatment menu is being written up with prices.''', 'salon image')

swap('''<section class="section" id="book">
  <div class="wrap">
    <div class="sect-head" data-sr>''',
'''<section class="section" id="book">
  <div class="wrap">
    <figure class="sec-shot" style="margin:0 0 var(--s-12)" data-sr>
      <img src="assets/salon-lounge.jpg" width="900" height="1125" loading="lazy" alt="Inside sh-WOAH, the pedicure lounge and styling stations">
    </figure>
    <div class="sect-head" data-sr>''', 'book image')

swap('    <div class="steps" data-sr>',
'''    <div class="split" data-sr>
      <figure><img src="assets/bridal-door.jpg" width="560" height="600" loading="lazy" alt="The bridal door at sh-WOAH, a gown visible through the glass"></figure>
      <div class="steps" style="grid-template-columns:1fr;margin-top:0">''', 'bridal split open')
swap('''<p>Trials, timings and the party, worked out with the team.</p></div>
    </div>''',
'''<p>Trials, timings and the party, worked out with the team.</p></div>
      </div>
    </div>''', 'bridal split close')

swap('''    <div data-sr>
      <button class="btn btn-primary btn-lg" type="button" onclick="waSend('Concept','Ask about the store',[],this)">Ask what is in the store</button>''',
'''    <div class="split" data-sr>
      <figure><img src="assets/concept-door.jpg" width="440" height="600" loading="lazy" alt="The concept store door at sh-WOAH, rails of pieces visible inside"></figure>
      <div>
      <button class="btn btn-primary btn-lg" type="button" onclick="waSend('Concept','Ask about the store',[],this)">Ask what is in the store</button>''', 'concept split open')
swap('''      <div class="wa-preview" data-preview></div>
    </div>
    <div data-dev-only hidden style="margin-top:var(--s-10)">''',
'''      <div class="wa-preview" data-preview></div>
      </div>
    </div>
    <div data-dev-only hidden style="margin-top:var(--s-10)">''', 'concept split close')

p.write_text(s)
print(f'{n_ok} replacements applied')
