# Capstone run: before, trial 2

- Produced by: `run_capstone.py::main`
- Service: http://127.0.0.1:5000, `Server` header: `gunicorn`, restarted for this trial (`GET /health` said `detector_loaded: false` before the first request)
- 2026-11-16 14:15

| Criterion | Target | This trial | Passed |
|---|---|---|---|
| 1. Every request leaves exactly one complete log record | 20 of 20 | 20/20 | yes |
| 2. A crash still writes a record and returns JSON | 3 of 3 | 0/3 (record 3/3, JSON response 0/3) | NO |
| 3. Cold start is bounded and the log reports it correctly | 3 of 3 checks | 3/3 (first 1686.2 ms, second 31.1 ms) | yes |
| 4. A valid appeal always changes status and is always recorded | 5 of 5 | 5/5 | yes |
| 5. Bad input gets a clear error, never a crash | 4 of 4, then /ping 200 | 4/4, /ping 200 | yes |

---

## What actually came back

### 1. Every request leaves exactly one complete log record

`run_capstone.py::check_log_completeness`. Requests sent: 20. `logs/requests.jsonl` grew by: 20. Lines that parse and have all eight fields: 20.

The status the client got for each request, in order:

```
GET /health -> 200
POST /ping -> 200
GET /log?limit=1 -> 200
POST /submit valid, own creator_id -> 200
POST /submit valid, own creator_id -> 200
POST /submit valid, own creator_id -> 200
POST /submit valid, same creator_id -> 200
POST /submit valid, same creator_id -> 200
POST /submit valid, same creator_id -> 200
POST /submit valid, same creator_id -> 200
POST /submit valid, same creator_id -> 200
POST /submit valid, same creator_id -> 429
POST /submit valid, same creator_id -> 429
POST /submit with no text -> 400
POST /submit with no text -> 400
POST /submit with "hi" -> 422
POST /submit with "hi" -> 422
POST /appeal valid -> 200
POST /appeal with an unknown id -> 404
POST /appeal with an unknown id -> 404
```

The lines the log gained while those were sent:

