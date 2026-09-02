#!/usr/bin/env /usr/bin/python3
"""
expand_parts.py — turn a transcribed parts table into the curated parts file.

    tools/expand_parts.py a3            # data/a3.parts.raw.json -> data/a3.parts.json

The raw file is a row-for-row transcription of the printed table (two readers,
see manual-text/README.md), with the REF DES column kept exactly as printed:
"CR5-CR9", "Q1, Q2", "TP1-TP6". This expands those into one entry per
designator, assigns a kind from the designator family and the description,
and drops the assembly's own header row. Quantities stay as printed: the
table's TOT QTY counts every part of that stock number on the board, not the
designators in the row, so a range row's quantity is the group's, and REF
means "counted on an earlier row".

Anything it cannot parse is printed and left out, never guessed.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KIND_BY_PREFIX = {
    "C": "cap", "R": "res", "CR": "diode", "Q": "transistor", "U": "ic",
    "DS": "led", "F": "fuse", "FL": "part", "XF": "mech", "T": "transformer",
    "S": "switch", "W": "wire", "RT": "thermistor", "TP": "testpoint",
    "MP": "mech", "H": "mech", "J": "connector", "P": "connector",
    "E": "terminal", "BT": "battery", "HR": "heater", "RV": "varistor",
    "VR": "zener", "L": "inductor", "K": "relay", "Z": "resnet",
}
REF_RE = re.compile(r"^([A-Z]{1,2})(\d+)$")


def kind_for(ref, desc):
    m = REF_RE.match(ref)
    prefix = m.group(1) if m else ""
    kind = KIND_BY_PREFIX.get(prefix, "part")
    d = (desc or "").upper()
    if prefix == "CR":
        if "ZEN" in d:
            kind = "zener"
        elif "LIGHT EMITTING" in d or "LED" in d.split(","):
            kind = "led"
        elif "BRIDGE" in d:
            kind = "diode"
    return kind


def expand_ref(text):
    """'CR5-CR9' -> [CR5..CR9]; 'Q1, Q2' -> [Q1, Q2]; 'R44' -> [R44]. None if unparseable."""
    t = text.replace("*", "").replace(" ", "")
    if not t:
        return None
    out = []
    for piece in t.split(","):
        if "-" in piece:
            a, b = piece.split("-", 1)
            ma, mb = REF_RE.match(a), REF_RE.match(b)
            if not ma or not mb or ma.group(1) != mb.group(1):
                return None
            lo, hi = int(ma.group(2)), int(mb.group(2))
            if hi < lo or hi - lo > 60:
                return None
            out += ["%s%d" % (ma.group(1), n) for n in range(lo, hi + 1)]
        else:
            if not REF_RE.match(piece):
                return None
            out.append(piece)
    return out


def main(asm):
    src = os.path.join(ROOT, "data", "%s.parts.raw.json" % asm)
    dst = os.path.join(ROOT, "data", "%s.parts.json" % asm)
    raw = json.load(open(src, encoding="utf-8"))
    asm_id = raw.get("assembly", asm.upper())
    components, problems, seen = [], [], {}
    for row in raw["rows"]:
        printed = (row.get("ref") or "").strip()
        if printed.upper() == asm_id.upper() or printed == "":
            continue                                   # the assembly's own header row
        refs = expand_ref(printed)
        if refs is None:
            problems.append("cannot parse REF DES %r (%s)" % (printed, row.get("desc")))
            continue
        for ref in refs:
            if ref in seen:
                problems.append("%s appears twice: %r and %r" % (ref, seen[ref], printed))
                continue
            seen[ref] = printed
            qty = (row.get("totQty") or "").strip()
            entry = {
                "ref": ref,
                "kind": kind_for(ref, row.get("desc")),
                "desc": (row.get("desc") or "").strip(),
                "fluke": (row.get("fluke") or "").strip(),
                "mfrCode": (row.get("mfrCode") or "").strip(),
                "mfrPart": (row.get("mfrPart") or "").strip(),
                "qty": None if qty.upper() == "REF" else qty,
                "qtyRef": qty.upper() == "REF",
                "recQty": (row.get("recQty") or "").strip() or None,
                "notes": (row.get("note") or "").strip() or None,
                "esd": False,
                "star": bool(row.get("star")),
                "page": row.get("page"),
                "src": "Table %s" % raw.get("table", "?"),
            }
            if len(refs) > 1:
                entry["group"] = printed.replace("*", "").strip()
            components.append(entry)

    extras_path = os.path.join(ROOT, "data", "%s.parts.extras.json" % asm)
    if os.path.exists(extras_path):
        extras = json.load(open(extras_path, encoding="utf-8"))
        for e in extras.get("components", []):
            if e["ref"] in seen:
                problems.append("extra %s is already in the parts table" % e["ref"])
                continue
            seen[e["ref"]] = "extras"
            # An extra is normally an item lettered on a drawing with no parts-table
            # line (notInParts). A part the change/errata sheet ADDS to the table
            # carries its own stock number and says notInParts: false, notOnDrawing:
            # true -- it is in the (amended) parts list but not on the 1983 drawing.
            entry = {"ref": e["ref"], "kind": e.get("kind") or kind_for(e["ref"], e.get("desc")),
                     "desc": e.get("desc", ""), "fluke": e.get("fluke", ""),
                     "mfrCode": e.get("mfrCode", ""), "mfrPart": e.get("mfrPart", ""),
                     "qty": e.get("qty"), "qtyRef": False, "recQty": e.get("recQty"),
                     "notes": e.get("notes"), "esd": False, "star": False,
                     "page": e.get("page"), "src": e.get("src", "drawing"),
                     "notInParts": e.get("notInParts", True)}
            if e.get("notOnDrawing"):
                entry["notOnDrawing"] = True
            if e.get("aliases"):
                entry["aliases"] = e["aliases"]
            components.append(entry)
        # Amendments: the change/errata sheet renames a designator (aliases) or
        # changes a stock number (a note) on a row the 1983 table already has.
        # The transcription stays verbatim; the amendment is merged here.
        by_ref = {c["ref"]: c for c in components}
        for a in extras.get("amend", []):
            c = by_ref.get(a["ref"])
            if not c:
                problems.append("amendment for %s, which is not in the parts table" % a["ref"])
                continue
            if a.get("aliases"):
                c["aliases"] = sorted(set((c.get("aliases") or []) + a["aliases"]))
            if a.get("notes"):
                c["notes"] = (c["notes"] + "; " if c.get("notes") else "") + a["notes"]
            for key in ("asBuilt", "laterFluke"):
                if a.get(key):
                    c[key] = a[key]

    out = {
        "_comment": [
            "Generated by tools/expand_parts.py from data/%s.parts.raw.json -- edit the raw" % asm,
            "file (the transcription), data/%s.parts.extras.json (items lettered on the" % asm,
            "drawings but absent from the table) or this script, not this file.",
            "One entry per designator; 'group' records the printed row a range came from.",
            "'qty' is the printed TOT QTY of that stock number on the board; null with",
            "qtyRef=true where the table prints REF (counted on an earlier row).",
        ],
        "assembly": asm_id,
        "table": raw.get("table"),
        "name": raw.get("name"),
        "pages": raw.get("pages"),
        "footnotes": raw.get("footnotes", []),
        "components": components,
    }
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    kinds = {}
    for c in components:
        kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
    print("%s: %d rows -> %d designators; kinds: %s" % (
        asm, len(raw["rows"]), len(components),
        ", ".join("%s %d" % kv for kv in sorted(kinds.items()))))
    for p in problems:
        print("  PROBLEM:", p)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "a3")
