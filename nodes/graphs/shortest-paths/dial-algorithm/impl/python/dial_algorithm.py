# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dial-algorithm/. The authors are listed in prov/T0RAP2.jsonl.

import math

INF = math.inf


def dial(
    adj: list[list[tuple[int, int]]], s: int
) -> tuple[list[float], list[int | None]]:
    """Dijkstra's algorithm with a circular array of C + 1 buckets.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Precondition: every weight w is an integer with 0 <= w (a ValueError is raised
    otherwise); C is the largest weight. Returns (d, parent) with d[v] = math.inf and
    parent[v] = None for vertices not reachable from s. Bucket i mod (C + 1) holds
    the vertices with tentative distance i; an entry whose vertex already has a
    smaller label is stale and skipped. Time O(m + nC), extra space O(n + m + C).
    """
    n = len(adj)
    C = 0
    for u in range(n):
        for _, w in adj[u]:
            if not isinstance(w, int) or isinstance(w, bool) or w < 0:
                raise ValueError("Dial's algorithm needs nonnegative integer weights")
            C = max(C, w)
    d: list[float] = [INF] * n  # @line L1
    parent: list[int | None] = [None] * n
    buckets: list[list[int]] = [[] for _ in range(C + 1)]
    d[s] = 0  # @line L2
    buckets[0].append(s)
    i = 0  # @line L3
    left = 1
    while left > 0:  # @line L4
        while not buckets[i % (C + 1)]:  # @line L5
            i += 1
        u = buckets[i % (C + 1)].pop()  # @line L6
        left -= 1
        if d[u] < i:  # @line L7
            continue
        for v, w in adj[u]:  # @line L8
            if i + w < d[v]:  # @line L9
                d[v] = i + w  # @line L10
                parent[v] = u
                buckets[(i + w) % (C + 1)].append(v)
                left += 1
    return d, parent  # @line L11
