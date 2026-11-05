# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alt-algorithm/. The authors are listed in prov/DBXZ34.jsonl.

import heapq
import math

INF = math.inf


def _dijkstra(adj: list[list[tuple[int, float]]], s: int) -> list[float]:
    """Plain Dijkstra with a lazy-deletion heap; distances from s."""
    d = [INF] * len(adj)
    d[s] = 0
    heap = [(0, s)]
    while heap:
        du, u = heapq.heappop(heap)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(heap, (d[v], v))
    return d


def alt_preprocess(
    adj: list[list[tuple[int, float]]], landmarks: list[int]
) -> list[tuple[list[float], list[float]]]:
    """For each landmark L, return (dist from L, dist to L).

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Precondition: every weight is nonnegative (a ValueError is raised otherwise).
    Time O(k (n + m) log m) for k landmarks, space O(k n).
    """
    n = len(adj)
    radj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u in range(n):
        for v, w in adj[u]:
            if w < 0:
                raise ValueError("ALT needs nonnegative weights")
            radj[v].append((u, w))
    tables = []
    for lm in landmarks:
        tables.append((_dijkstra(adj, lm), _dijkstra(radj, lm)))  # @line L1
    return tables


def _lower_bound(tables, v: int, t: int) -> float:
    """Landmark lower bound on dist(v, t); INF means that v cannot reach t."""
    h = 0
    for frm, to in tables:
        # dist(v, t) >= dist(v, L) - dist(t, L)
        if to[t] < INF:
            h = max(h, to[v] - to[t])
        # dist(v, t) >= dist(L, t) - dist(L, v)
        if frm[v] < INF:
            h = max(h, frm[t] - frm[v])
    return h


def alt_query(
    adj: list[list[tuple[int, float]]],
    tables: list[tuple[list[float], list[float]]],
    s: int,
    t: int,
) -> tuple[float, list[int] | None, int]:
    """Return (dist, path, scans): the distance from s to t, a shortest path, and
    the number of vertices scanned.

    tables comes from alt_preprocess on the same graph. If t is not reachable from s,
    returns (math.inf, None, scans). This is A* search with the landmark lower bound
    as heuristic, which is consistent, so each vertex is scanned at most once.
    """
    n = len(adj)
    h: list[float | None] = [None] * n  # computed on first touch

    def bound(v: int) -> float:
        if h[v] is None:
            h[v] = _lower_bound(tables, v, t)  # @line L2
        return h[v]

    g = [INF] * n
    parent: list[int | None] = [None] * n
    done = [False] * n
    g[s] = 0  # @line L3
    heap = [(bound(s), s)] if bound(s) < INF else []
    scans = 0
    while heap:  # @line L4
        _, u = heapq.heappop(heap)  # @line L5
        if done[u]:
            continue
        done[u] = True
        scans += 1
        if u == t:  # @line L6
            path = [t]
            while path[-1] != s:
                path.append(parent[path[-1]])
            return g[t], path[::-1], scans
        for v, w in adj[u]:  # @line L7
            if bound(v) < INF and g[u] + w < g[v]:  # @line L8
                g[v] = g[u] + w  # @line L9
                parent[v] = u
                heapq.heappush(heap, (g[v] + bound(v), v))
    return INF, None, scans  # @line L10
