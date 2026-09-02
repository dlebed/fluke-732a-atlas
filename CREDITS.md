# Credits

The MIT licence in `LICENSE` covers the code in this repository — the engine
under `js/`, the pipeline under `tools/`, and the curated data files under
`data/`. It does not cover the material described below, which is included or
derived under the terms its own authors set.

## Service manual material — Fluke

The board drawings, schematic sheets and diagrams under `assets/`, the
transcribed manual text under `docs/manual/`, the parts tables, procedures,
symptom table and expected values under `data/`, and the manual sections
shipped inside the page as `data/manual.js` are all derived from the Fluke
*732A DC Reference Standard Instruction Manual* (P/N 645051, May 1983) and
its *Change/Errata Information, Issue No. 3* (7/85). Fluke owns that material;
it is reproduced here for the education and repair of the instrument it
documents, and it is not covered by the MIT licence above.

The manual PDFs themselves are **not** included in this repository. See the
README for where the pipeline expects to find them.

## Engine — the 5700A Interactive Troubleshooter

The engine (`js/`, `css/`, `index.html`) and most of the pipeline (`tools/`)
are adapted from the Fluke 5700A Interactive Troubleshooter, an MIT-licensed
project by the same author. The 732A Atlas keeps that project's conventions:
standalone HTML, one dataset per assembly, curated inputs that survive a
rebuild.

## Photographs

There are none yet. The `photo` layer stays in the schema for the day a board
is photographed; any photograph added later carries its own credit here.

## No affiliation

This is an independent project. It is not produced, endorsed or supported by
Fluke Corporation.
