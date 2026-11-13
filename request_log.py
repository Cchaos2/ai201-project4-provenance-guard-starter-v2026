"""
The request log. <- UNIT 9 (capstone)

One JSON object per line in logs/requests.jsonl: one line per HTTP request,
whatever the route and whatever the outcome.

It is separate from the audit log on purpose. `audit.jsonl` records
*decisions*: what the service concluded about a piece of writing. This file
records *requests*: what arrived, what went back, and how long it took,
including the requests that never became a decision.

    import request_log

    request_log.write({"route": "/submit", "status": 200, "duration_ms": 812.4})
    request_log.read(limit=10)
"""

import json
import threading
from datetime import datetime, timezone

import config

_lock = threading.Lock()


def write(record: dict) -> dict:
    """Append one record. The timestamp is when the response was ready."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        **record,
    }
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)
    with _lock:
        with config.REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    return entry


def read(limit: int | None = None) -> list[dict]:
    """Read the log back, oldest first. `limit` keeps the most recent N."""
    if not config.REQUEST_LOG.exists():
        return []
    entries = []
    for line in config.REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # one bad row shouldn't make the whole log unreadable
    return entries[-limit:] if limit else entries


if __name__ == "__main__":
    # python request_log.py        -> print the last ten records
    for entry in read(limit=10):
        print(json.dumps(entry, ensure_ascii=False))
