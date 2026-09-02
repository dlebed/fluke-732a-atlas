#!/usr/bin/env python3
"""
vlm_place.py — place the designators tesseract cannot read, by asking a vision
model where each one is and then snapping its answer to the ink.

The 732A drawings are hand-lettered and the labels often touch the component
outlines, which is exactly the case a connected-component reader fails on.
A vision-language model reads those labels fine, but asked for a coordinate it
answers to about a label's width: good enough to say which glyphs are meant,
not good enough to be a marker. So the two are combined: the model names the
spot, and a connected-component pass on the full-resolution image turns that
spot into the label's own bounding box.

A model cannot be called from a script -- it is reached through an agent --
so the tool prepares the question and consumes the answer:

    tools/vlm_place.py plan  a3 board [--grid 3x3] [--tile-width 1400]
                                       [--only C1 R5 ...] [--all] [--refs-file list.json]
        cuts .build/a3/drawing_full.png into overlapping tiles, draws a grid on
        each whose labels are FULL-IMAGE pixel coordinates, and writes
            .build/a3/vlm/tiles/board/tile_<r>_<c>.png
            .build/a3/vlm/tiles/board/manifest.json
        It prints the question an agent should put to the model for each tile.

    ... the agent asks, and writes answers.json:
        {"tiles": {"tile_0_1": [{"ref": "C3", "x": 5620, "y": 2210}, ...], ...}}
        with x, y in full-image pixels as read off the grid labels ...

    tools/vlm_place.py merge a3 board answers.json [--no-refine]
        dedupes designators reported from overlapping tiles, refines each
        point onto the lettering, and writes .build/a3/vlm_board.json, which
        build_coords.py reads as the 'vlm' placement tier:
            {"space": "board", "image": {"w": W, "h": H},
             "entries": [{"ref": "C1", "x": .., "y": .., "w": .., "h": .., "refined": true}]}
        x, y are the box centre, in pixels of the space's _full.png.

    tools/vlm_place.py render a3 board [--out dir]
        every entry drawn on the image as a box with its ref, cropped and
        tiled a few at a time so a person can check them, plus an overview.

Which designators 'plan' asks for: by default the ones still unplaced in that
space -- the board's known designators (data/<asm>.js if built, else
data/<asm>.parts.json + data/<asm>.testpoints.json) minus what
data/<asm>.coords.json already places there. --all asks for every known
designator, --only for a given list. Before any of those files exist,
--refs-file supplies the list, or --all tiles the image with no list and the
question becomes 'name and place everything you can read'.

Nothing here decides a placement is right. Entries land in the 'vlm' tier,
which the app labels as needing confirmation, and 'render' exists so a person
can look before trusting them.

/usr/bin/python3 (3.9), PIL, numpy, scipy. No ImageMagick needed.
"""

import argparse
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None       # a 600 dpi D-sheet is 50 Mpx and that is fine

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
import spaces      # noqa: E402  -- needs HERE on the path first

# Each tile extends this far (as a fraction of the nominal tile) into its
# neighbours, so a label sitting on a seam is whole in at least one tile.
OVERLAP = 0.15
# A white band around each tile where the grid labels live, so they never
# sit on top of the drawing's own ink.
MARGIN = 30
FOOTER = 16
# Grid lines land roughly this many tile pixels apart, on round full-image
# coordinates: '2400' is easier to read and interpolate from than '2387'.
GRID_TARGET = 100
NICE_STEPS = (20, 25, 40, 50, 100, 150, 200, 250, 300, 400, 500, 600, 800, 1000)
# The nominal tile edge the automatic grid aims for, in full-image pixels.
AUTO_TILE = 1800

# Refinement: a reported point is snapped to the ink around it.
SEARCH_RADIUS = 90            # a component must come within this of the point
GLYPH_H = (18, 110)           # lettering height at 600 dpi
GLYPH_W_MAX = 160             # two touching glyphs at most; wider is artwork
GLYPH_W_MIN = 4               # thinner is a stray line fragment
PAD = 6
FALLBACK_BOX = (140, 70)      # when nothing qualifies: a box at the point
INK_THRESHOLD = 150           # grey below this is ink
MAX_GLYPHS = 8                # 'OUT1018' is seven; longer is a sentence
SIZE_RATIO = (0.6, 1.6)       # a chained glyph's height against its neighbour's, either way round
GAP_RATIO = 0.8               # letter spacing, as a fraction of the glyph height
SECOND_LINE_GAP = 0.5         # a label's second line sits this close, in glyph heights
STACK_GAP = 0.6               # stacked glyphs ('R' over '1' over '9') sit this close, in glyph heights
SQUARE = (0.75, 1.33)         # w/h of a lone blob that is an outline, not a label
WINDOW = 420                  # half-size of the window a point is refined in

# A point reported outside its own tile (beyond this fraction of the tile's
# size) means the grid labels were misread; it is dropped rather than placed.
OUTSIDE_TOLERANCE = 0.05

FONTS = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]

