# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-scheduling/. The authors are listed in prov/7BR0CN.jsonl.

"""Greedy scheduling of a computation DAG of unit-time strands on p processors.

At each time step the scheduler runs min(p, r) of the r ready strands. A
strand is ready when all its predecessors ran in earlier steps. The schedule
length T_p satisfies max(W/p, S) <= T_p <= (W - S)/p + S, where W is the
number of strands and S the number of strands on a longest path.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Any, Callable


def work_and_span(n: int, edges: list[tuple[int, int]]) -> tuple[int, int]:
    """Return (W, S) of the DAG with strands 0..n-1. Raise ValueError on a cycle."""
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        succ[u].append(v)
        indeg[v] += 1
    d = [1] * n
    queue = deque(v for v in range(n) if indeg[v] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in succ[u]:
            d[v] = max(d[v], d[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if seen < n:
        raise ValueError("the graph has a cycle")
    return n, max(d, default=0)


def greedy_schedule(
    n: int,
    edges: list[tuple[int, int]],
    p: int,
    rng: random.Random | None = None,
    priority: Callable[[int], Any] | None = None,
) -> list[list[int]]:
    """Return a greedy schedule: steps[t] is the list of strands run at step t + 1.

    Precondition: p >= 1 and the edges (u, v) on strands 0..n-1 form a DAG.
    Tie breaking among ready strands: by ``priority`` (smallest key first) if
    given, else uniformly at random with ``rng`` if given, else first ready,
    first run. Cost: Theta(n + m) for the first-ready rule, plus the cost of
    sorting or sampling the ready set for the other rules.
    """
    if p < 1:
        raise ValueError("p must be at least 1")
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:  # @line L1
        succ[u].append(v)
        indeg[v] += 1
    ready = deque(v for v in range(n) if indeg[v] == 0)  # @line L2
    steps: list[list[int]] = []  # @line L3
    while ready:  # @line L4
        k = min(p, len(ready))  # @line L5
        if priority is not None:  # @line L6
            pool = sorted(ready, key=priority)
            run, rest = pool[:k], pool[k:]
        elif rng is not None:
            pool = list(ready)
            rng.shuffle(pool)
            run, rest = pool[:k], pool[k:]
        else:
            run = [ready.popleft() for _ in range(k)]
            rest = list(ready)
        ready = deque(rest)  # @line L7
        newly: list[int] = []
        for u in run:  # @line L8
            for v in succ[u]:
                indeg[v] -= 1  # @line L9
                if indeg[v] == 0:  # @line L10
                    newly.append(v)
        ready.extend(newly)  # @line L11
        steps.append(run)  # @line L12
    if sum(len(s) for s in steps) < n:
        raise ValueError("the graph has a cycle")
    return steps  # @line L13
