# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prim/. The authors are listed in prov/6NDZ9M.jsonl.

import heapq


def prim(n: int, edges: list[tuple[int, int, float]]) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge of weight w. Weights may be negative and may tie, the graph may be
    disconnected, and parallel edges and self-loops are allowed. Each tree
    is grown from its lowest-numbered vertex. If the graph is connected,
    the result has n - 1 edges and is a minimum spanning tree.

    Cost: O((n + m) log m) time with a binary heap that keeps stale
    entries, and O(n + m) extra space, where m = len(edges).
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v, _) in enumerate(edges):
        adj[u].append((v, i))
        if v != u:
            adj[v].append((u, i))
    inf = float("inf")
    key: list[float] = [inf] * n  # @line L1
    parent_edge: list[int | None] = [None] * n
    in_tree = [False] * n
    for r in range(n):  # @line L2
        if not in_tree[r]:  # @line L3
            key[r] = 0  # @line L4
            q: list[tuple[float, int]] = [(0, r)]
            while q:  # @line L5
                _, u = heapq.heappop(q)  # @line L6
                if in_tree[u]:  # @line L7: a stale entry
                    continue
                in_tree[u] = True  # @line L8
                for v, i in adj[u]:  # @line L9
                    w = edges[i][2]
                    if not in_tree[v] and w < key[v]:  # @line L10
                        key[v] = w  # @line L11
                        parent_edge[v] = i
                        heapq.heappush(q, (w, v))  # @line L12
    return [i for i in parent_edge if i is not None]  # @line L13
