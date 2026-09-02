#!/usr/bin/env python3
"""
assemble.py — merge the curated and geometric data into data/<asm>.js.

The 732A Instruction Manual (P/N 645051, May 1983) is a 600 dpi scan with no
text layer, so nothing here is parsed from a PDF: every input is a curated
JSON file, transcribed and checked by a second reader. Each file is owned by a
different process so that re-running any one of them never destroys the
others:

  data/<asm>.board.json        identity, the drawing layer, the schematic sheets
  data/<asm>.parts.json        the parts table (Table 5-4 / 5-5 / 5-6), ranges expanded
  data/<asm>.procedures.json   §4-44, Table 4-3 and the like, as numbered steps
  data/<asm>.testpoints.json   expected values and their citations
  data/<asm>.reference.json    overview, rail circuits, part functions, symptoms
                               (Table 4-2), warnings, caveats, tables
  data/<asm>.caps.json         which rail each capacitor sits on
  data/<asm>.coords.json       board and schematic positions (build_coords.py,
                               Author Mode)

Output is a plain <script src> file rather than JSON so the page works from
file:// with no server. It calls BoardExplorer.register({...}) with the object
data/schema.md describes.

Usage: tools/assemble.py <asm>        asm = a3 | a4 | a5 | sys | zz ...
       tools/assemble.py all          every data/*.board.json
"""

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MANUAL = "732A Instruction Manual, P/N 645051, May 1983"


