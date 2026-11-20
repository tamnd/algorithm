# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjusted-winner/. The authors are listed in prov/8XAEP1.jsonl.

from fractions import Fraction
from typing import Sequence

TOTAL = Fraction(100)


def adjusted_winner(pa: Sequence, pb: Sequence) -> list[Fraction]:
    """Brams and Taylor's adjusted winner for agents A and B.

    pa[g] and pb[g] are the nonnegative points of A and B on good g; each
    list sums to 100. Returns s, where s[g] is the share of good g that A
    gets and 1 - s[g] is the share of B. At most one s[g] is strictly
    between 0 and 1, and both agents get the same number of points.
    """
    p = [[Fraction(x) for x in pa], [Fraction(x) for x in pb]]
    m = len(p[0])
    if len(p[1]) != m or any(x < 0 for x in p[0] + p[1]):
        raise ValueError("two lists of the same length with nonnegative points")
    if sum(p[0]) != TOTAL or sum(p[1]) != TOTAL:
        raise ValueError("the points of each agent must sum to 100")
    s = [Fraction(1) if p[0][g] >= p[1][g] else Fraction(0) for g in range(m)]  # @line L1
    t = [sum(p[0][g] * s[g] for g in range(m)), sum(p[1][g] * (1 - s[g]) for g in range(m))]  # @line L2
    if t[0] == t[1]:  # @line L3
        return s
    w = 0 if t[0] > t[1] else 1  # @line L4
    lo = 1 - w

    def held_by_w(g: int) -> bool:
        return s[g] == 1 if w == 0 else s[g] == 0

    def ratio_key(g: int) -> tuple:
        # pW / pL in increasing order; pL = 0 means an infinite ratio
        if p[lo][g] == 0:
            return (1, Fraction(0), g)
        return (0, p[w][g] / p[lo][g], g)

    goods = sorted((g for g in range(m) if held_by_w(g) and p[w][g] > 0), key=ratio_key)  # @line L5
    for g in goods:  # @line L6
        if t[w] - p[w][g] >= t[lo] + p[lo][g]:  # @line L7
            share_to_lo = Fraction(1)
        else:
            share_to_lo = (t[w] - t[lo]) / (p[w][g] + p[lo][g])  # @line L8
        t[w] -= share_to_lo * p[w][g]
        t[lo] += share_to_lo * p[lo][g]
        s[g] = s[g] - share_to_lo if w == 0 else s[g] + share_to_lo
        if t[w] == t[lo]:
            break
    return s  # @line L9


def points(pa: Sequence, pb: Sequence, s: Sequence[Fraction]) -> tuple[Fraction, Fraction]:
    """The points of A and of B under the shares s."""
    ta = sum(Fraction(pa[g]) * s[g] for g in range(len(s)))
    tb = sum(Fraction(pb[g]) * (1 - s[g]) for g in range(len(s)))
    return ta, tb
