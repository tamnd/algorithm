# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-lateness-minimization/. The authors are listed in prov/BNQ857.jsonl.

"""Maximum lateness on one machine with release dates.

schrage: the non-preemptive heuristic in the delivery time form, a
2-approximation for 1|r_j|max(C_j + q_j) with q_j >= 0.
preemptive_edd: the exact rule for 1|r_j,pmtn|Lmax.
"""

import heapq
from typing import Sequence


def schrage(p: Sequence[int], r: Sequence[int], q: Sequence[int]) -> tuple[list[int], list[int], int]:
    """Whenever the machine is free, start the released job with the largest delivery time.

    Returns (order, start times, max_j (C_j + q_j)). Time O(n log n).
    """
    n = len(p)
    if not (len(r) == len(q) == n):
        raise ValueError("p, r and q must have the same length")
    if any(x < 0 for x in p) or any(x < 0 for x in q):
        raise ValueError("p and q must be nonnegative")
    by_release = sorted(range(n), key=lambda j: r[j])
    t, i = 0, 0  # @line L1
    heap: list[tuple[int, int]] = []
    order: list[int] = []
    start = [0] * n
    value = None
    while i < n or heap:  # @line L2
        while i < n and r[by_release[i]] <= t:  # @line L3
            j = by_release[i]
            heapq.heappush(heap, (-q[j], j))
            i += 1
        if not heap:  # @line L4
            t = r[by_release[i]]
            continue
        _, j = heapq.heappop(heap)  # @line L5
        start[j] = max(t, r[j])  # @line L6
        t = start[j] + p[j]
        order.append(j)
        if value is None or t + q[j] > value:
            value = t + q[j]
    return order, start, (0 if value is None else value)  # @line L7


def delivery_value(p: Sequence[int], r: Sequence[int], q: Sequence[int], order: Sequence[int]) -> int:
    """max_j (C_j + q_j) when the order runs without unforced idle time."""
    t, best = 0, None
    for j in order:
        t = max(t, r[j]) + p[j]
        if best is None or t + q[j] > best:
            best = t + q[j]
    return 0 if best is None else best


def lateness_value(p: Sequence[int], r: Sequence[int], d: Sequence[int], order: Sequence[int]) -> int:
    """L_max of the order when it runs without unforced idle time (None for no jobs)."""
    t, best = 0, None
    for j in order:
        t = max(t, r[j]) + p[j]
        if best is None or t - d[j] > best:
            best = t - d[j]
    return best


def preemptive_edd(p: Sequence[int], r: Sequence[int], d: Sequence[int]) -> tuple[list[tuple[int, int, int]], list[int], int]:
    """At each moment run the released, unfinished job with the earliest due date.

    Returns (pieces as (job, from, to), completion times, L_max). Exact for
    1|r_j,pmtn|Lmax. Time O(n log n): a job is preempted only at a release.
    """
    n = len(p)
    if not (len(r) == len(d) == n):
        raise ValueError("p, r and d must have the same length")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    by_release = sorted(range(n), key=lambda j: r[j])
    rem = list(p)
    comp = [0] * n
    pieces: list[tuple[int, int, int]] = []
    heap: list[tuple[int, int]] = []
    t, i = 0, 0
    while i < n or heap:
        while i < n and r[by_release[i]] <= t:
            j = by_release[i]
            heapq.heappush(heap, (d[j], j))
            i += 1
        if not heap:
            t = r[by_release[i]]
            continue
        _, j = heap[0]
        nxt = r[by_release[i]] if i < n else None
        run = rem[j] if nxt is None else min(rem[j], nxt - t)
        if run > 0:
            if pieces and pieces[-1][0] == j and pieces[-1][2] == t:
                pieces[-1] = (j, pieces[-1][1], t + run)
            else:
                pieces.append((j, t, t + run))
        t += run
        rem[j] -= run
        if rem[j] == 0:
            heapq.heappop(heap)
            comp[j] = t
    lmax = max((comp[j] - d[j] for j in range(n)), default=None)
    return pieces, comp, lmax
