#!/usr/bin/env python3
"""Check a final-project holdout submission before you upload it.

Your file has one row per holdout record and three columns:

    id        the record's id, exactly as in holdout_features.csv
    score     your model's output for that record: a probability for a yes/no or class decision,
              or the predicted value for a number
    decision  what you recommend the business does with that record; the brief's "What you submit" section says
              exactly what it means for your scenario (1/0, a quantity, or a class)

Usage, from your scenario's folder (the one unzipped from Canvas, holding this file beside submission.json):

    python validate_submission.py TeamName_holdout_predictions.csv

or, in a Colab cell, after uploading the folder's files:

    !python validate_submission.py TeamName_holdout_predictions.csv

It reads ``submission.json`` and ``holdout_features.csv`` beside it. (In the full project repository, run it from the
repository root and name the scenario: ``python templates/validate_submission.py FILE 07``.) It checks the format
only: it cannot tell you how good your decisions are.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def find_scenario(arg: str | None) -> Path:
    """The scenario folder: the one this file sits in (or the current folder) when it holds submission.json, as in a
    scenario's zip; otherwise, in the project repository, ``scenarios/<arg>``."""
    for here in (HERE, Path.cwd()):
        if (here / "submission.json").exists() and (here / "holdout_features.csv").exists():
            return here
    if arg is None:
        raise SystemExit("run this from your scenario's folder: submission.json and holdout_features.csv must be beside it")
    prefix = f"{int(arg):02d}-" if arg.isdigit() else None
    hits = [p for p in sorted((ROOT / "scenarios").iterdir())
            if p.is_dir() and (p.name == arg or (prefix and p.name.startswith(prefix)))]
    if len(hits) != 1:
        raise SystemExit(f"no single scenario matches {arg!r}; use its number (07) or folder name")
    return hits[0]


def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    path, scen = Path(sys.argv[1]), find_scenario(sys.argv[2] if len(sys.argv) == 3 else None)
    spec = json.loads((scen / "submission.json").read_text())
    holdout = pd.read_csv(scen / "holdout_features.csv", usecols=["id"])
    sub = pd.read_csv(path)
    problems, notes = [], []

    cols = list(sub.columns)
    if cols != ["id", "score", "decision"]:
        problems.append(f"the columns must be exactly id, score, decision (in that order); found {cols}")
    if "id" in sub:
        ids, want = sub["id"].astype(str), set(holdout["id"].astype(str))
        if ids.duplicated().any():
            problems.append(f"{int(ids.duplicated().sum())} id(s) appear more than once")
        if set(ids) != want:
            problems.append(f"the ids do not match holdout_features.csv: {len(want - set(ids))} missing, "
                            f"{len(set(ids) - want)} not in the holdout")
    if "score" in sub:
        sc = pd.to_numeric(sub["score"], errors="coerce")
        if sc.isna().any():
            problems.append(f"{int(sc.isna().sum())} score(s) are missing or not numbers")
        elif (spec["decision"] in ("binary", "class") and spec.get("score", "probability") == "probability"
              and ((sc < 0) | (sc > 1)).any()):
            problems.append("score must be a probability between 0 and 1 for this scenario")
    if "decision" in sub:
        d = sub["decision"]
        if d.isna().any():
            problems.append(f"{int(d.isna().sum())} decision(s) are missing")
        elif spec["decision"] == "binary":
            bad = ~d.astype(str).isin(["0", "1", "0.0", "1.0"])
            if bad.any():
                problems.append(f"decision must be 1 or 0 for this scenario; {int(bad.sum())} row(s) are not")
            elif spec.get("capacity_share") is not None:
                cap = math.floor(spec["capacity_share"] * len(holdout))
                n = int(pd.to_numeric(d).sum())
                if n > cap:
                    if spec.get("capacity_strict"):
                        problems.append(f"you mark {n:,} records with decision 1; the capacity is {cap:,}. Mark at "
                                        f"most {cap:,}: the brief's What you submit says so.")
                    else:
                        notes.append(f"you recommend acting on {n:,} records; the capacity is {cap:,}. Only your "
                                     f"{cap:,} highest-scored will be acted on.")
        elif spec["decision"] == "quantity":
            q = pd.to_numeric(d, errors="coerce")
            if q.isna().any() or (q < 0).any():
                problems.append("decision must be a number of zero or more for this scenario")
            elif (q % 1 != 0).any():
                problems.append(f"decision must be a whole number for this scenario; {int((q % 1 != 0).sum())} row(s) "
                                "are not")
        elif spec["decision"] == "class":
            bad = ~d.astype(str).isin([str(x) for x in spec["classes"]])
            if bad.any():
                problems.append(f"decision must be one of {spec['classes']}; {int(bad.sum())} row(s) are not")

    print(f"{path.name} against {spec.get('scenario', scen.name)}: {len(sub):,} rows")
    for n in notes:
        print(f"  note: {n}")
    if problems:
        for p in problems:
            print(f"  PROBLEM: {p}")
        raise SystemExit("Fix the problems above before you submit.")
    print("  The format is right. (This cannot tell you how good your decisions are.)")


if __name__ == "__main__":
    main()
