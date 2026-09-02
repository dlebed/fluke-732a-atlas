#!/usr/bin/env python3
"""
build_coords.py — turn the reader passes plus hand corrections into
data/<asm>.coords.json.

Three sources, in rising order of authority:

  .build/<asm>/ocr_<space>.json      tesseract (ocr_designators.py)
  .build/<asm>/vlm_<space>.json      a vision model (vlm_place.py merge)
  data/<asm>.coords.overrides.json   hand corrections

Each placement carries how it was arrived at, and the app shows that: a marker
the reader placed and several passes agreed on is not the same claim as one a
single pass produced, neither is the same as one a vision model named on a
hand-lettered drawing, and none of them is the same as one a person put there.

  verified   placed or confirmed by hand
  agreed     several independent OCR passes landed on the same spot
  single     one pass found it, nothing corroborates it
  ambiguous  passes disagreed, or the reader and the vision model did
  collision  two designators claim the same spot
  vlm        read by a vision model from the drawing; the reader had nothing

The vision model fills in where tesseract cannot read: a designator the reader
did not place takes the model's box as `vlm`. Where both placed it, the
reader's box is kept unless the two disagree by more than a box width -- then
the model's box wins and the placement is `ambiguous`, because one of them is
looking at the wrong label and a person has to say which. Overrides win over
both, and `confirm: [refs]` in the overrides marks a read position as verified
without retyping its geometry.

Usage: tools/build_coords.py <assembly-id>
"""

import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
import spaces      # noqa: E402  -- needs HERE on the path first

# Marker footprint for a test point placed with the "row" shorthand: wide
# enough to span the label and the pad beside it, tall enough for the text.
ROW_TP_W, ROW_TP_H = 105, 118
DEFAULT_PAD = 1.35      # OCR boxes hug the glyphs; a little margin reads better

# Outlines a marker may be drawn with. A shape is only meaningful on a hand
# placed entry: a read designator's box is the lettering, not the part, and an
# ellipse inscribed in a rotated label is a thin oval beside the component
# rather than a ring around it. So a shape has to arrive with a body box, and
# only the overrides carry those.
SHAPES = ("rect", "circle", "point")

TIERS = ("verified", "agreed", "ambiguous", "single", "collision", "vlm")


def load(path, default=None):
    if not os.path.exists(path):
        return default
    return json.load(open(path, encoding="utf-8"))


class _Pairs(list):
    """A JSON object kept as its key/value pairs, duplicates and all."""


def duplicate_keys(path):
    """
    Every key repeated inside one JSON object, as "a.b.c" paths in file order.

    JSON parsers take the last value for a repeated key and say nothing about
    it. In a hand-edited overrides file that is silent data loss rather than a
    curiosity: paste four entries under "board" when one of those designators
    is already there and the whole object is replaced rather than merged, so
    three of the four vanish. The only symptom is that the markers do not
    appear.

    object_pairs_hook is the one point where the duplicate still exists -- but
    it fires innermost-first with no idea where it is in the file, so it is
    used only to *preserve* the pairs, and the tree is walked afterwards to
    attach a path to each one.
    """
    tree = json.load(open(path, encoding="utf-8"), object_pairs_hook=_Pairs)
    found = []

    def walk(node, trail):
        if isinstance(node, _Pairs):
            seen = set()
            for key, value in node:
                where = trail + [key]
                if key in seen:
                    found.append(".".join(where))
                seen.add(key)
                walk(value, where)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, trail + ["[%d]" % i])

    walk(tree, [])
    return found


def image_size(build_dir, space, *records):
    """
    Width and height of a space's full-resolution image.

    The reader outputs record the size they were measured against, and those
    are versioned while the image is not; the image itself is the fact when
    it is there. Both are consulted so a fresh checkout with only the reader
    output still builds.
    """
    path = spaces.image_path(build_dir, space)
    if path and os.path.exists(path):
        try:
            out = subprocess.run(["magick", "identify", "-format", "%w %h", path],
                                 capture_output=True, text=True, check=True).stdout.split()
            return int(out[0]), int(out[1])
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            pass
    for rec in records:
        if not rec:
            continue
        if rec.get("width") and rec.get("height"):
            return rec["width"], rec["height"]
        img = rec.get("image") or {}
        if img.get("w") and img.get("h"):
            return img["w"], img["h"]
    return None


