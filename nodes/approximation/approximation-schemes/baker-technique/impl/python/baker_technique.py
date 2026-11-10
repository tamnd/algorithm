# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baker-technique/. The authors are listed in prov/2A03SS.jsonl.

"""Baker's layering technique on a graph given as adjacency sets, with breadth-first levels.

baker_max deletes one class of levels (for maximization, such as independent set); baker_min uses pieces of
k + 1 levels that overlap in one class (for minimization, such as vertex cover). The pieces are solved by a
given exact solver."""

from collections import deque
from typing import Callable, Optional, Sequence

Graph = Sequence[set]
Solver = Callable[[Graph, list[int]], set]


def bfs_levels(adj: Graph) -> list[int]:
    """The breadth-first level of each vertex; each component starts at level 0 from its least vertex."""
    level = [-1] * len(adj)
    for root in range(len(adj)):
        if level[root] >= 0:
            continue
        level[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
    return level


def baker_max(adj: Graph, k: int, solve: Solver, stats: Optional[dict] = None) -> set:
    """Delete the levels = r (mod k), solve each band of k - 1 levels, keep the best r. For independent set."""
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
            sol |= solve(adj, band)  # @line L5
        values.append(len(sol))
        if best is None or len(sol) > len(best):  # @line L6
            best = sol
    if stats is not None:
        stats["values"] = values
    return best if best is not None else set()  # @line L7


def baker_min(adj: Graph, k: int, solve: Solver, stats: Optional[dict] = None) -> set:
    """Pieces of the k + 1 levels r + jk, ..., r + (j + 1)k, which overlap in the levels = r (mod k); keep the best r.
    For vertex cover: every edge joins equal or adjacent levels, so it lies inside some piece."""
    level = bfs_levels(adj)
    best: Optional[set] = None
    values = []
    for r in range(k):
        pieces: dict[int, list[int]] = {}
        for v in range(len(adj)):
            j = (level[v] - r) // k
            pieces.setdefault(j, []).append(v)
            if (level[v] - r) % k == 0:
                pieces.setdefault(j - 1, []).append(v)  # a boundary level belongs to two pieces
        sol: set = set()
        for piece in pieces.values():
            sol |= solve(adj, piece)
        values.append(len(sol))
        if best is None or len(sol) < len(best):
            best = sol
    if stats is not None:
        stats["values"] = values
    return best if best is not None else set()


def exact_independent_set(adj: Graph, vertices: list[int]) -> set:
    """A maximum independent set of the induced subgraph, by branching on a vertex of highest degree (small inputs)."""
    vs = sorted(vertices)
    idx = {v: i for i, v in enumerate(vs)}
    nb = [0] * len(vs)
    for v in vs:
        for u in adj[v]:
            if u in idx:
                nb[idx[v]] |= 1 << idx[u]
    best = [0]
    stack = [((1 << len(vs)) - 1, 0)]
    while stack:
        cand, chosen = stack.pop()
        if bin(chosen).count("1") + bin(cand).count("1") <= bin(best[0]).count("1"):
            continue
        if cand == 0:
            best[0] = chosen
            continue
        i = max((j for j in range(len(vs)) if cand >> j & 1), key=lambda j: bin(nb[j] & cand).count("1"))
        if nb[i] & cand == 0:
            stack.append((cand & ~(1 << i), chosen | 1 << i))
            continue
        stack.append((cand & ~(1 << i), chosen))
        stack.append((cand & ~(1 << i) & ~nb[i], chosen | 1 << i))
    return {vs[j] for j in range(len(vs)) if best[0] >> j & 1}


def exact_vertex_cover(adj: Graph, vertices: list[int]) -> set:
    """A minimum vertex cover of the induced subgraph: the complement of a maximum independent set."""
    return set(vertices) - exact_independent_set(adj, vertices)
