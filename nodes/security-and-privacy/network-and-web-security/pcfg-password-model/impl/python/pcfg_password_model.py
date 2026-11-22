# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcfg-password-model/. The authors are listed in prov/RSR0DF.jsonl.

"""A probabilistic context-free grammar of passwords, used to estimate strength.

A password is split into maximal runs of letters (L), digits (D) and other
symbols (S). The base structure is the list of (tag, length) pairs, for
example L3 D2 for "abc12". Following Weir et al. (2009), with the letter runs
learned from the training list as in Kelley et al. (2012), the grammar has a
rule START -> structure for each base structure seen in training, and a rule
(tag, length) -> x for each run x seen in training, each with its relative
frequency. The probability of a password is the probability of its one
derivation: P(structure) times the product of P(run | tag, length). A run or
structure not seen in training gives probability 0.

The guess number of w is 1 plus the number of strings with a higher
probability. It is an estimate under the model and its training list. The
code counts these strings and never lists them.
"""

import math
from fractions import Fraction
from typing import NamedTuple

Structure = tuple  # ((tag, length), ...)


class PCFGModel(NamedTuple):
    structures: dict  # Structure -> Fraction
    runs: dict  # (tag, length) -> {run string: Fraction}


def tag_of(ch: str) -> str:
    """L for an ASCII letter, D for an ASCII digit, S for any other character."""
    if ch.isascii() and ch.isalpha():
        return "L"
    if ch.isascii() and ch.isdigit():
        return "D"
    return "S"


def segment(w: str) -> list[tuple[str, str]]:
    """The maximal runs of w with their tags. Cost: O(len(w))."""
    out: list[tuple[str, str]] = []
    i = 0
    while i < len(w):
        t = tag_of(w[i])
        j = i + 1
        while j < len(w) and tag_of(w[j]) == t:
            j += 1
        out.append((t, w[i:j]))
        i = j
    return out


def structure_of(segs: list[tuple[str, str]]) -> Structure:
    return tuple((t, len(x)) for t, x in segs)


def train(passwords: list[str]) -> PCFGModel:
    """Relative frequencies of the base structures and of the runs.

    Precondition: at least one non-empty password. Cost: O(N) for N characters.
    """
    s_count: dict = {}
    r_count: dict = {}
    for w in passwords:
        if not w:
            continue
        segs = segment(w)
        s = structure_of(segs)
        s_count[s] = s_count.get(s, 0) + 1
        for t, x in segs:
            d = r_count.setdefault((t, len(x)), {})
            d[x] = d.get(x, 0) + 1
    total = sum(s_count.values())
    if total == 0:
        raise ValueError("the training list has no non-empty password")
    structures = {s: Fraction(c, total) for s, c in s_count.items()}
    runs = {}
    for key, d in r_count.items():
        n = sum(d.values())
        runs[key] = {x: Fraction(c, n) for x, c in d.items()}
    return PCFGModel(structures, runs)


def probability(m: PCFGModel, w: str) -> Fraction:
    """PCFG-SCORE of the page, as an exact probability. Cost: O(len(w))."""
    segs = segment(w)  # @line L1
    s = structure_of(segs)  # @line L2
    p = m.structures.get(s, Fraction(0))  # @line L3
    for t, x in segs:  # @line L4
        p *= m.runs.get((t, len(x)), {}).get(x, Fraction(0))  # @line L5
    return p  # @line L6


def strength_bits(m: PCFGModel, w: str) -> float:
    """-log2 P(w); infinite when the model gives w probability 0."""
    p = probability(m, w)
    if p == 0:
        return math.inf
    return math.log2(p.denominator) - math.log2(p.numerator)


def count_above(m: PCFGModel, t: Fraction) -> int:
    """The number of strings v with P(v) > t, for t > 0.

    For each structure, it walks the runs of each slot in decreasing order of
    probability and stops as soon as even the best choice for the remaining
    slots cannot beat t. Cost: O(r) per string counted plus the cut-offs, for
    structures of at most r slots.
    """
    if t <= 0:
        raise ValueError("the threshold must be positive")
    total = 0
    for s, ps in m.structures.items():
        lists = [sorted(m.runs[key].values(), reverse=True) for key in s]
        best_rest = [Fraction(1)] * (len(s) + 1)  # product of the best choice of slots i..r-1
        for i in range(len(s) - 1, -1, -1):
            best_rest[i] = best_rest[i + 1] * lists[i][0]
        stack = [(0, ps)]
        while stack:
            i, p = stack.pop()
            if i == len(s):
                total += 1
                continue
            for q in lists[i]:
                if p * q * best_rest[i + 1] <= t:
                    break  # the lists are sorted, so no later choice is better
                stack.append((i + 1, p * q))
    return total


def guess_number(m: PCFGModel, w: str) -> int:
    """1 + the number of strings more probable than w. Precondition: P(w) > 0."""
    p = probability(m, w)
    if p == 0:
        raise ValueError("the model gives this password probability 0")
    return count_above(m, p) + 1
