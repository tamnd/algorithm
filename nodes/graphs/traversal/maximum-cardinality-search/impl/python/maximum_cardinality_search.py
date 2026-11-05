# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-cardinality-search/. The authors are listed in prov/M2KXJV.jsonl.


def maximum_cardinality_search(adj: list[list[int]]) -> list[int]:
    """Return a maximum cardinality search order of a simple undirected graph.

    The graph has the vertices 0 .. n-1 and the adjacency lists adj, with each edge in
    both lists and no loops or parallel edges. Each step visits an unvisited vertex
    with the most visited neighbours. Ties go to the vertex that entered its bucket
    first, and the first bucket starts as 0 .. n-1, so the search starts at 0.
    Time O(n + m), extra space O(n).
    """
    n = len(adj)
    size = [0] * n  # @line L1
    visited = [False] * n
    buckets: list[dict[int, None]] = [{} for _ in range(n + 1)]
    buckets[0] = dict.fromkeys(range(n))
    j = 0
    order: list[int] = []
    for _ in range(n):  # @line L2
        v = next(iter(buckets[j]))  # @line L3
        del buckets[j][v]
        visited[v] = True  # @line L4
        order.append(v)
        for w in adj[v]:  # @line L5
            if not visited[w]:
                del buckets[size[w]][w]  # @line L6
                size[w] += 1
                buckets[size[w]][w] = None
        j += 1  # @line L7
        while j >= 0 and not buckets[j]:  # @line L8
            j -= 1
    return order  # @line L9
