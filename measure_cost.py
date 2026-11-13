#!/usr/bin/env python3
"""
What does one run cost?  <- UNIT 9 (capstone)

    gunicorn app:app --bind 127.0.0.1:5000 --workers 1 --timeout 120    # terminal 1
    python measure_cost.py                                              # terminal 2

Nothing in this service calls a paid API, so the cost of one run is compute
time on the machine the service runs on.

This sends ten real submissions (the ten pieces of my own writing in
scenarios.py), each under its own creator_id so the rate limiter doesn't
answer instead of the route. Then it reads each one's `duration_ms` back from
logs/requests.jsonl. The number is the service's own measurement of the time
from the request arriving to the response being ready, not a stopwatch on
this side, so it leaves out network time.
"""

import datetime as dt
import sys

import config
import request_log
from scenarios import MY_WRITING

URL = f"http://{config.HOST}:{config.PORT}"
RUNS = 10


def main():
    try:
        import requests
    except ImportError:
        sys.exit("requests isn't installed. Run: pip install -r requirements.txt")

    stamp = dt.datetime.now().strftime("%H%M%S")
    texts = MY_WRITING[:RUNS]
    creator_ids = [f"cost_{stamp}_{i}" for i in range(1, len(texts) + 1)]

    for creator_id, text in zip(creator_ids, texts):
        try:
            response = requests.post(
                f"{URL}/submit",
                json={"text": text, "creator_id": creator_id},
                timeout=120,
            )
        except requests.exceptions.ConnectionError:
            sys.exit(f"Nothing is answering at {URL}. Start the service first.")
        if response.status_code != 200:
            sys.exit(f"{creator_id} got {response.status_code}, not 200: {response.text[:200]}")

    # Read the service's own record of each of those ten requests.
    by_creator = {
        entry.get("input", {}).get("creator_id"): entry
        for entry in request_log.read()
        if entry.get("route") == "/submit"
    }
    rows = []
    for creator_id, text in zip(creator_ids, texts):
        entry = by_creator.get(creator_id)
        if entry is None:
            sys.exit(f"No request-log record for {creator_id}. Is the service "
                     f"writing to {config.REQUEST_LOG}?")
        rows.append((creator_id, len(text.split()), entry["status"],
                     entry["duration_ms"], entry["detector_loaded_at_start"]))

    print(f"Cost of one run: {len(rows)} submissions to {URL}/submit")
    print(f"Read back from {config.REQUEST_LOG.relative_to(config.ROOT)}\n")
    print(f"{'creator_id':<18} {'words':>5} {'status':>6} {'duration_ms':>11}  model in memory at start")
    for creator_id, words, status, duration, loaded in rows:
        print(f"{creator_id:<18} {words:>5} {status:>6} {duration:>11.1f}  {loaded}")

    durations = [row[3] for row in rows]
    mean = round(sum(durations) / len(durations), 1)   # rounded first, so the arithmetic below adds up
    print(f"\nmean   {mean:.1f} ms   (min {min(durations):.1f}, max {max(durations):.1f})")

    cold = [row[3] for row in rows if not row[4]]
    if cold:
        warm = [row[3] for row in rows if row[4]]
        print(f"note   {len(cold)} of these loaded the model first (cold). "
              f"Mean of the {len(warm)} warm ones: {sum(warm) / len(warm):.1f} ms")

    per_day = 100 * mean / 1000
    print(f"\n100 runs a day x {mean:.1f} ms = {100 * mean:.0f} ms = {per_day:.2f} s of compute per day")


if __name__ == "__main__":
    main()
