#!/usr/bin/env python3
"""Swap the hero photograph in one command.

    python3 tools/set-hero.py <path-to-new-image>

Does the mechanical half of a hero swap, end to end:
  1. validates the image (min 1400px wide, landscape),
  2. generates WebP + JPEG derivatives at up to five widths into assets/hero/,
  3. rewrites every srcset, the img width/height and the .hero-frame
     aspect-ratio and cover factor in index.html to match the new image,
  4. writes crop commands for the door-measurement step to tools/MEASURE-DOORS.txt.

What it deliberately does NOT do: touch the three .hot-* door coordinates.
Those are measured off the actual photograph by cropping each storefront and
reading its edges (the crop commands are generated for you). Guessed hotspot
coordinates on a navigation photograph send customers to the wrong door, so the
measurement step stays human. Run from the repo root.
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERO = ROOT / 'assets' / 'hero'
INDEX = ROOT / 'index.html'
CWEBP = 'cwebp'

def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('command failed: ' + ' '.join(cmd) + '\n' + r.stderr)
    return r.stdout

def dims(path):
    out = run('sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(path))
    w = int(re.search(r'pixelWidth: (\d+)', out).group(1))
    h = int(re.search(r'pixelHeight: (\d+)', out).group(1))
    return w, h

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1]).expanduser()
    if not src.exists():
        sys.exit('no such file: ' + str(src))

    w, h = dims(src)
    if w < 1400:
        sys.exit(f'refusing: {w}px wide. A full-bleed hero wants 1400px minimum, '
                 'and upscaling a small image is exactly what this site never does.')
    if h >= w:
        sys.exit(f'refusing: {w}x{h} is portrait. The hero frame is landscape.')

    print(f'source {src.name}: {w}x{h}')

    # 1. derivatives. Same filenames the HTML already uses, widths capped at source.
    widths = sorted({min(x, w) for x in (480, 640, 900, 1200, 1600, w)})
    HERO.mkdir(parents=True, exist_ok=True)
    for old in HERO.glob('exterior-*'):
        old.unlink()
    pairs = []
    for tw in widths:
        th = round(h * tw / w)
        tmp = f'/tmp/set-hero-{tw}.png'
        run('sips', '--resampleWidth', str(tw), '-s', 'format', 'png', str(src), '--out', tmp)
        run('sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '72', tmp,
            '--out', str(HERO / f'exterior-{tw}.jpg'))
        run(CWEBP, '-q', '72', '-quiet', tmp, '-o', str(HERO / f'exterior-{tw}.webp'))
        pairs.append(tw)
        print(f'  wrote exterior-{tw}.webp / .jpg')

    # 2. rewrite index.html references
    s = INDEX.read_text()
    webp_set = ', '.join(f'assets/hero/exterior-{x}.webp {x}w' for x in pairs)
    jpg_set = ', '.join(f'assets/hero/exterior-{x}.jpg {x}w' for x in pairs)
    fallback = f'assets/hero/exterior-{pairs[-2] if len(pairs) > 1 else pairs[-1]}.jpg'
    n = 0
    s, k = re.subn(r'imagesrcset="[^"]*"', f'imagesrcset="{webp_set}"', s, count=1); n += k
    s, k = re.subn(r'(<source type="image/webp" sizes="100vw" srcset=")[^"]*(")',
                   r'\1' + webp_set + r'\2', s, count=1); n += k
    s, k = re.subn(r'(srcset=")assets/hero/exterior-[^"]*\.jpg[^"]*(")',
                   r'\1' + jpg_set + r'\2', s, count=1); n += k
    s, k = re.subn(r'src="assets/hero/exterior-\d+\.jpg" width="\d+" height="\d+"',
                   f'src="{fallback}" width="{w}" height="{h}"', s, count=1); n += k
    s, k = re.subn(r'aspect-ratio:\d+/\d+;width:max\(100%,calc\(100svh \* [\d.]+\)\)',
                   f'aspect-ratio:{w}/{h};width:max(100%,calc(100svh * {w / h:.4f}))', s, count=1); n += k
    if n != 5:
        sys.exit(f'patched {n} of 5 references. index.html has drifted; fix by hand.')
    INDEX.write_text(s)
    print('index.html: srcsets, fallback, dimensions and cover factor updated (5 of 5)')

    # 3. the measurement step, written out so nobody has to remember it
    steps = f"""DOOR MEASUREMENT for {src.name} ({w}x{h})
The three .hot-* rules in index.html still hold the OLD coordinates.

1. Crop each doorway region and LOOK at it (adjust offsets until the crop
   holds exactly one sign plus its door, edge to edge):
     sips -c <h> <w> --cropOffset <top> <left> "{src}" --out /tmp/door.png
2. For each door convert edges to percentages of {w}x{h}:
     left% = left/{w}*100   top% = top/{h}*100
     width% = w/{w}*100     height% = h/{h}*100
3. Update the three rules in index.html (.hot-bridal, .hot-concept, .hot-salon)
   and keep the label text matched to the real left-to-right order.
4. node tools/shot-hero.mjs and LOOK: every label on its own door at 1440,
   1280 and 768.
5. If the new shot is front-on, all three doors may fit a phone: try enabling
   the hotspots under 900px with a shorter hero band before falling back to
   the bottom list.
"""
    (ROOT / 'tools' / 'MEASURE-DOORS.txt').write_text(steps)
    print('wrote tools/MEASURE-DOORS.txt')
    print('\nNOT DONE YET: door coordinates. Follow tools/MEASURE-DOORS.txt.')

main()
