# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dag-shortest-paths/. The authors are listed in prov/277N5Y.jsonl.

import math
from collections import deque


def topological_order(adj: list[list[tuple[int, float]]]) -> list[int]:
    """Kahn's algorithm. Raises ValueError if the graph has a directed cycle."""
    n = len(adj)
    indeg = [0] * n
    for u in range(n):
        for v, _ in adj[u]:
            indeg[v] += 1
    queue = deque(u for u in range(n) if indeg[u] == 0)
    order: list[int] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) < n:
        raise ValueError("the graph has a directed cycle")
    return order


def dag_shortest_paths(
    adj: list[list[tuple[int, float]]], s: int
) -> tuple[list[float], list[int | None]]:
    """Shortest-path distances from s in a directed acyclic graph with any real weights.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Negative weights are allowed. Precondition: the graph has no directed cycle
    (a ValueError is raised otherwise). d[v] is math.inf when v is unreachable.
    Time O(n + m), extra space O(n).
    """
    order = topological_order(adj)  # @line L1
    n = len(adj)
    d = [math.inf] * n  # @line L2
    parent: list[int | None] = [None] * n
    d[s] = 0  # @line L3
    for u in order:  # @line L4
        if d[u] != math.inf:  # @line L5
            for v, w in adj[u]:  # @line L6
                if d[u] + w < d[v]:  # @line L7
                    d[v] = d[u] + w  # @line L8
                    parent[v] = u
    return d, parent  # @line L9
