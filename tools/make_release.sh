#!/usr/bin/env bash
#
# make_release.sh — build the standalone package a user actually runs.
#
# The repository carries the whole chain: the page, and the pipeline that turns
# the scanned 732A manual into the datasets behind it. Someone servicing a
# reference standard wants only the first half. This copies that half into a
# directory and zips it.
#
# Usage:   tools/make_release.sh [output-name]
#          tools/make_release.sh                  # -> dist/fluke-732a-atlas{,.zip}
#
# The file list is derived, never hardcoded: whatever index.html loads, plus
# whatever image paths the datasets themselves name. Add a dataset, or another
# schematic sheet, and this picks it up with no edit here. If a referenced file
# is missing the script stops rather than shipping a package with a hole in it.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
NAME="${1:-fluke-732a-atlas}"
OUT="$ROOT/dist/$NAME"

cd "$ROOT"
rm -rf "$OUT" "$OUT.zip"
mkdir -p "$OUT"

say() { printf '  %s\n' "$*"; }

# ---- 1. the page, its styles and the engine ---------------------------------
#
# index.html names every script and stylesheet it needs, so read them off it
# rather than keeping a second list here that can drift.
missing=0
while read -r ref; do
  [ -z "$ref" ] && continue
  case "$ref" in http*|//*|data:*|'#'*) continue;; esac
  if [ ! -f "$ref" ]; then echo "MISSING, referenced by index.html: $ref" >&2; missing=1; continue; fi
  mkdir -p "$OUT/$(dirname "$ref")"
  cp "$ref" "$OUT/$ref"
done < <(grep -oE '(src|href)="[^"]+"' index.html | sed 's/.*="//;s/"//' | sort -u)
cp index.html "$OUT/"
say "page, styles and engine"

# ---- 2. the images the datasets ask for -------------------------------------
#
# assemble.py bakes the drawing and schematic paths into data/<asm>.js, so the
# datasets are the authority on which images exist.
n=0
while read -r img; do
  [ -z "$img" ] && continue
  if [ ! -f "$img" ]; then echo "MISSING, referenced by a dataset: $img" >&2; missing=1; continue; fi
  mkdir -p "$OUT/$(dirname "$img")"
  cp "$img" "$OUT/$img"
  n=$((n + 1))
