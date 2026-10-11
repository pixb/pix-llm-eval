# Scorecard template — 001_svg_test

Copy this file to `runs/<model>/001_svg_test/score.md` and fill the
`Score` / `Notes` columns. Weights are frozen — never change them.

**Judge = a model other than the one under test. Self-scoring is not
allowed.** Record the judge's name in the scorecard:

**Judge: <model name>** (independent of <model under test>)

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

After filling in, run `python3 scripts/score_calc.py runs/<model>/001_svg_test/score.md`
to verify the arithmetic before reporting.
