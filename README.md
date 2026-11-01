# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a small backend service a writing site can plug into. The
site sends it a piece of writing; it sends back a guess about whether the
writing is AI-generated, how confident that guess is, a plain-English label a
reader would see, and a `content_id` the writer can use to appeal.

### The path a submission takes

1. **The route receives the request** (`app.py::submit`). The site sends
   `POST /submit` with JSON containing `text` and `creator_id`. The route reads
   the body into a dict and pulls out both fields; a missing `creator_id`
   becomes `"unknown"`. This step adds *structure*: we know what was sent and
   by whom.
2. **The input is checked before anything expensive runs** (`app.py::submit`).
   If `text` is missing, not a string, empty, or over the size limit, the route
   answers right away with a `400` and a readable message. Text too short for
   the model to score gets a `422` instead of a crash. This step adds *safety*:
   bad input never reaches a signal and never becomes a `500`.
3. **Signal one scores how predictable the text is**
   (`detector.py::model_signal`). GPT-2, running locally, measures the text's
   perplexity and turns it into a 0–1 `model_score` (higher = more likely AI).
   This adds a first opinion based on *which words* appear.
4. **Signal two scores the shape of the text** (`stylometry.py::style_signal`).
   Without reading for meaning, it measures sentence-length spread, vocabulary
   variety and punctuation, and turns them into a 0–1 `style_score` (higher =
   more likely AI). This adds a second, independent opinion based on
   *structure*.
5. **The two scores become one** (`scoring.py::combine_signals`). The
   combining rule turns both scores into one `confidence` from 0.0
   (confidently human) to 1.0 (confidently AI). This adds the decision about
   how much to trust each signal, and what to do when they disagree.
6. **The number becomes words** (`scoring.py::score_to_label`). `confidence`
   is compared with the two thresholds in `config.py` to produce a short
   `guess` (`human` / `unsure` / `ai`) and a full-sentence `label`. This adds
   *meaning for a person*: what the system thinks, how sure it is, and what the
   writer can do.
7. **The decision is logged and returned** (`audit.py::log_decision`). A
   unique `content_id` is created and one entry goes into `logs/audit.jsonl`:
   timestamp, content_id, creator_id, guess, model_score, style_score,
   combined score, label, and status `decided`. The same values go back to the
   site as JSON. This adds *accountability*: every decision can be
   reconstructed later, and the content_id is what the writer needs to appeal.

**If the writer disagrees:** the site sends `POST /appeal` (`app.py::appeal`)
with the `content_id` and the writer's reasoning. The route checks the
content_id exists (`audit.entries_for`), appends an appeal entry with
`audit.log_appeal` (status becomes `under_review`; the original decision stays
in the log untouched), and confirms to the writer.

### The false positive this design is built around

**Who:** Ana, a nursing student writing in her second language, posts a short
essay she wrote herself about her first night shift.

**What she submitted:** *"My first night shift was very hard. I was nervous
before it started. The patients needed many things. I learned that teamwork
is very important. I am proud that I finished the shift."*

**What score she got:** signal one gave her a perplexity of 36.6, which is a
`model_score` of **0.582**, already leaning AI just because her words are
common and her order is plain. Signal two will lean AI too: five sentences of
almost the same length, repeated words ("very", "shift"), and no punctuation
except full stops. Both signals lean the same way **for the same reason,
plain writing**, so their agreement is not evidence. With the starter's
placeholder thresholds (AI above 0.65), a style score of about 0.7 would put
her combined score near or over the line.

**What the label said to her (in a badly designed system):** "AI-generated
(0.68)." She reads that as a public accusation of cheating, with a number she
doesn't understand and no way to prove she wrote it. The likely result is
that she stops posting, and the site loses the kind of writer it is meant to
protect.

**What she can do about it:** appeal with her `content_id` and her reasoning.
The service records it next to the original decision, moves the item to
`under_review`, and tells her a person will look at it.

**What this forces on my design:**
- The AI threshold has to sit well above where plain human writing lands.
  Ana's case suggests the placeholder 0.65 is too low.
- The "unsure" band has to be wide. A wrong "unsure" costs a writer little; a
  wrong "AI" costs them a lot.
- No label can sound like a verdict. Even the AI label says it's an automated
  estimate that can be wrong, shows no raw numbers, and points to the appeal.
- The appeal can never fail silently. An unknown content_id gets a clear
  `404`, and every accepted appeal is logged and changes the status.
- Agreement between the two signals should not raise confidence by itself,
  because both share the "plain writing" weakness.

### The endpoints

**`POST /submit`**

