#!/usr/bin/env python3
"""
One trial of my five capstone criteria.  <- UNIT 9 (capstone), MILESTONE 5

A trial, as criteria.md defines it:

    1. Stop the service.
    2. Start it again:  gunicorn app:app --bind 127.0.0.1:5000 --workers 1 --timeout 120
    3. In another terminal:  python run_capstone.py --label before --trial 1

Do that three times (--trial 1, 2, 3). Then print the run-log table:

    python run_capstone.py --label before --table

What it runs, in this order:

    criterion 3  cold start            the first two /submit after the restart
    criterion 1  one record each       the 20-request session in criteria.md
    criterion 4  the appeal path       run_extra_checks.py::appeal_trial (Unit 8)
    criterion 5  bad input gets a 400  run_extra_checks.py::bad_input_trial (Unit 8)
    criterion 2  a crash is recorded   last, because it makes logs/audit.jsonl
                                       read-only for three requests, then puts
                                       the permissions back

It sends requests and reads logs/requests.jsonl back. It changes nothing in the
service. Each trial writes results/capstone_<label>_trial<N>.md (the real
output) and a .json next to it (the scores the table is built from).
"""

import argparse
import datetime as dt
import json
import os
import stat
import sys

import config
from run_extra_checks import appeal_trial, bad_input_trial
from scenarios import MY_WRITING

URL = f"http://{config.HOST}:{config.PORT}"

REQUIRED_FIELDS = ("timestamp", "method", "route", "input", "status",
                   "outcome", "output", "duration_ms")

COLD_LIMIT_MS = 10_000     # criterion 3, check 1
WARM_LIMIT_MS = 100        # criterion 3, check 3

CRITERIA = [
    ("1", "Every request leaves exactly one complete log record", "20 of 20"),
    ("2", "A crash still writes a record and returns JSON", "3 of 3"),
    ("3", "Cold start is bounded and the log reports it correctly", "3 of 3 checks"),
    ("4", "A valid appeal always changes status and is always recorded", "5 of 5"),
    ("5", "Bad input gets a clear error, never a crash", "4 of 4, then /ping 200"),
]


# ── reading the request log back ─────────────────────────────────────────────

def raw_lines():
    """Every line of logs/requests.jsonl, exactly as written."""
    if not config.REQUEST_LOG.exists():
        return []
    return config.REQUEST_LOG.read_text(encoding="utf-8").splitlines()


def record_for(creator_id):
    """The raw line and parsed record of the last /submit from one creator_id."""
    for line in reversed(raw_lines()):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (record.get("route") == "/submit"
                and isinstance(record.get("input"), dict)
                and record["input"].get("creator_id") == creator_id):
            return line, record
    return None, None


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# ── criterion 3 ── cold start ────────────────────────────────────────────────

def check_cold_start(requests, tag):
    lines, records = [], []
    for i in (0, 1):
        creator_id = f"cap_{tag}_c3_{i + 1}"
        requests.post(f"{URL}/submit",
                      json={"text": MY_WRITING[i], "creator_id": creator_id},
                      timeout=120)
        line, record = record_for(creator_id)
        lines.append(line)
        records.append(record or {})
    first, second = records
    checks = {
        f"1. first /submit takes at most {COLD_LIMIT_MS:,} ms":
            is_number(first.get("duration_ms")) and first["duration_ms"] <= COLD_LIMIT_MS,
        "2. first record has detector_loaded_at_start: false":
            first.get("detector_loaded_at_start") is False,
        f"3. second record has detector_loaded_at_start: true and takes at most {WARM_LIMIT_MS} ms":
            second.get("detector_loaded_at_start") is True
            and is_number(second.get("duration_ms")) and second["duration_ms"] <= WARM_LIMIT_MS,
    }
    held = sum(checks.values())
    return {
        "score": f"{held}/3 (first {first.get('duration_ms')} ms, second {second.get('duration_ms')} ms)",
        "passed": held == 3,
        "checks": checks,
        "log_lines": lines,
    }


