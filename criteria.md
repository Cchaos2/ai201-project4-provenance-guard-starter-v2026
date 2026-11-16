# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is rarely called AI

<!-- Your criterion. It must name a number. -->
Of 10 pieces of writing I wrote myself (each at least 100 words, sent to
`POST /submit`), at most 1 comes back with `guess: "ai"` (the high-confidence
AI label), in each of 3 trials.


**Why this target:**
On a writing site, wrongly accusing a real writer costs
far more than letting some AI text through, so I accept missed detections to
keep false accusations rare. This is a real risk, not a theoretical one:
signal one already scored a plain paragraph I wrote in a second-language
style at 0.582, leaning AI just because the words were common. One in ten is
the most I would accept if it were my own work being judged.



---

## 2. Clearly-AI and clearly-human text score far apart

<!-- Your criterion. -->
Across 5 clearly AI-generated texts (produced by a chatbot from a one-line
prompt, not edited) and 5 clearly human texts (my own writing, or writing
published before 2022), the average `confidence` of the AI set is at least
0.30 higher than the average of the human set, in each of 3 trials.


**Why this target:**
If the two groups score close together, the confidence
number carries no real information and every label is basically a guess.
A gap of 0.30 is the width of the starter's unsure band (0.35 to 0.65), so
anything smaller means typical AI and human texts could land on the same side
of my thresholds.


---

## 3. Every label is reachable

<!-- Your criterion. -->
For each of the three labels (`human`, `unsure`, `ai`), I can submit at least
2 different texts that receive that label, and I record those inputs and
their responses in the README, in each of 3 trials.


**Why this target:**
A label that can never appear is dead code. If "unsure"
can't be reached, the system pretends to be certain when it isn't; if "human"
can't be reached, every writer is treated as a suspect. This is a real risk
here: while the style signal returns a fixed 0.5, a weighted average can't go
below 0.25, so the human label is close to unreachable.


---

## 4. A valid appeal always changes status and is always recorded

<!-- Your criterion. -->
For 5 out of 5 appeals sent to `POST /appeal` with a `content_id` returned by
an earlier `POST /submit`, the response is `200` with `status:
"under_review"`, and `GET /log` shows a new appeal entry for that content_id
containing the writer's reasoning, while the original `decided` entry is
still there unchanged.


**Why this target:**
The appeal is the only recourse for a writer who was
wrongly flagged, like the second-language writer in my false-positive trace.
If it ever fails silently, that person has no way to be heard. This part of
the system is plain code with no model involved, so 100% is the honest
target, not an easy one.


---

## 5. Bad input gets a clear error, never a crash

<!-- Your criterion. -->
Four malformed `POST /submit` requests (`text` missing, `text` empty `""`,
`text` only whitespace, and `text: null`) each return a `400` with a JSON body
containing an `error` field and a readable `message`. After all four,
`POST /ping` still returns `200`. This holds in 4 of 4 cases, in each of 3
trials.


**Why this target:**
Scoring empty text would either crash the service (the
detector raises an error on fewer than 3 tokens) or produce a meaningless
confidence that could still be shown to a reader as a judgment about a
person. A crash on malformed input is one of the most common real failures,
and it should never take the service down for other writers.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

## Capstone (Unit 9) — acceptance criteria

Written and committed before any test of these criteria was run. The measurements they cite (42.4 ms, 53.9 ms and 3,180 ms) come from the Milestone 3 instrumentation session. Criteria 1–3 are new and are about the extension (the request log, the gunicorn run path, and the cold-start measurement). Criteria 4–5 are my Unit 7 criteria 4 and 5, copied unchanged.

**How to run a trial.** Stop the service. Start it again with the gunicorn command in RUNNING.md. Run `python run_capstone.py` once. Every criterion below is checked in each of 3 trials.

---

### 1. Every request leaves exactly one complete log record

**Target:** In each trial, the scripted session sends the 20 requests below. While those 20 are sent, `logs/requests.jsonl` must grow by exactly 20 lines. Every new line must parse as JSON and contain at least these eight fields: `timestamp`, `method`, `route`, `input`, `status`, `outcome`, `output`, `duration_ms`. Records also carry a ninth field, `detector_loaded_at_start`, but this criterion doesn't depend on it. Target: 20 of 20, in each of 3 trials.

