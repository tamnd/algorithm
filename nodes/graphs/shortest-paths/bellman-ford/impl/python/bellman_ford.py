# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-ford/. The authors are listed in prov/2PW2HK.jsonl.

import math


def bellman_ford(
    n: int, edges: list[tuple[int, int, float]], s: int
) -> tuple[list[float], list[int | None], list[int] | None]:
    """Single-source shortest paths with any real weights, and negative-cycle detection.

    The graph has the vertices 0 .. n-1 and the directed edges (u, v, w) of the list.
    Returns (d, parent, cycle). If no cycle of negative weight is reachable from s,
    cycle is None, d[v] is the distance from s (math.inf if v is unreachable) and the
    parent pointers form a shortest-path tree. Otherwise cycle lists the vertices of a
    negative cycle in path order (cycle[i] -> cycle[i + 1], and the last one -> the
    first one), and d and parent are not distances. Time O(n m), extra space O(n).
    """
    d = [math.inf] * n  # @line L1
    parent: list[int | None] = [None] * n
    d[s] = 0  # @line L2
    for _ in range(n - 1):  # @line L3
        changed = False  # @line L4
        for u, v, w in edges:  # @line L5
            if d[u] != math.inf and d[u] + w < d[v]:  # @line L6
                d[v] = d[u] + w  # @line L7
                parent[v] = u
                changed = True
        if not changed:  # @line L8
            return d, parent, None
    for u, v, w in edges:  # @line L9
        if d[u] != math.inf and d[u] + w < d[v]:  # @line L10
            d[v] = d[u] + w
            parent[v] = u
            x = v  # @line L11
            for _ in range(n):
                x = parent[x]  # type: ignore[assignment]
            cycle = [x]  # @line L12
            y = parent[x]
            while y != x:
                cycle.append(y)  # type: ignore[arg-type]
                y = parent[y]  # type: ignore[index]
            cycle.reverse()
            return d, parent, cycle
    return d, parent, None  # @line L13
