# Scoring criteria — 001_svg_test

Score each item, then sum. Max total: 10.
Fill this out in `runs/<model>/001-svg-test/score.md` (copy this file).

**Judge = a model other than the one under test. Self-scoring is not
allowed.** Record the judge's name in the scorecard, and cite verifiable
evidence (measurement, script output, pixel check) per line — impressions
only for items explicitly marked subjective.

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | SVG is valid and renders standalone at 1200×675 (no external refs, no missing fonts breaking layout) | 2 | /2 | |
| 2 | Node editor window: title bar + queue toolbar present | 1 | /1 | |
| 3 | All 3 nodes present and distinctly colored: Checkpoint Loader / CLIP Text Encode / KSampler | 1 | /1 | |
| 4 | Bezier wires actually connect the nodes (not decorative curves) | 1 | /1 | |
| 5 | Typography: "comfyui" 86px, "0.30.0" 58px, white, right-aligned block | 1 | /1 | |
| 6 | Background gradient uses #6366f1 → #a855f7 → #ec4899 | 1 | /1 | |
| 7 | Bottom 120px dark info bar with "Release Notes · COMFYUI" + subtitle | 1 | /1 | |
| 8 | White text AAA contrast (≥7:1) against every backdrop it sits on | 1 | /1 | |
| 9 | No elements unrelated to ComfyUI | 0.5 | /0.5 | |
| 10 | Overall aesthetic quality (proportion, hierarchy, detail polish) | 0.5 | /0.5 | |

**Total: ___ / 10**

## Reference checks

- Contrast: pick the white text color and its underlying fill, verify
  ratio ≥ 7:1 (e.g. WebAIM contrast checker).
- Render: open the SVG in a browser / rsvg-convert, screenshot to PNG,
  then judge visually.
