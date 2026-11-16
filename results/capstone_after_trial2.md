# Capstone run: after, trial 2

- Produced by: `run_capstone.py::main`
- Service: http://127.0.0.1:5000, `Server` header: `gunicorn`, restarted for this trial (`GET /health` said `detector_loaded: false` before the first request)
- 2026-11-16 15:31

| Criterion | Target | This trial | Passed |
|---|---|---|---|
| 1. Every request leaves exactly one complete log record | 20 of 20 | 20/20 | yes |
| 2. A crash still writes a record and returns JSON | 3 of 3 | 3/3 (record 3/3, JSON response 3/3) | yes |
| 3. Cold start is bounded and the log reports it correctly | 3 of 3 checks | 3/3 (first 1682.1 ms, second 30.3 ms) | yes |
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
{"timestamp": "2026-11-16T20:31:54.453+00:00", "method": "GET", "route": "/health", "input": {}, "status": 200, "outcome": "ok", "output": {"ok": true}, "duration_ms": 1.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.454+00:00", "method": "POST", "route": "/ping", "input": {"message": "capstone"}, "status": 200, "outcome": "ok", "output": {"ok": true}, "duration_ms": 0.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.456+00:00", "method": "GET", "route": "/log", "input": {"limit": "1"}, "status": 200, "outcome": "ok", "output": {"count": 1}, "duration_ms": 0.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.492+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 832, "text_preview": "The images were available in three formats: PNG, JPG, and JPEG, and exhibited a ", "creator_id": "cap_after2_153152_c1_own1"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_f99b5c47ffb3", "guess": "unsure", "confidence": 0.5494, "model_score": 0.7945, "style_score": 0.3052, "status": "decided"}, "duration_ms": 34.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.538+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1087, "text_preview": "Data augmentation was employed to improve the robustness and generalization capa", "creator_id": "cap_after2_153152_c1_own2"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_74754cc41a16", "guess": "unsure", "confidence": 0.5449, "model_score": 0.7507, "style_score": 0.3483, "status": "decided"}, "duration_ms": 45.3, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.584+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1060, "text_preview": "Several Convolutional Neural Networks (CNNs) were evaluated for the classificati", "creator_id": "cap_after2_153152_c1_own3"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_9f9e07cb32bf", "guess": "unsure", "confidence": 0.5043, "model_score": 0.6363, "style_score": 0.3063, "status": "decided"}, "duration_ms": 44.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.617+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_0cb7e9019c6f", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 31.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.650+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_d79221a5d51f", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 31.5, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.683+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_7eeddfcd3cce", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 31.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.716+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_003b2b9703cf", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 32.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.750+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_9c1ba0b786b2", "guess": "unsure", "confidence": 0.5431, "model_score": 0.4853, "style_score": 0.6297, "status": "decided"}, "duration_ms": 32.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.751+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 429, "outcome": "rejected", "output": {"error": "rate_limited", "message": "Too many submissions. Try again shortly.", "limit": "5 per 1 minute"}, "duration_ms": 0.3, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.752+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 691, "text_preview": "A custom dataset was created, as previously mentioned, to generate pairs of augm", "creator_id": "cap_after2_153152_c1_same"}, "status": 429, "outcome": "rejected", "output": {"error": "rate_limited", "message": "Too many submissions. Try again shortly.", "limit": "5 per 1 minute"}, "duration_ms": 0.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.753+00:00", "method": "POST", "route": "/submit", "input": {"creator_id": "cap_after2_153152_c1_notext1"}, "status": 400, "outcome": "rejected", "output": {"error": "bad_request", "message": "Send JSON with a non-empty \"text\" field."}, "duration_ms": 0.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.754+00:00", "method": "POST", "route": "/submit", "input": {"creator_id": "cap_after2_153152_c1_notext2"}, "status": 400, "outcome": "rejected", "output": {"error": "bad_request", "message": "Send JSON with a non-empty \"text\" field."}, "duration_ms": 0.1, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.755+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 2, "text_preview": "hi", "creator_id": "cap_after2_153152_c1_hi1"}, "status": 422, "outcome": "rejected", "output": {"error": "text_too_short", "message": "This is too short to judge. Please submit at least a few sentences."}, "duration_ms": 0.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.756+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 2, "text_preview": "hi", "creator_id": "cap_after2_153152_c1_hi2"}, "status": 422, "outcome": "rejected", "output": {"error": "text_too_short", "message": "This is too short to judge. Please submit at least a few sentences."}, "duration_ms": 0.2, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.757+00:00", "method": "POST", "route": "/appeal", "input": {"content_id": "c_9f9e07cb32bf", "reasoning_length": 20, "reasoning_preview": "I wrote this myself."}, "status": 200, "outcome": "ok", "output": {"content_id": "c_9f9e07cb32bf", "status": "under_review", "message": "Thanks, we've received your appeal. A person will review this decision, and the ..."}, "duration_ms": 1.0, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.759+00:00", "method": "POST", "route": "/appeal", "input": {"content_id": "c_unknown_after2_153152_1", "reasoning_length": 20, "reasoning_preview": "I wrote this myself."}, "status": 404, "outcome": "rejected", "output": {"error": "not_found", "message": "We couldn't find a submission with id c_unknown_after2_153152_1."}, "duration_ms": 0.9, "detector_loaded_at_start": true}
{"timestamp": "2026-11-16T20:31:54.761+00:00", "method": "POST", "route": "/appeal", "input": {"content_id": "c_unknown_after2_153152_2", "reasoning_length": 20, "reasoning_preview": "I wrote this myself."}, "status": 404, "outcome": "rejected", "output": {"error": "not_found", "message": "We couldn't find a submission with id c_unknown_after2_153152_2."}, "duration_ms": 0.9, "detector_loaded_at_start": true}
```

### 2. A crash still writes a record and returns JSON

`run_capstone.py::check_crash`, with `logs/audit.jsonl` read-only.

**Crash 1** (record ok: True, JSON response ok: True)

What the client got:

```
HTTP 500
Content-Type: application/json

