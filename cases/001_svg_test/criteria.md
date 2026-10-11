# Scoring criteria — 001_svg_test

The scorecard table (weights frozen) lives in
`scorecard.template.md` — the judge copies **that** file into
`runs/<model>/001_svg_test/score.md` and fills it in. This file only
defines *how* to judge.

**Judge = a model other than the one under test. Self-scoring is not
allowed.** Record the judge's name in the scorecard.

**How to judge (vision-first):** look at `result.png` first and score
presence/layout/aesthetic items straight from the image. Then run a
small number of targeted spot-checks only where a graded claim needs a
number (contrast ratio, exact font size, path validity, 1–3px edge
clips). Cite either the measurement or the observed detail per line —
impressions only for items explicitly marked subjective.

**Max total: 10.** Sum the filled scores, then verify with
`python3 scripts/score_calc.py runs/<model>/001_svg_test/score.md`.

## Reference checks

- **Default: eyeball `result.png`** — presence, hierarchy, obvious
  defects (clipping, overlaps, dead space) are judged visually.
- **Spot-check with a number only when a score depends on it:**
  - item 8: contrast ratio of white text vs its actual fill (must be ≥ 7:1)
  - items 5/6: font-size / gradient stops in the SVG source
  - item 1: one rsvg-convert render + XML/path sanity (validity only)
