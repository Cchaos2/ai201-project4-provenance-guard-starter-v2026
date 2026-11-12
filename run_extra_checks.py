#!/usr/bin/env python3
"""
Criteria 4 and 5, three trials each.  <- UNIT 8, MILESTONE 3

run_eval.py only calls POST /submit and records the status code, so two of my
criteria need checks it can't make:

  4. An appeal against a real content_id returns 200 with status
     "under_review", the log gains one appeal entry carrying the writer's
     reasoning, and the original "decided" entry is still there, unchanged.
  5. Each malformed POST /submit (text missing, "", whitespace, null) returns
     a 400 whose JSON has an `error` and a readable `message`, and POST /ping
     still returns 200 afterwards.

    python app.py                               # one terminal
    python run_extra_checks.py --label before   # another

It only sends requests; it changes nothing in the service. Writes
results/extra_checks_<date>_<label>.md.
"""

import argparse
import datetime as dt
import json
import sys

import config

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

# Any real text works for an appeal; this is the Unit 7 clearly-human sample.
APPEAL_TEXT = json.loads(
    (config.ROOT / "samples" / "human_1.json").read_text(encoding="utf-8")
)["text"]


def entries_for(url, content_id):
    import requests
    entries = requests.get(f"{url}/log", timeout=30).json()["entries"]
    return [e for e in entries if e.get("content_id") == content_id]


def appeal_trial(url, trial, n=5):
    """Criterion 4: submit, appeal, then read the log back. One row per appeal."""
    import requests

    rows = []
    for i in range(1, n + 1):
        creator = f"x_appeal_t{trial}_{i}"
        reasoning = f"I wrote this myself. (criterion 4, trial {trial}, appeal {i})"
        row = {"appeal": i, "creator_id": creator}
        try:
            sub = requests.post(f"{url}/submit",
                                json={"text": APPEAL_TEXT, "creator_id": creator},
                                timeout=90)
            row["submit_status"] = sub.status_code
            content_id = sub.json().get("content_id")
            if not content_id:
                raise ValueError(f"submit returned no content_id: {sub.text[:200]}")
            row["content_id"] = content_id
            decided_before = [e for e in entries_for(url, content_id)
                              if e.get("status") == "decided"]

            ap = requests.post(f"{url}/appeal",
                               json={"content_id": content_id, "reasoning": reasoning},
                               timeout=30)
            row["appeal_status"] = ap.status_code
            row["appeal_response"] = ap.json()

            after = entries_for(url, content_id)
            decided_after = [e for e in after if e.get("status") == "decided"]
            appeals = [e for e in after if e.get("event") == "appeal"]
            row["appeal_log_entry"] = appeals[-1] if appeals else None
            row["decided_entry_unchanged"] = (
                len(decided_before) == 1 and decided_before == decided_after
            )
            row["passed"] = bool(
                sub.status_code == 200
                and ap.status_code == 200
                and row["appeal_response"].get("status") == "under_review"
                and len(appeals) == 1
                and appeals[0].get("reasoning") == reasoning
                and appeals[0].get("status") == "under_review"
                and row["decided_entry_unchanged"]
            )
        except Exception as exc:  # noqa: BLE001 — a failure is a result
            row["error"] = f"{type(exc).__name__}: {exc}"
            row["passed"] = False
        rows.append(row)
    return rows


def bad_bodies(trial):
    # A fresh creator_id per case and trial, so the rate limiter never answers
    # instead of the route.
    return [
        ("text missing", {"creator_id": f"x_bad_missing_t{trial}"}),
        ("text empty", {"text": "", "creator_id": f"x_bad_empty_t{trial}"}),
        ("text whitespace", {"text": "   \n\t  ", "creator_id": f"x_bad_space_t{trial}"}),
        ("text null", {"text": None, "creator_id": f"x_bad_null_t{trial}"}),
    ]


def bad_input_trial(url, trial):
    """Criterion 5: four malformed submissions, then /ping."""
    import requests

    rows = []
    for case, body in bad_bodies(trial):
        row = {"case": case, "sent": body}
        try:
            r = requests.post(f"{url}/submit", json=body, timeout=30)
            row["status"] = r.status_code
            payload = r.json()
            row["response"] = payload
            row["passed"] = bool(
                r.status_code == 400
                and isinstance(payload.get("error"), str) and payload["error"].strip()
                and isinstance(payload.get("message"), str) and payload["message"].strip()
            )
        except Exception as exc:  # noqa: BLE001
            row["error"] = f"{type(exc).__name__}: {exc}"
            row["passed"] = False
        rows.append(row)

    try:
        ping = requests.post(f"{url}/ping", json={"message": "still alive?"}, timeout=10)
        ping_status = ping.status_code
    except Exception as exc:  # noqa: BLE001
        ping_status = f"{type(exc).__name__}"
    return rows, ping_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    try:
        import requests
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    appeal_runs, bad_runs = [], []
    for trial in range(1, args.trials + 1):
        appeals = appeal_trial(args.url, trial)
        bad, ping_status = bad_input_trial(args.url, trial)
        appeal_runs.append(appeals)
        bad_runs.append((bad, ping_status))
        print(f"trial {trial}: appeals {sum(r['passed'] for r in appeals)}/{len(appeals)}  ·  "
              f"bad input {sum(r['passed'] for r in bad)}/{len(bad)}, /ping {ping_status}")

    write_report(args, appeal_runs, bad_runs)


def write_report(args, appeal_runs, bad_runs):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"extra_checks_{stamp}{label}.md"

    n = len(appeal_runs)
    head = " | ".join(f"Run {i}" for i in range(1, n + 1))
    c4 = " | ".join(f"{sum(r['passed'] for r in t)}/{len(t)}" for t in appeal_runs)
    c5 = " | ".join(f"{sum(r['passed'] for r in rows)}/{len(rows)}, /ping {ping}"
                    for rows, ping in bad_runs)

    lines = [
        f"# Extra checks{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_extra_checks.py::main` "
        "(`appeal_trial` for criterion 4, `bad_input_trial` for criterion 5)",
        "- Service: `app.py::submit`, `app.py::appeal`, `GET /log`, `POST /ping`",
        f"- {n} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"| Criterion | Target | {head} |",
        f"|---|---|{'|'.join(['---'] * n)}|",
        f"| 4. A valid appeal changes status and is recorded | 5 of 5 | {c4} |",
        f"| 5. Bad input gets a 400 with error + message; /ping still 200 "
        f"| 4 of 4, /ping 200 | {c5} |",
        "",
        "---",
        "",
        "## What actually came back",
        "",
    ]
    for t, (appeals, (bad, ping)) in enumerate(zip(appeal_runs, bad_runs), 1):
        lines += [f"### Trial {t}", "",
                  "**Criterion 4: appeals**", "", "```json",
                  json.dumps(appeals, indent=2, ensure_ascii=False), "```", "",
                  "**Criterion 5: bad input**", "", "```json",
                  json.dumps({"requests": bad, "ping_status_after": ping},
                             indent=2, ensure_ascii=False),
                  "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()