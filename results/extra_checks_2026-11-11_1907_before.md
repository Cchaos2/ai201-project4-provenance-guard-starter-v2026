# Extra checks — before

- Produced by: `run_extra_checks.py::main` (`appeal_trial` for criterion 4, `bad_input_trial` for criterion 5)
- Service: `app.py::submit`, `app.py::appeal`, `GET /log`, `POST /ping`
- 3 trials · 2026-11-11 19:07

| Criterion | Target | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| 4. A valid appeal changes status and is recorded | 5 of 5 | 5/5 | 5/5 | 5/5 |
| 5. Bad input gets a 400 with error + message; /ping still 200 | 4 of 4, /ping 200 | 4/4, /ping 200 | 4/4, /ping 200 | 4/4, /ping 200 |

---

## What actually came back

### Trial 1

**Criterion 4: appeals**

```json
[
  {
    "appeal": 1,
    "creator_id": "x_appeal_t1_1",
    "submit_status": 200,
    "content_id": "c_e6bfd9ee51cc",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_e6bfd9ee51cc",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_e6bfd9ee51cc",
      "creator_id": "x_appeal_t1_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:44+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_t1_2",
    "submit_status": 200,
    "content_id": "c_ed5206805d5e",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_ed5206805d5e",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_ed5206805d5e",
      "creator_id": "x_appeal_t1_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:44+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_t1_3",
    "submit_status": 200,
    "content_id": "c_78f5c12be7d8",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_78f5c12be7d8",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_78f5c12be7d8",
      "creator_id": "x_appeal_t1_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_t1_4",
    "submit_status": 200,
    "content_id": "c_1f09f7e45a0a",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_1f09f7e45a0a",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_1f09f7e45a0a",
      "creator_id": "x_appeal_t1_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_t1_5",
    "submit_status": 200,
    "content_id": "c_94f332248c2b",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_94f332248c2b",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_94f332248c2b",
      "creator_id": "x_appeal_t1_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  }
]
```

**Criterion 5: bad input**

```json
{
  "requests": [
    {
      "case": "text missing",
      "sent": {
        "creator_id": "x_bad_missing_t1"
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
        "creator_id": "x_bad_empty_t1"
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
        "creator_id": "x_bad_space_t1"
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
        "creator_id": "x_bad_null_t1"
      },
      "status": 400,
      "response": {
        "error": "bad_request",
        "message": "Send JSON with a non-empty \"text\" field."
      },
      "passed": true
    }
  ],
  "ping_status_after": 200
}
```

### Trial 2

**Criterion 4: appeals**

```json
[
  {
    "appeal": 1,
    "creator_id": "x_appeal_t2_1",
    "submit_status": 200,
    "content_id": "c_f22c32b17cd1",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_f22c32b17cd1",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_f22c32b17cd1",
      "creator_id": "x_appeal_t2_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_t2_2",
    "submit_status": 200,
    "content_id": "c_0a13e4aee45c",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_0a13e4aee45c",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_0a13e4aee45c",
      "creator_id": "x_appeal_t2_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_t2_3",
    "submit_status": 200,
    "content_id": "c_8a3125344bbf",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_8a3125344bbf",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_8a3125344bbf",
      "creator_id": "x_appeal_t2_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_t2_4",
    "submit_status": 200,
    "content_id": "c_a90a6c84f4be",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_a90a6c84f4be",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_a90a6c84f4be",
      "creator_id": "x_appeal_t2_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_t2_5",
    "submit_status": 200,
    "content_id": "c_d6ac6aafa7bf",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_d6ac6aafa7bf",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_d6ac6aafa7bf",
      "creator_id": "x_appeal_t2_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  }
]
```

**Criterion 5: bad input**

```json
{
  "requests": [
    {
      "case": "text missing",
      "sent": {
        "creator_id": "x_bad_missing_t2"
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
        "creator_id": "x_bad_empty_t2"
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
        "creator_id": "x_bad_space_t2"
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
        "creator_id": "x_bad_null_t2"
      },
      "status": 400,
      "response": {
        "error": "bad_request",
        "message": "Send JSON with a non-empty \"text\" field."
      },
      "passed": true
    }
  ],
  "ping_status_after": 200
}
```

### Trial 3

**Criterion 4: appeals**

```json
[
  {
    "appeal": 1,
    "creator_id": "x_appeal_t3_1",
    "submit_status": 200,
    "content_id": "c_11c25f09da6e",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_11c25f09da6e",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_11c25f09da6e",
      "creator_id": "x_appeal_t3_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_t3_2",
    "submit_status": 200,
    "content_id": "c_748330a470c5",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_748330a470c5",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_748330a470c5",
      "creator_id": "x_appeal_t3_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_t3_3",
    "submit_status": 200,
    "content_id": "c_0d3d472acabe",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_0d3d472acabe",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_0d3d472acabe",
      "creator_id": "x_appeal_t3_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_t3_4",
    "submit_status": 200,
    "content_id": "c_05406b7048d4",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_05406b7048d4",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_05406b7048d4",
      "creator_id": "x_appeal_t3_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_t3_5",
    "submit_status": 200,
    "content_id": "c_53299dcf5bdd",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_53299dcf5bdd",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_53299dcf5bdd",
      "creator_id": "x_appeal_t3_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-12T00:07:45+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  }
]
```

**Criterion 5: bad input**

```json
{
  "requests": [
    {
      "case": "text missing",
      "sent": {
        "creator_id": "x_bad_missing_t3"
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
        "creator_id": "x_bad_empty_t3"
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
        "creator_id": "x_bad_space_t3"
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
        "creator_id": "x_bad_null_t3"
      },
      "status": 400,
      "response": {
        "error": "bad_request",
        "message": "Send JSON with a non-empty \"text\" field."
      },
      "passed": true
    }
  ],
  "ping_status_after": 200
}
```
