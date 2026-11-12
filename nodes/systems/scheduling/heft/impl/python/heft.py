# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heft/. The authors are listed in prov/PKPCT3.jsonl.

import heapq
from fractions import Fraction
from typing import NamedTuple, Sequence

Edge = tuple[int, int]


class Slot(NamedTuple):
    task: int
    proc: int
    start: Fraction
    finish: Fraction


def _graph(n: int, comm: dict[Edge, int]) -> tuple[list[list[int]], list[list[int]], list[int]]:
    succ: list[list[int]] = [[] for _ in range(n)]
    pred: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (i, j) in comm:
        succ[i].append(j)
        pred[j].append(i)
        indeg[j] += 1
    # Kahn's algorithm that takes the smallest ready index first
    topo, ready = [], [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(ready)
    while ready:
        i = heapq.heappop(ready)
        topo.append(i)
        for j in succ[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                heapq.heappush(ready, j)
    if len(topo) != n:
        raise ValueError("the task graph has a cycle")
    return succ, pred, topo


def upward_ranks(w: Sequence[Sequence[int]], comm: dict[Edge, int]) -> list[Fraction]:
    """rank_u(i) = mean_q w[i][q] + max over successors j of (comm[i, j] + rank_u(j)).

    comm[i, j] is the cost to send the data of edge i -> j between two different
    processors; it is the same for every pair of processors here, so it is also
    the mean cost. Exact fractions keep the ties exact.
    """
    n = len(w)
    succ, _, topo = _graph(n, comm)
    rank = [Fraction(0)] * n
    for i in reversed(topo):
        mean = Fraction(sum(w[i]), len(w[i]))
        rank[i] = mean + max((comm[(i, j)] + rank[j] for j in succ[i]), default=Fraction(0))  # @line L1
    return rank


def heft(w: Sequence[Sequence[int]], comm: dict[Edge, int]) -> tuple[list[Fraction], list[int], list[Slot]]:
    """HEFT (Topcuoglu, Hariri and Wu 2002).

    w[i][q] is the time of task i on processor q. Phase 1 sorts the tasks by
    decreasing upward rank. Phase 2 puts each task, in this order, on the
    processor that gives it the earliest finish time, and may insert it into an
    idle gap between two tasks already there. A transfer costs comm[i, j] when
    the two tasks run on different processors and 0 on the same processor.
    Return (ranks, task order, slots indexed by task).
    Cost: O(e q + n^2 q) time for n tasks, e edges and q processors.
    """
    n = len(w)
    nproc = len(w[0]) if n else 0
    _, pred, topo = _graph(n, comm)
    rank = upward_ranks(w, comm)
    pos = {t: x for x, t in enumerate(topo)}
    order = sorted(range(n), key=lambda i: (-rank[i], pos[i]))  # @line L2
    busy: list[list[tuple[Fraction, Fraction]]] = [[] for _ in range(nproc)]  # sorted (start, finish)
    slot: list = [None] * n
    for i in order:  # @line L3
        best = None
        for q in range(nproc):  # @line L4
            ready = max(  # @line L5
                (slot[j].finish + (0 if slot[j].proc == q else comm[(j, i)]) for j in pred[i]),
                default=Fraction(0),
            )
            # insertion policy: the first idle gap on q, at or after ready, that holds the task
            start = Fraction(ready)
            for s, f in busy[q]:  # @line L6
                if start + w[i][q] <= s:
                    break
                start = max(start, f)
            finish = start + w[i][q]  # @line L7
            if best is None or finish < best.finish:
                best = Slot(i, q, start, finish)
        slot[i] = best  # @line L8
        busy[best.proc].append((best.start, best.finish))
        busy[best.proc].sort()
    return rank, order, slot  # @line L9


def makespan(slots: Sequence[Slot]) -> Fraction:
    return max((s.finish for s in slots), default=Fraction(0))
