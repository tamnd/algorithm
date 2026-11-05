# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsatur/. The authors are listed in prov/4C0R37.jsonl.

from collections.abc import Sequence


def dsatur(adj: Sequence[Sequence[int]]) -> list[int]:
    """DSATUR coloring (Brelaz 1979) of a simple undirected graph.

    adj[v] lists the neighbours of v (vertices 0 .. n-1, each edge in both lists,
    no self-loops, no parallel edges). At each step it colors an uncolored vertex
    of largest saturation (number of distinct colors among its neighbours), ties
    broken by the largest number of uncolored neighbours, then by the smallest
    index. The vertex gets the smallest color in 1, 2, ... not used next to it.
    Returns the list of colors. Time O(n^2 + m), extra space O(n + m).
    """
    n = len(adj)
    c = [0] * n  # @line L1: 0 means not colored yet
    seen: list[set[int]] = [set() for _ in range(n)]  # colors next to v
    dunc = [len(adj[v]) for v in range(n)]  # uncolored neighbours of v
    for _ in range(n):  # @line L2
        v = -1  # @line L3
        for u in range(n):
            if c[u] == 0 and (v < 0 or (len(seen[u]), dunc[u]) > (len(seen[v]), dunc[v])):
                v = u
        k = 1  # @line L4
        while k in seen[v]:
            k += 1
        c[v] = k  # @line L5
        for w in adj[v]:  # @line L6
            if c[w] == 0:
                seen[w].add(k)  # @line L7
                dunc[w] -= 1  # @line L8
    return c  # @line L9
