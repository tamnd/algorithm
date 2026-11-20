# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instant-runoff-voting/. The authors are listed in prov/P7TC87.jsonl.

from typing import Sequence

Ranking = Sequence[int]


def instant_runoff_rounds(profile: Sequence[Ranking], m: int) -> tuple[int, list[tuple[list[int], int]]]:
    """Run instant-runoff voting and return (winner, rounds).

    The candidates are 0, ..., m - 1 (m >= 1). Each ballot ranks distinct candidates, best
    first; a ballot may be truncated and leave some candidates out, and it is exhausted when
    none of its candidates is still in the race. Each entry of rounds is (count, x): count[a]
    is the number of ballots on the pile of a in that round (0 for eliminated candidates), and
    x is the candidate eliminated in that round, or -1 in the last round.

    The count stops when a continuing candidate has more than half of the ballots that are not
    exhausted, or when one candidate is left. Among the continuing candidates with the fewest
    ballots, the one with the largest index is eliminated, so that the smallest index wins a
    final tie. Time O(L + m^2) with L the total length of the ballots, which is O(n m + m^2)
    for full rankings; extra space O(n + m).
    """
    continuing = [True] * m  # @line L1
    ptr = [0] * len(profile)
    piles: list[list[int]] = [[] for _ in range(m)]
    for i, r in enumerate(profile):  # @line L2
        if len(r) > 0:
            piles[r[0]].append(i)
    left = m
    rounds = []
    while True:  # @line L3
        active = sum(len(piles[a]) for a in range(m) if continuing[a])  # @line L4
        count = [len(piles[a]) if continuing[a] else 0 for a in range(m)]
        for a in range(m):  # @line L5
            if continuing[a] and (2 * count[a] > active or left == 1):
                rounds.append((count, -1))
                return a, rounds  # @line L6
        x = -1
        for a in range(m):  # @line L7
            if continuing[a] and (x == -1 or count[a] <= count[x]):
                x = a
        rounds.append((count, x))
        continuing[x] = False  # @line L8
        left -= 1
        for i in piles[x]:  # @line L9
            r = profile[i]
            ptr[i] += 1
            while ptr[i] < len(r) and not continuing[r[ptr[i]]]:  # @line L10
                ptr[i] += 1
            if ptr[i] < len(r):  # @line L11
                piles[r[ptr[i]]].append(i)
        piles[x] = []


def instant_runoff(profile: Sequence[Ranking], m: int) -> int:
    """Return the instant-runoff winner, with the tie rules of instant_runoff_rounds."""
    return instant_runoff_rounds(profile, m)[0]
