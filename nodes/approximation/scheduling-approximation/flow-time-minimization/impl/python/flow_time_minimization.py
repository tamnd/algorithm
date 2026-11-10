# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flow-time-minimization/. The authors are listed in prov/FGZ81Z.jsonl.

"""Flow time on one machine: SRPT for the total flow time with preemption,
and first in, first out (FIFO) for the maximum flow time."""

import heapq
from typing import Sequence


def srpt_flow(p: Sequence[int], r: Sequence[int]) -> tuple[list[int], int]:
    """Preemptive SRPT. Returns (completion times, total flow time sum_j (C_j - r_j)).

    Optimal for 1|r_j,pmtn|sum F_j. Ties go to the smaller remaining time, then the smaller index.
    """
    n = len(p)
    if len(r) != n or any(x < 0 for x in p) or any(x < 0 for x in r):
        raise ValueError("need nonnegative p and r of the same length")
    by_release = sorted(range(n), key=lambda j: (r[j], j))  # @line L1
    heap: list[tuple[int, int]] = []
    comp = [0] * n
    t, i = 0, 0  # @line L2
    while i < n or heap:  # @line L3
        while i < n and r[by_release[i]] <= t:  # @line L4
            j = by_release[i]
            heapq.heappush(heap, (p[j], j))
            i += 1
        if not heap:
            t = r[by_release[i]]
            continue
        rem, j = heapq.heappop(heap)  # @line L5
        nxt = r[by_release[i]] if i < n else None
        if nxt is None or t + rem <= nxt:  # @line L6
            t += rem
            comp[j] = t
        else:
            heapq.heappush(heap, (rem - (nxt - t), j))
            t = nxt
    return comp, sum(comp[j] - r[j] for j in range(n))  # @line L7


def flows_of_order(p: Sequence[int], r: Sequence[int], order: Sequence[int]) -> list[int]:
    """Flow times when the jobs run whole in this order, each as early as possible."""
    flow = [0] * len(p)
    t = 0
    for j in order:
        t = max(t, r[j]) + p[j]
        flow[j] = t - r[j]
    return flow


def fifo_max_flow(p: Sequence[int], r: Sequence[int]) -> tuple[list[int], int]:
    """FIFO order and its maximum flow time; optimal for 1|r_j|F_max, with or without preemption."""
    order = sorted(range(len(p)), key=lambda j: (r[j], j))
    return order, max(flows_of_order(p, r, order), default=0)
