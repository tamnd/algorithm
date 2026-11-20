# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plurality-voting/. The authors are listed in prov/WM09B3.jsonl.

from typing import Sequence

Ranking = Sequence[int]


def plurality_scores(profile: Sequence[Ranking], m: int) -> list[int]:
    """Return s with s[a] the number of voters who rank candidate a first.

    The candidates are 0, ..., m - 1 and each ranking lists them best first. Only the first
    entry of each ranking is read, so the time is O(n + m) for n voters.
    """
    s = [0] * m  # @line L1
    for r in profile:  # @line L2
        s[r[0]] += 1  # @line L3
    return s


def plurality_winners(profile: Sequence[Ranking], m: int) -> frozenset[int]:
    """Return the set of candidates with the most first places (the plurality correspondence)."""
    s = plurality_scores(profile, m)
    best = max(s)  # @line L4
    return frozenset(a for a in range(m) if s[a] == best)  # @line L5


def plurality(profile: Sequence[Ranking], m: int) -> int:
    """Return the plurality winner; a tie goes to the candidate with the smallest index.

    Precondition: m >= 1. With no voters every candidate has 0 first places, so candidate 0
    wins. Time O(n + m), extra space O(m).
    """
    return min(plurality_winners(profile, m))  # @line L6
