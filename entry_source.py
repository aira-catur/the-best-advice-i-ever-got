#!/usr/bin/env python3
"""The Best Advice I Ever Got -- entry builder (DRAFT).

Goal: write ONE sentence (<=200 chars, no trailing newline) to
entry.txt in MAKEFUN_OUTPUT_DIR (default /output).

Judge brief (from RULES.txt): most on-subject, most earned, most
alive as writing. Criteria in order:
  1. Single sentence about the best advice actually received.
  2. Advice worth carrying: specific, earned, true beyond its moment.
  3. Real voice recalling a real moment, not a slogan/fortune cookie.
  4. Tight: every word earns its place, reads in one breath.
  5. Lands: leaves the reader with something to keep.

Juri Kejam -- Round 1 (draft stage):
  - Killed pure slogans ("believe in yourself", "never give up"):
    no person, no moment, no cost -> fortune-cookie filler.
  - Killed abstract imperatives with no giver: the brief demands
    advice someone actually gave, so every candidate must carry a
    concrete giver and/or a concrete scene.
  - Killed two-clause sermons that preach instead of recall.

Juri Kejam -- Round 2 (after first run; winner scored 151 chars):
  - Attacked the draft winner head-on: is the fishing scene decoration
    or load-bearing? It survives -- the net he 'could not afford to
    replace' is the cost that earns the advice, and 'fix the small
    tear today' transfers intact to debt, health, work and marriage,
    so it is true beyond its moment (criterion 2).
  - Killed the wedding and toolbox lines on re-read: warm, but their
    second halves preach a general rule instead of landing on an
    image; the winner ends on a picture ('the hole you ignored')
    that keeps working after the last word (criterion 5).
  - Killed the bus-driver line: charming voice, but the advice is
    networking in disguise -- cleverness, not wisdom.
  - Tightness check: every clause of the winner either names the
    giver, the cost, the act, or the reason; nothing can be cut
    without losing one of those, so the text stands unedited.
  - Scoring hardened below: sermon endings and second-person
    preaching are now penalised, a transferable image is bonused,
    and ties break toward the shorter text (the gate's own
    tie-break also favours fewer bytes).
"""

import os
import re

CANDIDATES = [
    "My grandfather, mending a net he could not afford to replace, told me to fix the small tear today because the sea only ever finds the hole you ignored.",
    "Before my first job my mother said, pack your pride last and your questions first, because the man who asks early is never the fool who guesses late.",
    "My old foreman said, measure the board twice and your temper once, because wood forgives a pencil mark but people remember every word you cut loose.",
    "Grandma said, when someone shows you the price of everything, show them the cost of leaving, and walk out before the bargaining starts on your worth.",
    "My father, handing me his worn toolbox, said a borrowed tool returned clean and early buys you more trust than any promise you will ever make.",
    "The night I failed, my teacher kept me after class and said, do not marry your first draft of yourself; even good men are rewritten by staying.",
    "My uncle, a fisherman with nine fingers, said the sea does not punish the careful, only the hurried who call their luck a kind of skill.",
    "Mother said, eat before you argue and sleep before you decide, because half the regrets in this house were just hunger and tiredness talking.",
    "My grandmother whispered at my wedding, love him loudly in private and argue quietly in public, and you will never have to win an audience to keep a home.",
    "An old nurse told me, holding my shaking hands in the corridor, to breathe for the patient first, because panic is contagious and so is calm.",
    "My dad said, when the money is tight, pay the honest man first, because your name travels faster than your feet in a small town.",
    "Before I left home, my mother folded my shirt and said, be easy to help and hard to fool, and the world will mostly meet you halfway.",
    "My grandfather said, plant trees whose shade you will never sit in, but write your name on none of them, because kindness remembered is just vanity.",
    "The bus driver who drove my school route for ten years said, wave at people on your way up the hill; you will want those faces friendly on the way down.",
    "My aunt, widowed young, told me to keep one small joy that no sorrow can schedule, because grief visits everyone but it should never find you empty.",
    "My father said, never lend what you cannot give, and never give what you will resent, because both turn a friend into a debt.",
]

# Words that signal a lived scene / concrete giver.
GIVERS = ["grandfather", "grandma", "grandmother", "mother", "father",
          "dad", "teacher", "foreman", "uncle", "aunt", "nurse",
          "bus driver"]
CONCRETE = ["net", "toolbox", "shirt", "board", "hill", "corridor",
            "wedding", "sea", "trees", "hands", "class"]
SLOGAN = ["believe in yourself", "never give up", "follow your dreams",
          "be yourself", "stay positive"]


def score(sentence: str) -> float:
    s = sentence.lower()
    total = 0.0
    # 1. On-subject: a giver actually gave it.
    total += 3.0 * sum(1 for g in GIVERS if g in s)
    total += 1.5 * sum(1 for v in ("said", "told me", "whispered") if v in s)
    # 2. Specific / earned: concrete nouns from a lived scene.
    total += 2.0 * sum(1 for c in CONCRETE if c in s)
    # 3. Real voice: a because-clause that earns the advice.
    total += 2.0 if "because" in s else 0.0
    # 4. Tightness: prefer 110-165 chars, penalise bloat.
    n = len(sentence)
    total += max(0.0, 3.0 - abs(n - 140) / 25.0)
    # 5. Landing: ends on a concrete / resonant noun, not a filler word.
    last = re.findall(r"[A-Za-z']+", sentence)[-1].lower()
    total += 1.5 if last in CONCRETE or last in ("home", "town", "skill", "debt") else 0.0
    # Slogan penalty.
    total -= 5.0 * sum(1 for p in SLOGAN if p in s)
    # Round-2 hardening: penalise preaching at the reader; the advice
    # must be recalled, not lectured.
    total -= 2.0 * s.count(" you will ")
    total -= 1.0 * s.count(" you should ")
    # Bonus for an image that transfers beyond its own scene.
    total += 1.5 * sum(1 for img in ("hole", "tear", "shade") if img in s)
    return total


def main() -> None:
    # Highest score wins; ties break toward the shorter text.
    ranked = sorted(CANDIDATES, key=lambda c: (score(c), -len(c)),
                    reverse=True)
    winner = ranked[0]
    terminators = sum(winner.count(t) for t in ".!?")
    assert terminators == 1 and winner.endswith(".")
    assert 1 <= len(winner) <= 200
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(winner)  # no trailing newline


if __name__ == "__main__":
    main()
