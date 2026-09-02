#!/usr/bin/env /usr/bin/python3
"""
share_interconnect.py — give each board the positions read once on the shared
interconnect figures.

    tools/share_interconnect.py            # all of a3, a4, a5
    tools/share_interconnect.py a3

Figure 8-1 (the interconnect) is SYS's drawing and every board's sheet sh2;
Figure 8-2 (motherboard / battery / LED) is SYS's sh1 and A3/A4's sh3. The
same image is behind both, so a position is the same pixel on both. SYS names
its items with an assembly prefix (A3TP1, A4Q13); this strips the prefix, keeps
what the board actually has, and writes the boxes into the board's
coords.overrides.json under schematic.sh2 / sh3 in pixels of the shared crop
(9517x5608 and 9436x5556), which is what build_coords.py expects there.
Entries the board's overrides already carry by hand are left alone.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path, default=None):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else default


def known_refs(asm):
    refs = set()
    parts = load(os.path.join(ROOT, "data", "%s.parts.json" % asm), {})
    refs.update(c["ref"] for c in parts.get("components", []))
    tps = load(os.path.join(ROOT, "data", "%s.testpoints.json" % asm), {})
    refs.update(t["ref"] for t in tps.get("testpoints", []))
    return refs


def main(boards):
    sys_coords = load(os.path.join(ROOT, "data", "sys.coords.json"))
    if not sys_coords:
        sys.exit("no data/sys.coords.json -- build SYS first")
    sys_board = load(os.path.join(ROOT, "data", "sys.board.json"))
    sizes = {}
    from PIL import Image
    sizes["board"] = Image.open(os.path.join(ROOT, ".build", "sys", "drawing_full.png")).size
    sizes["sh1"] = Image.open(os.path.join(ROOT, ".build", "sys", "sch1_full.png")).size
    placements = sys_coords.get("placement") or sys_coords.get("placements") or {}
    for asm in boards:
        board = load(os.path.join(ROOT, "data", "%s.board.json" % asm))
        sheets = {s["src"]: s["id"] for s in board.get("schematics", [])}
        target = {}                                     # sys space -> board sheet id
        if "assets/sys/drawing.png" in sheets:
            target["board"] = sheets["assets/sys/drawing.png"]
        if "assets/sys/sch1.png" in sheets:
            target["sh1"] = sheets["assets/sys/sch1.png"]
        refs = known_refs(asm)
        prefix = asm.upper()
        over_path = os.path.join(ROOT, "data", "%s.coords.overrides.json" % asm)
        over = load(over_path, {})
        sch = over.setdefault("schematic", {})
        sizes_decl = over.setdefault("sheetImageSize", {})
        added = {}
        for sys_space, sheet_id in target.items():
            W, H = sizes[sys_space]
            sizes_decl[sheet_id] = {"w": W, "h": H}
            dest = sch.setdefault(sheet_id, {})
            for ref, entry in placements.items():
                if not ref.startswith(prefix):
                    continue
                bare = ref[len(prefix):]
                if not re.match(r"^[A-Z]+\d+$", bare) or bare not in refs:
                    continue
                geo = entry.get("board") if sys_space == "board" else next(
                    (s for s in entry.get("sch", []) if s.get("sheet") == "sh1"), None)
                if not geo:
                    continue
                if bare in dest and not dest[bare].get("_fromSys"):
                    continue                            # hand-placed on the board side wins
                dest[bare] = {"x": int(round(geo["x"] * W)), "y": int(round(geo["y"] * H)),
                              "w": int(round(geo["w"] * W)), "h": int(round(geo["h"] * H)),
                              "_fromSys": ref}
                added.setdefault(sheet_id, []).append(bare)
        over.setdefault("_sharedComment", [
            "schematic.sh2 (and sh3 on A3/A4) are the positions read on the shared Figures",
            "8-1 / 8-2 for SYS, copied here by tools/share_interconnect.py with the assembly",
            "prefix stripped ('_fromSys' names the SYS item). Re-running the script",
            "refreshes them; an entry without _fromSys was placed by hand and is kept."])
        with open(over_path, "w", encoding="utf-8") as f:
            json.dump(over, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print("%s: %s" % (asm, ", ".join("%s %d (%s)" % (k, len(v), " ".join(sorted(v))) for k, v in added.items()) or "nothing to share"))


if __name__ == "__main__":
    main([a.lower() for a in sys.argv[1:]] or ["a3", "a4", "a5"])