RED = (220, 40, 40)
GRID_RED = (235, 90, 90)


# --------------------------------------------------------------------------
# small helpers

def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def font(size):
    for path in FONTS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def vlm_dir(asm):
    return os.path.join(ROOT, ".build", asm, "vlm")


def tiles_dir(asm, space):
    return os.path.join(vlm_dir(asm), "tiles", space)


def manifest_path(asm, space):
    return os.path.join(tiles_dir(asm, space), "manifest.json")


def result_path(asm, space):
    return os.path.join(ROOT, ".build", asm, "vlm_%s.json" % space)


def rel(path):
    """Repository-relative when the path is inside it, absolute otherwise."""
    path = os.path.abspath(path)
    if path.startswith(ROOT + os.sep):
        return os.path.relpath(path, ROOT)
    return path


def norm_ref(ref):
    return re.sub(r"\s+", "", str(ref or "")).upper()


def sort_key(ref):
    m = re.match(r"^([A-Z]*?)(\d*)([A-Z]*?)(\d*)$", ref)
    if not m:
        return (ref, 0, "", 0)
    return (m.group(1), int(m.group(2) or 0), m.group(3), int(m.group(4) or 0))


# --------------------------------------------------------------------------
# what to look for

def known_designators(asm):
    """
    The board's designators and where they came from, or (None, reason).

    The built dataset is the authority once it exists. Before assemble.py has
    run, the curated parts and test point files carry the same names, and
    that is what a placement pass needs -- coordinates are built before the
    dataset, not after.
    """
    built = os.path.join(ROOT, "data", "%s.js" % asm)
    if os.path.exists(built):
        text = open(built, encoding="utf-8").read()
        data = json.loads(text[text.index("register(") + 9:text.rindex(");")])
        refs = {c["ref"] for c in data.get("components", [])}
        refs |= {t["ref"] for t in data.get("testpoints", [])}
        return refs, rel(built)

    refs, used = set(), []
    parts = load_json(os.path.join(ROOT, "data", "%s.parts.json" % asm))
    if parts:
        refs |= {c["ref"] for c in parts.get("components", []) if c.get("ref")}
        used.append("data/%s.parts.json" % asm)
    tps = load_json(os.path.join(ROOT, "data", "%s.testpoints.json" % asm))
    if tps:
        refs |= {t["ref"] for t in tps.get("testpoints", []) if t.get("ref")}
        used.append("data/%s.testpoints.json" % asm)
    if used:
        return refs, " + ".join(used)
    return None, ("neither data/%s.js nor data/%s.parts.json / data/%s.testpoints.json exists"
                  % (asm, asm, asm))


def placed_in(asm, space):
    """Designators data/<asm>.coords.json already places in this space, and
    the ones it says are not on the drawing at all."""
    coords = load_json(os.path.join(ROOT, "data", "%s.coords.json" % asm))
    if not coords:
        return set(), set(), False
    placed = set()
    for ref, entry in (coords.get("placement") or {}).items():
        if space == "board":
            if entry.get("board"):
                placed.add(ref)
        elif any(s.get("sheet") == space for s in entry.get("sch", [])):
            placed.add(ref)
    absent = set(coords.get("notOnDrawing") or []) if space == "board" else set()
    return placed, absent, True


def read_refs_file(path):
    data = load_json(path)
    if data is None:
        sys.exit("cannot read %s" % path)
    if isinstance(data, dict):
        data = data.get("refs") or data.get("components") or data.get("designators") or []
    out = []
    for item in data:
        ref = item.get("ref") if isinstance(item, dict) else item
        if ref:
            out.append(norm_ref(ref))
    return out


def wanted_designators(asm, space, args):
    """The list plan asks for, plus one line saying how it was arrived at."""
    known, source = known_designators(asm)
    if args.only:
        refs = [norm_ref(r) for r in args.only]
        if known is not None:
            unknown = [r for r in refs if r not in known]
            if unknown:
                print("warning: not a designator on this board (%s): %s"
                      % (source, " ".join(unknown)))
        return refs, "--only (%d given)" % len(refs)

    if args.refs_file:
        refs = read_refs_file(args.refs_file)
        return sorted(set(refs), key=sort_key), "--refs-file %s (%d)" % (args.refs_file, len(refs))

    if known is None:
        if args.all:
            return None, "no designator list: %s -- tiling without one" % source
        sys.exit("cannot tell what is unplaced: %s.\n"
                 "Give --refs-file <json list of designators>, or --all to tile "
                 "without a list and ask the model to name everything it reads." % source)

    placed, absent, have_coords = placed_in(asm, space)
    if args.all:
        refs = sorted(known - absent, key=sort_key)
        how = "every designator known from %s" % source
    else:
        refs = sorted(known - placed - absent, key=sort_key)
        how = ("%d of %d known (%s) still unplaced on %s"
               % (len(refs), len(known), source, space)
               if have_coords else
               "every designator known from %s (no data/%s.coords.json yet, so all are unplaced)"
               % (source, asm))
    if absent:
        how += "; %d listed as notOnDrawing left out" % len(absent)
    return refs, how


