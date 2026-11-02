"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: the coefficient of variation
    (standard deviation of sentence lengths in words, divided by the mean).

    Scale: 0.0 and up, no fixed top. 0.0 means every sentence is the same
    length; around 1.0 means very lumpy. LOW spread means more AI-like.

    Edge case: fewer than two sentences has no spread, so this returns 0.0,
    and `style_signal` treats spread as neutral below MIN_SENTENCES.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. 0 to 1; higher means more varied vocabulary.

    Computed and printed, but NOT used in style_signal (weight 0). On my
    calibration texts it pointed the wrong way: the clearly-AI sample scored
    0.848 and the clearly-human sample 0.734, because generated prose avoids
    repeating words while people repeat names and small words. It also falls
    as text gets longer, so length alone moves it.
    """
    w = words(text)
    return len(set(w)) / len(w) if w else 0.0


# Punctuation that varies between writers: commas, semicolons, colons, em/en
# dashes, a spaced hyphen used as a dash, parentheses, double quotes, ! and ?.
# Full stops and apostrophes are left out: every writer uses them.
_VARIED_PUNCT = re.compile(r"[,;:\u2014\u2013()\"!?\u201c\u201d]|(?<=\s)-(?=\s)")


def punctuation_density(text: str) -> float:
    """
    Varied punctuation marks per word. 0.0 and up (typically 0 to 0.15).
    LOW density means more AI-like (plain, uniform punctuation).
    """
    w = words(text)
    if not w:
        return 0.0
    return len(_VARIED_PUNCT.findall(text)) / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

# Scaling: each measure is mapped onto 0-1 where 1.0 = most AI-like.
SPREAD_AI_AT = 0.2      # spread at or below this -> 1.0 (sentences in step)
SPREAD_HUMAN_AT = 1.0   # spread at or above this -> 0.0 (very lumpy)
PUNCT_HUMAN_AT = 0.12   # density at or above this -> 0.0; zero density -> 1.0

MIN_SENTENCES = 3       # below this, spread is treated as neutral (0.5)
FULL_TRUST_WORDS = 100  # below this, the score is pulled toward 0.5


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. **Higher means more likely AI.**

    1. spread_ai = 1 at spread <= 0.2, 0 at spread >= 1.0, linear between.
       (Flipped: low spread is AI-like.) Neutral 0.5 under 3 sentences.
    2. punct_ai  = 1 at density 0, 0 at density >= 0.12, linear between.
       (Flipped: low density is AI-like.)
    3. raw = average of the two. Type-token ratio has weight 0 (see above).
    4. Short text is unreliable, so the score is pulled toward 0.5:
       style = 0.5 + (raw - 0.5) * min(1, word_count / 100).
    """
    w = words(text)
    if not w:
        return 0.5

    if len(sentences(text)) < MIN_SENTENCES:
        spread_ai = 0.5
    else:
        spread = sentence_length_spread(text)
        spread_ai = _clip((SPREAD_HUMAN_AT - spread) / (SPREAD_HUMAN_AT - SPREAD_AI_AT))

    punct_ai = _clip(1.0 - punctuation_density(text) / PUNCT_HUMAN_AT)

    raw = (spread_ai + punct_ai) / 2
    reliability = min(1.0, len(w) / FULL_TRUST_WORDS)
    return round(0.5 + (raw - 0.5) * reliability, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("(type_token_ratio is shown but not used in style_signal)")