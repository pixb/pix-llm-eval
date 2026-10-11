# Scorecard template — 002_zimage_prompt

Copy this file to `runs/<model>/002_zimage_prompt/score.md` and fill the
`Score` / `Notes` columns. Weights are frozen — never change them.

**Judge = a model other than the one under test. Self-scoring is not
allowed.** Record the judge's name in the scorecard:

**Judge: <model name>** (independent of <model under test>)

Two-stage judging: Stage A = items 1–5 from `prompt.txt` alone (before
opening the image); Stage B = items 6–8 with `result.png` open, graded
against prompt intent (see `criteria.md`). No fixed seed by design —
score the one-shot render as-is.

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Output format: single paragraph, pure English, no explanations/markdown | 0.5 | /0.5 | |
| 2 | CFG=1 safety: zero negation words (no / not / without / avoid …), zero negative-prompt phrasing | 1.5 | /1.5 | count each violation |
| 3 | Scene coverage: stone stairway + bamboo + mist + light shafts + fallen leaves | 1.5 | /1.5 | 0.5 per missing element, floor 0 |
| 4 | Figure handling: elderly monk, full-body, clearly a small part of the frame (not dominating) | 1.5 | /1.5 | prompt must state scale/placement |
| 5 | Style + palette + quality suffix: 工笔淡彩 (gongbi, fine outline + light-colour wash — NOT ink-wash 水墨), emerald-green + pale-gold palette, ends with 8K/high-res suffix | 1.5 | /1.5 | 0.5 each |
| 6 | Image matches prompt intent: all key elements visible (stair, bamboo, mist, monk sweeping) | 1 | /1 | |
| 7 | Aesthetic quality: gongbi line work, depth, colour harmony | 1 | /1 | subjective; cite specific observation |
| 8 | Composition: monk small in frame, stairs lead the eye, no clipping/extra limbs | 1.5 | /1.5 | |

**Total: ___ / 10**

After filling in, run `python3 scripts/score_calc.py runs/<model>/002_zimage_prompt/score.md`
to verify the arithmetic before reporting.
