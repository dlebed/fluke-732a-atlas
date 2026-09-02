#!/usr/bin/env /usr/bin/python3
"""
find_outline.py — measure the crop rectangles on a scanned figure page.

    tools/find_outline.py .build/pages/p600-88.png            # frame + largest outline
    tools/find_outline.py .build/pages/p600-88.png --show out.png --scale 8

Prints the drawn figure frame (the long horizontal/vertical rules that box the
figure) and, inside it, the bounding box of the largest connected ink component,
which on a component-locator page is the PCB outline. Both are printed as
ImageMagick geometry (WxH+X+Y) in pixels of the input image. --show renders a
downscaled copy with both rectangles drawn on it, to be looked at before the
numbers are trusted.
"""
import argparse
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("page")
ap.add_argument("--show")
ap.add_argument("--scale", type=int, default=8)
ap.add_argument("--min-frac", type=float, default=0.45,
                help="a rule must span this fraction of the page to count as frame")
a = ap.parse_args()

im = Image.open(a.page).convert("L")
w, h = im.size
ink = np.asarray(im) < 128

# --- the frame: longest rules ---------------------------------------------
# A rule a few pixels thick and a fraction of a degree off square never fills
# one row; dilate along the rule's own direction first so the profile sees it.
# The horizontal rules are the reliable pair (they are what the profile finds
# on every page); the frame's x extent is then read off the ink in those rows
# rather than from the vertical rules, which on some scans are too light.
thick = ndimage.maximum_filter(ink, size=(9, 1))
rows = thick.sum(axis=1) / w
ry = np.where(rows > a.min_frac)[0]
if len(ry) < 2:
    raise SystemExit("no frame found (try --min-frac lower)")
fy0, fy1 = ry.min(), ry.max()
band = ink[fy0:fy0 + 12].any(axis=0) | ink[fy1 - 11:fy1 + 1].any(axis=0)
xs = np.where(band)[0]
fx0, fx1 = xs.min(), xs.max()
print("frame  %dx%d+%d+%d" % (fx1 - fx0 + 1, fy1 - fy0 + 1, fx0, fy0))

# --- largest ink component inside the frame -------------------------------
inner = ink[fy0 + 40:fy1 - 40, fx0 + 40:fx1 - 40]
small = inner[::4, ::4]
lab, n = ndimage.label(small, structure=np.ones((3, 3)))
objs = ndimage.find_objects(lab)
best, area = None, 0
for i, sl in enumerate(objs):
    ar = (sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start)
    if ar > area:
        best, area = sl, ar
y0, y1 = best[0].start * 4 + fy0 + 40, best[0].stop * 4 + fy0 + 40
x0, x1 = best[1].start * 4 + fx0 + 40, best[1].stop * 4 + fx0 + 40
print("outline %dx%d+%d+%d" % (x1 - x0, y1 - y0, x0, y0))

if a.show:
    s = a.scale
    out = im.resize((w // s, h // s)).convert("RGB")
    d = ImageDraw.Draw(out)
    d.rectangle([fx0 // s, fy0 // s, fx1 // s, fy1 // s], outline=(0, 120, 255), width=2)
    d.rectangle([x0 // s, y0 // s, x1 // s, y1 // s], outline=(255, 0, 0), width=2)
    out.save(a.show)
    print("wrote", a.show)
