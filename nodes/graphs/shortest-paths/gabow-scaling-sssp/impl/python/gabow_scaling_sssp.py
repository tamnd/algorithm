# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-scaling-sssp/. The authors are listed in prov/N36TQW.jsonl.

import math

INF = math.inf


def gabow_scaling(
    adj: list[list[tuple[int, int]]], s: int, trace: list | None = None
) -> tuple[list, list]:
    """Single-source shortest paths by bit scaling, for nonnegative integer weights.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Every weight must be an integer >= 0, or ValueError is raised. Returns (d,
    parent): d[v] is the distance from s (math.inf if v is unreachable) and parent[v]
    the previous vertex on a shortest path (None for s and unreachable vertices).
    If trace is a list, the labels after each scale are appended to it.
    Time O((n + m) log N) for the largest weight N, extra space O(n).
    """
    n = len(adj)
    top = 0
    for u in range(n):
        for _, w in adj[u]:
            if not isinstance(w, int) or w < 0:
                raise ValueError("weights must be nonnegative integers")
            top = max(top, w)
    b = top.bit_length()  # @line L1
    d: list = [INF] * n  # scale 0: all weights are 0
    parent: list = [None] * n
    d[s] = 0
    stack = [s]
    while stack:
        u = stack.pop()
        for v, _ in adj[u]:
            if d[v] == INF:
                d[v], parent[v] = 0, u
                stack.append(v)
    if trace is not None:
        trace.append(list(d))
    for i in range(1, b + 1):  # @line L2
        shift = b - i
        delta = [INF] * n
        par: list = [None] * n
        delta[s] = 0
        buckets: list[list[int]] = [[] for _ in range(n)]
        buckets[0].append(s)
        done = [False] * n
        for level in range(n):  # Dial's algorithm on the reduced lengths
            for u in buckets[level]:
                if done[u] or delta[u] != level:
                    continue
                done[u] = True
                for v, w in adj[u]:
                    wi = w >> shift  # @line L3
                    r = wi + 2 * d[u] - 2 * d[v]  # @line L4
                    nd = level + r
                    if nd < delta[v] and nd < n:  # @line L5
                        delta[v], par[v] = nd, u
                        buckets[nd].append(v)
        for v in range(n):
            if d[v] != INF:
                d[v] = 2 * d[v] + delta[v]  # @line L6
        parent = par
        if trace is not None:
            trace.append(list(d))
    return d, parent  # @line L7