def load_vlm(build_dir, space, W, H):
    """
    The vision model's placements for one space, normalised.

    vlm_place.py writes pixels of that space's _full.png with x, y at the box
    centre; the file records the image size it was read against, and a
    mismatch means the crop was re-extracted since and every entry is stale.
    """
    data = load(os.path.join(build_dir, "vlm_%s.json" % space))
    if not data:
        return {}
    img = data.get("image") or {}
    if img and (img.get("w") != W or img.get("h") != H):
        sys.exit("vlm_%s.json was read against %sx%s but the image is %dx%d -- "
                 "re-run tools/vlm_place.py" % (space, img.get("w"), img.get("h"), W, H))
    out = {}
    for e in data.get("entries") or []:
        ref = e.get("ref")
        if not ref or e.get("x") is None or e.get("y") is None:
            continue
        w = e.get("w") or 140
        h = e.get("h") or 70
        out[ref] = {
            "x": round(e["x"] / float(W), 5), "y": round(e["y"] / float(H), 5),
            "w": round(w / float(W), 5), "h": round(h / float(H), 5),
            "refined": bool(e.get("refined", True)),
        }
    return out


def disagree(reader, vlm, W, H):
    """More than a box width apart, in pixels: one of them is on another label."""
    dx = (reader["x"] - vlm["x"]) * W
    dy = (reader["y"] - vlm["y"]) * H
    width = max(reader.get("w", 0), vlm.get("w", 0)) * W
    return math.hypot(dx, dy) > width


def vlm_note(entry):
    if entry.get("refined"):
        return None
    return "Placed by a vision model; the box could not be snapped to the lettering"


