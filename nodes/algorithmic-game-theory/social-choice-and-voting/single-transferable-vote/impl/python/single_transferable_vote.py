# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-transferable-vote/. The authors are listed in prov/CH8C0N.jsonl.

from fractions import Fraction
from typing import Sequence

Ranking = Sequence[int]


def droop_quota(v: int, k: int) -> Fraction:
    """Return the Droop quota floor(v / (k + 1)) + 1 for v valid ballots and k seats."""
    return Fraction(v // (k + 1) + 1)


def hare_quota(v: int, k: int) -> Fraction:
    """Return the Hare quota v / k for v valid ballots and k seats."""
    return Fraction(v, k)


def stv_count(profile: Sequence[Ranking], m: int, k: int, quota: str = "droop"):
    """Run the single transferable vote and return (winners, log).

    The candidates are 0, ..., m - 1 and k >= 1 is the number of seats. Each ballot ranks
    distinct candidates, best first, and may be truncated. Surplus votes move by the
    inclusive Gregory rule: every ballot on the pile of an elected candidate e moves on with
    its weight multiplied by (t(e) - q) / t(e), where t(e) is the tally of e and q the quota.
    In a round, the continuing candidate with the largest tally is elected if it has at least
    q, ties to the smallest index; otherwise the continuing candidate with the smallest tally
    is eliminated, ties to the largest index. When the continuing candidates are no more than
    the empty seats, all of them are elected, by tally and then by index.

    winners lists the elected candidates in the order of election, min(k, m) of them. Each
    log entry is (action, candidate, tally), where action is "elect", "eliminate" or "fill",
    and tally is the list of the tallies of the continuing candidates at that moment (None for
    the others). All weights are exact fractions.
    """
    valid = [r for r in profile if len(r) > 0]
    v = len(valid)
    q = droop_quota(v, k) if quota == "droop" else hare_quota(v, k)  # @line L1
    continuing = [True] * m  # @line L2
    weight = [Fraction(1)] * v
    ptr = [0] * v
    piles: list[list[int]] = [[] for _ in range(m)]
    tally = [Fraction(0)] * m
    for i, r in enumerate(valid):  # @line L3
        piles[r[0]].append(i)
        tally[r[0]] += 1
    left = m
    winners: list[int] = []
    log = []

    def move(i: int) -> None:
        r = valid[i]
        ptr[i] += 1
        while ptr[i] < len(r) and not continuing[r[ptr[i]]]:
            ptr[i] += 1
        if ptr[i] < len(r):
            piles[r[ptr[i]]].append(i)
            tally[r[ptr[i]]] += weight[i]

    while len(winners) < k and left > 0:  # @line L4
        snapshot = [tally[a] if continuing[a] else None for a in range(m)]
        if left <= k - len(winners):  # @line L5
            rest = sorted((a for a in range(m) if continuing[a]), key=lambda a: (-tally[a], a))
            for a in rest:
                continuing[a] = False
                winners.append(a)
                log.append(("fill", a, snapshot))
            return winners, log  # @line L6
        e = -1
        for a in range(m):
            if continuing[a] and (e == -1 or tally[a] > tally[e]):
                e = a
        if tally[e] >= q and tally[e] > 0:  # @line L7
            continuing[e] = False  # @line L8
            left -= 1
            winners.append(e)
            log.append(("elect", e, snapshot))
            f = (tally[e] - q) / tally[e]  # @line L9
            if f > 0:
                for i in piles[e]:  # @line L10
                    weight[i] *= f
                    move(i)
            piles[e] = []
        else:
            x = -1
            for a in range(m):  # @line L11
                if continuing[a] and (x == -1 or tally[a] <= tally[x]):
                    x = a
            continuing[x] = False  # @line L12
            left -= 1
            log.append(("eliminate", x, snapshot))
            for i in piles[x]:  # @line L13
                move(i)
            piles[x] = []
    return winners, log  # @line L14


def single_transferable_vote(profile: Sequence[Ranking], m: int, k: int, quota: str = "droop") -> list[int]:
    """Return the k winners of the single transferable vote, in the order of election."""
    return stv_count(profile, m, k, quota)[0]
