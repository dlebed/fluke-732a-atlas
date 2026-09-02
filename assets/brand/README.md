# Brand

The mark is a zener diode — the reference element that gives a 732A its
10 V — drawn in Fluke amber inside an outlined square, the same square the
5700A troubleshooter's mark used, so the two tools read as a family. The
lockup sets **ATLAS** over **732A SERVICE** beside it.

| File | Use |
|---|---|
| `mark.svg` | the mark for dark grounds: silk (`#e9e3d2`) square, amber (`#f2b035`) diode |
| `mark-light.svg` | for light grounds: ink (`#1d1f20`) square, deeper amber (`#c8890f`) |
| `mark-mono.svg` | one colour, `currentColor` — the printable service report uses this geometry inline |
| `mark-onblack.svg` | the dark mark on its own `#16181a` tile |
| `favicon.svg` | the browser tab icon (the on-black tile) |
| `lockup-dark.svg`, `lockup-light.svg` | 240 × 72 mark + wordmark, for the README and anywhere the name is needed in full |
| `source/` | the design package as delivered |

## Geometry (32 × 32 grid)

| Element | |
|---|---|
| Square | `x=2 y=2 w=28 h=28`, stroke 2 |
| Anode / cathode leads | `M16 4.5 L16 11.5` and `M16 23 L16 27.5`, stroke 2.2 |
| Triangle | `M8 23.5 L24 23.5 L16 11.6 Z`, filled |
| Zener bar | `M6.5 14.5 L10 11 L22 11 L25.5 7.5`, stroke 2.6, square caps |

`index.html` inlines the mark rather than loading the file so it stays sharp
at any zoom and takes `--silk` and `--fluke` from the stylesheet. Below about
20 px the leads and the bent bar merge; use the on-black tile for favicons.

The lockup's wordmark is set in Barlow Condensed 700 with a fallback to the
system's condensed sans; the sub-line in Barlow 500. Neither font ships with
the tool, so the page's own lockup (`.brand-text` in `css/app.css`) uses the
fallback stack with the same letter-spacing.
