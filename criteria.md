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
