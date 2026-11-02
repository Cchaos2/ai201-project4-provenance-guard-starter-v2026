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
   If `text` is missing, not a string, or empty, the route answers right away
   with a `400` and a readable message; text over 20,000 characters gets a
   `413`; text too short for the model to score gets a `422` instead of a
   crash. Each refusal is recorded with `audit.log_rejection`. This step adds *safety*:
   bad input never reaches a signal and never becomes a `500`.
3. **Signal one scores how predictable the text is**
   (`detector.py::model_signal`). GPT-2, running locally, measures the text's
   perplexity and turns it into a 0–1 `model_score` (higher = more likely AI).
   This adds a first opinion based on *which words* appear.
4. **Signal two scores the shape of the text** (`stylometry.py::style_signal`).
   Without reading for meaning, it measures sentence-length spread and
   punctuation density, and turns them into a 0–1 `style_score` (higher =
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
it (`stylometry.py::style_signal`). Two measures are scored, each mapped to
0–1 with higher meaning "more AI":
- **Sentence-length spread:** the standard deviation of sentence lengths
  divided by their mean. A spread of 0.2 or less scores 1.0 (sentences march
  in step); 1.0 or more scores 0.0 (lumpy); linear in between.
- **Punctuation density:** commas, semicolons, colons, dashes, parentheses,
  quotes, `!` and `?` per word. Zero scores 1.0 (plain); 0.12 or more scores
  0.0; linear in between.

The two are averaged. Two safety rules: with fewer than 3 sentences, spread
counts as a neutral 0.5; and the result is pulled toward 0.5 for short text,
`style = 0.5 + (raw − 0.5) × min(1, words / 100)`, because a few sentences
can't be measured reliably.

**A measure I dropped:** type-token ratio (unique words ÷ total words) is
still computed and printed, but has weight 0. On my samples it pointed the
wrong way: the clearly-AI text scored 0.848 and the clearly-human text
0.734, because generated prose avoids repeating words while people repeat
names and small words. It also falls as text gets longer, so length alone
moves it.

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

**The rule:** A weighted average that leans on the model signal, plus one
rule for real disagreement. If the two signals point **opposite ways** (one
above 0.5, the other below) **and** are at least 0.35 apart, the result is
pulled halfway back toward 0.5, because two methods contradicting each other
is uncertainty and shouldn't produce a confident label. Two signals on the
same side are not a split, however far apart.

**The numbers** (all in `config.py`):
- `confidence = 0.6 × model_score + 0.4 × style_score`
- If the signals are on opposite sides of 0.5 and differ by ≥ 0.35:
  `confidence = 0.5 + (confidence − 0.5) × 0.5`
- Thresholds: human below **0.35**, unsure from 0.35 to 0.70, AI above
  **0.70** (raised from the starter's 0.65 because of the false-positive
  trace above).

The model signal gets more weight because the style signal is the cheaper
one to fool on purpose (typos and sentence-chopping move it in seconds) and
is unreliable on short text.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** the
clearly-human sample. Signal one only half-recognized it as human
(`model_score` 0.4445, which alone would land in "unsure"), while signal two
was sure (`style_score` 0.0417: very uneven sentence lengths and lots of
dashes, commas and quotes). My first version of the disagreement rule
triggered on any gap of 0.35 or more, so it pulled this text from 0.2834 to
0.3917, "unsure", even though both signals said human. I changed the rule to
trigger only when the signals point **opposite ways**. Now the text scores
0.2834, "human". A true split, like `model_score` 0.85 with `style_score`
0.30, is still pulled from 0.63 to 0.565: "unsure", not "AI".

**Calibration run** (`python calibrate.py`, which runs both signals directly
on six chosen inputs):

```
input                  model   style  combined  guess
--------------------------------------------------------
clearly AI            0.7544  0.6708    0.7210  ai
clearly human         0.4445  0.0417    0.2834  human
formal human          0.6080  0.5634    0.5902  unsure
lightly-edited AI     0.6999  0.5595    0.6437  unsure
borderline            0.3489  0.4740    0.3989  unsure
plain human (Ana)     0.5820  0.6650    0.6152  unsure
```

*Formal human* is the abstract of a 2017 journal paper. *Lightly-edited AI*
is the clearly-AI text with contractions, a dash, and some sentences
shortened or merged by hand.

**What it shows:**
- Clearly-AI and clearly-human text score **0.44 apart** (0.7210 vs 0.2834),
  so the combined score carries real information.
- **No human text was called AI.** The formal abstract (0.5902) and Ana's
  plain writing (0.6152) both land in "unsure". Both lean AI on *both*
  signals, which is exactly the plain/formal-writing blind spot named above;
  the 0.70 threshold is what keeps them from being accused.
- **Light editing was enough to move AI text out of the "AI" label** (0.7210
  to 0.6437). That is the trade I chose: some AI text gets through as
  "unsure" so that real writers aren't wrongly accused. It is also the
  attack I expect Unit 8 to use.
- The clearly-AI text clears the AI threshold by only 0.021, so the "AI"
  label is hard to reach. The label tests below confirm it is reachable by
  two different texts.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. Our automated check didn't find signs that it was generated by AI. |
| unsure | above 0.35 and below 0.70 | We can't tell how this was written. Our automated check found mixed signals, which is common in real writing too, so we're not making any judgment about it. |
| high-confidence AI | 0.70 – 1.00 | Our automated check found strong signs that this may have been generated by AI. This is an estimate, not proof, and it can be wrong. If you wrote this yourself, you can ask for a person to review it. |

The text lives in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`)
and the mapping in `scoring.py::score_to_label`; the ranges come from
`config.py` (`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.70`). Every score
from 0 to 1 maps to exactly one label, with no gaps. The test inputs are in
`samples/`.

**All three are reachable** (each sent to `POST /submit`):

| Input (`samples/`) | model_score | style_score | confidence | guess |
|---|---|---|---|---|
| `ai_1`: clearly-AI paragraph | 0.7544 | 0.6708 | 0.7210 | ai |
| `ai_2`: shorter clearly-AI paragraph | 0.7993 | 0.6159 | 0.7259 | ai |
| `human_1`: clearly-human paragraph | 0.4445 | 0.0417 | 0.2834 | human |
| `human_2`: my own paragraph about my week | 0.6257 | 0.4170 | 0.5422 | unsure |
| `human_3`: a paragraph I adapted myself from Pangram's website description of its detector | 0.2899 | 0.4278 | 0.3451 | human |
| `unsure_1`: borderline paragraph | 0.3489 | 0.4740 | 0.3989 | unsure |
| `unsure_2`: Ana's plain writing | 0.5820 | 0.6650 | 0.6152 | unsure |

**What the table shows:** each of the three labels was reached by at least
two different texts (criterion 3). But "human" was hard to reach for my own
writing. My `human_2` paragraph landed in "unsure": its "First... Then...
Finally" structure is the way AI text usually organizes itself, so signal
one found it fairly predictable (0.6257). That's the system doing what I
designed it to do: a real writer the signals can't place gets "we can't
tell", not an accusation. `human_3` reached "human", but only just (0.3451
against a 0.35 cutoff), and mostly because it is full of brand names and
figures ("OpenAI", "DeepSeek", "26 models", "99.7%") that GPT-2 can't
predict. That's the other side of signal one's blind spot: unusual words
read as human whoever wrote them, so the same trick would help AI text
pass. Both are cases to test again in Unit 8.

**A false positive I found while testing:** a short, plain paragraph I
wrote myself, *"Today is going to be a good day. And also it is going to be
a great start to the week. There are a lot of things to do, but I believe
everything is possible!"* (33 words), was labelled **high-confidence AI**
(`confidence` 0.7655, `model_score` 0.8925, `style_score` 0.5751). Signal
one scored it as more machine-like than my clearly-AI sample, because
common words in an ordinary order are exactly what GPT-2 predicts well.
Signal two couldn't pull it back, because with so few words it is pulled
toward 0.5 by design. This is the blind spot from my false-positive trace,
confirmed on my own writing. It falls outside criterion 1, which covers
texts of 100 words or more, but it shows that short, plain posts are where
a real writer is most likely to be wrongly accused. I'm keeping it
(`samples/false_positive_short.json`) as a case to diagnose in Unit 8.

**Why I worded the "unsure" one this way:** Most real writing lands in
"unsure", including one of my own human paragraphs, so this label must not
read as a suspicion. It says *we* can't tell, which puts the uncertainty on
the system, not on the writer. It names the reason in plain words ("mixed
signals"), says that is common in real writing, and says outright that no
judgment is being made. It avoids the word "AI" entirely, because in a label
people skim, that one word reads like an accusation.

**Why the AI label is worded carefully too:** it says "may have been", calls
itself "an estimate, not proof", admits it "can be wrong", and tells the
writer the next step (ask for a person to review it). A wrong "AI" label is
the expensive mistake, as the 33-word example above shows, so the label
itself carries the way out.

---

## Sample Run

The run follows Ana, the writer from my false-positive trace: she submits
her plain-English paragraph, gets "unsure", and appeals anyway.

**A submission**

```bash
$ cat samples/unsure_2.json
{"creator_id": "ana", "text": "My first night shift was very hard. I was nervous before it started. The patients needed many things. I learned that teamwork is very important. I am proud that I finished the shift."}

$ curl -s -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d @samples/unsure_2.json
```

```json
{
  "confidence": 0.6152,
  "content_id": "c_0e11cb746849",
  "guess": "unsure",
  "label": "We can't tell how this was written. Our automated check found mixed signals, which is common in real writing too, so we're not making any judgment about it.",
  "model_score": 0.582,
  "status": "decided",
  "style_score": 0.665
}
```

**An appeal**

```bash
$ curl -i -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_0e11cb746849", "reasoning": "I wrote this myself about my first night shift. English is my second language, so I use simple words I am sure of."}'
```

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "content_id": "c_0e11cb746849",
  "message": "Thanks, we've received your appeal. A person will review this decision, and the automated result won't be treated as final in the meantime.",
  "status": "under_review"
}
```

An appeal with an id that doesn't exist gets a clear error and writes
nothing to the log:

```bash
$ curl -i -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_doesnotexist", "reasoning": "test"}'
```

```
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{
  "error": "not_found",
  "message": "We couldn't find a submission with id c_doesnotexist."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.6152,
      "content_id": "c_0e11cb746849",
      "creator_id": "ana",
      "guess": "unsure",
      "label": "We can't tell how this was written. Our automated check found mixed signals, which is common in real writing too, so we're not making any judgment about it.",
      "model_score": 0.582,
      "status": "decided",
      "style_score": 0.665,
      "timestamp": "2026-11-02T14:17:18+00:00"
    },
    {
      "content_id": "c_0e11cb746849",
      "creator_id": "ana",
      "event": "appeal",
      "reasoning": "I wrote this myself about my first night shift. English is my second language, so I use simple words I am sure of.",
      "status": "under_review",
      "timestamp": "2026-11-02T14:20:00+00:00"
    }
  ]
}
```

The original `decided` entry is unchanged; the appeal sits right after it
with status `under_review`, and its `creator_id` was taken from the
original decision rather than sent by the writer. The two 404 appeals
(`c_PASTE_HERE` and `c_doesnotexist`) left no entry at all.

**Bad input** gets a `400` and a readable message, never a crash, and each
refusal is logged (from my Milestone 3 run):

```bash
$ curl -i -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "", "creator_id": "carlos"}'
```

```
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{
  "error": "bad_request",
  "message": "Send JSON with a non-empty \"text\" field."
}
```

```json
{
  "creator_id": "carlos",
  "event": "rejected",
  "reason": "missing_text",
  "status": "rejected",
  "timestamp": "2026-11-02T01:18:15+00:00"
}
```

---

## How I Used AI

I used Claude throughout as a reviewer and pair-programmer. Two moments
changed the project.

**Moment 1: a 403 that wasn't my code**

- *What I asked for:* my first hardcoded `/submit` seemed to return nothing.
  Then, from a second terminal, `curl` returned `403 Forbidden`. I pasted the
  full response and asked what was wrong with my route.
- *What came back:* the answer was in the headers. The response said
  `Server: AirTunes`, not `Server: Werkzeug`, so the request had reached
  macOS's AirPlay Receiver, which also listens on port 5000, not my Flask
  app. My server wasn't running at that moment, so AirPlay answered instead.
  It also explained that the terminal running `python app.py` is busy with
  the server, so requests must go from a second terminal.
- *What I changed:* I turned off AirPlay Receiver (System Settings → General
  → AirDrop & Handoff), restarted the server, and from then on checked
  `/ping` first and looked for `Server: Werkzeug` in every `curl -i`
  response. That is the control-route habit the brief describes: when
  something breaks, first find out whether it's the service or the handler.

**Moment 2: my own writing was labelled AI**

- *What I asked for:* a short paragraph I wrote myself ("Today is going to
  be a good day...", 33 words) came back as high-confidence AI at 0.7655. I
  asked Claude why, and whether I should change the thresholds.
- *What came back:* it pointed at the two signal scores. `model_score` was
  0.8925, higher than my clearly-AI sample, because common words in an
  ordinary order are exactly what GPT-2 predicts; `style_score` was 0.5751,
  pulled toward 0.5 because the text was short. It advised against moving the
  thresholds to hide the result: the text is outside criterion 1 (which needs
  100+ words), and it is a real case for Unit 8's diagnosis.
- *What I changed:* I kept the text as evidence
  (`samples/false_positive_short.json`), wrote it up under Label Variants,
  and wrote two longer paragraphs of my own to test the human label. The
  first (`human_2`) still landed in "unsure" (0.5422), which taught me that
  "First... Then... Finally" structure reads as AI. The second (`human_3`)
  reached "human", but only just (0.3451). I reported both results as they
  came out instead of tuning the system until my tests passed.

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