| Requests | Count | Expected status |
|---|---|---|
| `GET /health`, `POST /ping`, `GET /log` | 3 | 200 |
| Valid `/submit`, each with its own `creator_id` | 3 | 200 |
| Valid `/submit`, all from one `creator_id` | 7 | 200 five times, then 429 twice |
| `/submit` with no text | 2 | 400 |
| `/submit` with `"hi"` | 2 | 422 |
| Valid `/appeal` | 1 | 200 |
| `/appeal` with an unknown id | 2 | 404 |

The session covers these five status codes: 200, 400, 404, 422 and 429. It does not cover 405, 413 or 503, which the service can also return.

**Why this target:** The log is the only evidence of what my service did. A missing line can't be seen afterwards: a log with 19 of 20 lines looks exactly like a complete one unless someone counts. So anything below 100% would allow the silent loss the log exists to prevent.

---

### 2. A crash still writes a record and returns JSON

**Target:** I force an unhandled exception in `POST /submit` by making the audit log read-only (`chmod a-w logs/audit.jsonl`) and then sending a valid `/submit`. The route should fail when it tries to write the decision. A crash counts as passing only if both halves hold:

- **Record:** `logs/requests.jsonl` gets a record with `status: 500`, `outcome: "error"`, a non-empty `exception` field, and a `duration_ms`.
- **Response:** the client gets a JSON body with an `error` field and a `message` field.

Target: 3 of 3 forced crashes, in each of 3 trials. After each trial I restore write permission (`chmod u+w logs/audit.jsonl`).

**Why this target:** My Unit 9 log has no 500 entries because nothing crashed, so this path of the logging hook has never actually run. A crash is the event I'd most need a record of. A log that drops crashes fails exactly when it matters, so the target is 100%. The JSON response is part of the target because every other error in my service already returns `{"error", "message"}`, and a client shouldn't have to handle a different format just because the failure was unexpected.

---

### 3. Cold start is bounded and the log reports it correctly

**Target:** In each trial, all three of these must hold:

1. The first `POST /submit` after the restart takes at most 10,000 ms (`duration_ms`).
2. That record has `detector_loaded_at_start: false`.
3. The second `POST /submit` has `detector_loaded_at_start: true` and takes at most 100 ms.

The two submissions are pieces 1 and 2 of `MY_WRITING` in `scenarios.py` (175 and 102 words), each under its own `creator_id`.

Target: all three checks hold, in each of 3 trials.

**Why this target:** I measured one cold start at 3,180 ms, so 10,000 ms gives about three times that for a slower disk or a busy machine. It also stays far below gunicorn's `--timeout 120`, where the worker would be killed. The 100 ms warm bound is about twice the slowest warm run I measured (53.9 ms, mean 42.4 ms). That's loose enough for normal noise, but it would catch a model that reloads on every request. The flag checks matter because my cost write-up separates cold runs from warm ones using that field, and a flag that is always `true` would make that split wrong without any visible sign.

---

### 4. A valid appeal always changes status and is always recorded *(Unit 7 criterion 4, unchanged)*

For 5 out of 5 appeals sent to `POST /appeal` with a `content_id` returned by
an earlier `POST /submit`, the response is `200` with `status:
"under_review"`, and `GET /log` shows a new appeal entry for that content_id
containing the writer's reasoning, while the original `decided` entry is
still there unchanged.

**Why this target:**
The appeal is the only recourse for a writer who was
wrongly flagged, like the second-language writer in my false-positive trace.
If it ever fails silently, that person has no way to be heard. This part of
the system is plain code with no model involved, so 100% is the honest
target, not an easy one.

---

### 5. Bad input gets a clear error, never a crash *(Unit 7 criterion 5, unchanged)*

Four malformed `POST /submit` requests (`text` missing, `text` empty `""`,
`text` only whitespace, and `text: null`) each return a `400` with a JSON body
containing an `error` field and a readable `message`. After all four,
`POST /ping` still returns `200`. This holds in 4 of 4 cases, in each of 3
trials.

**Why this target:**
Scoring empty text would either crash the service (the
detector raises an error on fewer than 3 tokens) or produce a meaningless
confidence that could still be shown to a reader as a judgment about a
person. A crash on malformed input is one of the most common real failures,
and it should never take the service down for other writers.