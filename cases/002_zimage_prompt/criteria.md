# Scoring criteria — 002_zimage_prompt

The scorecard table (weights frozen) lives in
`scorecard.template.md` — the judge copies **that** file into
`runs/<model>/002_zimage_prompt/score.md` and fills it in. This file
only defines *how* to judge.

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

**Max total: 10.** Sum the filled scores, then verify with
`python3 scripts/score_calc.py runs/<model>/002_zimage_prompt/score.md`.

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
