# Extra checks — after

- Produced by: `run_extra_checks.py::main` (`appeal_trial` for criterion 4, `bad_input_trial` for criterion 5)
- Service: `app.py::submit`, `app.py::appeal`, `GET /log`, `POST /ping`
- 3 trials · 2026-11-11 20:21

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
    "content_id": "c_182de27de5d9",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_182de27de5d9",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_182de27de5d9",
      "creator_id": "x_appeal_t1_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:07+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_t1_2",
    "submit_status": 200,
    "content_id": "c_41f896044034",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_41f896044034",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_41f896044034",
      "creator_id": "x_appeal_t1_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:07+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_t1_3",
    "submit_status": 200,
    "content_id": "c_615c5ea4a03d",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_615c5ea4a03d",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_615c5ea4a03d",
      "creator_id": "x_appeal_t1_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_t1_4",
    "submit_status": 200,
    "content_id": "c_70a092de7d78",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_70a092de7d78",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_70a092de7d78",
      "creator_id": "x_appeal_t1_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_t1_5",
    "submit_status": 200,
    "content_id": "c_e1b73ff0e3a3",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_e1b73ff0e3a3",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_e1b73ff0e3a3",
      "creator_id": "x_appeal_t1_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 1, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
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
    "content_id": "c_2b5928021f7e",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_2b5928021f7e",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_2b5928021f7e",
      "creator_id": "x_appeal_t2_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_t2_2",
    "submit_status": 200,
    "content_id": "c_7e7ab0f7942b",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_7e7ab0f7942b",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_7e7ab0f7942b",
      "creator_id": "x_appeal_t2_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_t2_3",
    "submit_status": 200,
    "content_id": "c_9277cb7906f0",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_9277cb7906f0",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_9277cb7906f0",
      "creator_id": "x_appeal_t2_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_t2_4",
    "submit_status": 200,
    "content_id": "c_09770b35dfec",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_09770b35dfec",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_09770b35dfec",
      "creator_id": "x_appeal_t2_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_t2_5",
    "submit_status": 200,
    "content_id": "c_f1b4f5ced5f4",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_f1b4f5ced5f4",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_f1b4f5ced5f4",
      "creator_id": "x_appeal_t2_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 2, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
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
    "content_id": "c_7d925c073d0c",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_7d925c073d0c",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_7d925c073d0c",
      "creator_id": "x_appeal_t3_1",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 1)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 2,
    "creator_id": "x_appeal_t3_2",
    "submit_status": 200,
    "content_id": "c_453533499fc1",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_453533499fc1",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_453533499fc1",
      "creator_id": "x_appeal_t3_2",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 2)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 3,
    "creator_id": "x_appeal_t3_3",
    "submit_status": 200,
    "content_id": "c_697ba6e12874",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_697ba6e12874",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_697ba6e12874",
      "creator_id": "x_appeal_t3_3",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 3)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 4,
    "creator_id": "x_appeal_t3_4",
    "submit_status": 200,
    "content_id": "c_7f526afd843b",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_7f526afd843b",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_7f526afd843b",
      "creator_id": "x_appeal_t3_4",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 4)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
    },
    "decided_entry_unchanged": true,
    "passed": true
  },
  {
    "appeal": 5,
    "creator_id": "x_appeal_t3_5",
    "submit_status": 200,
    "content_id": "c_dff9c31fa5b1",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "c_dff9c31fa5b1",
      "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
      "status": "under_review"
    },
    "appeal_log_entry": {
      "content_id": "c_dff9c31fa5b1",
      "creator_id": "x_appeal_t3_5",
      "event": "appeal",
      "reasoning": "I wrote this myself. (criterion 4, trial 3, appeal 5)",
      "status": "under_review",
      "timestamp": "2026-11-12T01:21:08+00:00"
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
