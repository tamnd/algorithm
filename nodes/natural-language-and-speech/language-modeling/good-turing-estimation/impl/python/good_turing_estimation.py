# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/good-turing-estimation/. The authors are listed in prov/7B0QFN.jsonl.

"""Good-Turing estimation, exact in Fraction.

The input is a mapping from each seen type to its count r >= 1 in a sample
of N tokens. N_r is the number of types seen exactly r times. The adjusted
count of a type seen r times is r* = (r + 1) N_(r+1) / N_r, and the unseen
types get the total mass P_0 = N_1 / N.

Where the formula has no estimate (N_(r+1) = 0, or r > k for a cut-off k),
the code keeps r* = r. It then scales the seen probabilities so that they
sum to 1 - P_0, which makes the result a proper distribution.
"""

from collections import Counter
from fractions import Fraction
from typing import Hashable, Iterable, Mapping


def type_counts(tokens: Iterable[Hashable]) -> dict[Hashable, int]:
    """Count the tokens of a sample."""
    return dict(Counter(tokens))


def counts_of_counts(counts: Mapping[Hashable, int]) -> dict[int, int]:
    """Return {r: N_r} for the counts r >= 1 that occur."""
    out: Counter = Counter()
    for r in counts.values():
        if r < 1:
            raise ValueError("every count must be at least 1")
        out[r] += 1
    return dict(out)


def turing_counts(nr: Mapping[int, int], k: int | None = None) -> dict[int, Fraction]:
    """Return {r: r*}: r* = (r + 1) N_(r+1) / N_r where N_(r+1) > 0 and r <= k, else r* = r."""
    rstar = {}
    for r in sorted(nr):  # @line L3
        if (k is None or r <= k) and nr.get(r + 1, 0) > 0:
            rstar[r] = Fraction((r + 1) * nr[r + 1], nr[r])  # @line L4
        else:
            rstar[r] = Fraction(r)  # @line L5
    return rstar


def good_turing(counts: Mapping[Hashable, int], k: int | None = None):
    """Return (p, p0, rstar).

    p maps each seen type to its probability (a Fraction), p0 = N_1 / N is
    the total probability of all unseen types, and rstar maps r to r*.
    The values of p sum to 1 - p0, so p0 + sum(p) = 1 exactly.
    Cost: O(T) arithmetic operations for T seen types, after the counting.
    """
    if not counts:
        raise ValueError("empty sample")
    n = sum(counts.values())  # @line L1
    nr = counts_of_counts(counts)
    p0 = Fraction(nr.get(1, 0), n)  # @line L2
    rstar = turing_counts(nr, k)
    s = sum(nr[r] * rstar[r] for r in nr)  # @line L6
    p = {x: (1 - p0) * rstar[r] / s for x, r in counts.items()}  # @line L7
    return p, p0, rstar  # @line L8


def raw_good_turing(counts: Mapping[Hashable, int]) -> tuple[dict[Hashable, Fraction], Fraction]:
    """Return (p, p0) with p(x) = r* / N from the formula alone, so r* = 0 where N_(r+1) = 0.

    The most frequent type gets 0. With p0 the values sum to 1 exactly when
    every count s >= 2 that occurs has N_(s-1) > 0; otherwise mass is lost.
    """
    n = sum(counts.values())
    nr = counts_of_counts(counts)
    p = {x: Fraction((r + 1) * nr.get(r + 1, 0), nr[r] * n) for x, r in counts.items()}
    return p, Fraction(nr.get(1, 0), n)


def unseen_type_probability(p0: Fraction, num_unseen: int) -> Fraction:
    """Share the unseen mass equally among num_unseen >= 1 unseen types."""
    if num_unseen < 1:
        raise ValueError("there is no unseen type to receive the mass N_1 / N")
    return p0 / num_unseen
