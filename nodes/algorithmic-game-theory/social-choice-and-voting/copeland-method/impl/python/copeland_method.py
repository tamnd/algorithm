# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copeland-method/. The authors are listed in prov/D4PRR4.jsonl.

from fractions import Fraction
from typing import Sequence

Ranking = Sequence[int]


def pairwise_counts(profile: Sequence[Ranking], m: int) -> list[list[int]]:
    """Return N with N[a][b] the number of voters who rank a above b. Time O(n m^2)."""
    N = [[0] * m for _ in range(m)]  # @line L1
    for r in profile:
        for i, a in enumerate(r):
            for b in r[i + 1:]:
                N[a][b] += 1
    return N


def copeland_scores(profile: Sequence[Ranking], m: int) -> list[int]:
    """Return s with s[a] the number of majority contests a wins minus the number it loses.

    A contest with N[a][b] == N[b][a] is a tie and counts for neither side.
    """
    N = pairwise_counts(profile, m)
    s = [0] * m  # @line L2
    for a in range(m):  # @line L3
        for b in range(a + 1, m):
            if N[a][b] > N[b][a]:  # @line L4
                s[a] += 1
                s[b] -= 1
            elif N[b][a] > N[a][b]:  # @line L5
                s[b] += 1
                s[a] -= 1
    return s


def copeland_winners(profile: Sequence[Ranking], m: int) -> frozenset[int]:
    """Return the set of candidates with the highest Copeland score (the correspondence)."""
    s = copeland_scores(profile, m)
    best = max(s)
    return frozenset(a for a in range(m) if s[a] == best)  # @line L6


def copeland(profile: Sequence[Ranking], m: int) -> int:
    """Return the Copeland winner; a tie goes to the candidate with the smallest index.

    Precondition: m >= 1. Time O(n m^2), extra space O(m^2).
    """
    return min(copeland_winners(profile, m))  # @line L7


def copeland_ranking(profile: Sequence[Ranking], m: int) -> tuple[int, ...]:
    """Return the candidates sorted by Copeland score, highest first, ties to the smaller index."""
    s = copeland_scores(profile, m)
    return tuple(sorted(range(m), key=lambda a: (-s[a], a)))


def copeland_alpha_scores(profile: Sequence[Ranking], m: int, alpha: Fraction) -> list[Fraction]:
    """Return the Copeland^alpha scores: 1 for each win and alpha for each tie, 0 <= alpha <= 1.

    For alpha = 1/2 the score is (m - 1 + s[a]) / 2 with s the score of copeland_scores, so it
    orders the candidates in the same way.
    """
    N = pairwise_counts(profile, m)
    out = []
    for a in range(m):
        t = Fraction(0)
        for b in range(m):
            if b != a:
                if N[a][b] > N[b][a]:
                    t += 1
                elif N[a][b] == N[b][a]:
                    t += alpha
        out.append(t)
    return out
