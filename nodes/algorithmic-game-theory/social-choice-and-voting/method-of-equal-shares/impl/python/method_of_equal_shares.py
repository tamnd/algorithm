# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/method-of-equal-shares/. The authors are listed in prov/KK2YJY.jsonl.
"""The method of equal shares (MES, first called Rule X) for approval ballots.

An approval profile is a sequence of n ballots, each a set of candidates (or projects) among
0, ..., m - 1. Every voter starts with an equal share of the total budget. A candidate c with
cost cost[c] is affordable if its supporters have at least cost[c] left. For an affordable
candidate, rho(c) is the least amount such that the supporters pay cost[c] in total when each
pays min(rho, its budget). Each round buys the affordable candidate with the least rho, ties
to the smallest index. For committees (all costs 1, budget k), the committee is completed by
seq-Phragmen started from the leftover budgets, as in Lackner and Skowron (Rule 11). Every
amount is an exact Fraction.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple


def rho(budgets: Sequence[Fraction], cost) -> Optional[Fraction]:
    """Return the least r with sum(min(r, b) for b in budgets) == cost, or None if sum < cost."""
    remaining = Fraction(cost)
    b = sorted(budgets)
    s = len(b)
    for j, x in enumerate(b):
        if x * (s - j) >= remaining:
            return remaining / (s - j)
        remaining -= x
    return None


def equal_shares_phase1(profile, m: int, budget, costs: Optional[Sequence] = None
                        ) -> Tuple[List[int], List[Fraction], List[Fraction]]:
    """Run the first phase. Return (order, rhos, leftover budgets of the voters).

    Each voter starts with budget / n. Costs default to 1 and must be positive.
    O(m n log n) arithmetic operations per round, at most m rounds.
    """
    n = len(profile)
    costs = [Fraction(1)] * m if costs is None else [Fraction(c) for c in costs]
    if any(c <= 0 for c in costs):
        raise ValueError("costs must be positive")
    supporters = [[i for i in range(n) if c in profile[i]] for c in range(m)]
    x = [Fraction(budget) / n] * n  # @line L1
    order, rhos = [], []
    chosen = [False] * m
    while True:  # @line L2
        best, best_rho = None, None
        for c in range(m):  # @line L3
            if chosen[c]:
                continue
            r = rho([x[i] for i in supporters[c]], costs[c])
            if r is not None and (best_rho is None or r < best_rho):  # @line L4
                best, best_rho = c, r
        if best is None:  # @line L5
            return order, rhos, x
        chosen[best] = True  # @line L6
        order.append(best)
        rhos.append(best_rho)
        for i in supporters[best]:  # @line L7
            x[i] -= min(best_rho, x[i])


def equal_shares(profile, m: int, k: int) -> Tuple[int, ...]:
    """Return the committee of size k elected by MES with seq-Phragmen completion, sorted."""
    return tuple(sorted(equal_shares_order(profile, m, k)[0]))


def equal_shares_order(profile, m: int, k: int) -> Tuple[Tuple[int, ...], int, List[Optional[Fraction]]]:
    """Return (order, phase1_size, completion_times) for committees: costs 1, budget k.

    The completion is seq-Phragmen with the starting loads -x_i, where x_i is the leftover
    budget of voter i; completion_times[j] is the time at which the j-th added candidate is
    bought (None for a candidate that no voter approves, added in index order at the end).
    """
    if not 0 <= k <= m:
        raise ValueError("need 0 <= k <= m")
    n = len(profile)
    if n == 0:
        return tuple(range(k)), 0, [None] * k
    order, _, x = equal_shares_phase1(profile, m, k)
    phase1 = len(order)
    supporters = [[i for i in range(n) if c in profile[i]] for c in range(m)]
    y = [-b for b in x]  # @line L8
    chosen = [c in order for c in range(m)]
    times = []
    while len(order) < k:  # @line L9
        best, best_t = None, None
        for c in range(m):
            if chosen[c] or not supporters[c]:
                continue
            t = (1 + sum((y[i] for i in supporters[c]), Fraction(0))) / len(supporters[c])
            if best_t is None or t < best_t:
                best, best_t = c, t
        if best is None:
            best = min(c for c in range(m) if not chosen[c])
        else:
            for i in supporters[best]:
                y[i] = best_t
        chosen[best] = True
        order.append(best)
        times.append(best_t)
    return tuple(order), phase1, times  # @line L10