```json
{"timestamp": "2026-11-16T19:15:47.472+00:00", "method": "GET", "route": "/health", "input": {}, "status": 200, "outcome": "ok", "output": {"ok": true}, "duration_ms": 0.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.473+00:00", "method": "POST", "route": "/ping", "input": {"message": "capstone"}, "status": 200, "outcome": "ok", "output": {"ok": true}, "duration_ms": 0.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.475+00:00", "method": "GET", "route": "/log", "input": {"limit": "1"}, "status": 200, "outcome": "ok", "output": {"count": 1}, "duration_ms": 0.8, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.510+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 832, "text_preview": "The images were available in three formats: PNG, JPG, and JPEG, and exhibited a ", "creator_id": "cap_before2_141545_c1_own1"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_cbb15f700686", "guess": "unsure", "confidence": 0.5494, "model_score": 0.7945, "style_score": 0.3052, "status": "decided"}, "duration_ms": 34.4, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.558+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1087, "text_preview": "Data augmentation was employed to improve the robustness and generalization capa", "creator_id": "cap_before2_141545_c1_own2"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_56d9316a354e", "guess": "unsure", "confidence": 0.5449, "model_score": 0.7507, "style_score": 0.3483, "status": "decided"}, "duration_ms": 46.0, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.606+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1060, "text_preview": "Several Convolutional Neural Networks (CNNs) were evaluated for the classificati", "creator_id": "cap_before2_141545_c1_own3"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_90eda8f90768", "guess": "unsure", "confidence": 0.5043, "model_score": 0.6363, "style_score": 0.3063, "status": "decided"}, "duration_ms": 45.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.641+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_ded3a519f652", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 32.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.675+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_63968bc3119b", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 31.7, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.709+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_afb7f71393cf", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 32.0, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.742+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_a0f5a047a3d0", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 32.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.777+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_e032c246c60e", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 32.4, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.779+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 429, "outcome": "rejected", "output": {"error": "rate_limited", "message": "Too many submissions. Try again shortly.", "limit": "5 per 1 minute"}, "duration_ms": 0.3, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.781+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_before2_141545_c1_same"}, "status": 429, "outcome": "rejected", "output": {"error": "rate_limited", "message": "Too many submissions. Try again shortly.", "limit": "5 per 1 minute"}, "duration_ms": 0.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.782+00:00", "method": "POST", "route": "/submit", "input": {"creator_id": "cap_before2_141545_c1_notext1"}, "status": 400, "outcome": "rejected", "output": {"error": "bad_request", "message": "Send JSON with a non-empty \"text\" field."}, "duration_ms": 0.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.783+00:00", "method": "POST", "route": "/submit", "input": {"creator_id": "cap_before2_141545_c1_notext2"}, "status": 400, "outcome": "rejected", "output": {"error": "bad_request", "message": "Send JSON with a non-empty \"text\" field."}, "duration_ms": 0.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.784+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 2, "text_preview": "hi", "creator_id": "cap_before2_141545_c1_hi1"}, "status": 422, "outcome": "rejected", "output": {"error": "text_too_short", "message": "This is too short to judge. Please submit at least a few sentences."}, "duration_ms": 0.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.786+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 2, "text_preview": "hi", "creator_id": "cap_before2_141545_c1_hi2"}, "status": 422, "outcome": "rejected", "output": {"error": "text_too_short", "message": "This is too short to judge. Please submit at least a few sentences."}, "duration_ms": 0.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.788+00:00", "method": "POST", "route": "/appeal", "input": {"content_id": "c_90eda8f90768", "reasoning_length": 20, "reasoning_preview": "I wrote this myself."}, "status": 200, "outcome": "ok", "output": {"content_id": "c_90eda8f90768", "status": "under_review", "message": "Thanks, we've received your appeal. A person will review this decision, and the ..."}, "duration_ms": 1.0, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.790+00:00", "method": "POST", "route": "/appeal", "input": {"content_id": "c_unknown_before2_141545_1", "reasoning_length": 20, "reasoning_preview": "I wrote this myself."}, "status": 404, "outcome": "rejected", "output": {"error": "not_found", "message": "We couldn't find a submission with id c_unknown_before2_141545_1."}, "duration_ms": 0.8, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T19:15:47.791+00:00", "method": "POST", "route": "/appeal", "input": {"content_id": "c_unknown_before2_141545_2", "reasoning_length": 20, "reasoning_preview": "I wrote this myself."}, "status": 404, "outcome": "rejected", "output": {"error": "not_found", "message": "We couldn't find a submission with id c_unknown_before2_141545_2."}, "duration_ms": 0.8, "detector_loaded_at_start": true}
```

### 2. A crash still writes a record and returns JSON

`run_capstone.py::check_crash`, with `logs/audit.jsonl` read-only.

**Crash 1** (record ok: True, JSON response ok: False)

What the client got:

```
HTTP 500
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

```

What the log got:

```json
{"timestamp": "2026-11-16T19:15:48.043+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1072, "text_preview": "The western part of the United States, like other countries located along the Pa", "creator_id": "cap_before2_141545_c2_1"}, "status": 500, "outcome": "error", "output": {"body": "not_json"}, "duration_ms": 40.3, "detector_loaded_at_start": true, "exception": "PermissionError: [Errno 13] Permission denied: '/Users/carcon/projects/ai201-project4-provenance-guard-starter-v2026/logs/audit.jsonl'"}
```

**Crash 2** (record ok: True, JSON response ok: False)

What the client got:

```
HTTP 500
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

```

What the log got:

```json
{"timestamp": "2026-11-16T19:15:48.075+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 693, "text_preview": "Previous work has been conducted using supervised learning, achieving 64% accura", "creator_id": "cap_before2_141545_c2_2"}, "status": 500, "outcome": "error", "output": {"body": "not_json"}, "duration_ms": 30.4, "detector_loaded_at_start": true, "exception": "PermissionError: [Errno 13] Permission denied: '/Users/carcon/projects/ai201-project4-provenance-guard-starter-v2026/logs/audit.jsonl'"}
```

**Crash 3** (record ok: True, JSON response ok: False)

What the client got:

```
HTTP 500
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

```

What the log got:

