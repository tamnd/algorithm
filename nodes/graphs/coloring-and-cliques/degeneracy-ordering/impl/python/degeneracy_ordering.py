# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/degeneracy-ordering/. The authors are listed in prov/JTSFJW.jsonl.

from collections.abc import Sequence


def degeneracy_ordering(adj: Sequence[Sequence[int]]) -> tuple[list[int], int]:
    """Smallest-last ordering (Matula and Beck) of a simple undirected graph.

    adj[v] lists the neighbours of v (vertices 0 .. n-1, each edge in both lists,
    no self-loops, no parallel edges). Repeatedly removes a vertex of minimum
    degree in the remaining graph. Returns (removed, d): removed is the removal
    order, and d is the degeneracy, the largest degree a vertex had when it was
    removed. Each vertex has at most d neighbours that are removed after it, so
    greedy coloring in the order reversed(removed) uses at most d + 1 colors.
    Ties are broken by taking the vertex that entered its bucket last.
    Time O(n + m), extra space O(n).
    """
    n = len(adj)
    deg = [len(adj[v]) for v in range(n)]  # @line L1
    buckets: list[dict[int, None]] = [{} for _ in range(n)]
    for v in range(n):
        buckets[deg[v]][v] = None
    removed = [False] * n
    order: list[int] = []
    d = 0  # @line L2
    i = 0
    for _ in range(n):  # @line L3
        while not buckets[i]:  # @line L4
            i += 1
        v, _none = buckets[i].popitem()  # @line L5
        d = max(d, i)  # @line L6
        order.append(v)
        removed[v] = True
        for w in adj[v]:  # @line L7
            if not removed[w]:
                del buckets[deg[w]][w]  # @line L8
                deg[w] -= 1
                buckets[deg[w]][w] = None
        i = max(i - 1, 0)  # @line L9
    return order, d  # @line L10
