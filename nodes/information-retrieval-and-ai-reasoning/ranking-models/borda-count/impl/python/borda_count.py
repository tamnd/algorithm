# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/borda-count/. The authors are listed in prov/2CGC7D.jsonl.

from fractions import Fraction
from typing import Any, Hashable, Sequence

Ranking = Sequence[Hashable]


def borda_scores(rankings: Sequence[Ranking]) -> dict[Any, Fraction]:
    """Return the Borda score of each item of the union of the rankings.

    Each ranking lists distinct items, best first, and may be partial. With n items in
    the union, the item at rank i of a list gets n - i + 1 points. The items that a list
    leaves out share the points of the ranks |L| + 1 to n equally, so each gets
    (n - |L| + 1) / 2 points from that list.
    """
    union = {x for r in rankings for x in r}  # @line L1
    n = len(union)
    score = {x: Fraction(0) for x in union}  # @line L2
    for r in rankings:  # @line L3
        for i, x in enumerate(r, start=1):
            score[x] += n - i + 1  # @line L4
        rest = Fraction(n - len(r) + 1, 2)
        listed = set(r)
        for x in union - listed:
            score[x] += rest  # @line L5
    return score


def borda(rankings: Sequence[Ranking]) -> list[Any]:
    """Return the items sorted by Borda score, high first, ties by item."""
    score = borda_scores(rankings)
    return sorted(score, key=lambda x: (-score[x], x))  # @line L6
