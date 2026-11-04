# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/held-karp-algorithm/. The authors are listed in prov/X3NDEJ.jsonl.

from typing import Sequence

INF = float("inf")


def held_karp(d: Sequence[Sequence[float]]) -> tuple[float, list[int]]:
    """Return (length, tour) of a shortest travelling salesman tour.

    d is an n by n matrix of distances, n >= 1; d[i][j] is the cost of the
    edge from city i to city j and need not be symmetric. The tour starts at
    city 0, lists every city once, and the edge back to 0 is implied.
    Time Theta(n^2 2^n), space Theta(n 2^n).
    """
    n = len(d)
    if n == 1:  # @line L1
        return 0, [0]
    m = n - 1  # cities 1 .. n-1 use bits 0 .. n-2
    full = (1 << m) - 1
    c = [[INF] * n for _ in range(1 << m)]
    p = [[-1] * n for _ in range(1 << m)]
    for j in range(1, n):  # @line L2
        c[1 << (j - 1)][j] = d[0][j]
        p[1 << (j - 1)][j] = 0
    for s in range(1, full + 1):  # @line L3
        if s & (s - 1) == 0:
            continue  # sets of size 1 were filled by line L2
        for j in range(1, n):  # @line L4
            bit = 1 << (j - 1)
            if not s & bit:
                continue
            r = s ^ bit
            best_val, best_i = INF, -1
            for i in range(1, n):  # @line L5
                if r & (1 << (i - 1)):
                    v = c[r][i] + d[i][j]
                    if v < best_val:
                        best_val, best_i = v, i
            c[s][j] = best_val
            p[s][j] = best_i  # @line L6
    best, last = INF, -1
    for j in range(1, n):  # @line L7
        v = c[full][j] + d[j][0]
        if v < best:
            best, last = v, j
    s, j, tour = full, last, []  # @line L8
    while j != 0:  # @line L9
        tour.append(j)  # @line L10
        s, j = s ^ (1 << (j - 1)), p[s][j]  # @line L11
    tour.reverse()
    return best, [0] + tour  # @line L12