Request (JSON object):

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | Not empty or whitespace only; at most 20,000 characters; long enough for the model to score (a sentence or more) |
| `creator_id` | string | no | Identifies the writer; defaults to `"unknown"` if missing |

Success, `200`:

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | `c_` + 12 hex characters, e.g. `c_3f9a1b2c4d5e`. Needed to appeal |
| `guess` | string | Exactly one of `"human"`, `"unsure"`, `"ai"` |
| `confidence` | float 0–1 | Combined score; 0 = confidently human, 1 = confidently AI |
| `label` | string | The full sentence a reader sees |
| `model_score` | float 0–1 | Signal one (higher = more AI). Always present |
| `style_score` | float 0–1 | Signal two (higher = more AI). Always present |
| `status` | string | `"decided"` |

Errors all use `{"error": "<code>", "message": "<readable sentence>"}`:

| Case | HTTP | `error` |
|---|---|---|
| `text` missing, not a string, empty, or whitespace | 400 | `bad_request` |
| `text` over 20,000 characters | 413 | `text_too_long` |
| `text` too short for the model to score | 422 | `text_too_short` |

**`POST /appeal`**

Request (JSON object):

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | Must already exist in the audit log |
| `reasoning` | string | yes | The writer's explanation; not empty or whitespace only |

The writer doesn't send `creator_id`; the route takes it from the original
decision in the log, so an appeal is always tied to the person who submitted.

Success, `200`:

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | The item appealed |
| `status` | string | Always `"under_review"` |
| `message` | string | "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime." |

Errors:

| Case | HTTP | `error` |
|---|---|---|
| `content_id` or `reasoning` missing or empty | 400 | `bad_request` |
| `content_id` not found in the log | 404 | `not_found` |

A successful appeal appends one log entry (timestamp, content_id, creator_id,
`event: "appeal"`, `status: "under_review"`, reasoning). The original `decided`
entry is never edited, and `GET /log` shows both, in order.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity: how surprised the GPT-2 language model,
running locally, is by each next word, over the first 400 tokens. It is turned
into a 0–1 score with a logistic curve: a perplexity of 45 maps to 0.5, lower
perplexity pushes the score toward 1.0 (AI-like), higher pushes it toward 0.0
(human-like).

**Why that might differ between human and AI writing:** A language model
writes by repeatedly picking a likely next word, so text a model produced
tends to be text a model finds easy to predict. People make odd word choices,
add specific details, and change direction mid-sentence, and all of that
surprises a model.

**What it can't see:** Predictability is not authorship. This signal rewards
common words in plain sentences, and many real people write exactly that
way: someone writing in a second language, a younger writer, anyone writing
plainly on purpose. My own test shows it: a plain paragraph I wrote as a
second-language writer would scored **0.582** (perplexity 36.6), already
leaning AI. It also fails the other way: AI text that uses rare or ornate
vocabulary scores as human, because rare words are what a model fails to
predict. It can't see who typed the text or whether a person edited AI
output, and anything after the first ~400 tokens is invisible to it.

### Signal two — the style signal

**What it measures:** The shape of the text, without understanding any of
it. Three measures, each scaled to 0–1 and pointed so that higher means "more
AI", then averaged into `style_score`:
- **Sentence-length spread:** the standard deviation of sentence lengths
  divided by their mean. *Low* spread (sentences marching in step) means more
  AI-like.
- **Type-token ratio:** unique words divided by total words. *Low* variety
  (repeated vocabulary) means more AI-like.
- **Punctuation density:** commas, semicolons, colons, dashes, parentheses,
  quotes, `!` and `?` per word. *Low* density (plain, uniform punctuation)
  means more AI-like.

A text with fewer than two sentences has no spread to measure, so that measure
returns a neutral 0.5 instead of crashing.

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences, a safe band of vocabulary and tidy
punctuation, because "most likely next word" produces average-shaped text.
Human writing is lumpier: a three-word sentence next to a forty-word one,
dashes, asides, fragments, quoted speech.

**What it can't see:** It can't read. It has no idea what the text says or
who wrote it, so anything that changes the shape without changing the author
moves it: typos, chopping long sentences into short ones, adding dashes and
semicolons, pasting in a quotation. Those edits take seconds, so AI text can
be made to look human cheaply. It is unreliable on short text, since two or
three sentences don't give a stable spread, and type-token ratio falls as
text gets longer, so length alone can look like a signal. Like signal one, it
can also flag a plain human writer whose sentences happen to be even.

**Why these are two different signals:** signal one depends on *which words*
appear; signal two ignores the words and looks only at *structure*. Swapping
common words for rare synonyms moves signal one but barely moves signal two;
splitting sentences moves signal two but barely moves signal one.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
