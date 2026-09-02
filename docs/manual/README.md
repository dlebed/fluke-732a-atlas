# The 732A manual as text

The May 1983 *732A DC Reference Standard Instruction Manual* (Fluke P/N
645051) exists only as a 600 dpi scan with no text layer. The files here are
its transcription — the text layer the PDF lacks — made so the manual never
has to be read by machine again, and so the atlas can carry the manual
inside itself (`tools/build_manual.py` turns these files into
`data/manual.js`, the Manual tab).

| File | Source pages (PDF / printed) | Holds |
|---|---|---|
| `01-specifications.md` | 9–12 / 1-1–1-4 | §1, Table 1-1 accessories, Table 1-2 specifications |
| `02-operation.md` | 13–20 / 2-1–2-8 | §2 operation, Tables 2-1 and 2-2, Figures 2-1–2-4 |
| `03-theory.md` | 21–24 / 3-1–3-4 | §3 theory of operation, Figure 3-1 block diagram |
| `04-maintenance.md` | 25–31 / 4-1–4-7 | §4-1–4-31, Table 4-1 test equipment, Figures 4-1–4-5 |
| `04-calibration.md` | 32–37 / 4-8–4-13 | §4-32–4-40 acceptance test, null verification, Procedures A and B, Figures 4-6–4-11 |
| `04-service-troubleshooting.md` | 38–42 / 4-14–4-18 | §4-41–4-54, the battery charger adjustment, Tables 4-2 and 4-3, Figure 4-12 |
| `05-parts-final-assembly.md` | 43–49 / 5-1–5-9 | §5 contents, Table 5-1 final assembly, Figure 5-1 callouts |
| `05-parts-a1-a2.md` | 50–53 / 5-10–5-13 | Tables 5-2 (A1) and 5-3 (A2) |
| `05-parts-a6-a7.md` | 63–66 / 5-21–5-24 | Figure 5-6 callouts, Tables 5-7 (A6) and 5-8 (A7) |
| `06-07-accessories-general.md` | 67–70, 81–84 | §6 accessories, §7 general information, §7A manual change information and Table 7A-1 revision levels, §8 contents |
| `07-abbreviations.md` | 70 / 7-2 | List of abbreviations and symbols |
| `07-manufacturer-codes.md` | 71–75 / 7-3–7-7 | Federal supply codes for manufacturers |
| `08-schematic-and-interconnect-notes.md` | 85–93 / 8-3–8-11 | Everything lettered on the hand-drawn sheets: pin legends, printed values, test-point nets, notes, ref-des tables |
| `errata-issue3-1985.md` | separate 18-page PDF | Change/errata sheet Issue 3 (7/85): every change with the assembly revision it applies to |

The A3, A4 and A5 parts tables (Tables 5-4, 5-5, 5-6) are transcribed row for
row into `data/a3.parts.raw.json`, `data/a4.parts.raw.json` and
`data/a5.parts.raw.json`, because the pipeline consumes them.

## Conventions

- **Verbatim.** The manual's own wording, numbering, table cells, footnotes
  and typos (`Referance`, `Unijuction`, `trouleshooting`, `PROGRMABLE`) are
  kept as printed. Nothing is corrected silently; the 1985 errata records
  what Fluke corrected, and `docs/review-notes.md` records what was found
  wrong by reading the schematics.
- Every heading carries its PDF page and printed page:
  `### 4-44. Battery Charger Adjustment Procedure (PDF p38, manual p4-14)`.
- Figures are transcribed as their callouts, labels and notes, with only a
  brief description of the geometry.
- `[unclear: …]` marks the few places the scan cannot be read with
  confidence; each names the best reading. `[transcriber note: …]` is a note
  about the source, not an uncertainty.

## How it was made, and how far to trust it

Three independent readings of every page:

1. A vision model transcribed each section from the page images, using a
   600 dpi tesseract read as a draft.
2. A second, independent model re-read the pages against the file and
   corrected it in place (every correction is logged in the workflow
   journal; typical finds were a dropped figure callout or a typo that had
   been "helpfully" fixed).
3. A third full pass, paragraph by paragraph, with an audit sampling the
   proofreaders.

On top of that, every six-digit stock number and five-digit manufacturer
code in the three parts tables was compared by machine against the 600 dpi
tesseract read (`tools/check_parts_ocr.py`): no disagreement remained that
was not a tesseract glyph slip. Rows the two vision readers disagreed on were
adjudicated from a full-resolution crop of that row. Tables 1-2, 4-2, 4-3,
§3 and §4-44 were additionally checked by hand against the page.

What the transcription cannot fix: the manual disagrees with itself in
places (Table 1-1's M07-200-601 vs §6-7's M07-200-603; the fuse ratings in
§2-19 vs the rear-panel legend in Figure 2-2; Figure 8-1's heater wire
colours vs Figure 8-2's). Those are transcribed as printed and noted where
they matter.

The manual and the errata are Fluke's; see `CREDITS.md`.
