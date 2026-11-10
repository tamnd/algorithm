# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baker-planar-ptas/. The authors are listed in prov/N8D9ER.jsonl.

"""Baker's PTAS for maximum independent set and minimum vertex cover on planar graphs.

Levels are breadth-first levels. Each band is solved exactly by dynamic programming over the tree decomposition
of a minimum-degree elimination order: the bag of v is {v} plus its later neighbours S_v at elimination time."""

from collections import deque
from itertools import combinations
from typing import Optional, Sequence

Graph = Sequence[set]


def bfs_levels(adj: Graph) -> list[int]:
    level = [-1] * len(adj)
    for root in range(len(adj)):
        if level[root] < 0:
            level[root] = 0
            queue = deque([root])
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if level[v] < 0:
                        level[v] = level[u] + 1
                        queue.append(v)
    return level


def elimination(adj: Graph, vertices: Sequence[int]) -> tuple[list[int], dict[int, frozenset]]:
    """A minimum-degree elimination order of the induced subgraph and the later neighbours S_v of each v."""
    keep = set(vertices)
    g = {v: adj[v] & keep for v in vertices}
    order, later = [], {}
    while g:
        v = min(g, key=lambda u: (len(g[u]), u))
        nb = g.pop(v)
        for a in nb:
            g[a].discard(v)
            g[a] |= nb - {a}
        order.append(v)
        later[v] = frozenset(nb)
    return order, later


def max_independent_set(adj: Graph, vertices: Sequence[int], stats: Optional[dict] = None) -> set:
    """A maximum independent set of the subgraph induced by vertices, exactly, in time O(n 2^w w) for width w."""
    order, later = elimination(adj, vertices)  # @line L5
    pos = {v: i for i, v in enumerate(order)}
    children: dict[int, list[int]] = {v: [] for v in order}
    for v in order:
        if later[v]:
            children[min(later[v], key=pos.__getitem__)].append(v)
    table: dict[int, dict[frozenset, tuple[int, bool]]] = {}
    states = 0
    for v in order:  # @line L6
        sv = sorted(later[v])
        tv: dict[frozenset, tuple[int, bool]] = {}
        for size in range(len(sv) + 1):
            for t in combinations(sv, size):
                ts = frozenset(t)
                if any(b in adj[a] for a, b in combinations(t, 2)):
                    continue
                options = [(False, ts)]
                if not (adj[v] & ts):
                    options.append((True, ts | {v}))
                best = None
                for take, chosen in options:
                    val = int(take) + sum(table[c][chosen & later[c]][0] for c in children[v])
                    if best is None or val > best[0]:
                        best = (val, take)
                tv[ts] = best
        states += len(tv)
        table[v] = tv
    taken: dict[int, bool] = {}
    for v in reversed(order):  # @line L7
        ts = frozenset(u for u in later[v] if taken[u])
        taken[v] = table[v][ts][1]
    if stats is not None:
        stats["states"] = stats.get("states", 0) + states
        stats["bound"] = stats.get("bound", 0) + sum(2 ** len(later[v]) for v in order)
        stats["width"] = max([stats.get("width", 0)] + [len(later[v]) for v in order])
    return {v for v in order if taken[v]}


def baker_independent_set(adj: Graph, k: int, stats: Optional[dict] = None) -> set:
    """At least (1 - 1/k) OPT vertices, pairwise non-adjacent."""
    level = bfs_levels(adj)  # @line L1
    best: Optional[set] = None
    values = []
    for r in range(k):  # @line L2
        bands: dict[int, list[int]] = {}
        for v in range(len(adj)):
            if level[v] % k != r:  # @line L3
                bands.setdefault((level[v] - r) // k, []).append(v)  # @line L4
        sol: set = set()
        for band in bands.values():
            sol |= max_independent_set(adj, band, stats)  # @line L8
        values.append(len(sol))
        if best is None or len(sol) > len(best):  # @line L9
            best = sol
    if stats is not None:
        stats["values"] = values
    return best if best is not None else set()  # @line L10


def baker_vertex_cover(adj: Graph, k: int, stats: Optional[dict] = None) -> set:
    """At most (1 + 1/k) OPT vertices that touch every edge, from pieces of k + 1 levels."""
    level = bfs_levels(adj)
    best: Optional[set] = None
    values = []
    for r in range(k):
        pieces: dict[int, list[int]] = {}
        for v in range(len(adj)):
            j = (level[v] - r) // k
            pieces.setdefault(j, []).append(v)
            if (level[v] - r) % k == 0:
                pieces.setdefault(j - 1, []).append(v)
        sol: set = set()
        for piece in pieces.values():
            sol |= set(piece) - max_independent_set(adj, piece, stats)
        values.append(len(sol))
        if best is None or len(sol) < len(best):
            best = sol
    if stats is not None:
        stats["values"] = values
    return best if best is not None else set()
