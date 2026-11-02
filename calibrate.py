#!/usr/bin/env python3
"""
Milestone 4 calibration: both signals and the combined score, side by side.

    python calibrate.py

Runs the signals directly (no server needed) over the calibration inputs
below and prints one table. If a score surprises you, the two signal columns
show which signal is off.
"""

import detector
import scoring
import stylometry

INPUTS = {
    "clearly AI": (
        "The importance of effective time management cannot be overstated in today's "
        "fast-paced work environment. Professionals who develop strong organizational "
        "habits are better positioned to meet deadlines and reduce stress. There are "
        "several key strategies that can help individuals improve their productivity. "
        "First, prioritization is essential. By identifying the most important tasks and "
        "addressing them first, workers can ensure that critical objectives are met. "
        "Second, minimizing distractions plays a significant role. Setting aside dedicated "
        "blocks of time for concentrated work is widely considered beneficial. Finally, "
        "regular breaks are important for maintaining performance."
    ),
    "clearly human": (
        "I didn't sleep. Not properly, anyway — I lay there listening to the boiler "
        "tick and thinking about the thing I'd said to Marcus at the pub, which was "
        "stupid, and which he will absolutely bring up again. Twice now. So: coffee, and "
        "the long way round to work, and a plan. The plan lasted until about ten past "
        "nine, when Priya asked how the weekend was and I said \"fine\" in the voice that "
        "means it wasn't, and she put her mug down and looked at me. That's the trouble "
        "with Priya. She notices."
    ),
    # REPLACE with a formal paragraph YOU wrote (a cover letter, a work email,
    # an academic paragraph), ideally from before 2022. At least 80 words.
    "formal human": "Ultra-High Performance Concrete (UHPC) is an advanced technology in concrete industry with superior characteristics such as high strength in compression and tension, ductility, and durability. This paper determines the tensile and compressive behavior of UHPC and a comparison is made with Normal Strength Concrete (NC) for the development of a numerical model to simulate the behavior of UHPC using the Finite Element (FE). The experimental tests including a cylinder and cube compressive test, flexural, briquette and splitting tension tests to evaluate the ultimate capacity of the material in compression and tension and its modulus of elasticity. The primary focus of this research, however, was to simulate material properties of UHPC through commercial FE software allowing the study of the structures including UHPC. The numerical analysis provides the mechanical properties of UHPC that can be used in FE software using Concrete Damage Plasticity model (CDP) to define ductal UHPC in the absence of sufficient experimental data. The numerical and the experimental results were generally in good agreement.",
    "lightly-edited AI": (
        "Effective time management matters a lot in today's fast-paced work environment. "
        "People who build strong organizational habits are better at meeting deadlines and "
        "they feel less stressed. A few strategies can really help. First, prioritize. If "
        "you identify the most important tasks and do them first, the critical stuff gets "
        "done. Second, cut down on distractions — they play a bigger role than you'd "
        "think. Blocking off time for focused work is widely seen as useful. And finally, "
        "take regular breaks, because they help you keep performing well."
    ),
    "borderline": (
        "Time management matters more than people admit, especially now that work moves as "
        "fast as it does. If you're organised you hit deadlines, and you're less frazzled "
        "doing it. A few things actually help. Prioritise — work out what genuinely "
        "matters and do that first. Cut the interruptions; notifications wreck focus and "
        "the damage is worse than it feels at the time. And take breaks, short ones, often."
    ),
    "plain human (Ana)": (
        "My first night shift was very hard. I was nervous before it started. The patients "
        "needed many things. I learned that teamwork is very important. I am proud that I "
        "finished the shift."
    ),
}


def main():
    print(f"{'input':<20} {'model':>7} {'style':>7} {'combined':>9}  guess")
    print("-" * 56)
    for name, text in INPUTS.items():
        if text.startswith("REPLACE"):
            print(f"{name:<20} (skipped: replace the placeholder text in calibrate.py)")
            continue
        m = detector.model_signal(text)
        s = stylometry.style_signal(text)
        c = scoring.combine_signals(m, s)
        guess, _ = scoring.score_to_label(c)
        print(f"{name:<20} {m:>7.4f} {s:>7.4f} {c:>9.4f}  {guess}")


if __name__ == "__main__":
    main()