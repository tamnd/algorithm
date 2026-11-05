# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/highway-hierarchies/. The authors are listed in prov/B70115.jsonl.

import heapq
import math

INF = math.inf


def _dijkstra(adj, s: int) -> list[float]:
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


def _radius(dist: list[float], h: int) -> float:
    """Distance to the h-th closest vertex (the vertex itself is the first)."""
    finite = sorted(x for x in dist if x < INF)
    return finite[h - 1] if len(finite) >= h else INF


class HighwayLevel:
    """One level of a highway hierarchy: radii and the set of highway edges."""

    def __init__(self, rfwd, rbwd, highway) -> None:
        self.rfwd = rfwd  # forward neighborhood radius of each vertex
        self.rbwd = rbwd  # backward neighborhood radius of each vertex
        self.highway = highway  # set of (u, i): the i-th edge out of u is a highway edge


def hh_preprocess(adj: list[list[tuple[int, float]]], h: int) -> HighwayLevel:
    """Compute the highway network of adj for neighborhood size h >= 1.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Precondition: every weight is nonnegative (a ValueError is raised otherwise).
    An edge (u, v) is a highway edge if it lies on some shortest s-t path with v
    outside the forward neighborhood of s and u outside the backward neighborhood
    of t. This version tests the definition directly from all-pairs distances,
    O(n (m + n log n) + n^2 m) time, which is meant for checking, not for speed.
    """
    n = len(adj)
    radj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u in range(n):
        for v, w in adj[u]:
            if w < 0:
                raise ValueError("highway hierarchies need nonnegative weights")
            radj[v].append((u, w))
    dist = [_dijkstra(adj, s) for s in range(n)]
    rfwd = [_radius(dist[s], h) for s in range(n)]  # @line L1
    rbwd = [_radius([dist[x][t] for x in range(n)], h) for t in range(n)]
    highway = set()
    for u in range(n):
        for i, (v, w) in enumerate(adj[u]):
            for s in range(n):
                if dist[s][u] == INF or dist[s][v] <= rfwd[s]:
                    continue
                if any(
                    dist[s][t] < INF
                    and dist[s][u] + w + dist[v][t] == dist[s][t]
                    and dist[u][t] > rbwd[t]
                    for t in range(n)
                ):
                    highway.add((u, i))  # @line L2
                    break
    return HighwayLevel(rfwd, rbwd, highway)


def hh_query(
    adj: list[list[tuple[int, float]]], hw: HighwayLevel, s: int, t: int
) -> tuple[float, list[int] | None, int]:
    """Return (dist, path, scans) from s to t, or (math.inf, None, scans)."""
    n = len(adj)
    if s == t:
        return 0, [s], 0
    radj: list[list[tuple[int, float, bool]]] = [[] for _ in range(n)]
    out: list[list[tuple[int, float, bool]]] = [[] for _ in range(n)]
    for u in range(n):
        for i, (v, w) in enumerate(adj[u]):
            is_hw = (u, i) in hw.highway
            out[u].append((v, w, is_hw))
            radj[v].append((u, w, is_hw))
    graph = [out, radj]
    radius = [hw.rfwd[s], hw.rbwd[t]]
    dist = [[INF] * n, [INF] * n]
    pred: list[list[int | None]] = [[None] * n, [None] * n]
    done = [[False] * n, [False] * n]
    dist[0][s] = 0
    dist[1][t] = 0
    heaps = [[(0, s)], [(0, t)]]
    mu, meet, scans = INF, None, 0
    while True:
        side = min((0, 1), key=lambda i: heaps[i][0][0] if heaps[i] else INF)
        if not heaps[side] or heaps[side][0][0] >= mu:  # @line L6
            break
        du, u = heapq.heappop(heaps[side])
        if done[side][u]:
            continue
        done[side][u] = True
        scans += 1
        if du + dist[1 - side][u] < mu:  # @line L5
            mu, meet = du + dist[1 - side][u], u
        inside = du <= radius[side]  # u is in the neighborhood of the side's root
        for v, w, is_hw in graph[side][u]:  # @line L3
            if (inside or is_hw) and du + w < dist[side][v]:  # @line L4
                dist[side][v] = du + w
                pred[side][v] = u
                heapq.heappush(heaps[side], (dist[side][v], v))
    if meet is None:
        return INF, None, scans
    fwd = [meet]
    while fwd[-1] != s:
        fwd.append(pred[0][fwd[-1]])
    bwd = [meet]
    while bwd[-1] != t:
        bwd.append(pred[1][bwd[-1]])
    return mu, fwd[::-1] + bwd[1:], scans  # @line L7
