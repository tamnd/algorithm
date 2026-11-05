# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnson/. The authors are listed in prov/GE9795.jsonl.

import heapq

Edge = tuple[int, int, float]


def bellman_ford_from_new_source(n: int, edges: list[Edge]) -> list[float] | None:
    """Distances from an added vertex q with an arc of weight 0 to each vertex.

    Returns None when the graph has a negative cycle. Time O(nm).
    """
    h = [0.0] * n  # round 1 relaxes the arcs q -> v of weight 0 and sets every label to 0
    if n == 0:
        return h
    # With n + 1 vertices, rounds 2 .. n make the labels final when there is no negative
    # cycle, so round n + 1 (the last pass of this loop) changes nothing.
    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if h[u] + w < h[v]:
                h[v] = h[u] + w
                changed = True
        if not changed:
            return h
    return None  # round n + 1 would still change a label


def dijkstra(n: int, adj: list[list[tuple[int, float]]], s: int) -> list[float | None]:
    """Dijkstra with a binary heap; all weights in adj must be nonnegative."""
    dist: list[float | None] = [None] * n
    best = [float("inf")] * n
    best[s] = 0.0
    pq = [(0.0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if dist[u] is not None:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] is None and d + w < best[v]:
                best[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def johnson(n: int, edges: list[Edge]) -> list[list[float | None]] | None:
    """All-pairs shortest paths on vertices 0 .. n-1 with arcs (u, v, w), w any real.

    Returns the matrix D with D[u][v] = delta(u, v), or None when v is not reachable
    from u. Returns None (no matrix) when the graph has a negative cycle.
    Time O(nm log n) with the binary heap used here, extra space O(n^2 + m).
    """
    # @line L1: the added vertex q is implicit: its arcs of weight 0 start every label at 0
    h = bellman_ford_from_new_source(n, edges)  # @line L2
    if h is None:  # @line L3
        return None
    # @line L4: h[v] = delta(q, v)
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:  # @line L5
        adj[u].append((v, w + h[u] - h[v]))
    dist: list[list[float | None]] = []
    for u in range(n):  # @line L6
        du = dijkstra(n, adj, u)  # @line L7
        row: list[float | None] = []
        for v in range(n):  # @line L8
            x = du[v]
            row.append(None if x is None else x - h[u] + h[v])
        dist.append(row)
    return dist  # @line L9