done < <(grep -ohE '"assets/[^"]+"' data/*.js | tr -d '"' | sort -u)
say "$n board images"

# The mark is used by the README, the favicon by the page; neither is named in
# a dataset.
mkdir -p "$OUT/assets/brand"
for f in favicon.svg mark.svg lockup-dark.svg mark-onblack.svg; do
  [ -f "assets/brand/$f" ] && cp "assets/brand/$f" "$OUT/assets/brand/$f"
done

# ---- 3. the documents that have to travel with it ---------------------------
#
# The licence is not optional. CREDITS.md travels when it exists: the drawings,
# schematics, parts tables and procedures are derived from Fluke's manual and
# the credit for that has to be reproduced with any redistribution. There are
# no photographs in this package, so no photograph credit is owed.
[ -f LICENSE ] || { echo "MISSING: LICENSE must ship with the package" >&2; exit 1; }
cp LICENSE "$OUT/"
docs="LICENSE"
if [ -f CREDITS.md ]; then cp CREDITS.md "$OUT/"; docs="$docs, CREDITS.md"; fi

# A README written for the package rather than the repository: the full one
# documents a pipeline that is deliberately not in here. The safety wording is
# the manual's own (§4-51 and the Section 4 warning), and it is carried here
# in the script rather than lifted from README.md so the package can never be
# built without it.
{
  printf '<img src="assets/brand/lockup-dark.svg" alt="Atlas — 732A service" width="240" height="72">\n\n'
  printf '# 732A Atlas\n\n'
  printf 'A bench tool for servicing the Fluke 732A DC Reference Standard: find a part on\n'
  printf 'the board, see what a test point should read and what to reference it against,\n'
  printf "step through the manual's procedures, look a symptom up, and record what you\n"
  printf 'measured so the readings are still there next year.\n\n'
  printf 'Standalone HTML: open `index.html` in a browser and it works. No server, no\n'
  printf 'build step, no install, no network. Everything you record stays in your own\n'
  printf "browser's local storage.\n\n"
  printf 'Author Mode — the greyed **Author** tab, top right — adds editing: move a\n'
  printf 'marker onto the part it actually labels, or place one the readers missed.\n'
  printf 'Those edits apply in normal use too, and *Export coordinates* hands them back\n'
  printf 'for folding into the source data.\n\n'
  printf -- '---\n\n'
  printf '## Safety and disclaimer\n\n'
  printf '**Read this before opening the instrument.**\n\n'
  printf '### Mains and battery\n\n'
  printf 'The 732A runs from the ac line and from an internal battery pack, and both are\n'
  printf 'hazardous in their own way.\n\n'
  printf 'The Pre-Regulator assembly (A3) carries the ac line: the power connector, the\n'
  printf 'fuseholder, the power transformer and the rectified raw supply at up to 60 V dc\n'
  printf 'are all live whenever the instrument is plugged in. The manual (§4-51) says:\n'
  printf '*to avoid electrical shock hazard, remove any jewelry before beginning testing;\n'
  printf 'high voltage ac may be present, do not perform alone; exercise appropriate\n'
  printf 'caution when working in or around the ac power connector, fuseholder and\n'
  printf 'power transformer.*\n\n'
  printf '**The battery assembly is capable of generating extremely high peak currents.**\n'
  printf 'Avoid accidental shorting of the battery terminals — a probe, a ring or a\n'
  printf 'dropped tool across them will weld, burn and can start a fire. The battery is\n'
  printf 'live whether or not the instrument is plugged in or switched on.\n\n'
  printf 'The internal voltage measurements are made with power applied. Take care not to\n'
  printf 'short adjacent test points or board traces with a probe (manual Caution, §4-51).\n\n'
  printf 'Servicing, opening or repairing the instrument is done entirely at your own risk,\n'
  printf 'and the manual restricts it to qualified personnel. Do not attempt it unless you\n'
  printf 'are competent to work on live equipment, and never work alone.\n\n'
  printf '### The Reference assembly is not field-repairable\n\n'
  printf 'The manual states that the Reference PCB (A5) is not to be repaired in the field:\n'
  printf 'starred parts in its parts list are to be returned to Fluke or the whole assembly\n'
  printf 'replaced, because the reference is aged and characterised as a unit and any\n'
  printf 'repair invalidates its calibration. This tool places its parts so you can find\n'
  printf 'them; it publishes no expected values for them, because the manual publishes none.\n\n'
  printf '### The information here may be wrong\n\n'
  printf 'Every value, position and procedure step in this tool was transcribed by a\n'
  printf 'machine or a person from a 1983 scan with no text layer, then checked by a\n'
  printf 'second reader. Errors survive that. The tool cites the table or paragraph each\n'
  printf 'value came from; when a reading matters, read the manual page it cites, not\n'
  printf 'this tool. Where the manual gives no tolerance the tool says so and the band\n'
  printf 'shown is an assumption, marked as inferred.\n\n'
  printf 'No warranty of any kind. The authors accept no liability for any injury, damage\n'
  printf 'or loss arising from the use of this tool or of the information in it.\n\n'
  printf -- '---\n\n'
  printf '## Licence and credits\n\n'
  printf 'The code is MIT licensed — see `LICENSE`.\n\n'
  printf 'The board drawings, schematic sheets, parts lists, procedures and symptom table\n'
  printf "are derived from Fluke's 732A Instruction Manual (P/N 645051, May 1983), which\n"
  printf 'carries its own terms'
  if [ -f CREDITS.md ]; then printf ', set out in `CREDITS.md`, which must travel with any\nredistribution of this package'; fi
  printf '. There are no photographs in this package.\n\n'
  printf 'This is an independent project, not affiliated with or endorsed by Fluke\n'
  printf 'Corporation.\n\n'
  printf 'Source, including the pipeline that builds the datasets:\n'
  printf 'https://github.com/dlebed/fluke-732a-atlas\n'
} > "$OUT/README.md"
say "$docs and a package README"

[ "$missing" -eq 0 ] || { echo "refusing to package: files above are missing" >&2; exit 1; }

# ---- 4. check nothing from the workshop came along --------------------------
strays=$(find "$OUT" \( -name '*.py' -o -name '*.sh' -o -name '.build' -o -name 'tools' \
  -o -name '*.coords.json' -o -name '*.overrides.json' -o -name '*.testpoints.json' \
  -o -name '*.reference.json' -o -name '*.caps.json' -o -name '*.parts.json' \
  -o -name '*.parts.raw.json' -o -name '*.procedures.json' -o -name '*.board.json' \
  -o -name 'manual-text' -o -name '.git' -o -name '.claude' \
  -o -name 'test-logs' -o -name 'CLAUDE.md' -o -name '.DS_Store' \) -print)
if [ -n "$strays" ]; then echo "workshop files leaked into the package:" >&2; echo "$strays" >&2; exit 1; fi

# Every reference resolves inside the package, not just in the source tree.
( cd "$OUT"
  for ref in $(grep -oE '(src|href)="[^"]+"' index.html | sed 's/.*="//;s/"//' | sort -u); do
    case "$ref" in http*|//*|data:*|'#'*) continue;; esac
    [ -f "$ref" ] || { echo "broken in package: $ref" >&2; exit 1; }
  done
  for img in $(grep -ohE '"assets/[^"]+"' data/*.js | tr -d '"' | sort -u); do
    [ -f "$img" ] || { echo "broken in package: $img" >&2; exit 1; }
  done )
say "every reference resolves"

# ---- 5. zip it --------------------------------------------------------------
( cd "$ROOT/dist" && zip -r -q -X "$NAME.zip" "$NAME" -x '*/.*' )

printf '\n%s\n' "$NAME"
say "$(find "$OUT" -type f | wc -l | tr -d ' ') files, $(du -sh "$OUT" | cut -f1)"
say "dist/$NAME/"
say "dist/$NAME.zip ($(du -h "$OUT.zip" | cut -f1))"
