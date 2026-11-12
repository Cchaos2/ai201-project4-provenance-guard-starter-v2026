"""
Turn a run_eval.py report into run-log numbers for criteria 1, 2, 3 and 5.

    python summarize_eval.py results/run_<date>_before.md

It reads the JSON that run_eval.py saved under "What actually came back" and
counts what each target in criteria.md needs. It sends nothing. Criterion 4
(and the full criterion 5 check) come from run_extra_checks.py instead.
"""

import json
import math
import re
import sys
from pathlib import Path


def load(path):
    text = Path(path).read_text(encoding="utf-8")
    body = text.split("## What actually came back", 1)[1]
    parts = re.split(r"^### (.+)$", body, flags=re.M)
    data = {}
    for name, content in zip(parts[1::2], parts[2::2]):
        blocks = re.findall(r"```json\n(.*?)\n```", content, flags=re.S)
        data[name.strip()] = [json.loads(b) for b in blocks]
    return data


def mean(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return sum(values) / len(values) if values else math.nan


def stable(trials):
    """True when every trial returned the same status, guess and score per input."""
    shape = [[(r.get("status"), r.get("guess"), r.get("confidence")) for r in t]
             for t in trials]
    return all(s == shape[0] for s in shape)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    data = load(sys.argv[1])
    rows, notes = [], []

    c1 = data.get("c1 own writing")
    if c1:
        counts = [sum(1 for r in t if r.get("guess") == "ai") for t in c1]
        n = len(c1[0])
        rows.append(("1. My own writing flagged as AI", "≤ 1 of 10",
                     [f"{c}/{n}" for c in counts],
                     "MET" if all(c <= 1 for c in counts) else "MISSED"))
        notes.append(f"c1 guesses per trial: "
                     f"{[[r.get('guess') for r in t] for t in c1]}")
        notes.append(f"c1 identical across trials: {stable(c1)}")

    ai, hu = data.get("c2 AI set"), data.get("c2 human set")
    if ai and hu:
        gaps = []
        for t, (a, h) in enumerate(zip(ai, hu), 1):
            ma = mean(r.get("confidence") for r in a)
            mh = mean(r.get("confidence") for r in h)
            gaps.append(ma - mh)
            notes.append(f"c2 trial {t}: AI mean {ma:.4f} − human mean {mh:.4f} "
                         f"= gap {ma - mh:.4f}")
        rows.append(("2. AI vs human average confidence gap", "≥ 0.30",
                     [f"{g:.3f}" for g in gaps],
                     "MET" if all(g >= 0.30 for g in gaps) else "MISSED"))
        notes.append(f"c2 identical across trials: {stable(ai) and stable(hu)}")

    c3 = data.get("c3 label coverage")
    if c3:
        cells, every_trial = [], True
        for t, trial in enumerate(c3, 1):
            per_label = {g: sum(1 for r in trial if r.get("guess") == g)
                         for g in ("human", "unsure", "ai")}
            reached = sum(1 for v in per_label.values() if v >= 2)
            every_trial &= reached == 3
            cells.append(f"{reached}/3")
            notes.append(f"c3 trial {t}: texts per label {per_label}")
        rows.append(("3. Every label reached by at least 2 texts", "3 of 3",
                     cells, "MET" if every_trial else "MISSED"))
        notes.append(f"c3 identical across trials: {stable(c3)}")

    c5 = data.get("c5 bad input")
    if c5:
        counts = [sum(1 for r in t if r.get("status") == 400) for t in c5]
        n = len(c5[0])
        rows.append(("5. Bad input gets a 400 (status codes; full check in "
                     "run_extra_checks.py)", "4 of 4",
                     [f"{c}/{n}" for c in counts],
                     "MET" if all(c == n for c in counts) else "MISSED"))
        notes.append(f"c5 statuses per trial: {[[r.get('status') for r in t] for t in c5]}")

    trials = max((len(r[2]) for r in rows), default=3)
    print("| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, trials + 1))
          + " | Verdict |")
    print("|---|---|" + "|".join(["---"] * trials) + "|---|")
    for name, target, cells, verdict in rows:
        print(f"| {name} | {target} | {' | '.join(cells)} | {verdict} |")
    print()
    for note in notes:
        print(note)


if __name__ == "__main__":
    main()