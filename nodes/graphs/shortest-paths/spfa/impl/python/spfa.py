# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spfa/. The authors are listed in prov/W784DG.jsonl.

from collections import deque


def spfa(
    adj: list[list[tuple[int, float]]], s: int
) -> tuple[list[float | None], list[int | None]] | None:
    """Single-source shortest paths with arbitrary real weights (SPFA).

    adj[u] lists the arcs (v, w) out of u, for vertices 0 .. n-1. Returns
    (dist, parent): dist[v] is the distance from s, or None when v is not
    reachable; parent[v] is the vertex before v on one shortest path. Returns
    None when a negative cycle is reachable from s. Negative cycles that s
    cannot reach do not matter. Worst-case time O(n m), extra space O(n).
    """
    n = len(adj)
    dist: list[float | None] = [None] * n  # @line L1: None stands for infinity
    parent: list[int | None] = [None] * n
    arcs = [0] * n  # number of arcs of the walk whose weight is dist[v]
    in_queue = [False] * n
    dist[s] = 0  # @line L2
    queue: deque[int] = deque([s])
    in_queue[s] = True
    while queue:  # @line L3
        u = queue.popleft()  # @line L4
        in_queue[u] = False
        du = dist[u]
        assert du is not None
        for v, w in adj[u]:  # @line L5
            dv = dist[v]
            if dv is None or du + w < dv:  # @line L6
                dist[v] = du + w  # @line L7
                parent[v] = u
                arcs[v] = arcs[u] + 1
                if arcs[v] >= n:  # @line L8: the walk repeats a vertex
                    return None
                if not in_queue[v]:  # @line L9
                    queue.append(v)
                    in_queue[v] = True
    return dist, parent  # @line L10
