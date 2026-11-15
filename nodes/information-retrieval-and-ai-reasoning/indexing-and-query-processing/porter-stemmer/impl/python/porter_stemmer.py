# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/porter-stemmer/. The authors are listed in prov/MAYHA4.jsonl.
"""The Porter stemmer, with the rules of the 1980 paper.

With definitive=True the stemmer follows the later reference version of
Porter (the ANSI C and BCPL code) instead: it adds the rule LOGI -> LOG to
step 2, replaces ABLI -> ABLE by BLI -> BLE, and leaves words of one or two
letters alone.
"""

from typing import Callable

VOWELS = "aeiou"

Condition = Callable[[str], bool]
Rule = tuple[str, str, Condition]


def consonant_flags(w: str) -> list[bool]:
    """Return a list whose entry i tells if letter i of w is a consonant.

    A consonant is a letter other than a, e, i, o, u, and other than a y
    that follows a consonant. Precondition: w is lower case. Cost O(|w|).
    """
    flags: list[bool] = []
    for i, c in enumerate(w):
        if c in VOWELS:
            flags.append(False)
        elif c == "y":
            flags.append(i == 0 or not flags[i - 1])
        else:
            flags.append(True)
    return flags


def measure(v: str) -> int:
    """Return m for v written as [C](VC){m}[V]: the number of vowels directly followed by a consonant.

    Precondition: v is lower case. Cost O(|v|).
    """
    f = consonant_flags(v)
    m = 0  # @line L13
    for i in range(len(v) - 1):  # @line L14
        if not f[i] and f[i + 1]:
            m += 1
    return m  # @line L15


def has_vowel(v: str) -> bool:
    """The condition *v*: v contains a vowel. Cost O(|v|)."""
    return not all(consonant_flags(v))


def ends_double_consonant(v: str) -> bool:
    """The condition *d: v ends with two equal letters that are both consonants. Cost O(|v|).

    Porter's C code tests only that the last letter is a consonant. The two
    readings differ only for a final yy, whose y before the last is a vowel.
    """
    if len(v) < 2 or v[-1] != v[-2]:
        return False
    f = consonant_flags(v)
    return f[-1] and f[-2]


def ends_cvc(v: str) -> bool:
    """The condition *o: v ends consonant, vowel, consonant, and the last letter is not w, x or y. Cost O(|v|)."""
    if len(v) < 3 or v[-1] in "wxy":
        return False
    f = consonant_flags(v)
    return f[-3] and not f[-2] and f[-1]


def _m_gt(k: int) -> Condition:
    return lambda v: measure(v) > k


def _always(v: str) -> bool:
    return True


STEP_1A: list[Rule] = [("sses", "ss", _always), ("ies", "i", _always), ("ss", "ss", _always), ("s", "", _always)]
STEP_1B: list[Rule] = [("eed", "ee", _m_gt(0)), ("ed", "", has_vowel), ("ing", "", has_vowel)]
STEP_1C: list[Rule] = [("y", "i", has_vowel)]
STEP_2_PAIRS = [
    ("ational", "ate"), ("tional", "tion"), ("enci", "ence"), ("anci", "ance"), ("izer", "ize"),
    ("abli", "able"), ("alli", "al"), ("entli", "ent"), ("eli", "e"), ("ousli", "ous"),
    ("ization", "ize"), ("ation", "ate"), ("ator", "ate"), ("alism", "al"), ("iveness", "ive"),
    ("fulness", "ful"), ("ousness", "ous"), ("aliti", "al"), ("iviti", "ive"), ("biliti", "ble"),
]
STEP_2: list[Rule] = [(a, b, _m_gt(0)) for a, b in STEP_2_PAIRS]
STEP_2_DEFINITIVE: list[Rule] = [(a, b, _m_gt(0)) for a, b in STEP_2_PAIRS if a != "abli"] + [
    ("bli", "ble", _m_gt(0)),
    ("logi", "log", _m_gt(0)),
]
STEP_3: list[Rule] = [
    (a, b, _m_gt(0))
    for a, b in [("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"), ("ical", "ic"), ("ful", ""), ("ness", "")]
]
STEP_4_SUFFIXES = [
    "al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment",
    "ent", "ou", "ism", "ate", "iti", "ous", "ive", "ize",
]
STEP_4: list[Rule] = [(a, "", _m_gt(1)) for a in STEP_4_SUFFIXES] + [
    ("ion", "", lambda v: measure(v) > 1 and v[-1:] in ("s", "t")),
]
STEP_5A: list[Rule] = [("e", "", lambda v: measure(v) > 1 or (measure(v) == 1 and not ends_cvc(v)))]
# (m > 1 and *d and *L) -> single letter. The stem v is the word without its last l,
# so the word ends with ll exactly when v ends with l. Removing one consonant of a
# final run of consonants does not change m.
STEP_5B: list[Rule] = [("l", "", lambda v: measure(v) > 1 and v.endswith("l"))]


def tidy_1b(w: str) -> str:
    """The second part of step 1b, done after the rule ED or ING has removed its suffix. Cost O(|w|)."""
    if w.endswith(("at", "bl", "iz")):  # @line L9
        return w + "e"
    if ends_double_consonant(w) and w[-1] not in "lsz":  # @line L10
        return w[:-1]
    if measure(w) == 1 and ends_cvc(w):  # @line L11
        return w + "e"
    return w  # @line L12


def apply_step(rules: list[Rule], w: str, step: str = "") -> str:
    """Apply one step: the rule with the longest S1 that ends w, if its condition holds for the stem.

    Precondition: no two rules of the list have the same S1. Cost O(|w|) for a fixed rule list.
    """
    best = None
    for rule in rules:  # @line L2
        if w.endswith(rule[0]) and (best is None or len(rule[0]) > len(best[0])):
            best = rule
    if best is None:  # @line L3
        return w
    s1, s2, cond = best
    v = w[: len(w) - len(s1)]  # @line L4
    if not cond(v):  # @line L5
        return w
    w = v + s2  # @line L6
    if step == "1b" and s1 in ("ed", "ing"):  # @line L7
        w = tidy_1b(w)
    return w


def step_1a(w: str) -> str:
    return apply_step(STEP_1A, w)


def step_1b(w: str) -> str:
    return apply_step(STEP_1B, w, "1b")


def step_1c(w: str) -> str:
    return apply_step(STEP_1C, w)


def step_2(w: str, definitive: bool = False) -> str:
    return apply_step(STEP_2_DEFINITIVE if definitive else STEP_2, w)


def step_3(w: str) -> str:
    return apply_step(STEP_3, w)


def step_4(w: str) -> str:
    return apply_step(STEP_4, w)


def step_5a(w: str) -> str:
    return apply_step(STEP_5A, w)


def step_5b(w: str) -> str:
    return apply_step(STEP_5B, w)


def porter_stem(w: str, definitive: bool = False) -> str:
    """Return the Porter stem of w.

    Precondition: w is a word of lower case letters a to z (it may be empty).
    Cost O(|w|): eight steps, each with a fixed number of rules of bounded length.
    """
    if definitive and len(w) <= 2:
        return w
    steps = [
        (STEP_1A, "1a"), (STEP_1B, "1b"), (STEP_1C, "1c"),
        (STEP_2_DEFINITIVE if definitive else STEP_2, "2"),
        (STEP_3, "3"), (STEP_4, "4"), (STEP_5A, "5a"), (STEP_5B, "5b"),
    ]
    for rules, name in steps:  # @line L1
        w = apply_step(rules, w, name)
    return w  # @line L8
