# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apsp-repeated-squaring/. The authors are listed in prov/TRREJZ.jsonl.

import math

INF = math.inf


def apsp_repeated_squaring(
    n: int, edges: list[tuple[int, int, float]]
) -> list[list[float]] | None:
    """All-pairs shortest-path weights by repeated min-plus squaring.

    The graph has the vertices 0 .. n-1 and the directed edges (u, v, w); weights may
    be negative, and parallel edges and self-loops are allowed. Returns the distance
    matrix (math.inf for no path), or None if the graph has a cycle of negative
    weight. Time Θ(n^3 log n), extra space Θ(n^2).
    """
    L = [[INF] * n for _ in range(n)]  # @line L1
    for i in range(n):
        L[i][i] = 0
    for u, v, w in edges:  # @line L2
        if w < L[u][v]:
            L[u][v] = w
    k = 1  # @line L3
    while k < n:  # @line L4
        # L[i][i] <= 0 always, so the term t = i makes M start as a copy of L
        M = [row[:] for row in L]  # @line L5
        for i in range(n):  # @line L6
            Li, Mi = L[i], M[i]
            for t in range(n):
                lit = Li[t]
                if lit == INF:
                    continue
                Lt = L[t]
                for j in range(n):  # @line L7
                    if lit + Lt[j] < Mi[j]:
                        Mi[j] = lit + Lt[j]
        L = M  # @line L8
        k *= 2
    if any(L[i][i] < 0 for i in range(n)):  # @line L9
        return None
    return L  # @line L10
