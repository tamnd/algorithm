# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breadth-first-search/. The authors are listed in prov/HAEH1M.jsonl.

from collections import deque


def breadth_first_search(adj: list[list[int]], s: int) -> tuple[list[int | None], list[int | None]]:
    """Run BFS from s on the graph with vertices 0 .. n-1 and adjacency lists adj.

    Returns (dist, parent). dist[v] is the least number of edges on a path from s to v,
    or None when v is not reachable. parent[v] is the vertex before v on one shortest
    path (None for s and for unreachable vertices). The graph may be directed or
    undirected (an undirected edge is in both lists). Time O(n + m), extra space O(n).
    """
    n = len(adj)
    dist: list[int | None] = [None] * n  # @line L1: None stands for infinity
    parent: list[int | None] = [None] * n
    dist[s] = 0  # @line L2
    q = deque([s])  # @line L3
    while q:  # @line L4
        u = q.popleft()  # @line L5
        du = dist[u]
        assert du is not None
        for v in adj[u]:  # @line L6
            if dist[v] is None:  # @line L7
                dist[v] = du + 1  # @line L8
                parent[v] = u  # @line L9
                q.append(v)  # @line L10
    return dist, parent  # @line L11
