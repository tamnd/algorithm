# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welsh-powell-algorithm/. The authors are listed in prov/NAP2ZB.jsonl.

from collections.abc import Sequence


def welsh_powell_algorithm(adj: Sequence[Sequence[int]]) -> list[int]:
    """Color the vertices 0 .. n-1 of a simple undirected graph by the Welsh-Powell rule.

    adj[v] lists the neighbours of v (each edge is in both lists). The vertices are
    sorted by non-increasing degree, ties broken by the smaller index. Then color
    classes are built one at a time: a pass over the sorted list gives the current
    color to each uncolored vertex with no neighbour of that color. Returns the list
    of colors 1, 2, ..., k. Time O(n log n + n k + m) for k colors, extra space O(n).
    """
    n = len(adj)
    sigma = sorted(range(n), key=lambda v: (-len(adj[v]), v))  # @line L1
    c = [0] * n  # @line L2: 0 means not colored
    blocked = [0] * n  # blocked[v] == k means v has a neighbour of color k
    k = 0  # @line L3
    for i in range(n):  # @line L4
        if c[sigma[i]] == 0:  # @line L5
            k += 1  # @line L6
            for j in range(i, n):  # @line L7
                v = sigma[j]  # @line L8
                if c[v] == 0 and blocked[v] != k:  # @line L9
                    c[v] = k  # @line L10
                    for w in adj[v]:  # @line L11
                        blocked[w] = k
    return c  # @line L12