```json
{"timestamp": "2026-11-16T19:15:48.113+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 832, "text_preview": "The images were available in three formats: PNG, JPG, and JPEG, and exhibited a ", "creator_id": "cap_before2_141545_c2_3"}, "status": 500, "outcome": "error", "output": {"body": "not_json"}, "duration_ms": 35.8, "detector_loaded_at_start": true, "exception": "PermissionError: [Errno 13] Permission denied: '/Users/carcon/projects/ai201-project4-provenance-guard-starter-v2026/logs/audit.jsonl'"}
```

### 3. Cold start is bounded and the log reports it correctly

`run_capstone.py::check_cold_start`. The first two `/submit` after the restart:

```json
{"timestamp": "2026-11-16T19:15:47.435+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1072, "text_preview": "The western part of the United States, like other countries located along the Pa", "creator_id": "cap_before2_141545_c3_1"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_0e5f89c8109e", "guess": "unsure", "confidence": 0.6909, "model_score": 0.7426, "style_score": 0.6134, "status": "decided"}, "duration_ms": 1686.2, "detector_loaded_at_start": false}
{"timestamp": "2026-11-16T19:15:47.468+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 693, "text_preview": "Previous work has been conducted using supervised learning, achieving 64% accura", "creator_id": "cap_before2_141545_c3_2"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_280b93077d88", "guess": "unsure", "confidence": 0.6754, "model_score": 0.6478, "style_score": 0.7168, "status": "decided"}, "duration_ms": 31.1, "detector_loaded_at_start": true}
```

```
held    1. first /submit takes at most 10,000 ms
held    2. first record has detector_loaded_at_start: false
held    3. second record has detector_loaded_at_start: true and takes at most 100 ms
```

### 4. A valid appeal always changes status and is always recorded

`run_extra_checks.py::appeal_trial`, called by `run_capstone.py::check_appeals`.

```json
[
  {
    "appeal": 1,
    "creator_id": "x_appeal_tbefore2_141545_1",
    "submit_status": 200,
    "content_id": "c_bf17f5fc417e",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_bf17f5fc417e",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_bf17f5fc417e",
      "creator_id": "x_appeal_tbefore2_141545_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial before2_141545, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-16T19:15:47+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_tbefore2_141545_2",
    "submit_status": 200,
    "content_id": "c_d8dccd2f9f2f",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_d8dccd2f9f2f",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_d8dccd2f9f2f",
      "creator_id": "x_appeal_tbefore2_141545_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial before2_141545, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-16T19:15:47+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_tbefore2_141545_3",
    "submit_status": 200,
    "content_id": "c_a643510e1ec5",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_a643510e1ec5",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_a643510e1ec5",
      "creator_id": "x_appeal_tbefore2_141545_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial before2_141545, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-16T19:15:47+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_tbefore2_141545_4",
    "submit_status": 200,
    "content_id": "c_279faf7ec846",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_279faf7ec846",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_279faf7ec846",
      "creator_id": "x_appeal_tbefore2_141545_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial before2_141545, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-16T19:15:47+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_tbefore2_141545_5",
    "submit_status": 200,
    "content_id": "c_4d1d610de508",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_4d1d610de508",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_4d1d610de508",
      "creator_id": "x_appeal_tbefore2_141545_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial before2_141545, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-16T19:15:47+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  }
]
```

### 5. Bad input gets a clear error, never a crash

`run_extra_checks.py::bad_input_trial`, called by `run_capstone.py::check_bad_input`. `POST /ping` afterwards: 200.

```json
[
  {
    "case": "text missing",
    "sent": {
      "creator_id": "x_bad_missing_tbefore2_141545"
    },
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\" field."
    },
    "passed": true
  },
  {
    "case": "text empty",
    "sent": {
      "text": "",
      "creator_id": "x_bad_empty_tbefore2_141545"
    },
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\" field."
    },
    "passed": true
  },
  {
    "case": "text whitespace",
    "sent": {
      "text": "   \n\t  ",
      "creator_id": "x_bad_space_tbefore2_141545"
    },
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\" field."
    },
    "passed": true
  },
  {
    "case": "text null",
    "sent": {
      "text": null,
      "creator_id": "x_bad_null_tbefore2_141545"
    },
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\" field."
    },
    "passed": true
  }
]
```