def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strip_comments(obj):
    """Drop the _comment keys used to document the curated files."""
    if isinstance(obj, dict):
        return {k: strip_comments(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [strip_comments(v) for v in obj]
    return obj


def sort_ref(ref):
    """'TP9' before 'TP10' -- designators sort by prefix then numerically."""
    m = re.match(r"^([A-Z]+)(\d+)([A-Z]*)$", ref)
    return (m.group(1), int(m.group(2)), m.group(3)) if m else (ref, 0, "")


def zone_for(sheet, x, y):
    """
    Map a normalised sheet position to its printed grid zone, e.g. 'C4'.

    A sheet may carry no grid at all -- the 732A's interconnect diagrams have
    no zone letters -- and then there is simply no zone to derive.
    """
    grid = sheet.get("grid") or {}
    frame, cols, rows = grid.get("frame"), grid.get("cols"), grid.get("rows")
    if not frame or not cols or not rows:
        return None
    fx = (x - frame["x0"]) / (frame["x1"] - frame["x0"])
    fy = (y - frame["y0"]) / (frame["y1"] - frame["y0"])
    if not (0 <= fx <= 1 and 0 <= fy <= 1):
        return None
    col = cols[min(len(cols) - 1, max(0, int(fx * len(cols))))]
    row = rows[min(len(rows) - 1, max(0, int(fy * len(rows))))]
    return "%s%s" % (row, col)


def merge_rails(rails, circuits):
    """Attach each rail's circuit description to its display record."""
    out = {}
    for key, rail in rails.items():
        rec = dict(rail)
        if key in circuits:
            rec["circuit"] = circuits[key]
        out[key] = rec
    return out


def curated_path(asm, kind):
    return os.path.join(ROOT, "data", "%s.%s.json" % (asm, kind))


def build(asm):
    board = strip_comments(load(curated_path(asm, "board")))
    if not board:
        sys.exit("no data/%s.board.json -- the dataset's identity, drawing layer and "
                 "sheets are declared there (see data/schema.md)" % asm)
    for key in ("id", "name", "layers", "schematics"):
        if key not in board:
            sys.exit("data/%s.board.json has no '%s'" % (asm, key))

    # The parts and test point files are required even when they are short:
    # a board silently assembled with no parts is the kind of failure that
    # looks like a working page with nothing on it.
    parts = strip_comments(load(curated_path(asm, "parts")))
    if parts is None:
        sys.exit("no data/%s.parts.json -- transcribe the parts table first" % asm)
    curated = strip_comments(load(curated_path(asm, "testpoints")))
    if curated is None:
        sys.exit("no data/%s.testpoints.json -- write the expectations first" % asm)

    reference = strip_comments(load(curated_path(asm, "reference"), {}))
    procedures_in = strip_comments(load(curated_path(asm, "procedures")))
    if procedures_in is None:
        # A5 has none: the reference is not field-repairable. Say so rather
        # than emitting an empty shell that looks like missing data.
        print("  note: no data/%s.procedures.json -- the dataset carries no procedure" % asm)
        procedures_in = {"procedures": []}
    # Which rail each capacitor sits on. Optional: a board with no audit yet
    # simply has no margins to show, which is different from having good ones.
    cap_audit = strip_comments(load(curated_path(asm, "caps"), {}))
    coords = load(os.path.join(ROOT, "data", "%s.coords.json" % asm), {}) or {}

    # ---- sheets and layers ------------------------------------------------
    # Identity and geometry of the sheets come from board.json; a zone grid
    # measured in Author Mode (coords.sheets.<id>.grid) wins over one typed in.
    sheets = [dict(s) for s in board["schematics"]]
    for s in sheets:
        measured = (coords.get("sheets") or {}).get(s["id"], {}).get("grid")
        if measured:
            s["grid"] = measured

    layers = [dict(l) for l in board["layers"]]
    for l in layers:
        stored = (coords.get("layers") or {}).get(l["id"], {})
        l["transform"] = stored.get("transform") or l.get("transform") \
            or ("identity" if l["id"] == "drawing" else None)
        if stored.get("landmarks"):
            l["landmarks"] = stored["landmarks"]
        # An alignment solved from four corner pairs is a starting alignment
        # and the dataset should say so rather than presenting it as measured.
        if stored.get("approximate"):
            l["approximate"] = True

    # ---- geometry -----------------------------------------------------------
    placement = coords.get("placement", {})
    not_on_drawing = set(coords.get("notOnDrawing", []))

    def geometry_for(ref):
        p = placement.get(ref, {})
        out = {}
        if p.get("board"):
            out["board"] = p["board"]
        if p.get("sch"):
            sch = []
            for entry in p["sch"]:
                e = dict(entry)
                sheet = next((s for s in sheets if s["id"] == e.get("sheet")), None)
                if sheet:
                    zone = zone_for(sheet, e.get("x", -1), e.get("y", -1))
                    if zone:
                        e["zone"] = zone
                sch.append(e)
            out["sch"] = sch
        for flag in ("verified", "schVerified"):
            if p.get(flag):
                out[flag] = True
        # How the position was arrived at, so the app can say so rather than
        # presenting a machine-read marker as though someone had checked it.
        for key in ("placement", "placementNote"):
            if p.get(key):
                out[key] = p[key]
        if ref in not_on_drawing:
            out["notOnDrawing"] = True
        return out

    # ---- components and test points -------------------------------------
    tp_by_ref = {t["ref"]: t for t in curated.get("testpoints", [])}
    functions = reference.get("functions") or {}

    components, testpoints = [], []
    seen = set()
    for part in parts.get("components", []):
        ref = part["ref"]
        if ref in seen:
            sys.exit("data/%s.parts.json lists %s twice -- expand ranges once" % (asm, ref))
        seen.add(ref)
        rec = {k: v for k, v in part.items() if v not in (None, False, "")}
        # A function note beats the parts-list description for telling someone
        # what a part is for, so it is carried alongside rather than merged in.
        if ref in functions:
            rec["function"] = functions[ref]
        rec.update(geometry_for(ref))
        if ref in tp_by_ref:
            # A test point is a parts-list line and an expectation record at
            # once. The expectation file owns everything but the BOM columns.
            merged = dict(tp_by_ref[ref])
            for col in ("desc", "fluke", "mfrCode", "mfrPart", "qty", "star", "page"):
                if part.get(col) not in (None, False, ""):
                    merged[col] = part[col]
            if ref in functions and "function" not in merged:
                merged["function"] = functions[ref]
            merged.update(geometry_for(ref))
            testpoints.append(merged)
        else:
            components.append(rec)

    # A test point does not have to be a purchasable part: the front-panel
    # binding posts on SYS and a plated pad on a board are real probe targets
    # with real expectations. What they lack is a BOM line, not a reason to
    # exist.
    for ref in sorted(tp_by_ref, key=sort_ref):
        if ref in seen:
            continue
        merged = dict(tp_by_ref[ref])
        merged["kind"] = merged.get("kind") or "testpoint"
        merged["notInParts"] = True
        if ref in functions and "function" not in merged:
            merged["function"] = functions[ref]
        merged.update(geometry_for(ref))
        testpoints.append(merged)
    testpoints.sort(key=lambda t: sort_ref(t["ref"]))

    # ---- procedures -----------------------------------------------------------
    # A step can name a test point that belongs to a DIFFERENT assembly: the
    # SYS Table 4-3 procedure measures A3 TP6 against TP4, and A3's own
    # procedure says to watch the front panel. Left alone, the app offers those
    # as clickable points on this board. The reference file names them per
    # step so the chip is not offered; the sentence still says what to do.
    #
    # foreignStepRefs is keyed by step number ("12": [...]) for every procedure
    # on the board, or by procedure id and then step ("4-44": {"12": [...]})
    # when the board has more than one and they number alike.
    foreign_spec = reference.get("foreignStepRefs") or {}

    def foreign_for(proc_id, n):
        out = set()
        flat = foreign_spec.get(str(n))
        if isinstance(flat, list):
            out.update(flat)
        nested = foreign_spec.get(str(proc_id))
        if isinstance(nested, dict):
            out.update(nested.get(str(n), []))
        return out

    procedures = []
    for proc in procedures_in.get("procedures", []):
        rec = dict(proc)
        steps = []
        for s in proc.get("steps", []):
            step = dict(s)
            foreign = foreign_for(proc.get("id"), s.get("n"))
            step["refs"] = [r for r in (s.get("refs") or []) if r not in foreign]
            steps.append(step)
        rec["steps"] = steps
        rec.setdefault("prereq", "")
        procedures.append(rec)

    dataset = {
        "id": board["id"],
        "name": board["name"],
        "pca": board.get("pca"),
        "pcb": board.get("pcb"),
        "drawingNo": board.get("drawingNo"),
        "virtual": bool(board.get("virtual")),
        "rev": board.get("rev"),
        "refs": board.get("refs") or {},
        "warnings": reference.get("warnings", []),
        "layers": layers,
        "schematics": sheets,
        "overview": reference.get("overview"),
        "rails": merge_rails(curated.get("rails", {}), reference.get("railCircuits", {})),
        # The Symptoms tab. The key is still faultCodes because the engine
        # renders the same array; the entries are Table 4-2 rows.
        "faultCodes": reference.get("faultCodes", []),
        "caveats": reference.get("caveats", []),
        # Reference tables shown verbatim. The renderer is generic over the
        # row keys, so a new table needs no engine change.
        "tables": [t for t in (reference.get("tables") or []) if t],
        "components": components,
        "testpoints": testpoints,
        "probePoints": curated.get("probePoints", []),
        "capAudit": cap_audit.get("caps", {}),
        "procedures": procedures,
    }

    out_path = os.path.join(ROOT, "data", "%s.js" % asm)
    body = json.dumps(dataset, indent=1, ensure_ascii=False)
    refs = dataset["refs"]
    cited = [refs.get(k) for k in ("parts", "locator", "schematic", "troubleshooting")
             if refs.get(k)]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("// Generated by tools/assemble.py -- do not hand-edit.\n")
        f.write("// Sources: %s (600 dpi scan, no text layer)" % MANUAL)
        f.write((":\n//          %s.\n" % ", ".join(cited)) if cited else ".\n")
        f.write("//          Transcribed and checked by a second reader; see manual-text/.\n")
        f.write("//          data/%s.{board,parts,procedures,testpoints,reference,caps}.json "
                "(curated),\n//          data/%s.coords.json (geometry).\n" % (asm, asm))
        f.write("// Author Mode exports a replacement for data/%s.coords.json.\n\n" % asm)
        f.write("BoardExplorer.register(%s);\n" % body)

    items = components + testpoints
    placed = sum(1 for c in items if c.get("board"))
    verified = sum(1 for c in items if c.get("verified"))
    sch_placed = sum(1 for c in items if c.get("sch"))
    off_drawing = sum(1 for c in items if c.get("notOnDrawing"))
    tiers = {}
    for c in items:
        if c.get("board"):
            tiers[c.get("placement") or "?"] = tiers.get(c.get("placement") or "?", 0) + 1
    links = sum(1 for c in items + dataset["probePoints"] if c.get("link"))
    print("wrote data/%s.js" % asm)
    print("  components      %d" % len(components))
    print("  test points     %d" % len(testpoints))
    print("  probe points    %d" % len(dataset["probePoints"]))
    print("  procedures      %d (%d steps)"
          % (len(procedures), sum(len(p["steps"]) for p in procedures)))
    print("  symptoms        %d" % len(dataset["faultCodes"]))
    print("  board placed    %d / %d  (%d verified, %d with no silkscreen)"
          % (placed, len(items), verified, off_drawing))
    for tier in ("verified", "agreed", "ambiguous", "single", "collision", "vlm"):
        if tiers.get(tier):
            print("    %-10s %3d" % (tier, tiers[tier]))
    print("  schematic placed %d / %d" % (sch_placed, len(items)))
    if links:
        print("  links           %d" % links)
    off_bom = [t["ref"] for t in testpoints if t.get("notInParts")]
    if off_bom:
        print("  test points with no parts-list line: %s" % ", ".join(off_bom))


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip())
    asm = argv[1].lower()
    if asm == "all":
        boards = sorted(glob.glob(os.path.join(ROOT, "data", "*.board.json")))
        if not boards:
            sys.exit("no data/*.board.json to build")
        for path in boards:
            build(os.path.basename(path).split(".")[0])
    else:
        build(asm)


if __name__ == "__main__":
    main(sys.argv)