{"error":"internal_error","message":"Something went wrong on our side and the request was not completed. Please try again."}

```

What the log got:

```json
{"timestamp": "2026-11-16T20:31:54.998+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1072, "text_preview": "The western part of the United States, like other countries located along the Pa", "creator_id": "cap_after2_153152_c2_1"}, "status": 500, "outcome": "error", "output": {"error": "internal_error", "message": "Something went wrong on our side and the request was not completed. Please try a..."}, "duration_ms": 39.8, "detector_loaded_at_start": true, "exception": "PermissionError: [Errno 13] Permission denied: '/Users/carcon/projects/ai201-project4-provenance-guard-starter-v2026/logs/audit.jsonl'"}
```

**Crash 2** (record ok: True, JSON response ok: True)

What the client got:

```
HTTP 500
Content-Type: application/json

{"error":"internal_error","message":"Something went wrong on our side and the request was not completed. Please try again."}

```

What the log got:

```json
{"timestamp": "2026-11-16T20:31:55.030+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 693, "text_preview": "Previous work has been conducted using supervised learning, achieving 64% accura", "creator_id": "cap_after2_153152_c2_2"}, "status": 500, "outcome": "error", "output": {"error": "internal_error", "message": "Something went wrong on our side and the request was not completed. Please try a..."}, "duration_ms": 30.4, "detector_loaded_at_start": true, "exception": "PermissionError: [Errno 13] Permission denied: '/Users/carcon/projects/ai201-project4-provenance-guard-starter-v2026/logs/audit.jsonl'"}
```

**Crash 3** (record ok: True, JSON response ok: True)

What the client got:

```
HTTP 500
Content-Type: application/json

{"error":"internal_error","message":"Something went wrong on our side and the request was not completed. Please try again."}

```

What the log got:

```json
{"timestamp": "2026-11-16T20:31:55.067+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 832, "text_preview": "The images were available in three formats: PNG, JPG, and JPEG, and exhibited a ", "creator_id": "cap_after2_153152_c2_3"}, "status": 500, "outcome": "error", "output": {"error": "internal_error", "message": "Something went wrong on our side and the request was not completed. Please try a..."}, "duration_ms": 35.3, "detector_loaded_at_start": true, "exception": "PermissionError: [Errno 13] Permission denied: '/Users/carcon/projects/ai201-project4-provenance-guard-starter-v2026/logs/audit.jsonl'"}
```

### 3. Cold start is bounded and the log reports it correctly

`run_capstone.py::check_cold_start`. The first two `/submit` after the restart:

```json
{"timestamp": "2026-11-16T20:31:54.419+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 1072, "text_preview": "The western part of the United States, like other countries located along the Pa", "creator_id": "cap_after2_153152_c3_1"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_16384bf10c40", "guess": "unsure", "confidence": 0.6909, "model_score": 0.7426, "style_score": 0.6134, "status": "decided"}, "duration_ms": 1682.1, "detector_loaded_at_start": false}
{"timestamp": "2026-11-16T20:31:54.451+00:00", "method": "POST", "route": "/submit", "input": {"text_length": 693, "text_preview": "Previous work has been conducted using supervised learning, achieving 64% accura", "creator_id": "cap_after2_153152_c3_2"}, "status": 200, "outcome": "ok", "output": {"content_id": "c_4b6ed40837a4", "guess": "unsure", "confidence": 0.6754, "model_score": 0.6478, "style_score": 0.7168, "status": "decided"}, "duration_ms": 30.3, "detector_loaded_at_start": true}
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
    "creator_id": "x_appeal_tafter2_153152_1",
    "submit_status": 200,
    "content_id": "c_673be0ce4069",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_673be0ce4069",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_673be0ce4069",
      "creator_id": "x_appeal_tafter2_153152_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial after2_153152, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-16T20:31:54+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_tafter2_153152_2",
    "submit_status": 200,
    "content_id": "c_de053ba9c7fb",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_de053ba9c7fb",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_de053ba9c7fb",
      "creator_id": "x_appeal_tafter2_153152_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial after2_153152, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-16T20:31:54+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_tafter2_153152_3",
    "submit_status": 200,
    "content_id": "c_c92cb5b8cf23",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_c92cb5b8cf23",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_c92cb5b8cf23",
      "creator_id": "x_appeal_tafter2_153152_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial after2_153152, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-16T20:31:54+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_tafter2_153152_4",
    "submit_status": 200,
    "content_id": "c_ae8e63def2ec",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_ae8e63def2ec",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_ae8e63def2ec",
      "creator_id": "x_appeal_tafter2_153152_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial after2_153152, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-16T20:31:54+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_tafter2_153152_5",
    "submit_status": 200,
    "content_id": "c_e09e8ee53d7d",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_e09e8ee53d7d",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_e09e8ee53d7d",
      "creator_id": "x_appeal_tafter2_153152_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial after2_153152, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-16T20:31:54+00:00"
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
      "creator_id": "x_bad_missing_tafter2_153152"
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
      "creator_id": "x_bad_empty_tafter2_153152"
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
      "creator_id": "x_bad_space_tafter2_153152"
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
      "creator_id": "x_bad_null_tafter2_153152"
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