# --------------------------------------------------------------------------
# plan

def parse_grid(text, W, H):
    if text:
        m = re.match(r"^\s*(\d+)\s*[xX×]\s*(\d+)\s*$", text)
        if not m:
            sys.exit("--grid wants CxR, e.g. 3x3")
        return int(m.group(1)), int(m.group(2))
    return max(1, int(W / AUTO_TILE + 0.5)), max(1, int(H / AUTO_TILE + 0.5))


def nice_step(scale):
    """Full-image pixels between grid lines so they land ~GRID_TARGET tile px apart."""
    want = GRID_TARGET / scale
    return min(NICE_STEPS, key=lambda s: abs(s - want))


def label_margin(W, H):
    """MARGIN, or wider when the largest coordinate label would not fit it."""
    draw = ImageDraw.Draw(Image.new("L", (1, 1)))
    return max(MARGIN, text_size(draw, str(max(W, H)), font(11))[0] + 8)


def draw_grid(tile, x0, y0, scale, step, title, margin=MARGIN):
    """
    The tile with a labelled grid: the label on a line is that line's
    coordinate in the full image, which is what the answer is written in.
    Labels are repeated on both edges so one is always near the point being
    read, and live in a white margin so they cover no ink.
    """
    tw, th = tile.size
    # The bottom band is taller by one text line: the tile's name goes on
    # its own row so it never collides with the bottom-edge x labels.
    canvas = Image.new("RGB", (tw + 2 * margin, th + 2 * margin + FOOTER), "white")
    canvas.paste(tile.convert("RGB"), (margin, margin))
    draw = ImageDraw.Draw(canvas)
    fnt = font(14)
    small = font(11)

    first_x = int(math.ceil(x0 / step)) * step
    X = first_x
    while (X - x0) * scale < tw:
        tx = margin + (X - x0) * scale
        draw.line([(tx, margin), (tx, margin + th)], fill=GRID_RED, width=1)
        label = str(X)
        lw, lh = text_size(draw, label, fnt)
        draw.text((tx - lw / 2, 2), label, fill=RED, font=fnt)
        draw.text((tx - lw / 2, margin + th + 2), label, fill=RED, font=fnt)
        X += step

    Y = int(math.ceil(y0 / step)) * step
    while (Y - y0) * scale < th:
        ty = margin + (Y - y0) * scale
        draw.line([(margin, ty), (margin + tw, ty)], fill=GRID_RED, width=1)
        label = str(Y)
        lw, lh = text_size(draw, label, small)
        draw.text((margin - lw - 2, ty - lh / 2 - 1), label, fill=RED, font=small)
        draw.text((margin + tw + 3, ty - lh / 2 - 1), label, fill=RED, font=small)
        Y += step

    # Its own row: the tile's name, so a stray image can be told apart.
    draw.text((margin, margin + th + margin + 2), title, fill=(90, 90, 90), font=small)
    return canvas


QUESTION_WITH_LIST = (
    "This is tile {tile} cropped from the {what} of the Fluke 732A {asm} assembly. "
    "A red grid is drawn over it. The number printed at the top and bottom of "
    "each vertical line, and at the left and right of each horizontal line, is "
    "that line's coordinate in the FULL image in pixels (not a coordinate within "
    "this tile).\n"
    "Find each of these component designators as printed on the drawing: {refs}.\n"
    "For every one you can read whole on this tile, give the position of the CENTRE "
    "of its printed label (the lettering itself, not the part's outline) as full-image "
    "pixel coordinates read off the grid and interpolated between the labelled lines. "
    "Answer with only a JSON list: [{{\"ref\": \"C3\", \"x\": 5620, \"y\": 2210}}, ...]. "
    "Leave out any designator you cannot see, or that is cut off at the edge; never "
    "guess, and list nothing that is not in the list above."
)

QUESTION_NO_LIST = (
    "This is tile {tile} cropped from the {what} of the Fluke 732A {asm} assembly. "
    "A red grid is drawn over it. The number printed at the top and bottom of "
    "each vertical line, and at the left and right of each horizontal line, is "
    "that line's coordinate in the FULL image in pixels (not a coordinate within "
    "this tile).\n"
    "List every component designator printed on it (they look like C3, CR7, R12, "
    "U2, TP5, Q4, J3, E1, HR2) and for each give the position of the CENTRE of its "
    "printed label (the lettering itself, not the part's outline) as full-image pixel "
    "coordinates read off the grid and interpolated between the labelled lines. "
    "Answer with only a JSON list: [{{\"ref\": \"C3\", \"x\": 5620, \"y\": 2210}}, ...]. "
    "Ignore pin numbers, net names, values and part numbers. Leave out anything you "
    "cannot read whole; never guess."
)


