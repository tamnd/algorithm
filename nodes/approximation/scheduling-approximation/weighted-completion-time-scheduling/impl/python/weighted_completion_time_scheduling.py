# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-completion-time-scheduling/. The authors are listed in prov/Y1GCMZ.jsonl.

"""Weighted completion time: Smith's rule, WSPT list scheduling on m machines,
and the SRPT conversion, a 2-approximation for 1|r_j|sum C_j."""

import heapq
from fractions import Fraction
from typing import Sequence


def wspt_order(p: Sequence[int], w: Sequence[int]) -> list[int]:
    """Jobs by nondecreasing p_j / w_j (Smith's rule); jobs with w_j = 0 go last."""
    return sorted(range(len(p)), key=lambda j: (w[j] == 0, Fraction(p[j], w[j]) if w[j] else 0, j))


def weighted_sum(p, w, order, r=None) -> int:
    """sum_j w_j C_j for the order on one machine, each job started as early as possible."""
    t, s = 0, 0
    for j in order:
        t = (t if r is None else max(t, r[j])) + p[j]
        s += w[j] * t
    return s


def wspt_list(p: Sequence[int], w: Sequence[int], m: int) -> tuple[list[list[int]], int]:
    """Take the jobs in WSPT order and put each on the machine that is free first.

    A (1 + sqrt 2)/2-approximation for P||sum w_j C_j (Kawaguchi and Kyan 1986).
    """
    loads = [(0, i) for i in range(m)]
    machines: list[list[int]] = [[] for _ in range(m)]
    total = 0
    for j in wspt_order(p, w):
        t, i = heapq.heappop(loads)
        machines[i].append(j)
        total += w[j] * (t + p[j])
        heapq.heappush(loads, (t + p[j], i))
    return machines, total


def srpt(p: Sequence[int], r: Sequence[int]) -> list[int]:
    """Completion times of the preemptive SRPT schedule, optimal for 1|r_j,pmtn|sum C_j."""
    n = len(p)
    by_release = sorted(range(n), key=lambda j: r[j])
    comp = [0] * n
    heap: list[tuple[int, int]] = []
    t, i = 0, 0
    while i < n or heap:
        while i < n and r[by_release[i]] <= t:
            j = by_release[i]
            heapq.heappush(heap, (p[j], j))
            i += 1
        if not heap:
            t = r[by_release[i]]
            continue
        rem, j = heapq.heappop(heap)
        nxt = r[by_release[i]] if i < n else None
        if nxt is None or t + rem <= nxt:
            t += rem
            comp[j] = t
        else:
            heapq.heappush(heap, (rem - (nxt - t), j))
            t = nxt
    return comp


def srpt_conversion(p: Sequence[int], r: Sequence[int]) -> tuple[list[int], list[int], int]:
    """2-approximation for 1|r_j|sum C_j (Phillips, Stein and Wein 1998).

    Returns (order, completion times, sum of completion times).
    """
    n = len(p)
    if len(r) != n:
        raise ValueError("p and r must have the same length")
    if any(x < 0 for x in p) or any(x < 0 for x in r):
        raise ValueError("p and r must be nonnegative")
    cp = srpt(p, r)  # @line L1
    order = sorted(range(n), key=lambda j: (cp[j], j))  # @line L2
    t = 0  # @line L3
    comp = [0] * n
    for j in order:  # @line L4
        t = max(t, r[j]) + p[j]  # @line L5
        comp[j] = t
    return order, comp, sum(comp)  # @line L6
