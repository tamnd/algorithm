# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-dijkstra/. The authors are listed in prov/BPW9SV.jsonl.

import heapq
import math

INF = math.inf


def bidirectional_dijkstra(
    adj: list[list[tuple[int, float]]], s: int, t: int
) -> tuple[float, list[int] | None]:
    """Return (dist, path): the distance from s to t and a shortest path.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Precondition: every weight w is nonnegative (a ValueError is raised otherwise).
    If t is not reachable from s, returns (math.inf, None). The forward search runs
    on adj from s, the backward search on the reversed edges from t, each a Dijkstra
    search with a lazy-deletion binary heap. At each step the side whose queue has
    the smaller minimum key moves. Time O(n + m log m), extra space O(n + m).
    """
    n = len(adj)
    radj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u in range(n):
        for v, w in adj[u]:
            if w < 0:
                raise ValueError("bidirectional Dijkstra needs nonnegative weights")
            radj[v].append((u, w))
    if s == t:
        return 0, [s]
    d = [[INF] * n, [INF] * n]  # @line L1
    parent: list[list[int | None]] = [[None] * n, [None] * n]
    done = [[False] * n, [False] * n]
    d[0][s] = 0
    d[1][t] = 0
    q: list[list[tuple[float, int]]] = [[(0, s)], [(0, t)]]  # @line L2
    mu = INF
    meet: tuple[int, int] | None = None  # an edge (a, b) with mu = d[0][a] + w + d[1][b]
    graph = (adj, radj)
    while True:  # @line L3
        top = [q[0][0][0] if q[0] else INF, q[1][0][0] if q[1] else INF]
        if top[0] + top[1] >= mu:  # @line L4
            break
        x = 0 if top[0] <= top[1] else 1  # @line L5
        y = 1 - x
        _, u = heapq.heappop(q[x])  # @line L6
        if done[x][u]:
            continue
        done[x][u] = True  # @line L7
        dx, dy = d[x], d[y]
        for v, w in graph[x][u]:  # @line L8
            if dx[u] + w < dx[v]:  # @line L9
                dx[v] = dx[u] + w
                parent[x][v] = u
                heapq.heappush(q[x], (dx[v], v))
            if v != u and dx[u] + w + dy[v] < mu:  # @line L10
                mu = dx[u] + w + dy[v]
                meet = (u, v) if x == 0 else (v, u)
    if meet is None:  # @line L11
        return INF, None
    a, b = meet
    front: list[int] = []
    x_: int | None = a
    while x_ is not None:
        front.append(x_)
        x_ = parent[0][x_]
    front.reverse()
    back: list[int] = []
    x_ = b
    while x_ is not None:
        back.append(x_)
        x_ = parent[1][x_]
    return mu, front + back