def plan(asm, space, args):
    src = spaces.require(os.path.join(ROOT, ".build", asm), space)
    image = Image.open(src)
    W, H = image.size
    image = image.convert("L")

    refs, how = wanted_designators(asm, space, args)
    if refs is not None and not refs:
        print("nothing to look for on %s %s: %s" % (asm, space, how))
        return

    cols, rows = parse_grid(args.grid, W, H)
    out = tiles_dir(asm, space)
    os.makedirs(out, exist_ok=True)
    for old in os.listdir(out):
        if old.startswith("tile_") and old.endswith(".png"):
            os.remove(os.path.join(out, old))

    nominal_w, nominal_h = W / cols, H / rows
    pad_x, pad_y = nominal_w * OVERLAP, nominal_h * OVERLAP
    margin = label_margin(W, H)
    what = "component locator drawing" if space == "board" else "schematic sheet %s" % space
    tiles = []
    for r in range(rows):
        for c in range(cols):
            x0 = max(0, int(round(c * nominal_w - pad_x)))
            y0 = max(0, int(round(r * nominal_h - pad_y)))
            x1 = min(W, int(round((c + 1) * nominal_w + pad_x)))
            y1 = min(H, int(round((r + 1) * nominal_h + pad_y)))
            crop = image.crop((x0, y0, x1, y1))
            scale = min(1.0, args.tile_width / float(x1 - x0))
            if scale < 1.0:
                crop = crop.resize((int(round((x1 - x0) * scale)),
                                    int(round((y1 - y0) * scale))), Image.LANCZOS)
            tid = "tile_%d_%d" % (r, c)
            step = nice_step(scale)
            canvas = draw_grid(crop, x0, y0, scale, step,
                               "%s %s %s  x %d-%d  y %d-%d" % (asm, space, tid, x0, x1, y0, y1),
                               margin)
            dest = os.path.join(out, tid + ".png")
            canvas.save(dest, optimize=True)
            tiles.append({
                "id": tid, "row": r, "col": c,
                "file": rel(dest),
                "box": [x0, y0, x1, y1],
                "scale": round(scale, 5),
                "gridStep": step,
                "margin": margin,
                "tileSize": list(canvas.size),
                "refs": refs,
            })

    question = (QUESTION_WITH_LIST if refs is not None else QUESTION_NO_LIST)
    manifest = {
        "assembly": asm, "space": space, "generatedBy": "tools/vlm_place.py plan",
        "image": {"w": W, "h": H, "file": rel(src)},
        "grid": "%dx%d" % (cols, rows), "tileWidth": args.tile_width,
        "overlap": OVERLAP,
        "refs": refs, "refsFrom": how,
        "question": question.replace("{what}", what).replace("{asm}", asm.upper())
                            .replace("{refs}", ", ".join(refs) if refs else "")
                            .replace("{{", "{").replace("}}", "}"),
        "answersShape": {"tiles": {"tile_<r>_<c>": [{"ref": "C3", "x": 5620, "y": 2210}]}},
        "tiles": tiles,
    }
    with open(manifest_path(asm, space), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)

    print("%d tiles (%dx%d, %d px wide + %d px margins, scale %s) in %s"
          % (len(tiles), cols, rows, args.tile_width, margin,
             "/".join(sorted({str(t["scale"]) for t in tiles})), rel(out)))
    print("image %s is %dx%d; grid labels are full-image pixels" % (rel(src), W, H))
    if refs is None:
        print("NO DESIGNATOR LIST -- %s" % how)
        print("the question asks the model to name everything it reads; merge will "
              "keep whatever looks like a designator")
    else:
        print("looking for %d designators: %s" % (len(refs), how))
    print("manifest: %s" % rel(manifest_path(asm, space)))
    print()
    print("Ask the model this about each tile (substituting the tile's name):")
    print("-" * 72)
    print(manifest["question"].replace("{tile}", "<tile>"))
    print("-" * 72)
    for t in tiles:
        print("  %-10s %-46s full-image x %d-%d  y %d-%d"
              % (t["id"], t["file"], t["box"][0], t["box"][2], t["box"][1], t["box"][3]))
    print()
    print("Collect the answers as")
    print('  {"tiles": {"tile_0_0": [{"ref": "C1", "x": 512, "y": 620}, ...], ...}}')
    print("then: tools/vlm_place.py merge %s %s <answers.json>" % (asm, space))


# --------------------------------------------------------------------------
# merge

