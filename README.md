# pix-llm-eval

Personal LLM evaluation notebook. There is **no runner code**: every
evaluation is driven manually from an agent conversation — the agent
generates the output, you inspect it and fill in a scorecard.

## Layout

```
pix-llm-eval/
├── cases/                       # frozen test cases
│   └── <case_id>/
│       ├── prompt.md            # the prompt sent to the model
│       ├── criteria.md          # how to judge (rules, defined BEFORE running)
│       └── scorecard.template.md # frozen scoring table; judge copies & fills this
├── scripts/
│   ├── generate_z_image.py      # z-image n8n webhook helper (body POST)
│   ├── score_calc.py            # verify score.md arithmetic (sum == Total, weights == 10)
│   └── validate_run.py          # lint runs/: meta fields, judge≠model, artifacts, sha256
├── .env.example                 # copy to .env; set N8N_WEBHOOK_URL
├── runs/                        # one directory per model
│   └── <model_name>/
│       └── <case_id>/
│           ├── meta.md          # model version, date, agent settings
│           ├── result.svg       # raw model output
│           ├── result.png       # rendered screenshot, for eyeballing
│           └── score.md         # filled-in copy of criteria.md
├── report.md                    # cross-model comparison table
└── README.md
```

`runs/` is **git-ignored** — results live only on your machine. Reasons:
(1) the model under test reads this working directory, and seeing prior
runs would contaminate the test; (2) scores are yours, not the repo's.
Before each test, **you decide** whether to wipe old results first
(`rm -rf runs/<model>` or all of `runs/`) so nothing can be referenced.
`report.md` stays committed — if you want scores hidden too, move or
ignore it as well.

## Workflow

1. **Define the case.** Create `cases/<case_id>/prompt.md`,
   `criteria.md` (how to judge) and `scorecard.template.md` (the frozen
   weight table). The rubric must be fixed before the run — never write
   criteria after seeing the result.
2. **Run.** In an agent conversation, give the model under test the
   prompt, collect its output. This model only *produces* output.
   For text-to-image cases (e.g. `002_zimage_prompt`): save the model's
   prompt as `runs/<model>/<case_id>/prompt.txt`, then generate the
   image with this repo's own helper —
   `cp .env.example .env` (set `N8N_WEBHOOK_URL`), then
   `python3 scripts/generate_z_image.py runs/<model>/<case_id>/prompt.txt runs/<model>/<case_id>/result.png`.
3. **Archive.** Create `runs/<model>/<case_id>/`, save the raw output as
   `result.*`, render a `result.png` where applicable, and record
   `meta.md`.
4. **Score with a different model.** A **judge model** — never the model
   being tested** — copies `cases/<case_id>/scorecard.template.md` into
   the run directory as `score.md` and fills in `Score` / `Notes`. Judge
   vision-first: read `result.png` directly and score qualitative items
   (presence, layout, aesthetics) from the image, then run only targeted
   numeric spot-checks for the claims that need a number (contrast
   ratio, font size in source, path arity / clip probes) — not a full
   battery every time. Evidence lines cite the measurement or the visual
   observation. The judge records its own name in `score.md`. Before
   reporting, verify the arithmetic:
   `python3 scripts/score_calc.py runs/<model>/<case_id>/score.md`.
5. **Human spot-check.** You review the judge's evidence for the
   subjective items and override where you disagree.
6. **Report.** Run `python3 scripts/validate_run.py runs/<model>/<case_id>`
   (or `--all`), fix any ERRORs, then add a row for the model in
   `report.md`. Warnings on legacy runs (missing sha256, misnamed
   directories) are informational and don't block.

## Naming

- `case_id`: `NNN_short_name`, zero-padded, stable forever
  (e.g. `001_svg_test`).
- `model_name`: the exact model version you tested
  (e.g. `MiMo-V2.6-Flash`). A new version ⇒ a new directory, so results
  never get silently overwritten.

## meta.md template

```markdown
- Model: <exact model id / version>
- Date: YYYY-MM-DD
- Driven by: <agent / manual>
- Settings: temperature, system prompt, single turn or multi-turn
- Output: <raw / with tool calls / regenerations>
- Image gen (if any): model + size + **seed as returned** (seeds are
  random by design — log for traceability, never fix them)
- sha256(result.png): <hex>       # one line per artifact; validate_run.py checks it
- sha256(result.svg): <hex>       # (001_* cases)
- Notes: anything that affects reproducibility
```

New runs should record a `sha256(...)` line per artifact
(`sha256sum runs/<model>/<case>/*`); legacy runs without checksums are
fine — `validate_run.py` only warns.

## Rules

- **No self-scoring.** The model that produced a run may never write or
  edit its own `score.md`. Scoring is always done by a different judge
  model (or by you). A self-score found in the wild gets replaced, with
  the original claim noted in `meta.md`.
- Every score line must carry checkable evidence — a measurement or a
  specific visual observation (e.g. "wire crosses node body at y≈350"),
  not a vague impression. Numeric spot-checks are reserved for claims
  graded on a number (contrast, sizes, overflow); subjective items
  (e.g. aesthetics) are marked as such and open to your override.
- One run = one directory. Never overwrite a previous run; re-running
  means a new directory (add a suffix, e.g. `001-svg-test-2`).
- Keep case prompts immutable once scored. If a case must change, bump
  its ID rather than editing in place.
- `runs/` never enters git (ignored + purged from history). Whether to
  wipe old run results before a new test is **your call each time** —
  wipe when the model under test must not see earlier outputs.
