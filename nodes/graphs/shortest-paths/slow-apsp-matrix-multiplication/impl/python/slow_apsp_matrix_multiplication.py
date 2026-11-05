# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slow-apsp-matrix-multiplication/. The authors are listed in prov/EK3RJN.jsonl.

import math

INF = math.inf


def weight_matrix(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]]:
    """W[i][i] = min(0, self-loops), W[i][j] = least weight of an arc i -> j, INF if none."""
    w = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, c in edges:
        if c < w[u][v]:
            w[u][v] = c
    return w


def extend(l: list[list[float]], w: list[list[float]]) -> list[list[float]]:
    """One min-plus product: walks of at most r arcs times one more arc (or none)."""
    n = len(l)
    out = [[INF] * n for _ in range(n)]  # @line L6
    for i in range(n):  # @line L7
        li, oi = l[i], out[i]
        for j in range(n):
            best = INF
            for k in range(n):  # @line L8
                cand = li[k] + w[k][j]
                if cand < best:
                    best = cand
            oi[j] = best
    return out  # @line L9


def slow_apsp(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]] | None:
    """All-pairs distances by n - 1 min-plus products; INF marks an unreachable pair.

    Vertices are 0 .. n-1 and edges are (u, v, weight) with any real weights.
    Returns None when the graph has a negative cycle. Time Θ(n^4), space Θ(n^2).
    """
    w = weight_matrix(n, edges)
    l = [row[:] for row in w]  # @line L1: walks with at most 1 arc
    for _ in range(2, n + 1):  # @line L2
        l = extend(l, w)  # @line L3
    if any(l[i][i] < 0 for i in range(n)):  # @line L4: n arcs are enough to close any cycle
        return None
    return l  # @line L5