def load_answers(path, manifest):
    """
    Every (tile, ref, x, y) the model reported, after the checks that need no
    image: the tile exists, the ref is a name, the point is a number and lies
    within the tile it was read from. Returns (reports, problems).
    """
    data = load_json(path)
    if data is None:
        sys.exit("cannot read %s" % path)
    tiles = data.get("tiles", data) if isinstance(data, dict) else None
    if not isinstance(tiles, dict):
        sys.exit('%s should be {"tiles": {"tile_r_c": [{"ref","x","y"}, ...]}}' % path)
    by_id = {t["id"]: t for t in manifest["tiles"]}
    reports, problems = [], []
    for tid, items in tiles.items():
        tile = by_id.get(tid)
        if not tile:
            problems.append("%s: not a tile in the manifest -- ignored (%d items)"
                            % (tid, len(items) if isinstance(items, list) else 0))
            continue
        if not isinstance(items, list):
            problems.append("%s: expected a list, got %s" % (tid, type(items).__name__))
            continue
        x0, y0, x1, y1 = tile["box"]
        tol_x, tol_y = (x1 - x0) * OUTSIDE_TOLERANCE, (y1 - y0) * OUTSIDE_TOLERANCE
        for item in items:
            if not isinstance(item, dict):
                problems.append("%s: %r is not an object" % (tid, item))
                continue
            ref = norm_ref(item.get("ref"))
            try:
                x, y = float(item["x"]), float(item["y"])
            except (KeyError, TypeError, ValueError):
                problems.append("%s: %s has no numeric x, y" % (tid, ref or "?"))
                continue
            if not ref:
                problems.append("%s: a point at %d,%d with no ref" % (tid, x, y))
                continue
            if not (x0 - tol_x <= x <= x1 + tol_x and y0 - tol_y <= y <= y1 + tol_y):
                problems.append("%s: %s at %d,%d is outside the tile (x %d-%d, y %d-%d) "
                                "-- grid labels misread, dropped"
                                % (tid, ref, x, y, x0, x1, y0, y1))
                continue
            reports.append({"tile": tid, "ref": ref, "x": x, "y": y})
    return reports, problems


def dedupe(reports, manifest):
    """
    One report per designator. A label in the overlap band is reported from
    two tiles; the reading from the tile whose centre it is nearest to is the
    one made with the most context around it, so that one is kept.
    """
    by_id = {t["id"]: t for t in manifest["tiles"]}

    def centrality(rep):
        x0, y0, x1, y1 = by_id[rep["tile"]]["box"]
        cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        return math.hypot((rep["x"] - cx) / (x1 - x0), (rep["y"] - cy) / (y1 - y0))

    groups = {}
    for rep in reports:
        groups.setdefault(rep["ref"], []).append(rep)
    kept, notes = [], []
    for ref in sorted(groups, key=sort_key):
        reps = sorted(groups[ref], key=centrality)
        best = reps[0]
        kept.append(best)
        if len(reps) > 1:
            spread = max(math.hypot(r["x"] - best["x"], r["y"] - best["y"]) for r in reps[1:])
            notes.append("%s reported %d times (%s); kept %s at %d,%d%s"
                         % (ref, len(reps), " ".join(r["tile"] for r in reps),
                            best["tile"], best["x"], best["y"],
                            "; the reports are %d px apart, so one of them is wrong"
                            % spread if spread > 150 else ""))
    return kept, notes


def components_near(gray, px, py):
    """
    Glyph-sized connected ink components in a window around the point, each
    as a dict with its full-image bbox. Labelling only the window rather than
    the whole sheet keeps this cheap on a 50 Mpx image.
    """
    H, W = gray.shape
    wx0, wy0 = max(0, int(px) - WINDOW), max(0, int(py) - WINDOW)
    wx1, wy1 = min(W, int(px) + WINDOW), min(H, int(py) + WINDOW)
    ink = gray[wy0:wy1, wx0:wx1] < INK_THRESHOLD
    labels, n = ndimage.label(ink)
    if not n:
        return []
    out = []
    for i, sl in enumerate(ndimage.find_objects(labels), 1):
        if sl is None:
            continue
        ys, xs = sl
        h, w = ys.stop - ys.start, xs.stop - xs.start
        if not (GLYPH_H[0] <= h <= GLYPH_H[1]) or not (GLYPH_W_MIN <= w <= GLYPH_W_MAX):
            continue
        out.append({"x0": wx0 + xs.start, "x1": wx0 + xs.stop,
                    "y0": wy0 + ys.start, "y1": wy0 + ys.stop, "w": w, "h": h})
    return out


def bbox_distance(c, px, py):
    dx = max(c["x0"] - px, 0, px - c["x1"])
    dy = max(c["y0"] - py, 0, py - c["y1"])
    return math.hypot(dx, dy)


def linked(a, b, axis):
    """
    Two glyphs belong to one label when they line up across the reading
    direction and sit close along it.

    axis 'x' is horizontal text: heights alike, vertical ranges overlap,
    small horizontal gap. axis 'y' covers two different things this drawing
    does: text rotated 90 degrees (the glyphs' widths are letter heights, so
    they are alike and no wider than a letter is tall) and glyphs stacked
    one over another ('R' over '1' over '9' inside a resistor body: heights
    alike, and the stack is tight -- a neighbouring label sits a full glyph
    or more away). A diode dome or a screw head beside the label is
    glyph-sized too; what keeps it out is that it matches neither pattern.
    """
    similar = lambda p, q: max(p, q) / float(min(p, q)) <= SIZE_RATIO[1]
    if axis == "x":
        if not similar(a["h"], b["h"]):
            return False
        overlap = min(a["y1"], b["y1"]) - max(a["y0"], b["y0"])
        if overlap < 0.3 * min(a["h"], b["h"]):
            return False
        gap = max(a["x0"], b["x0"]) - min(a["x1"], b["x1"])
        return gap <= GAP_RATIO * max(a["h"], b["h"])

    overlap = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
    if overlap < 0.3 * min(a["w"], b["w"]):
        return False
    gap = max(a["y0"], b["y0"]) - min(a["y1"], b["y1"])
    rotated = (similar(a["w"], b["w"]) and max(a["w"], b["w"]) <= GLYPH_H[1]
               and gap <= GAP_RATIO * max(a["w"], b["w"]))
    stacked = similar(a["h"], b["h"]) and gap <= STACK_GAP * max(a["h"], b["h"])
    return rotated or stacked


