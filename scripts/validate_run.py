#!/usr/bin/env python3
"""Validate run directories under runs/<model>/<case_id>/.

Checks per run:
  ERROR  meta.md missing, or Model / Date field missing
  ERROR  score.md missing
  ERROR  score.md arithmetic (delegates to score_calc.check_scorecard)
  ERROR  self-scoring: judge name in score.md == model under test
  ERROR  expected artifacts missing (result.png always; result.svg for
         001_* cases; prompt.txt for 002_* cases)
  WARN   case directory not named NNN_snake_case (e.g. 001-svg-test)
  WARN   meta.md Date not YYYY-MM-DD or year looks like a typo (< 2026)
  WARN   no sha256 lines in meta.md (required for new runs; legacy runs
         are fine — add checksums when re-validating)
  WARN   sha256 mismatch (ERROR with --strict)
  WARN   no recognizable Judge line in score.md

Usage:
  python3 scripts/validate_run.py [runs/<model>/<case> ...]
  python3 scripts/validate_run.py --all
  python3 scripts/validate_run.py --strict --all   # warnings → failures

Exit code: 0 clean (warnings allowed unless --strict), 1 any ERROR
(or any WARN with --strict).
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_calc import check_scorecard  # noqa: E402

CASE_DIR = re.compile(r"^\d{3}_[a-z0-9]+(_[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
META_MODEL = re.compile(r"^-\s*Model:\s*(.+?)\s*$", re.M)
META_DATE = re.compile(r"^-\s*Date:\s*(.+?)\s*$", re.M)
SHA = re.compile(r"^-\s*sha256\(([^)]+)\):\s*([0-9a-fA-F]{64})\s*$", re.M)
JUDGE = re.compile(r"\*\*Judge:\s*([^*]+?)\*\*|^Judge\s*[=:]\s*(.+?)\s*$", re.M)


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def judge_name(text: str) -> str | None:
    m = JUDGE.search(text)
    if not m:
        return None
    name = (m.group(1) or m.group(2) or "").strip()
    # strip trailing "(independent of ...)" annotation
    return re.sub(r"\s*\(.*\)\s*$", "", name).strip()


def validate_run(run: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []

    case_id = run.name
    if not CASE_DIR.match(case_id):
        warns.append(
            f"case dir {case_id!r} is not NNN_snake_case "
            "(e.g. 001_svg_test); legacy misnames kept as-is"
        )

    case_prefix = case_id.replace("-", "_").split("_")[0]

    # --- meta.md ---
    meta = run / "meta.md"
    model = None
    if not meta.is_file():
        errors.append("meta.md missing")
    else:
        meta_text = meta.read_text(encoding="utf-8")
        m = META_MODEL.search(meta_text)
        if not m:
            errors.append("meta.md has no '- Model:' field")
        else:
            model = m.group(1).strip()
        d = META_DATE.search(meta_text)
        if not d:
            errors.append("meta.md has no '- Date:' field")
        else:
            date = d.group(1).strip()
            if not DATE.match(date):
                warns.append(f"meta.md Date {date!r} is not YYYY-MM-DD")
            elif int(date[:4]) < 2026:
                warns.append(
                    f"meta.md Date year {date[:4]} predates the project "
                    "(2026+) — likely a typo"
                )
        shas = SHA.findall(meta_text)
        if not shas:
            warns.append(
                "meta.md has no sha256(...) lines "
                "(required for new runs; legacy runs unaffected)"
            )
        for fname, expected in shas:
            fp = run / fname
            if not fp.is_file():
                warns.append(f"sha256({fname}) recorded but file missing")
            elif sha256_of(fp) != expected.lower():
                warns.append(
                    f"sha256({fname}) mismatch — artifact changed since meta.md"
                )

    # --- score.md ---
    score = run / "score.md"
    if not score.is_file():
        errors.append("score.md missing")
    else:
        score_text = score.read_text(encoding="utf-8")
        problems = check_scorecard(score)
        errors.extend(problems)
        judge = judge_name(score_text)
        if judge is None:
            warns.append("score.md has no recognizable '**Judge:**' line")
        elif model and judge.casefold() == model.casefold():
            errors.append(
                f"self-scoring: judge {judge!r} == model under test "
                f"{model!r} (violates no-self-score rule)"
            )

    # --- artifacts ---
    if not (run / "result.png").is_file():
        errors.append("result.png missing")
    if case_prefix == "001" and not (run / "result.svg").is_file():
        errors.append("result.svg missing (001_* case)")
    if case_prefix == "002" and not (run / "prompt.txt").is_file():
        errors.append("prompt.txt missing (002_* case)")

    if strict and warns:
        errors.extend(f"[strict] {w}" for w in warns)
        warns = []
    return errors, warns


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("runs", nargs="*", help="run directories")
    ap.add_argument("--all", action="store_true", help="scan runs/*/*")
    ap.add_argument(
        "--strict", action="store_true", help="treat warnings as failures"
    )
    args = ap.parse_args(argv)

    if args.all:
        dirs = sorted(p for p in Path("runs").glob("*/*") if p.is_dir())
    else:
        dirs = [Path(a) for a in args.runs]
    if not dirs:
        print("no run directories (pass paths or --all)", file=sys.stderr)
        return 1

    n_err = n_warn = 0
    for run in dirs:
        errors, warns = validate_run(run, args.strict)
        label = f"{run.parent.name}/{run.name}"
        if errors:
            n_err += 1
            print(f"FAIL {label}")
            for e in errors:
                print(f"  ERROR {e}")
            for w in warns:
                print(f"  warn  {w}")
        elif warns:
            n_warn += 1
            print(f"OK*  {label}  ({len(warns)} warning(s))")
            for w in warns:
                print(f"  warn  {w}")
        else:
            print(f"OK   {label}")

    print(f"\n{len(dirs)} run(s): {n_err} failed, {n_warn} ok-with-warnings")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
