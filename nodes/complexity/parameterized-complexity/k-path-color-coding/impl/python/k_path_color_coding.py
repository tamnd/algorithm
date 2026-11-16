# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-path-color-coding/. The authors are listed in prov/BTJ3GM.jsonl.
"""Color coding for k-path: find a simple path with k vertices.

colorful_path is COLORFUL-PATH of the page. It gets a coloring of the
vertices with the colors 0, ..., k-1 and finds a path with k vertices whose
colors are all different, by dynamic programming over (end vertex, color
set) pairs. A color set is a k-bit mask.

k_path is K-PATH of the page. It tries t random colorings. A fixed k-path
is colorful with probability k!/k^k, so t = ceil(ln(1/error) k^k/k!) trials
miss an existing path with probability at most error. A path that it
returns is always a real path, so the error is one-sided.

count_colorful_paths counts the colorful k-vertex paths as vertex
sequences. In an undirected graph each path with k >= 2 is counted twice,
once in each direction.

The graph is a mapping from each vertex to its neighbors. For a directed
graph, give the out-neighbors; the same code then finds directed paths.
"""

import math
import random
from collections.abc import Hashable, Iterable, Mapping, Sequence

Vertex = Hashable
Graph = Mapping[Vertex, Iterable[Vertex]]


def adjacency(vertices: Iterable[Vertex], edges: Iterable[tuple[Vertex, Vertex]]) -> dict[Vertex, list[Vertex]]:
    """Return the adjacency lists of the undirected graph with these vertices and edges."""
    adj: dict[Vertex, list[Vertex]] = {v: [] for v in vertices}
    for u, v in edges:
        if u == v:
            raise ValueError("self-loops are not allowed")
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    return adj


def _check(adj: Graph, colors: Mapping[Vertex, int], k: int) -> None:
    if k < 1:
        raise ValueError("k must be at least 1")
    for v in adj:
        if not 0 <= colors[v] < k:
            raise ValueError("colors must be in range(k)")


def colorful_path(adj: Graph, colors: Mapping[Vertex, int], k: int) -> list[Vertex] | None:
    """Return a path with k vertices of pairwise different colors, or None.

    D[v] maps a color set S to the predecessor of v on one colorful path
    that ends at v and uses exactly the colors in S (None for a path of one
    vertex). The pairs (v, S) are made layer by layer, by the size of S.
    """
    _check(adj, colors, k)
    table: dict[Vertex, dict[int, Vertex | None]] = {v: {} for v in adj}
    layer: list[tuple[Vertex, int]] = []
    for v in adj:
        table[v][1 << colors[v]] = None  # @line L1
        layer.append((v, 1 << colors[v]))
    for _ in range(k - 1):  # @line L2
        nxt: list[tuple[Vertex, int]] = []
        for u, s in layer:  # @line L3
            for v in adj[u]:
                bit = 1 << colors[v]
                if s & bit == 0 and (s | bit) not in table[v]:  # @line L4
                    table[v][s | bit] = u
                    nxt.append((v, s | bit))
        layer = nxt
    full = (1 << k) - 1
    for v, s in layer:
        if s == full:  # @line L5
            path = [v]
            while table[v][s] is not None:
                u = table[v][s]
                s ^= 1 << colors[v]
                v = u
                path.append(v)
            path.reverse()
            return path
    return None  # @line L6


def count_colorful_paths(adj: Graph, colors: Mapping[Vertex, int], k: int) -> int:
    """Return the number of vertex sequences that form a colorful path with k vertices.

    This is the counting form of the same table: N[v][S] is the number of
    colorful paths that end at v and use exactly the colors in S.
    """
    _check(adj, colors, k)
    count: dict[Vertex, dict[int, int]] = {v: {1 << colors[v]: 1} for v in adj}
    layer = {(v, 1 << colors[v]) for v in adj}
    for _ in range(k - 1):
        nxt: set[tuple[Vertex, int]] = set()
        for u, s in layer:
            c = count[u][s]
            for v in adj[u]:
                bit = 1 << colors[v]
                if s & bit == 0:
                    t = s | bit
                    count[v][t] = count[v].get(t, 0) + c
                    nxt.add((v, t))
        layer = nxt
    return sum(count[v][s] for v, s in layer)


def table_size(adj: Graph, colors: Mapping[Vertex, int], k: int) -> int:
    """Return the number of (v, S) pairs that COLORFUL-PATH sets, over all layers."""
    _check(adj, colors, k)
    seen = {(v, 1 << colors[v]) for v in adj}
    layer = set(seen)
    for _ in range(k - 1):
        nxt = set()
        for u, s in layer:
            for v in adj[u]:
                bit = 1 << colors[v]
                if s & bit == 0:
                    nxt.add((v, s | bit))
        seen |= nxt
        layer = nxt
    return len(seen)


def trials(k: int, error: float) -> int:
    """Return the number of colorings that K-PATH tries for a miss probability of at most error.

    One coloring finds a fixed k-path with probability at least p = k!/k^k,
    and (1 - p)^t <= exp(-p t), so t = ceil(ln(1/error) / p) is enough.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    if not 0 < error < 1:
        raise ValueError("error must be in (0, 1)")
    return math.ceil(math.log(1 / error) * k**k / math.factorial(k))


def k_path(adj: Graph, k: int, rng: random.Random, error: float = 1e-6) -> list[Vertex] | None:
    """Return a simple path with k vertices, or None.

    A returned path is always correct. If a k-path exists, None comes back
    with probability at most error.
    """
    t = trials(k, error)
    vertices: Sequence[Vertex] = list(adj)
    for _ in range(t):  # @line L7
        colors = {v: rng.randrange(k) for v in vertices}  # @line L8
        path = colorful_path(adj, colors, k)  # @line L9
        if path is not None:
            return path
    return None  # @line L10
