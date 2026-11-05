# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra/. The authors are listed in prov/27XR9T.jsonl.

import heapq
import math


def dijkstra(
    adj: list[list[tuple[int, float]]], s: int
) -> tuple[list[float], list[int | None]]:
    """Return (d, parent): shortest-path distances from s and a shortest-path tree.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Precondition: every weight w is nonnegative (a ValueError is raised otherwise).
    d[v] is math.inf when v is not reachable from s, and parent[v] is then None.
    The queue is a binary heap with lazy deletion: an entry whose vertex is already
    done is skipped. Time O(n + m log m), which is O((n + m) log n) without parallel
    edges; extra space O(n + m).
    """
    n = len(adj)
    for u in range(n):
        for _, w in adj[u]:
            if w < 0:
                raise ValueError("Dijkstra's algorithm needs nonnegative weights")
    d = [math.inf] * n  # @line L1
    parent: list[int | None] = [None] * n
    done = [False] * n
    d[s] = 0  # @line L2
    q: list[tuple[float, int]] = [(0, s)]  # @line L3
    while q:  # @line L4
        _, u = heapq.heappop(q)  # @line L5
        if not done[u]:  # @line L6
            done[u] = True  # @line L7
            for v, w in adj[u]:  # @line L8
                if d[u] + w < d[v]:  # @line L9
                    d[v] = d[u] + w  # @line L10
                    parent[v] = u
                    heapq.heappush(q, (d[v], v))  # @line L11
    return d, parent  # @line L12
