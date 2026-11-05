# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-shortest-path-algorithm/. The authors are listed in prov/758800.jsonl.

import math
from collections.abc import Callable

INF = math.inf
Edge = tuple[int, int, float]


def generic_sssp(
    n: int,
    edges: list[Edge],
    s: int,
    choose: Callable[[list[int]], int] | None = None,
) -> tuple[list[float], list[int | None], int] | None:
    """Ford's generic method: relax tense edges, in any order, until none is left.

    The graph has the vertices 0 .. n-1 and the directed edges (u, v, w); weights may
    be negative. choose(tense) gets the indices of the tense edges and returns one of
    them; by default the first is taken. Returns (d, parent, relaxations), with
    d[v] = math.inf for vertices not reachable from s, or None if a cycle of negative
    weight is reachable from s (found when a label rests on a walk of n edges).
    Each step scans all edges, O(m); the number of steps depends on choose and can
    be exponential in n.
    """
    d: list[float] = [INF] * n  # @line L1
    parent: list[int | None] = [None] * n
    hops = [0] * n
    d[s] = 0  # @line L2
    steps = 0
    while True:
        tense = [k for k, (u, v, w) in enumerate(edges) if d[u] + w < d[v]]  # @line L3
        if not tense:
            break
        k = tense[0] if choose is None else choose(tense)  # @line L4
        u, v, w = edges[k]
        d[v] = d[u] + w  # @line L5
        parent[v] = u
        hops[v] = hops[u] + 1
        steps += 1
        if hops[v] >= n:  # @line L6
            return None
    return d, parent, steps  # @line L7
