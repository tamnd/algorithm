# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steiner-tree-inapproximability/. The authors are listed in prov/46CJ97.jsonl.
"""The Bern-Plassmann reduction from vertex cover to Steiner tree with edge lengths 1 and 2.

A graph is (n, edges). The Steiner instance has the vertices of the graph as Steiner points and its edges
as terminals. For small instances only: the solver tries every set of Steiner points.
"""

from itertools import combinations


def vc_to_steiner(n: int, edges: list[tuple[int, int]]) -> tuple[list[list[int]], list[int], list[int]]:
    """Points 0 .. n-1 are Steiner points, points n .. n+m-1 are terminals. Returns (d, steiner, terminals)."""
    m = len(edges)
    size = n + m
    d = [[0] * size for _ in range(size)]
    for p in range(size):
        for q in range(size):
            if p == q:
                continue
            if p < n and q < n:
                d[p][q] = 1
            elif p >= n and q >= n:
                d[p][q] = 2
            else:
                v, e = (p, q - n) if p < n else (q, p - n)
                d[p][q] = 1 if v in edges[e] else 2
    return d, list(range(n)), list(range(n, n + m))


def mst_weight(d: list[list[int]], points: list[int]) -> int:
    """Prim's algorithm on the complete graph over the given points."""
    if len(points) <= 1:
        return 0
    best = {p: d[points[0]][p] for p in points[1:]}
    total = 0
    while best:
        p = min(best, key=best.get)
        total += best.pop(p)
        for q in best:
            best[q] = min(best[q], d[p][q])
    return total


def steiner_opt(d: list[list[int]], steiner: list[int], terminals: list[int]) -> tuple[int, tuple[int, ...]]:
    """In a metric on a complete graph, the best Steiner tree is the best spanning tree over the terminals and some Steiner points."""
    best = (mst_weight(d, terminals), ())
    for size in range(1, len(steiner) + 1):
        for s in combinations(steiner, size):
            w = mst_weight(d, terminals + list(s))
            if w < best[0]:
                best = (w, s)
    return best


def tree_to_cover(edges: list[tuple[int, int]], s: tuple[int, ...]) -> set[int]:
    """The Steiner points used, plus one end of each edge that they miss.

    With no Steiner points, start from a vertex of degree at least 2, so that the cover has at most m - 1 vertices.
    """
    cover = set(s)
    if not cover:
        deg: dict[int, int] = {}
        for u, v in edges:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        cover.add(max(deg, key=deg.get))
    for u, v in edges:
        if u not in cover and v not in cover:
            cover.add(u)
    return cover


def vertex_cover_number(n: int, edges: list[tuple[int, int]]) -> int:
    for size in range(n + 1):
        for c in combinations(range(n), size):
            cs = set(c)
            if all(u in cs or v in cs for u, v in edges):
                return size
    return n


def is_connected(n: int, edges: list[tuple[int, int]]) -> bool:
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    seen, stack = {0}, [0]
    while stack:
        for y in adj[stack.pop()]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return len(seen) == n
