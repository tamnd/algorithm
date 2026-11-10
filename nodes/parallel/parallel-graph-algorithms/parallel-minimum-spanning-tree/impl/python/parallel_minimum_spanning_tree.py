# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-minimum-spanning-tree/. The authors are listed in prov/8WQPZV.jsonl.

"""Parallel Boruvka for the minimum spanning forest, simulated one round at a time.

Edges are compared by the key (weight, index), so all keys differ and the
minimum spanning forest for these keys is unique.

Precondition: n >= 0 and edges is a list of triples (u, v, w) with
0 <= u, v < n, u != v, and w a number. Parallel edges are allowed.
Cost: each round does O(m + n') work for the minima and the relabeling,
where n' is the number of supervertices with an edge, and O(n' log n') work for
pointer jumping; its span is O(log n). There are at most ceil(log2 n) rounds,
so W = O((n + m) log n) and S = O(log^2 n).
"""

import math


class Cost:
    """Counters for work, span and rounds."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0
        self.active: list[int] = []  # supervertices with an edge at the start of each round


def _lg(x: int) -> int:
    return max(1, math.ceil(math.log2(max(x, 2))))


def parallel_boruvka(n: int, edges: list[tuple[int, int, float]], cost: Cost | None = None) -> list[int]:
    """Return the sorted indices of the edges of the minimum spanning forest for the keys (weight, index)."""
    c = cost if cost is not None else Cost()
    F: list[int] = []  # @line L1
    E = [(u, v, (w, i)) for i, (u, v, w) in enumerate(edges)]
    V = sorted({u for u, _, _ in E} | {v for _, v, _ in E})
    P = list(range(n))
    while E:  # @line L2
        c.rounds += 1
        c.active.append(len(V))
        best: dict[int, tuple[float, int]] = {}
        other: dict[int, int] = {}
        for u, v, k in E:  # @line L3 (a min-reduce over the edges of each vertex)
            for a, b in ((u, v), (v, u)):
                if a not in best or k < best[a]:
                    best[a], other[a] = k, b
        c.work += 2 * len(E) + len(V)
        c.span += _lg(len(E))
        for v in V:  # @line L4
            P[v] = other[v]
        two_cycle = [v for v in V if P[P[v]] == v and v < P[v]]  # @line L5 (reads the P of line L4 only)
        for v in two_cycle:
            P[v] = v
        c.work += 2 * len(V)
        c.span += 2
        for v in V:  # @line L6
            if P[v] != v:
                F.append(best[v][1])
        c.work += len(V)
        c.span += 1
        while any(P[v] != P[P[v]] for v in V):  # @line L7
            nxt = {v: P[P[v]] for v in V}
            for v in V:
                P[v] = nxt[v]
            c.work += len(V)
            c.span += 1
        E = [(P[u], P[v], k) for u, v, k in E if P[u] != P[v]]  # @line L8 (a pack)
        c.work += len(E) + 1
        c.span += _lg(len(E) + 1)
        V = sorted({u for u, _, _ in E} | {v for _, v, _ in E})  # @line L9
        c.work += len(V) + 1
        c.span += _lg(len(V) + 1)
    return sorted(F)  # @line L10
