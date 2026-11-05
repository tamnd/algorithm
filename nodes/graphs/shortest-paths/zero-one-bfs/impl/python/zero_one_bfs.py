# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-one-bfs/. The authors are listed in prov/T8G377.jsonl.

from collections import deque


def zero_one_bfs(adj: list[list[tuple[int, int]]], s: int) -> tuple[list[int | None], list[int | None]]:
    """Single-source shortest paths when every arc weight is 0 or 1.

    adj[u] lists the arcs (v, w) out of u, for vertices 0 .. n-1, with w in {0, 1}.
    Returns (dist, parent): dist[v] is the distance from s, or None when v is not
    reachable; parent[v] is the vertex before v on one shortest path (None for s and
    for unreachable vertices). Raises ValueError on a weight other than 0 or 1, so a
    negative arc (and so a negative cycle) is rejected. Time O(n + m), extra space O(n + m).
    """
    n = len(adj)
    for u in range(n):
        for _, w in adj[u]:
            if w not in (0, 1):
                raise ValueError(f"arc weight {w} is not 0 or 1")
    dist: list[int | None] = [None] * n  # @line L1: None stands for infinity
    parent: list[int | None] = [None] * n
    done = [False] * n
    dist[s] = 0  # @line L2
    dq: deque[int] = deque([s])
    while dq:  # @line L3
        u = dq.popleft()  # @line L4
        if done[u]:  # @line L5: a stale copy of u
            continue
        done[u] = True  # @line L6
        du = dist[u]
        assert du is not None
        for v, w in adj[u]:  # @line L7
            dv = dist[v]
            if dv is None or du + w < dv:  # @line L8
                dist[v] = du + w  # @line L9
                parent[v] = u
                if w == 0:  # @line L10
                    dq.appendleft(v)
                else:
                    dq.append(v)  # @line L11
    return dist, parent  # @line L12
