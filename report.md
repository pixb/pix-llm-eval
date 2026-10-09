# Report

Cross-model comparison. One row per run, one column per case
(total score out of the case's max).

| Model | 001_svg_test (/10) | Total | Date | Judge | Notes |
|-------|--------------------|-------|------|-------|-------|
| MiMo-V2.6-Flash | ~~9.7~~ invalid | — | 2026-10-09 | self | self-scored → needs independent re-score; run files purged with the rest of `runs/`, row kept as record |
| laguna-s-2.1 | 9.8 | 9.8 | 2026-10-09 | MiMo-V2.6-Flash (independent) | fresh regeneration of 001_svg_test produced directly by laguna-s-2.1; `runs/laguna-s-2.1/001_svg_test/{result.svg,result.png,meta.md,score.md}` archived. All 3 prior defects fixed and re-verified by the judge: contrast (every white/near-white text ≥7:1, 0 white px on gradient), headline unclipped (ink bbox inside panel), wires = 2 real port-to-port beziers, no orphan. Deduction only on item 10 (0.3/0.5): KSampler overflows the editor window by 140px, dead canvas space, glyph-less toolbar buttons. |