def chain(seed, comps, axis):
    """The glyphs reachable from the seed along one reading direction."""
    got, frontier = [seed], [seed]
    rest = [c for c in comps if c is not seed]
    while frontier and len(got) < 3 * MAX_GLYPHS:
        cur = frontier.pop()
        for c in list(rest):
            if linked(cur, c, axis):
                rest.remove(c)
                got.append(c)
                frontier.append(c)
    if len(got) > MAX_GLYPHS:
        # A run of text longer than any designator; keep the glyphs nearest
        # the seed in reading order so the box stays a label, not a sentence.
        key = "x0" if axis == "x" else "y0"
        got.sort(key=lambda c: c[key])
        i = got.index(seed)
        lo = max(0, min(i - MAX_GLYPHS // 2, len(got) - MAX_GLYPHS))
        got = got[lo:lo + MAX_GLYPHS]
    return got


def second_line(line, comps):
    """
    A designator written on two lines -- 'CR' over '11', which this drawing
    does beside narrow parts -- is one label, so glyphs of the same height
    sitting directly under or over the line, within half a glyph of it,
    are taken in. A neighbouring part's label sits a full glyph or more
    away and stays out.
    """
    h = max(c["h"] for c in line)
    x0, x1 = min(c["x0"] for c in line), max(c["x1"] for c in line)
    y0, y1 = min(c["y0"] for c in line), max(c["y1"] for c in line)
    extra = []
    for c in comps:
        if c in line or not (SIZE_RATIO[0] <= c["h"] / float(h) <= SIZE_RATIO[1]):
            continue
        overlap = min(x1, c["x1"]) - max(x0, c["x0"])
        gap = max(y0, c["y0"]) - min(y1, c["y1"])
        if overlap >= 0.5 * c["w"] and gap <= SECOND_LINE_GAP * h:
            extra.append(c)
    if len(line) + len(extra) > MAX_GLYPHS:
        return line
    return line + extra


def label_from(seed, comps):
    """The glyphs of the label the seed belongs to, read in whichever
    direction collects more of them, plus a second line if it has one."""
    horizontal = chain(seed, comps, "x")
    vertical = chain(seed, comps, "y")
    if len(vertical) > len(horizontal):
        return vertical
    return second_line(horizontal, comps)


def bbox(glyphs):
    return (min(c["x0"] for c in glyphs), min(c["y0"] for c in glyphs),
            max(c["x1"] for c in glyphs), max(c["y1"] for c in glyphs))


def refine(gray, px, py):
    """
    Snap a reported point to the lettering there.

    Every glyph-sized component within SEARCH_RADIUS seeds a candidate label
    (the glyphs chained from it). The model reports the centre of the label,
    so the candidate whose centre is nearest the point is the one meant --
    not the candidate grown from the nearest component, which on a point that
    fell between two labels, or on a screw head beside one, is the wrong
    one. A lone near-square blob (a screw head, a diode dome, a pad) is never
    a designator, so it only counts when nothing else is there. Returns the
    padded box as (x, y, w, h, refined).
    """
    comps = components_near(gray, px, py)
    seeds = sorted((c for c in comps if bbox_distance(c, px, py) <= SEARCH_RADIUS),
                   key=lambda c: bbox_distance(c, px, py))
    if not seeds:
        return int(round(px)), int(round(py)), FALLBACK_BOX[0], FALLBACK_BOX[1], False

    candidates, seen = [], set()
    for seed in seeds:
        glyphs = label_from(seed, comps)
        key = tuple(sorted((c["x0"], c["y0"]) for c in glyphs))
        if key in seen:
            continue
        seen.add(key)
        x0, y0, x1, y1 = bbox(glyphs)
        blob = (len(glyphs) == 1 and
                SQUARE[0] <= glyphs[0]["w"] / float(glyphs[0]["h"]) <= SQUARE[1])
        candidates.append((blob, math.hypot((x0 + x1) / 2.0 - px, (y0 + y1) / 2.0 - py),
                           (x0, y0, x1, y1)))
    candidates.sort(key=lambda c: (c[0], c[1]))
    x0, y0, x1, y1 = candidates[0][2]
    x0, y0, x1, y1 = x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD
    return (int(round((x0 + x1) / 2.0)), int(round((y0 + y1) / 2.0)),
            int(x1 - x0), int(y1 - y0), True)


def merge(asm, space, answers_path, do_refine):
    manifest = load_json(manifest_path(asm, space))
    if not manifest:
        sys.exit("no %s -- run 'plan' first" % rel(manifest_path(asm, space)))
    src = spaces.require(os.path.join(ROOT, ".build", asm), space)
    W, H = manifest["image"]["w"], manifest["image"]["h"]

    reports, problems = load_answers(answers_path, manifest)
    known, source = known_designators(asm)
    wanted = manifest.get("refs")
    unknown = []
    if known is not None:
        keep = []
        for rep in reports:
            if rep["ref"] in known:
                keep.append(rep)
            else:
                unknown.append("%s@%s" % (rep["ref"], rep["tile"]))
        reports = keep
    kept, dupes = dedupe(reports, manifest)

    entries, unrefined = [], []
    if do_refine and kept:
        gray = np.asarray(Image.open(src).convert("L"))
        if gray.shape != (H, W):
            sys.exit("%s is %dx%d but the manifest was planned on %dx%d -- re-run plan"
                     % (rel(src), gray.shape[1], gray.shape[0], W, H))
    for rep in kept:
        if do_refine:
            x, y, w, h, ok = refine(gray, rep["x"], rep["y"])
        else:
            x, y, w, h, ok = int(round(rep["x"])), int(round(rep["y"])), \
                FALLBACK_BOX[0], FALLBACK_BOX[1], False
        x = max(0, min(W - 1, x))
        y = max(0, min(H - 1, y))
        entries.append({"ref": rep["ref"], "x": x, "y": y, "w": w, "h": h,
                        "refined": ok, "tile": rep["tile"],
                        "reported": [int(round(rep["x"])), int(round(rep["y"]))]})
        if not ok:
            unrefined.append(rep["ref"])

    result = {
        "space": space,
        "image": {"w": W, "h": H},
        "generatedBy": "tools/vlm_place.py merge",
        "answers": rel(answers_path),
        "refined": bool(do_refine),
        "entries": entries,
    }
    dest = result_path(asm, space)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)

    print("VLM placement -- %s %s" % (asm.upper(), space))
    print("=" * 60)
    print("%d reports read from %s" % (len(reports) + len(unknown), answers_path))
    for p in problems:
        print("  ! " + p)
    if unknown:
        print("  %d not a designator on this board (%s), dropped: %s"
              % (len(unknown), source, " ".join(unknown)))
    for note in dupes:
        print("  " + note)
    print("%d designators placed, %d refined onto lettering, %d left as a %dx%d box at the point"
          % (len(entries), len(entries) - len(unrefined), len(unrefined), *FALLBACK_BOX))
    if unrefined:
        print("  unrefined (no glyph-sized ink within %d px -- look at these first): %s"
              % (SEARCH_RADIUS, " ".join(unrefined)))
    if wanted:
        got = {e["ref"] for e in entries}
        missing = [r for r in wanted if r not in got]
        if missing:
            print("%d of the %d asked for were not placed: %s"
                  % (len(missing), len(wanted), " ".join(missing)))
        else:
            print("every one of the %d asked for was placed" % len(wanted))
    print("written to %s" % rel(dest))
    print("look at them: tools/vlm_place.py render %s %s   then tools/build_coords.py %s"
          % (asm, space, asm))


# --------------------------------------------------------------------------
# render

CROP = (640, 420)
PER_SHEET = 8
COLUMNS = 2
SHEET_WIDTH = 1500
OVERVIEW_WIDTH = 2400


def render(asm, space, out_dir):
    data = load_json(result_path(asm, space))
    if not data:
        sys.exit("no %s -- run 'merge' first" % rel(result_path(asm, space)))
    src = spaces.require(os.path.join(ROOT, ".build", asm), space)
    image = Image.open(src).convert("RGB")
    W, H = image.size
    if (W, H) != (data["image"]["w"], data["image"]["h"]):
        sys.exit("%s is %dx%d but vlm_%s.json was merged against %dx%d"
                 % (rel(src), W, H, space, data["image"]["w"], data["image"]["h"]))
    entries = sorted(data["entries"], key=lambda e: sort_key(e["ref"]))
    if not entries:
        print("no entries in %s" % rel(result_path(asm, space)))
        return
    out_dir = out_dir or os.path.join(vlm_dir(asm), "render", space)
    os.makedirs(out_dir, exist_ok=True)
    fnt, small = font(30), font(18)

    def box_of(e):
        return (e["x"] - e["w"] / 2.0, e["y"] - e["h"] / 2.0,
                e["x"] + e["w"] / 2.0, e["y"] + e["h"] / 2.0)

    def crop_entry(e):
        cw, ch = CROP
        x0 = max(0, min(W - cw, int(e["x"] - cw / 2)))
        y0 = max(0, min(H - ch, int(e["y"] - ch / 2)))
        tile = image.crop((x0, y0, x0 + cw, y0 + ch))
        draw = ImageDraw.Draw(tile)
        bx0, by0, bx1, by1 = box_of(e)
        colour = RED if e.get("refined") else (230, 140, 0)
        draw.rectangle([bx0 - x0, by0 - y0, bx1 - x0, by1 - y0], outline=colour, width=3)
        if e.get("reported"):
            rx, ry = e["reported"][0] - x0, e["reported"][1] - y0
            draw.line([(rx - 8, ry), (rx + 8, ry)], fill=(40, 120, 220), width=2)
            draw.line([(rx, ry - 8), (rx, ry + 8)], fill=(40, 120, 220), width=2)
        label = "%s  %s" % (e["ref"], "vlm" if e.get("refined") else "vlm, UNREFINED")
        lw, lh = text_size(draw, label, fnt)
        draw.rectangle([6, 6, 14 + lw, 14 + lh], fill="white")
        draw.text((10, 8), label, fill=colour, font=fnt)
        return tile

    sheets = []
    for start in range(0, len(entries), PER_SHEET):
        chunk = entries[start:start + PER_SHEET]
        tiles = [crop_entry(e) for e in chunk]
        rows = int(math.ceil(len(tiles) / float(COLUMNS)))
        gap = 6
        sheet = Image.new("RGB", (COLUMNS * (CROP[0] + gap) + gap, rows * (CROP[1] + gap) + gap),
                          (34, 34, 34))
        for i, tile in enumerate(tiles):
            sheet.paste(tile, (gap + (i % COLUMNS) * (CROP[0] + gap),
                               gap + (i // COLUMNS) * (CROP[1] + gap)))
        if sheet.size[0] > SHEET_WIDTH:
            s = SHEET_WIDTH / float(sheet.size[0])
            sheet = sheet.resize((SHEET_WIDTH, int(sheet.size[1] * s)), Image.LANCZOS)
        dest = os.path.join(out_dir, "%s_%s_%02d.png" % (asm, space, start // PER_SHEET + 1))
        sheet.save(dest, optimize=True)
        sheets.append(dest)
        print("%s  (%s)" % (rel(dest), " ".join(e["ref"] for e in chunk)))

    # The whole image at a glance, so a marker that landed on the wrong side
    # of the board shows up even if its own crop looks plausible.
    s = min(1.0, OVERVIEW_WIDTH / float(W))
    overview = image.resize((int(W * s), int(H * s)), Image.LANCZOS)
    draw = ImageDraw.Draw(overview)
    for e in entries:
        bx0, by0, bx1, by1 = box_of(e)
        colour = RED if e.get("refined") else (230, 140, 0)
        draw.rectangle([bx0 * s, by0 * s, bx1 * s, by1 * s], outline=colour, width=2)
        draw.text((bx1 * s + 2, by0 * s - 2), e["ref"], fill=colour, font=small)
    dest = os.path.join(out_dir, "%s_%s_overview.png" % (asm, space))
    overview.save(dest, optimize=True)
    print("%s  (all %d, red = refined, orange = unrefined, blue cross = the model's point)"
          % (rel(dest), len(entries)))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="action")
    sub.required = True

    p = sub.add_parser("plan", help="cut the image into gridded tiles and write the manifest")
    p.add_argument("assembly")
    p.add_argument("space", help="board, or sh1 / sh2 / ... for a schematic sheet")
    p.add_argument("--grid", help="tiles across x down, e.g. 3x3 (default: about %d px tiles)" % AUTO_TILE)
    p.add_argument("--tile-width", type=int, default=1400,
                   help="downscale each tile to this many px wide (default 1400)")
    p.add_argument("--only", nargs="+", metavar="REF", help="ask only for these designators")
    p.add_argument("--all", action="store_true",
                   help="ask for every known designator, not just the unplaced ones")
    p.add_argument("--refs-file", metavar="JSON",
                   help="a JSON list of designators, for before the data files exist")

    m = sub.add_parser("merge", help="turn answers.json into .build/<asm>/vlm_<space>.json")
    m.add_argument("assembly")
    m.add_argument("space")
    m.add_argument("answers", help='{"tiles": {"tile_r_c": [{"ref","x","y"}, ...]}}')
    m.add_argument("--no-refine", action="store_true",
                   help="keep the model's points as %dx%d boxes; do not snap to the ink"
                   % FALLBACK_BOX)

    r = sub.add_parser("render", help="draw the merged entries on the image for review")
    r.add_argument("assembly")
    r.add_argument("space")
    r.add_argument("--out", metavar="DIR", help="where to write (default .build/<asm>/vlm/render/<space>)")

    args = ap.parse_args()
    asm = args.assembly.lower()
    space = args.space.lower()
    if args.action == "plan":
        plan(asm, space, args)
    elif args.action == "merge":
        merge(asm, space, args.answers, not args.no_refine)
    else:
        render(asm, space, args.out)


if __name__ == "__main__":
    main()
