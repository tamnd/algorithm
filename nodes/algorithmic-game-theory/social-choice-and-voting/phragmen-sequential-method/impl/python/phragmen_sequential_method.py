# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phragmen-sequential-method/. The authors are listed in prov/EVEFGB.jsonl.
"""Phragmen's sequential method (seq-Phragmen) for approval ballots.

An approval profile is a sequence of n ballots, each a set of candidates among 0, ..., m - 1.
Each elected candidate has a cost (load) of 1 that its supporters share. In each round the
method elects the candidate whose cost can be shared so that the largest load of its
supporters is smallest, and every supporter then carries that load. Ties go to the smallest
candidate index. Every load is an exact Fraction.
"""

from fractions import Fraction
from typing import List, Tuple


def seq_phragmen(profile, m: int, k: int) -> Tuple[Tuple[int, ...], List[Fraction], List[Fraction]]:
    """Return (order, times, loads).

    order lists the k elected candidates in the order of election, times[r] is the load at
    which order[r] was elected, and loads[i] is the final load of voter i. A candidate that
    no voter approves is elected only when no approved candidate is left; it costs nothing
    and its time is None. O(k (m n + sum of ballot sizes)) arithmetic operations.
    """
    if not 0 <= k <= m:
        raise ValueError("need 0 <= k <= m")
    n = len(profile)
    supporters = [[i for i in range(n) if c in profile[i]] for c in range(m)]
    y = [Fraction(0)] * n  # @line L1
    order, times = [], []
    chosen = [False] * m
    for _ in range(k):  # @line L2
        best, best_t = None, None
        for c in range(m):  # @line L3
            if chosen[c] or not supporters[c]:
                continue
            t = (1 + sum((y[i] for i in supporters[c]), Fraction(0))) / len(supporters[c])
            if best_t is None or t < best_t:  # @line L4
                best, best_t = c, t
        if best is None:
            best = min(c for c in range(m) if not chosen[c])
        chosen[best] = True  # @line L5
        order.append(best)
        times.append(best_t)
        if best_t is not None:
            for i in supporters[best]:  # @line L6
                y[i] = best_t
    return tuple(order), times, y  # @line L7


def phragmen_committee(profile, m: int, k: int) -> Tuple[int, ...]:
    """Return the committee of seq-Phragmen as a sorted tuple."""
    return tuple(sorted(seq_phragmen(profile, m, k)[0]))
