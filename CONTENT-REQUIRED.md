# sh-WOAH website · CONTENT REQUIRED

Every gap between this build and a launchable site, who supplies it and which
surface it blocks. Production never shows a gap: the surface hides or carries
honest neutral copy until its row here is cleared. Dev preview (`?preview=dev`)
shows marked placeholders so composition can be judged.

Status key: OPEN (nothing supplied) · PARTIAL · CLEARED.

| # | Item | Who supplies | Blocks | Status |
|---|---|---|---|---|
| 1 | WhatsApp number, confirmed as the line the salon answers (CFG.wa stays empty until then; the public 077 075 4224 is verified as a phone only) | Harini | Every enquiry route on the site | OPEN |
| 2 | Prices and durations for the salon menu, in writing | Harini | Price surface in salon mode | OPEN |
| 3 | Bridal packages: names, what each covers, prices | Harini | Bridal packages surface | OPEN |
| 4 | Team roster: names, roles, photos, who may be asked for by name | Harini | Team section (not yet rendered), ask-for-a-person confidence | OPEN |
| 5 | Review subset: author, text, language, date, service line, source URL | BB pulls by hand from the Google listing, Harini confirms | Review wall | PARTIAL: 3 live, see below |
| 6 | Photography: salon interior, treatments, bridal portfolio, product, staff | Harini, or a BB shoot | The mosaic tiles and every mode's visual surface | PARTIAL |
| 7 | Logo files and variants, brand colours, fonts with licences | Harini | Wordmark, favicon (interim monogram ships flagged), og image (interim typographic ships flagged) | OPEN |
| 8 | Exact business name and capitalisation (site shows sh-WOAH and Sh-Woah today) | Harini | Title, structured data, footer | OPEN |
| 9 | Confirmed Google Maps place URL (a maps search link works meanwhile) | Harini or BB from the listing | Find us buttons, review link | PARTIAL |
| 10 | Opening hours and address confirmed at handover (currently public record: Banyan Complex, Heritance, Negombo · daily 10:00 to 20:00) | Harini | Find us, FAQ, structured data | PARTIAL |
| 11 | What jac is, the concept range and where the store actually lives ("two destinations" on her own site, one address listed) | Harini | Concept store shopfront (stays behind the dev flag until cleared) | OPEN |
| 12 | The 128 review count reconfirmed at launch (public count read August 2026; it will drift) | BB | Reviews headline | PARTIAL |
| 13 | Deployment host and framework decision, then DNS (client's step) | Harini with BB | Go-live | OPEN |
| 14 | Consent for analytics and which tool | Harini | Any measurement beyond WhatsApp tags | OPEN |
| 15 | Campaign tag convention agreed with the SMM (?c=..., readable names) | BB with Thulaib | Paid and posted door links | OPEN |
| 16 | All visible copy read and approved by Harini | Harini | Launch | OPEN |

## Photography record (item 6), received 26 August 2026

Eleven images arrived from Thulaib (`assets/src/IMG_8123.jpg` to `IMG_8133.jpg`,
1179px wide, which reads as phone screenshots of the salon's own posts).

**In production now, no identifiable faces:**
- `IMG_8123` the arcade exterior with the Bridal, Concept Store and Nails & Hair
  signboards. Used in the overview.
- `IMG_8124` the salon floor. Mosaic, salon cluster.
- `IMG_8127` a nail result, hands only. Mosaic, salon cluster.

**Held until Harini confirms consent, because a face on her website is her call:**
- `IMG_8126` lash treatment close-up (client's face)
- `IMG_8128` client showing nails (face)
- `IMG_8129` pedicure lounge in use (several customers and staff)
- `IMG_8130` manicure bar in use (several customers and staff; the visitor
  scene the report describes, worth publishing the day consent is confirmed)
- `IMG_8131` hair result (face) · `IMG_8132` styled portrait (face) ·
  `IMG_8133` hair and makeup result (face)

**Still wanted, and item 6 is now the biggest visual gap:**
1. **A straight-on photograph of the arcade showing all three signed doors.**
   The hero uses the real building and the doors are the navigation, but the only
   angle we hold is a perspective view down the colonnade, so Bridal sits small
   and far left. A front-on frame taken from across the courtyard, in daylight,
   would let all three doors read at once. This is a two minute phone job for
   anyone standing there. **It must be a real photograph. A generated or edited
   image of a real shopfront is not an option: customers navigate by it, and the
   consultancy report's own slide 9 names "bridal advertised with borrowed
   images" as the fault of the salons sh-WOAH is beating.**
2. A higher resolution original of the exterior. Ours is 1551px wide, which is
   sharp at 1x on a laptop and soft on a retina desktop for a full bleed hero.
3. One true product shot for the concept store.
4. A confirmed bridal set, and staff portraits for the team section.

## Reviews on the site (item 5), added 26 August 2026

Three reviews are live, read off the salon's own published Google reviews widget:
Moritz Hartkopf (German), Beth (English) and Laurina de Vries (Dutch), all five
stars, all about six months old.

**The rule applied, and it is the one to keep:** the widget truncates longer
reviews with a "Read more" link, so **only complete sentences were taken**. A
half sentence is never published as a whole one. Originals always ship beside
the translation and the translation is labelled as one. The page says "3 of the
128" and links to Google, so it never implies the whole set is on the site.

**Wanted from Harini or a hand pull:** the full text of the truncated reviews,
plus any review that names a staff member (the report found staff named by name,
and none of the three above does, so the ask-for-a-person surface still has no
evidence behind it). Bridal reviews are wanted most: all three here are salon.

**Not marked up in schema deliberately.** Review and aggregateRating schema needs
an exact average, which no source gives. The visible "Excellent" and "128" come
from the salon's own widget, so they are quoted, not computed.

## Photography record v2, received 26 August 2026

A second, better set of 12 arrived (`assets/src-v2/`, kept out of git). **Nine
are upscaled versions of the original phone photos** and match them room for
room, so they replaced the v1 crops: exterior, salon floor, nail bar, manicure
bar, pedicure lounge, lash work, nail result, hair result and the client with
her nails.

**Three were NOT used and must not be.** They are AI-generated images of places
that are not sh-WOAH: a hair salon with brass sconces and dark marble (the real
salon is cream tile, black metal ceiling, tan chairs), a bridal getting-ready
scene in a colonial room, and a still life of a pot on a brass shelf. Publishing
any of them would show a customer a salon that does not exist, which is exactly
the fabrication the whole build is built to avoid. Filenames held in
`assets/src-v2/`: `exec-58f55d36`, `exec-9914bc59`, `exec-94db5480`.

**Bridal still has no photography and its tiles carry no image.** Every supplied
photo is salon work. A manicure under a "Bridal" label claims a portfolio nobody
has supplied, so the bridal tiles stay designed until real bridal work arrives.

## Rules this file enforces

- Never fabricate. Never ship a placeholder to production.
- Every price on the rendered site must trace to item 2 or 3 in writing, or it
  comes out. The verification battery greps the rendered text for currency
  figures.
- No review renders unless its row is verified. The site never implies all 128
  are on the page.
- jac ships nothing public until item 11 is cleared.
