#!/usr/bin/env python3
"""Verify the arithmetic of a filled-in score.md.

Checks:
  - every table row has a numeric Score (not left as "___")
  - Score <= Weight for every item
  - the Weight column sums to 10
  - sum(Score) equals the stated **Total:**

Usage:
  python3 scripts/score_calc.py runs/<model>/<case>/score.md [...]
  python3 scripts/score_calc.py --all        # every runs/*/*/score.md

Exit code: 0 all OK, 1 any failure.
"""

import re
import sys
from pathlib import Path

ROW = re.compile(
    r"^\|\s*(\d+)\s*\|[^|]*\|\s*([\d.]+)\s*\|\s*([^|]+?)\s*\|\s*.*\|\s*$"
)
TOTAL = re.compile(r"\*\*Total:\s*([\d._]+)\s*/\s*(\d+)\s*\*\*", re.I)


def check_scorecard(path: Path) -> list[str]:
    """Return a list of problems; empty list means the card is clean."""
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    items: list[tuple[int, float, float | None]] = []
    for line in text.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        num, weight_s, score_s = int(m.group(1)), m.group(2), m.group(3)
        weight = float(weight_s)
        score_part = score_s.split("/")[0].strip()
        try:
            score = float(score_part)
        except ValueError:
            score = None
        items.append((num, weight, score))
        if score is None:
            problems.append(f"item {num}: Score column not filled ({score_s!r})")
        elif score > weight + 1e-9:
            problems.append(f"item {num}: Score {score} exceeds Weight {weight}")

    if not items:
        problems.append("no scorecard table rows found")
        return problems

    weight_sum = sum(w for _, w, _ in items)
    if abs(weight_sum - 10.0) > 1e-9:
        problems.append(f"Weights sum to {weight_sum:g}, expected 10")

    tm = TOTAL.search(text)
    if not tm:
        problems.append("no '**Total: X / 10**' line found")
    elif "_" in tm.group(1):
        problems.append("Total line not filled in")
    else:
        stated = float(tm.group(1))
        if tm.group(2) != "10":
            problems.append(f"Total denominator is {tm.group(2)}, expected 10")
        computed = sum(s for _, _, s in items if s is not None)
        if any(s is None for _, _, s in items):
            pass  # already reported above; skip misleading sum mismatch
        elif abs(computed - stated) > 1e-9:
            problems.append(
                f"stated Total {stated:g} != sum of items {computed:g}"
            )

    return problems


def main(argv: list[str]) -> int:
    if argv == ["--all"]:
        paths = sorted(Path("runs").glob("*/*/score.md"))
        if not paths:
            print("no runs/*/*/score.md found", file=sys.stderr)
            return 1
    else:
        paths = [Path(a) for a in argv]
        if not paths:
            print(__doc__, file=sys.stderr)
            return 1

    failed = 0
    for p in paths:
        if not p.is_file():
            print(f"FAIL {p}: file not found")
            failed += 1
            continue
        problems = check_scorecard(p)
        if problems:
            failed += 1
            print(f"FAIL {p}")
            for prob in problems:
                print(f"  - {prob}")
        else:
            text = p.read_text(encoding="utf-8")
            total = TOTAL.search(text)
            stated = total.group(1) if total else "?"
            print(f"OK   {p}  (Total {stated}/10)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
