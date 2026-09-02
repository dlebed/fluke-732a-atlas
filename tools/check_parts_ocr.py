#!/usr/bin/env /usr/bin/python3
"""
check_parts_ocr.py — machine cross-check of a transcribed parts table against
the 600-dpi tesseract read of the same pages.

    tools/check_parts_ocr.py a3

Two readers are better than one only if they are compared. The vision readers
produced data/<asm>.parts.raw.json; tesseract produced .build/ocr/p600-NN.txt.
This parses tesseract's lines into (ref, stock, code, part) where it can and
reports every row where the two disagree on the six-digit stock number, the
five-digit manufacturer code or the manufacturer part number, and every
tesseract row whose designator the JSON does not have. Disagreements are
things to look at on the page, not automatic errors -- tesseract misreads
too -- but a transposed digit that both readers agree on is rare, and one
they disagree on is caught here.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROW = re.compile(r"^\W*([A-Z]{1,2}\d+(?:\s*[-,]\s*[A-Z]{0,2}\d+)?\*?)\s+(.*?)\s+(\d{6})\s+(\d{5})\s+(\S+)(?:\s+(REF|\d+))?", re.I)

def norm(s):
    return re.sub(r"\s+", "", (s or "")).upper().replace("*", "")

def main(asm):
    raw = json.load(open(os.path.join(ROOT, "data", "%s.parts.raw.json" % asm)))
    by_ref = {norm(r["ref"]): r for r in raw["rows"]}
    seen, problems = set(), []
    for page in raw["pages"]:
        path = os.path.join(ROOT, ".build", "ocr", "p600-%02d.txt" % page)
        if not os.path.exists(path):
            print("no tesseract text for page", page); continue
        for line in open(path, encoding="utf-8"):
            m = ROW.match(line.strip())
            if not m:
                continue
            ref, desc, stock, code, part = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            key = norm(ref)
            # tesseract's usual slips on this typewriter face, in the designator only
            key = key.replace("CH", "C4").replace("CRY", "CR4").replace("CG", "C9").replace("CQ", "C9")
            row = by_ref.get(key)
            if not row:
                # try the printed-range keys: tesseract sometimes reads "CR5-CR9" fine, sometimes "CR5~CR9"
                cands = [k for k in by_ref if k.split("-")[0] == key.split("-")[0] and "-" in k]
                row = by_ref.get(cands[0]) if len(cands) == 1 else None
            if not row:
                problems.append("p%d tesseract row %r (%s %s %s) has no JSON row" % (page, ref, stock, code, part))
                continue
            seen.add(norm(row["ref"]))
            if row["fluke"] != stock:
                problems.append("p%d %s stock: JSON %s vs tesseract %s" % (page, row["ref"], row["fluke"], stock))
            if row["mfrCode"] != code:
                problems.append("p%d %s mfr code: JSON %s vs tesseract %s" % (page, row["ref"], row["mfrCode"], code))
            if norm(row["mfrPart"]) != norm(part) and norm(part) not in ("", "REF"):
                problems.append("p%d %s mfr part: JSON %r vs tesseract %r" % (page, row["ref"], row["mfrPart"], part))
    unseen = [r["ref"] for r in raw["rows"] if norm(r["ref"]) not in seen and r["fluke"]]
    print("%s: %d JSON rows, %d matched to a tesseract row, %d disagreements" % (asm, len(raw["rows"]), len(seen), len(problems)))
    for p in problems:
        print("  ", p)
    if unseen:
        print("  JSON rows tesseract did not parse (check by eye):", ", ".join(unseen))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "a3")