# ── criterion 1 ── twenty requests, twenty records ───────────────────────────

def check_log_completeness(requests, tag):
    def post(path, body):
        return requests.post(f"{URL}{path}", json=body, timeout=120)

    before = len(raw_lines())
    sent = []      # (what was sent, status the client got)

    sent.append(("GET /health", requests.get(f"{URL}/health", timeout=30).status_code))
    sent.append(("POST /ping", post("/ping", {"message": "capstone"}).status_code))
    sent.append(("GET /log?limit=1", requests.get(f"{URL}/log?limit=1", timeout=30).status_code))

    content_id = None
    for i in range(3):          # valid, each with its own creator_id
        r = post("/submit", {"text": MY_WRITING[2 + i], "creator_id": f"cap_{tag}_c1_own{i + 1}"})
        sent.append(("POST /submit valid, own creator_id", r.status_code))
        if r.status_code == 200:
            content_id = r.json().get("content_id")
    for i in range(7):          # valid, all from ONE creator_id: 5 a minute allowed
        r = post("/submit", {"text": MY_WRITING[5], "creator_id": f"cap_{tag}_c1_same"})
        sent.append(("POST /submit valid, same creator_id", r.status_code))
    for i in range(2):
        r = post("/submit", {"creator_id": f"cap_{tag}_c1_notext{i + 1}"})
        sent.append(("POST /submit with no text", r.status_code))
    for i in range(2):
        r = post("/submit", {"text": "hi", "creator_id": f"cap_{tag}_c1_hi{i + 1}"})
        sent.append(('POST /submit with "hi"', r.status_code))
    r = post("/appeal", {"content_id": content_id, "reasoning": "I wrote this myself."})
    sent.append(("POST /appeal valid", r.status_code))
    for i in range(2):
        r = post("/appeal", {"content_id": f"c_unknown_{tag}_{i + 1}", "reasoning": "I wrote this myself."})
        sent.append(("POST /appeal with an unknown id", r.status_code))

    new_lines = raw_lines()[before:]
    complete = 0
    problems = []
    for number, line in enumerate(new_lines, 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            problems.append(f"line {number} does not parse as JSON")
            continue
        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            problems.append(f"line {number} is missing {missing}")
        else:
            complete += 1

    growth = len(new_lines)
    return {
        "score": f"{complete}/20" + ("" if growth == 20 else f" (log grew by {growth}, not 20)"),
        "passed": len(sent) == 20 and growth == 20 and complete == 20,
        "requests_sent": len(sent),
        "log_grew_by": growth,
        "complete_records": complete,
        "problems": problems,
        "statuses_the_client_got": [f"{what} -> {status}" for what, status in sent],
        "log_lines": new_lines,
    }


# ── criterion 2 ── a forced crash ────────────────────────────────────────────

def check_crash(requests, tag):
    """
    Make logs/audit.jsonl read-only, send three valid submissions, put the
    permissions back. /submit scores the text and then fails when it tries to
    write the decision to the audit log.
    """
    path = config.AUDIT_LOG
    original_mode = stat.S_IMODE(os.stat(path).st_mode)
    rows = []
    os.chmod(path, original_mode & ~0o222)          # chmod a-w
    try:
        for i in range(3):
            creator_id = f"cap_{tag}_c2_{i + 1}"
            row = {"crash": i + 1, "creator_id": creator_id}
            r = requests.post(f"{URL}/submit",
                              json={"text": MY_WRITING[i], "creator_id": creator_id},
                              timeout=120)
            row["response_status"] = r.status_code
            row["response_content_type"] = r.headers.get("Content-Type")
            row["response_body"] = r.text[:300]
            try:
                body = r.json()
            except ValueError:
                body = None
            row["response_ok"] = bool(
                isinstance(body, dict)
                and isinstance(body.get("error"), str) and body["error"].strip()
                and isinstance(body.get("message"), str) and body["message"].strip()
            )
            line, record = record_for(creator_id)
            record = record or {}
            row["log_line"] = line
            row["record_ok"] = bool(
                record.get("status") == 500
                and record.get("outcome") == "error"
                and isinstance(record.get("exception"), str) and record["exception"].strip()
                and is_number(record.get("duration_ms"))
            )
            row["passed"] = row["record_ok"] and row["response_ok"]
            rows.append(row)
    finally:
        os.chmod(path, original_mode)               # always put it back
    passed = sum(row["passed"] for row in rows)
    return {
        "score": (f"{passed}/3 (record {sum(r['record_ok'] for r in rows)}/3, "
                  f"JSON response {sum(r['response_ok'] for r in rows)}/3)"),
        "passed": passed == 3,
        "rows": rows,
    }


# ── criteria 4 and 5 ── the Unit 8 checks, unchanged ─────────────────────────

def check_appeals(tag):
    rows = appeal_trial(URL, tag)
    passed = sum(row["passed"] for row in rows)
    return {"score": f"{passed}/5", "passed": passed == 5, "rows": rows}


def check_bad_input(tag):
    rows, ping_status = bad_input_trial(URL, tag)
    passed = sum(row["passed"] for row in rows)
    return {
        "score": f"{passed}/4, /ping {ping_status}",
        "passed": passed == 4 and ping_status == 200,
        "rows": rows,
        "ping_status_afterwards": ping_status,
    }


# ── the report ───────────────────────────────────────────────────────────────

def paths(label, trial):
    base = config.RESULTS_DIR / f"capstone_{label}_trial{trial}"
    return base.with_suffix(".md"), base.with_suffix(".json")


def block(text, language=""):
    return f"```{language}\n{text}\n```\n"


def write_report(label, trial, server, results):
    md_path, json_path = paths(label, trial)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [
        f"# Capstone run: {label}, trial {trial}\n",
        "- Produced by: `run_capstone.py::main`",
        f"- Service: {URL}, `Server` header: `{server}`, restarted for this trial "
        f"(`GET /health` said `detector_loaded: false` before the first request)",
        f"- {now}\n",
        "| Criterion | Target | This trial | Passed |",
        "|---|---|---|---|",
    ]
    for number, name, target in CRITERIA:
        r = results[number]
        out.append(f"| {number}. {name} | {target} | {r['score']} | {'yes' if r['passed'] else 'NO'} |")
    out.append("\n---\n\n## What actually came back\n")

    r = results["1"]
    out.append("### 1. Every request leaves exactly one complete log record\n")
    out.append("`run_capstone.py::check_log_completeness`. "
               f"Requests sent: {r['requests_sent']}. `logs/requests.jsonl` grew by: {r['log_grew_by']}. "
               f"Lines that parse and have all eight fields: {r['complete_records']}.\n")
    if r["problems"]:
        out.append(block("\n".join(r["problems"])))
    out.append("The status the client got for each request, in order:\n")
    out.append(block("\n".join(r["statuses_the_client_got"])))
    out.append("The lines the log gained while those were sent:\n")
    out.append(block("\n".join(r["log_lines"]), "json"))

    r = results["2"]
    out.append("### 2. A crash still writes a record and returns JSON\n")
    out.append("`run_capstone.py::check_crash`, with `logs/audit.jsonl` read-only.\n")
    for row in r["rows"]:
        out.append(f"**Crash {row['crash']}** (record ok: {row['record_ok']}, "
                   f"JSON response ok: {row['response_ok']})\n")
        out.append("What the client got:\n")
        out.append(block(f"HTTP {row['response_status']}\nContent-Type: "
                         f"{row['response_content_type']}\n\n{row['response_body']}"))
        out.append("What the log got:\n")
        out.append(block(row["log_line"] or "(no record for this request)", "json"))

    r = results["3"]
    out.append("### 3. Cold start is bounded and the log reports it correctly\n")
    out.append("`run_capstone.py::check_cold_start`. The first two `/submit` after the restart:\n")
    out.append(block("\n".join(line or "(no record)" for line in r["log_lines"]), "json"))
    out.append(block("\n".join(f"{'held  ' if ok else 'FAILED'}  {name}" for name, ok in r["checks"].items())))

    r = results["4"]
    out.append("### 4. A valid appeal always changes status and is always recorded\n")
    out.append("`run_extra_checks.py::appeal_trial`, called by `run_capstone.py::check_appeals`.\n")
    out.append(block(json.dumps(r["rows"], indent=2, ensure_ascii=False), "json"))

    r = results["5"]
    out.append("### 5. Bad input gets a clear error, never a crash\n")
    out.append("`run_extra_checks.py::bad_input_trial`, called by `run_capstone.py::check_bad_input`. "
               f"`POST /ping` afterwards: {r['ping_status_afterwards']}.\n")
    out.append(block(json.dumps(r["rows"], indent=2, ensure_ascii=False), "json"))

    config.RESULTS_DIR.mkdir(exist_ok=True)
    md_path.write_text("\n".join(out), encoding="utf-8")
    json_path.write_text(json.dumps({
        "label": label, "trial": trial, "when": now, "server": server,
        "scores": {n: {"score": results[n]["score"], "passed": results[n]["passed"]}
                   for n, _, _ in CRITERIA},
    }, indent=2), encoding="utf-8")
    return md_path


def print_table(label):
    """The run-log table, from the three trials' .json files."""
    trials = []
    for trial in (1, 2, 3):
        _, json_path = paths(label, trial)
        if not json_path.exists():
            sys.exit(f"No {json_path.name} yet. Run trial {trial} first.")
        trials.append(json.loads(json_path.read_text(encoding="utf-8")))
    print("| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |")
    print("|---|---|---|---|---|---|")
    for number, name, target in CRITERIA:
        cells = [t["scores"][number] for t in trials]
        verdict = "MET" if all(c["passed"] for c in cells) else "MISSED"
        print(f"| {number}. {name} | {target} | " + " | ".join(c["score"] for c in cells) + f" | {verdict} |")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", required=True, help="before or after")
    parser.add_argument("--trial", type=int, choices=(1, 2, 3))
    parser.add_argument("--table", action="store_true", help="print the run-log table and stop")
    parser.add_argument("--overwrite", action="store_true", help="replace this trial's saved result")
    args = parser.parse_args()

    if args.table:
        print_table(args.label)
        return
    if args.trial is None:
        sys.exit("Say which trial this is: --trial 1, 2 or 3")

    md_path, _ = paths(args.label, args.trial)
    if md_path.exists() and not args.overwrite:
        sys.exit(f"{md_path.name} already exists. A trial's result isn't replaced "
                 f"by accident; add --overwrite if you mean to.")

    try:
        import requests
        health = requests.get(f"{URL}/health", timeout=10)
    except Exception:  # noqa: BLE001
        sys.exit(f"Nothing answering at {URL}. Start the service first (see RUNNING.md).")
    if health.json().get("detector_loaded"):
        sys.exit("The model is already in memory, so this isn't a fresh start and "
                 "criterion 3 can't be measured. Stop the service, start it again, re-run.")
    server = health.headers.get("Server", "unknown")

    tag = f"{args.label}{args.trial}_{dt.datetime.now().strftime('%H%M%S')}"
    results = {}
    results["3"] = check_cold_start(requests, tag)
    results["1"] = check_log_completeness(requests, tag)
    results["4"] = check_appeals(tag)
    results["5"] = check_bad_input(tag)
    results["2"] = check_crash(requests, tag)

    md_path = write_report(args.label, args.trial, server, results)
    print(f"{args.label}, trial {args.trial}")
    for number, name, target in CRITERIA:
        r = results[number]
        print(f"  {number}. {name:<62} target {target:<24} {r['score']:<44} {'passed' if r['passed'] else 'FAILED'}")
    print(f"\nSaved {md_path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
