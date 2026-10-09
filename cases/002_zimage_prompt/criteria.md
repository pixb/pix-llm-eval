# Scoring criteria — 002_zimage_prompt

Score each item, then sum. Max total: 10.
Fill this out in `runs/<model>/002_zimage_prompt/score.md` (copy this file).

**Judge = a model other than the one under test. Self-scoring is not
allowed.** Record the judge's name in the scorecard.

**Two-stage judging:**

- **Stage A — prompt text only** (items 1–5): read `prompt.txt` cold,
  no image. Check format compliance, coverage of scene elements, and
  z-image-turbo safety rules (CFG=1: pure positive description, no
  negation words, no negative-prompt language).
- **Stage B — with the image** (items 6–8): open `result.png` and
  compare against the scene description in `prompt.md` (the prompt
  intent, not pixel match). Score composition / style / figure
  placement from the image itself.

**Seed policy: NO fixed seed (by design).** The image is generated
once with a random seed, so Stage B measures the *one-shot downstream
result* a real user would get — variance across models is accepted and
is part of what is being measured. Consequences for the judge:

- Log whatever seed / sampler / size the webhook returns in `meta.md`
  (traceability only — it does not affect the score).
- Regenerate **only** on infrastructure failure (empty image, timeout,
  webhook error). Never re-roll to improve or worsen a score; a merely
  "unlucky" render still gets scored as-is.
- Grade Stage B against prompt *intent*, not against an ideal render:
  penalize a missing/mis-scaled element, not a stylistic coincidence.

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

## Reference checks

- **Stage A** before looking at the image — prompt quality is the primary
  skill under test; the image is the downstream proof.
- Negation-word check is mechanical (output is pure English, so no CJK
  scan needed): case-insensitive scan of `prompt.txt` for
  `\b(no|not|without|avoid|never|don't|excluding|nor|neither)\b` plus
  the phrases `free of` / `devoid of` / `lack of`; each hit −0.5 on
  item 2 (floor 0).
- Item 7 must cite one concrete visual detail (e.g. "mist softens the
  upper third", "gold leaves read as brush strokes"), not a vibe word.
