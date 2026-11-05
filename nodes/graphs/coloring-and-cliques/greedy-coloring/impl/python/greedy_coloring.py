# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-coloring/. The authors are listed in prov/PM9EGC.jsonl.

from collections.abc import Sequence


def greedy_coloring(adj: Sequence[Sequence[int]], order: Sequence[int] | None = None) -> list[int]:
    """Color the vertices 0 .. n-1 greedily in the given order (default 0, 1, ..., n-1).

    adj[v] lists the neighbours of v in a simple undirected graph (each edge is in
    both lists). order is a permutation of the vertices. Each vertex gets the
    smallest color in 1, 2, ... that no earlier-colored neighbour has. Returns the
    list of colors. Time O(n + m), extra space O(n).
    """
    n = len(adj)
    if order is None:
        order = range(n)
    c = [0] * n  # @line L1: 0 means not colored yet
    used = [-1] * (n + 2)  # used[k] == v means color k is taken next to v
    for v in order:  # @line L2
        for w in adj[v]:  # @line L3
            if c[w] > 0:
                used[c[w]] = v  # @line L4
        k = 1  # @line L5
        while used[k] == v:  # @line L6
            k += 1
        c[v] = k  # @line L7
    return c  # @line L8