def build(asm):
    build_dir = os.path.join(ROOT, ".build", asm)
    ocr = load(os.path.join(build_dir, "ocr_board.json"))
    vlm_raw = load(os.path.join(build_dir, "vlm_board.json"))
    if not ocr and not vlm_raw:
        sys.exit("no reader pass for %s -- run tools/ocr_designators.py or "
                 "tools/vlm_place.py first" % asm)
    over_path = os.path.join(ROOT, "data", "%s.coords.overrides.json" % asm)
    if os.path.exists(over_path):
        repeated = duplicate_keys(over_path)
        if repeated:
            sys.exit("data/%s.coords.overrides.json repeats %d key%s, and JSON "
                     "keeps only the last of each:\n    %s\nMerge them by hand -- "
                     "the earlier entries are being discarded."
                     % (asm, len(repeated), "" if len(repeated) == 1 else "s",
                        "\n    ".join(repeated)))
    over = load(over_path, {}) or {}

    size = image_size(build_dir, "board", ocr, vlm_raw)
    if not size:
        sys.exit("cannot tell how large .build/%s/drawing_full.png is" % asm)
    W, H = size
    if ocr and (ocr.get("width") != W or ocr.get("height") != H):
        sys.exit("ocr_board.json was read against %sx%s but the drawing is %dx%d -- "
                 "re-run tools/ocr_designators.py" % (ocr.get("width"), ocr.get("height"), W, H))
    declared = over.get("imageSize", {})
    if declared and (declared.get("w") != W or declared.get("h") != H):
        sys.exit("overrides were measured against %sx%s but the drawing is %dx%d"
                 % (declared.get("w"), declared.get("h"), W, H))

    dropped = set(over.get("drop", []))
    not_on_drawing = set(over.get("notOnDrawing", []))
    manual = over.get("board", {})
    confirm = list(over.get("confirm", []))
    clash = sorted((set(confirm) & (dropped | set(manual))), key=sort_key)
    if clash:
        sys.exit("confirm names %s, which the same file also drops or places by hand -- "
                 "pick one" % " ".join(clash))

    placement = {}
    counts = dict((t, 0) for t in TIERS)

    hits = (ocr or {}).get("hits", {})
    vlm = load_vlm(build_dir, "board", W, H)
    disagreed = []
    for ref, hit in hits.items():
        if ref in dropped or ref in manual:
            continue
        box = {"x": hit["x"], "y": hit["y"],
               "w": round(hit["w"] * DEFAULT_PAD, 5),
               "h": round(hit["h"] * DEFAULT_PAD, 5),
               "shape": "rect"}
        tier = hit["confidence"]
        note = None
        other = vlm.get(ref)
        if other and disagree(box, other, W, H):
            # Two readers, two places: the model's box is taken because it
            # reads the fused lettering tesseract guesses at, but the
            # disagreement itself is the finding and it is flagged for review.
            box = {"x": other["x"], "y": other["y"], "w": other["w"], "h": other["h"],
                   "shape": "rect"}
            tier = "ambiguous"
            note = "The reader and the vision model disagreed about where this is"
            disagreed.append(ref)
        placement[ref] = {"board": box, "placement": tier}
        if note:
            placement[ref]["placementNote"] = note
        counts[tier] = counts.get(tier, 0) + 1

    for ref, entry in vlm.items():
        if ref in dropped or ref in manual or ref in placement:
            continue
        placement[ref] = {
            "board": {"x": entry["x"], "y": entry["y"],
                      "w": entry["w"], "h": entry["h"], "shape": "rect"},
            "placement": "vlm",
        }
        if vlm_note(entry):
            placement[ref]["placementNote"] = vlm_note(entry)
        counts["vlm"] += 1

    shaped = 0
    for ref, box in manual.items():
        w = box.get("w", ROW_TP_W if box.get("row") else 110)
        h = box.get("h", ROW_TP_H if box.get("row") else 115)
        shape = box.get("shape", "rect")
        if shape not in SHAPES:
            sys.exit("%s declares shape '%s'; known shapes are %s"
                     % (ref, shape, ", ".join(SHAPES)))
        entry = {
            "board": {
                "x": round(box["x"] / W, 5), "y": round(box["y"] / H, 5),
                "w": round(w / W, 5), "h": round(h / H, 5),
                "shape": shape,
            },
            "verified": True,
            "placement": "verified",
        }
        if box.get("note"):
            entry["placementNote"] = box["note"]
        placement[ref] = entry
        counts["verified"] += 1
        if shape != "rect":
            shaped += 1

    # A read position someone has looked at and agreed with. The geometry is
    # the reader's; what changes is the claim about it.
    confirmed, unconfirmable = [], []
    for ref in confirm:
        entry = placement.get(ref)
        if not entry or not entry.get("board"):
            unconfirmable.append(ref)
            continue
        was = entry.get("placement")
        counts[was] = counts.get(was, 1) - 1
        entry["placement"] = "verified"
        entry["verified"] = True
        entry.pop("placementNote", None)
        counts["verified"] += 1
        confirmed.append(ref)

    # Schematic sheets go through the same readers. A part is normally drawn
    # on exactly one sheet, so each hit becomes one occurrence; a part found
    # on two sheets legitimately gets two.
    sheet_drop = over.get("dropSchematic", {})
    sheet_confirm = over.get("confirmSchematic", {})
    rule = over.get("schematicSheetRule") or {}
    sheet_counts = {}
    wrong_sheet = 0

    def expected_sheet(ref):
        """Which sheet this designator can be on, or None if unconstrained."""
        if ref in (rule.get("exceptions") or {}):
            return rule["exceptions"][ref]
        threshold = rule.get("threshold")
        if threshold is None:
            return None
        digits = re.sub(r"\D", "", ref)
        if not digits:
            return None
        return rule["atOrAbove"] if int(digits) >= threshold else rule["below"]

    legend_skips = []
    legend_only = set()
    manual_sch = 0
    vlm_sch = 0
    confirmed_sch = []

    # A sheet is a sheet if anything at all knows about it: the crop or the
    # tesseract pass (spaces.py), the vision model's file, or the overrides
    # themselves. The last matters here more than it did before: the shared
    # interconnect sheets are simplified diagrams nobody runs a reader over,
    # and test points are placed by hand as a matter of course, so a sheet
    # that exists only as hand placements has to be built, not skipped.
    sheets = set(spaces.sheet_spaces(build_dir))
    for name in os.listdir(build_dir) if os.path.isdir(build_dir) else []:
        m = re.match(r"^vlm_(sh\d+)\.json$", name)
        if m:
            sheets.add(m.group(1))
    for key in ("schematic", "confirmSchematic", "dropSchematic"):
        for name in (over.get(key) or {}):
            if spaces.SHEET_RE.match(name):
                sheets.add(name)
    sheets = sorted(sheets, key=lambda s: int(s[2:]))

    sheet_manual = over.get("schematic") or {}

    for sheet in sheets:
        sheet_ocr = load(os.path.join(build_dir, "ocr_%s.json" % sheet))
        sheet_vlm_raw = load(os.path.join(build_dir, "vlm_%s.json" % sheet))
        manual_here = sheet_manual.get(sheet, {})
        if not sheet_ocr and not sheet_vlm_raw and not manual_here:
            continue
        # Two sheets of one figure are not necessarily the same size, so the
        # declaration may be one {w,h} for both sheets or one per sheet id.
        declared = over.get("sheetImageSize", {})
        declared = declared.get(sheet, declared) if declared else {}
        size = image_size(build_dir, sheet, sheet_ocr, sheet_vlm_raw)
        if not size and declared.get("w") and declared.get("h"):
            # Nothing measured the sheet, so the declaration is all there is.
            # Hand placements were typed against the size it states.
            size = (declared["w"], declared["h"])
        if not size:
            sys.exit("cannot tell how large .build/%s/%s is -- extract it, or declare "
                     "sheetImageSize.%s in the overrides" % (asm, spaces.image_for(sheet), sheet))
        sw, sh = size
        if sheet_ocr and (sheet_ocr.get("width") != sw or sheet_ocr.get("height") != sh):
            sys.exit("ocr_%s.json was read against %sx%s but the sheet is %dx%d -- "
                     "re-run tools/ocr_designators.py"
                     % (sheet, sheet_ocr.get("width"), sheet_ocr.get("height"), sw, sh))
        sheet_vlm = load_vlm(build_dir, sheet, sw, sh)
        dropped_here = set(sheet_drop.get(sheet, []))
        hits_here = (sheet_ocr or {}).get("hits", {})
        legend = legend_box(hits_here)
        placed_here = 0
        placed_refs = set()
        for ref, hit in hits_here.items():
            if ref in dropped_here or hit["confidence"] in ("collision",):
                continue
            if ref.startswith("TP"):
                hit, note = on_the_net(hit, legend)
                if note:
                    legend_skips.append("%s/%s" % (sheet, ref))
                    legend_only.add(ref)
            want = expected_sheet(ref)
            if want and want != sheet:
                wrong_sheet += 1
                continue
            occurrence = {
                "sheet": sheet,
                "x": hit["x"], "y": hit["y"],
                "w": round(hit["w"] * DEFAULT_PAD, 5),
                "h": round(hit["h"] * DEFAULT_PAD, 5),
                "placement": hit["confidence"],
            }
            other = sheet_vlm.get(ref)
            if other and disagree(occurrence, other, sw, sh):
                occurrence.update({"x": other["x"], "y": other["y"],
                                   "w": other["w"], "h": other["h"],
                                   "placement": "ambiguous",
                                   "placementNote": "The reader and the vision model "
                                                    "disagreed about where this is"})
            entry = placement.setdefault(ref, {})
            entry.setdefault("sch", []).append(occurrence)
            placed_here += 1
            placed_refs.add(ref)
        for ref, other in sheet_vlm.items():
            if ref in dropped_here or ref in placed_refs:
                continue
            want = expected_sheet(ref)
            if want and want != sheet:
                wrong_sheet += 1
                continue
            occurrence = {
                "sheet": sheet,
                "x": other["x"], "y": other["y"], "w": other["w"], "h": other["h"],
                "placement": "vlm",
            }
            if vlm_note(other):
                occurrence["placementNote"] = vlm_note(other)
            entry = placement.setdefault(ref, {})
            entry.setdefault("sch", []).append(occurrence)
            placed_here += 1
            placed_refs.add(ref)
            vlm_sch += 1
            legend_only.discard(ref)
        # Hand placements win over anything read, exactly as on the board. A
        # test point is written twice on a sheet and the reader cannot always
        # tell which is which -- so the ones that matter are placed by eye.
        if manual_here and declared and (declared.get("w") != sw or declared.get("h") != sh):
            sys.exit("schematic overrides for %s were measured against %sx%s but it is %dx%d"
                     % (sheet, declared.get("w"), declared.get("h"), sw, sh))
        for ref, box in manual_here.items():
            entry = placement.setdefault(ref, {})
            occurrence = {
                "sheet": sheet,
                "x": round(box["x"] / sw, 5), "y": round(box["y"] / sh, 5),
                "w": round(box.get("w", 95) / sw, 5),
                "h": round(box.get("h", 36) / sh, 5),
                "placement": "verified",
            }
            if box.get("note"):
                occurrence["placementNote"] = box["note"]
            others = [s for s in entry.get("sch", []) if s.get("sheet") != sheet]
            entry["sch"] = others + [occurrence]
            entry["schVerified"] = True
            manual_sch += 1
            if ref in legend_only:
                legend_only.discard(ref)
                placed_here += 1
        for ref in sheet_confirm.get(sheet, []):
            if ref in manual_here or ref in dropped_here:
                sys.exit("confirmSchematic.%s names %s, which the same file also drops "
                         "or places by hand -- pick one" % (sheet, ref))
            found = [o for o in (placement.get(ref) or {}).get("sch", [])
                     if o.get("sheet") == sheet]
            if not found:
                unconfirmable.append("%s/%s" % (sheet, ref))
                continue
            for o in found:
                o["placement"] = "verified"
                o.pop("placementNote", None)
            placement[ref]["schVerified"] = True
            confirmed_sch.append("%s/%s" % (sheet, ref))

        # What actually landed on the sheet, whichever source put it there.
        sheet_counts[sheet] = sum(1 for e in placement.values()
                                  for o in e.get("sch", []) if o.get("sheet") == sheet)

    coords = {
        "assembly": asm.upper(),
        "generatedBy": "tools/build_coords.py",
        "notOnDrawing": sorted(not_on_drawing, key=sort_key),
        "placement": placement,
        "layers": {},
        "sheets": over.get("sheets", {}),
    }

    # Layer alignment: solve a homography from whatever landmark pairs the
    # overrides give, so the file records the correspondences a person can
    # check rather than nine opaque matrix entries. No board has a photograph
    # yet, so this is normally empty; it is kept so one can be added later.
    for layer_id, spec in (over.get("layers") or {}).items():
        pairs = spec.get("landmarks") or []
        entry = {"landmarks": pairs}
        if spec.get("approximate"):
            entry["approximate"] = True
        matrix = solve_homography(pairs)
        if matrix:
            entry["transform"] = {"H": matrix}
        else:
            print("  WARNING: %s needs at least 4 usable landmarks to align" % layer_id)
        coords["layers"][layer_id] = entry

    existing = load(os.path.join(ROOT, "data", "%s.coords.json" % asm), {}) or {}
    if existing.get("layers") and not coords["layers"]:
        coords["layers"] = existing["layers"]
    if not coords["sheets"] and existing.get("sheets"):
        coords["sheets"] = existing["sheets"]

    path = os.path.join(ROOT, "data", "%s.coords.json" % asm)
    json.dump(coords, open(path, "w"), indent=1)

    print("wrote data/%s.coords.json" % asm)
    print("  board: placed %d, plus %d parts with no silkscreen on the drawing"
          % (sum(1 for e in placement.values() if e.get("board")), len(not_on_drawing)))
    for tier in TIERS:
        if counts.get(tier):
            print("    %-10s %3d" % (tier, counts[tier]))
    if shaped:
        print("    %-10s %3d  (drawn round rather than as a box)"
              % ("circle", shaped))
    if disagreed:
        print("  %d designator%s where the reader and the vision model disagree "
              "(taken from the model, tier ambiguous):\n    %s"
              % (len(disagreed), "" if len(disagreed) == 1 else "s",
                 " ".join(sorted(disagreed, key=sort_key))))
    if confirmed:
        print("  %d read position%s confirmed by hand" % (len(confirmed),
              "" if len(confirmed) == 1 else "s"))
    for sheet, n in sorted(sheet_counts.items()):
        print("  %s: placed %d" % (sheet, n))
    if wrong_sheet:
        print("  dropped %d reads that put a part on the wrong sheet" % wrong_sheet)
    if manual_sch:
        print("  %d schematic positions placed by hand" % manual_sch)
    if vlm_sch:
        print("  %d schematic positions from the vision model" % vlm_sch)
    if confirmed_sch:
        print("  %d schematic positions confirmed by hand" % len(confirmed_sch))
    if unconfirmable:
        print("  WARNING: confirm names %s, which nothing placed -- nothing to confirm"
              % " ".join(unconfirmable))
    legend_skips = [s for s in legend_skips if s.split("/")[1] in legend_only]
    if legend_skips:
        # Not a failure, but not the answer either: these point at the table
        # that names the signal rather than the net you would probe.
        print("  %d test points found only in the legend table, not on a net:"
              % len(legend_skips))
        print("    " + " ".join(sorted(legend_skips)))


