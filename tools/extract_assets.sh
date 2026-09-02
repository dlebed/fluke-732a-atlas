#!/usr/bin/env bash
#
# extract_assets.sh — build the image assets for one dataset of the 732A Atlas.
#
# The source is the scanned 732A Instruction Manual (P/N 645051, May 1983):
# 600 dpi 1-bit scans, one figure per page, the figure drawn inside a ruled
# frame. Every page is rendered upright with pdftoppm (which applies the page
# rotation the PDF carries), cropped to the region of interest at full
# resolution, and only then downscaled for the browser.
#
# Usage:   tools/extract_assets.sh <a3|a4|a5|sys>
#          MANUAL=/path/to/732A-manual.pdf tools/extract_assets.sh a3
#
# Crop rectangles are WxH+X+Y in pixels of the upright 600 dpi page
# (10200 x 6600). A board drawing is cropped to the PCB outline plus a 40 px
# margin -- the outline, not the page -- measured by tools/find_outline.py and
# confirmed by eye; a schematic or diagram is cropped to its ruled frame.
#
# Figure 8-1 (interconnect) and Figure 8-2 (motherboard / battery / LED) are
# shared: they are extracted once, under sys/, and the board datasets name the
# same asset files as their extra sheets. The per-board .build/ copies that
# the OCR pipeline expects for those sheets are symlinks to the sys crops.

set -euo pipefail

ASM="${1:?usage: tools/extract_assets.sh <a3|a4|a5|sys>}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
MANUAL="${MANUAL:-$(dirname "$ROOT")/732A-manual.pdf}"
[ -f "$MANUAL" ] || { echo "manual not found: $MANUAL (set MANUAL=...)" >&2; exit 1; }

DRAWING_WIDTH=3200      # browser copy of a board drawing
SHEET_WIDTH=4800        # browser copy of a schematic sheet or diagram

# Shared figures (Chapter 8), by PDF page: rectangle = the ruled frame.
INTERCONNECT_PAGE=85; INTERCONNECT_CROP="9517x5608+397+479"      # Figure 8-1
MOBO_SCH_PAGE=87;     MOBO_SCH_CROP="9436x5556+441+507"          # Figure 8-2 (cont), A1/A2/A6 schematic
MOBO_DRAW_PAGE=86;    MOBO_DRAW_CROP="9471x5548+242+440"         # Figure 8-2, A1/A2/A6 outlines

case "$ASM" in
  a3)
    DRAWING_PAGE=88;  DRAWING_CROP="3620x4552+5553+1022"   # Figure 8-3, PCB outline 5573..9113 x 1042..5514
    SHEET_PAGES=(89); SHEET_CROPS=("9440x5567+491+453")    # Figure 8-3 (cont), 732A-1003
    SHARED_SHEETS=(interconnect mobo_sch)                  # -> sh2, sh3
    ;;
  a4)
    DRAWING_PAGE=90;  DRAWING_CROP="3600x3170+5551+1713"   # Figure 8-4, PCB outline 5571..9089 x 1733..4823
    SHEET_PAGES=(91); SHEET_CROPS=("9701x5565+234+462")    # Figure 8-4 (cont), 732A-1002
    SHARED_SHEETS=(interconnect mobo_sch)
    ;;
  a5)
    DRAWING_PAGE=92;  DRAWING_CROP="4170x2380+5109+2193"   # Figure 8-5, PCB outline 5149..9237 x 2233..4533
    SHEET_PAGES=(93); SHEET_CROPS=("9468x5566+470+464")    # Figure 8-5 (cont), 732A-1001 / -1007
    SHARED_SHEETS=(interconnect)                           # -> sh2
    ;;
  sys)
    DRAWING_PAGE=$INTERCONNECT_PAGE; DRAWING_CROP="$INTERCONNECT_CROP"
    SHEET_PAGES=($MOBO_SCH_PAGE $MOBO_DRAW_PAGE); SHEET_CROPS=("$MOBO_SCH_CROP" "$MOBO_DRAW_CROP")
    SHARED_SHEETS=()
    ;;
  *) echo "unknown dataset '$ASM'" >&2; exit 1;;
esac

BUILD="$ROOT/.build/$ASM"; OUT="$ROOT/assets/$ASM"
mkdir -p "$BUILD" "$OUT"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/extract.XXXXXX")"; trap 'rm -rf "$TMP"' EXIT

render() {   # render <page> -> path of the upright 600 dpi PNG
  local page="$1"
  local cached="$ROOT/.build/pages/p600-$page.png"
  if [ -f "$cached" ]; then echo "$cached"; return; fi
  pdftoppm -r 600 -png -f "$page" -l "$page" "$MANUAL" "$TMP/p" >/dev/null
  echo "$TMP"/p-*"$page".png
}

crop() {     # crop <page> <geometry> <full.png> <browser.png> <width>
  local src
  src="$(render "$1")"
  magick "$src" -crop "$2" +repage -colorspace Gray -depth 8 "$3"
  magick "$3" -resize "${5}x" -colors 32 -define png:compression-level=9 "$4"
  printf '  %-22s %s -> %s\n' "$(basename "$4")" "$(magick identify -format '%wx%h' "$3")" "$(magick identify -format '%wx%h' "$4")"
}

echo "$ASM: drawing (page $DRAWING_PAGE)"
WIDTH=$DRAWING_WIDTH; [ "$ASM" = sys ] && WIDTH=$SHEET_WIDTH
crop "$DRAWING_PAGE" "$DRAWING_CROP" "$BUILD/drawing_full.png" "$OUT/drawing.png" "$WIDTH"

n=1
for i in "${!SHEET_PAGES[@]}"; do
  echo "$ASM: sheet $n (page ${SHEET_PAGES[$i]})"
  crop "${SHEET_PAGES[$i]}" "${SHEET_CROPS[$i]}" "$BUILD/sch${n}_full.png" "$OUT/sch${n}.png" "$SHEET_WIDTH"
  n=$((n + 1))
done

# Shared sheets: the sys dataset owns the crops; a board's .build gets a link so
# spaces.py and the reader see them as sh2, sh3 of that board.
for s in ${SHARED_SHEETS[@]+"${SHARED_SHEETS[@]}"}; do
  case "$s" in
    interconnect) src="$ROOT/.build/sys/drawing_full.png";;
    mobo_sch)     src="$ROOT/.build/sys/sch1_full.png";;
  esac
  [ -f "$src" ] || { echo "  $s: run tools/extract_assets.sh sys first" >&2; exit 1; }
  ln -sfn "$src" "$BUILD/sch${n}_full.png"
  echo "  sch${n}_full.png -> $(basename "$(dirname "$src")")/$(basename "$src") (shared, $s)"
  n=$((n + 1))
done
echo "done: $OUT"
