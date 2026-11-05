# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kahns-algorithm/. The authors are listed in prov/JVCQ4E.jsonl.

from collections import deque


def kahns_algorithm(adj: list[list[int]]) -> list[int] | None:
    """Return a topological ordering of the directed graph, or None if it has a cycle.

    The graph has the vertices 0 .. n-1 and the adjacency lists adj; parallel edges are
    allowed and each copy counts. Vertices of in-degree zero wait in a FIFO queue, which
    starts with them in the order 0 .. n-1. Time O(n + m), extra space O(n).
    """
    n = len(adj)
    indeg = [0] * n  # @line L1
    for u in range(n):  # @line L2
        for v in adj[u]:
            indeg[v] += 1
    queue: deque[int] = deque()  # @line L3
    order: list[int] = []
    for u in range(n):  # @line L4
        if indeg[u] == 0:
            queue.append(u)
    while queue:  # @line L5
        u = queue.popleft()  # @line L6
        order.append(u)
        for v in adj[u]:  # @line L7
            indeg[v] -= 1  # @line L8
            if indeg[v] == 0:  # @line L9
                queue.append(v)
    if len(order) < n:  # @line L10
        return None
    return order  # @line L11