def legend_box(hits):
    """
    Where the sheet's test point legend sits, found from the reads themselves.

    A test point can be written twice on a schematic: once in a table that
    says what its signal is called, and once beside the symbol on the net. The
    table gives itself away -- a stack of TP labels sharing an x to within a
    hair, marching evenly down the page -- so it can be located without a
    hand-measured rectangle per sheet.

    Returns (x0, y0, x1, y1) in normalised sheet space, or None.
    """
    points = []
    for ref, hit in hits.items():
        if not ref.startswith("TP"):
            continue
        points.append((hit["x"], hit["y"]))
        for alt in hit.get("alternates", []):
            points.append((alt["x"], alt["y"]))
    if not points:
        return None

    columns = {}
    for x, y in points:
        columns.setdefault(round(x, 2), []).append((x, y))
    column = max(columns.values(), key=len)
    if len(column) < 5:            # a handful in a line is not a table
        return None

    xs = [p[0] for p in column]
    ys = [p[1] for p in column]
    pad = 0.02
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def on_the_net(hit, legend):
    """
    Prefer the reading beside the symbol over the one in the legend table.

    Someone looking up a test point on the schematic wants the net they are
    about to put a probe on, not the row of the table that spells out its
    name -- the table tells you nothing about where the circuit is.
    """
    if not legend:
        return hit, False

    def inside(p):
        return legend[0] <= p["x"] <= legend[2] and legend[1] <= p["y"] <= legend[3]

    if not inside(hit):
        return hit, False

    # Best-voted candidate that is not in the table.
    outside = [a for a in hit.get("alternates", []) if not inside(a)]
    if not outside:
        return hit, True           # only ever seen in the table
    pick = max(outside, key=lambda a: (a.get("votes", 0), a.get("conf", 0)))
    out = dict(hit)
    out.update({"x": pick["x"], "y": pick["y"],
                "w": pick.get("w", hit["w"]), "h": pick.get("h", hit["h"]),
                "conf": pick.get("conf", hit.get("conf")),
                "votes": pick.get("votes", 1)})
    # It was read somewhere else as well, so it is worth a second look however
    # many passes agreed on the table row.
    out["confidence"] = "agreed" if pick.get("votes", 0) >= 3 else "single"
    return out, False


