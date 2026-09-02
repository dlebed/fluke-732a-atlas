#!/usr/bin/env /usr/bin/python3
"""
apply_review.py — fold marker-review verdicts into the overrides.

    tools/apply_review.py a3 board verdicts.json
    tools/apply_review.py a3 sh1   verdicts.json

verdicts.json is a list of {ok: [refs], wrong: [{ref, why}], unsure: [{ref, why}]}
(one entry per review sheet, as the review agents return them). Every ref under
ok is added to the overrides' `confirm` (board) or `confirmSchematic[sheet]`,
which build_coords.py turns into placement 'verified' without changing the box.
Every ref under wrong or unsure is removed from confirm if it was there, listed
on stdout, and written to .build/<asm>/vlm/replace_<space>.json so a targeted
`vlm_place.py plan --only` round can re-place it. Nothing is dropped here: a
wrong marker keeps its (wrong) position until the re-placement lands, and the
build marks it unconfirmed, which the app shows.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path, default):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else default


def main(asm, space, verdicts_path):
    over_path = os.path.join(ROOT, "data", "%s.coords.overrides.json" % asm)
    over = load(over_path, {})
    verdicts = json.load(open(verdicts_path, encoding="utf-8"))
    ok, bad = set(), {}
    for v in verdicts:
        ok.update(v.get("ok") or [])
        for w in (v.get("wrong") or []):
            bad[w["ref"]] = "wrong: " + w.get("why", "")
        for u in (v.get("unsure") or []):
            bad.setdefault(u["ref"], "unsure: " + u.get("why", ""))
    ok -= set(bad)                                   # a ref judged wrong on one sheet is not confirmed
    if space == "board":
        cur = set(over.get("confirm") or [])
        over["confirm"] = sorted((cur | ok) - set(bad))
        hand = set((over.get("board") or {}).keys())
    else:
        cs = over.setdefault("confirmSchematic", {})
        cur = set(cs.get(space) or [])
        cs[space] = sorted((cur | ok) - set(bad))
        hand = set(((over.get("schematic") or {}).get(space) or {}).keys())
    # a hand-placed entry may not also be confirmed: build_coords refuses it
    if space == "board":
        over["confirm"] = [r for r in over["confirm"] if r not in hand]
    else:
        over["confirmSchematic"][space] = [r for r in over["confirmSchematic"][space] if r not in hand]
    over.setdefault("_comment", [
        "Hand corrections over the readers. 'confirm' / 'confirmSchematic' list read",
        "positions that a reviewer looked at and found on the right lettering",
        "(tools/apply_review.py); 'board' / 'schematic' carry hand-placed boxes in pixels",
        "of .build/<asm>/drawing_full.png and schN_full.png; 'drop' names reads that",
        "point at another part's label."])
    with open(over_path, "w", encoding="utf-8") as f:
        json.dump(over, f, indent=1, ensure_ascii=False)
        f.write("\n")
    rep_path = os.path.join(ROOT, ".build", asm, "vlm", "replace_%s.json" % space)
    os.makedirs(os.path.dirname(rep_path), exist_ok=True)
    json.dump({"refs": sorted(bad), "why": bad}, open(rep_path, "w"), indent=1)
    print("%s %s: confirmed %d, to re-place %d -> %s" % (asm, space, len(ok), len(bad), os.path.relpath(rep_path, ROOT)))
    for r in sorted(bad):
        print("   ", r, "--", bad[r][:140])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__.strip())
    main(*sys.argv[1:])