def sort_key(ref):
    return (re.sub(r"\d", "", ref), int(re.sub(r"\D", "", ref) or 0))


def solve_homography(pairs):
    """
    Least-squares 3x3 homography mapping src to dst. Mirrors Geom.solveHomography
    in js/geom.js so the build and Author Mode agree on what a set of landmarks
    means. Needs four pairs; more are averaged.
    """
    if len(pairs) < 4:
        return None
    ata = [[0.0] * 9 for _ in range(8)]
    for pair in pairs:
        x, y = pair["src"]
        u, v = pair["dst"]
        for row in ([x, y, 1, 0, 0, 0, -u * x, -u * y, u],
                    [0, 0, 0, x, y, 1, -v * x, -v * y, v]):
            for r in range(8):
                for c in range(9):
                    ata[r][c] += row[r] * row[c]

    # Gaussian elimination with partial pivoting.
    n = 8
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(ata[r][col]))
        if abs(ata[pivot][col]) < 1e-12:
            return None
        ata[col], ata[pivot] = ata[pivot], ata[col]
        for r in range(n):
            if r == col:
                continue
            factor = ata[r][col] / ata[col][col]
            for c in range(col, n + 1):
                ata[r][c] -= factor * ata[col][c]
    h = [ata[i][n] / ata[i][i] for i in range(n)]
    return [round(v, 9) for v in h] + [1.0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: tools/build_coords.py <assembly-id>   (a3, a4, a5, sys)")
    build(sys.argv[1].lower())
