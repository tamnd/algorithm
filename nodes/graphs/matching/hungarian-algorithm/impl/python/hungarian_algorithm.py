# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hungarian-algorithm/. The authors are listed in prov/N33C44.jsonl.

import math
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction, float]


def hungarian_algorithm(cost: list[list[Number]]) -> tuple[Number, list[int]] | None:
    """Minimum-cost assignment of the rows of an n x m matrix to distinct columns, n <= m.

    The graph is bipartite (rows and columns) and weighted; cost[i][j] is the cost of
    giving column j to row i. Costs may be negative. An entry math.inf marks a
    missing edge. Returns (total, assign) with assign[i] the column of row i, or None
    if no assignment avoids the missing edges. For n = 0 the result is (0, []).
    Time O(n^2 m), so O(n^3) for a square matrix; space O(n + m) besides the input.
    """
    n = len(cost)
    if n == 0:
        return 0, []
    m = len(cost[0])
    if any(len(row) != m for row in cost):
        raise ValueError("the matrix must be rectangular")
    if n > m:
        raise ValueError("need at most as many rows as columns")
    finite = [x for row in cost for x in row if x != math.inf]
    if any(x != x or x == -math.inf for x in finite):
        raise ValueError("costs must be numbers or math.inf")
    big = None
    if len(finite) < n * m:  # replace a missing edge by a cost no optimum can afford
        lo, hi = (min(finite), max(finite)) if finite else (0, 0)
        big = n * (hi - lo) + abs(lo) + 1
    a = [[big if x == math.inf else x for x in row] for row in cost]

    # rows 1..n and columns 1..m; row 0 and column 0 are dummies
    u: list[Number] = [0] * (n + 1)  # @line L1
    v: list[Number] = [0] * (m + 1)
    p = [0] * (m + 1)  # p[j] is the row of column j, 0 if column j is free
    way = [0] * (m + 1)
    for i in range(1, n + 1):  # @line L2
        p[0] = i  # @line L3
        j0 = 0
        minv: list[Number] = [math.inf] * (m + 1)
        used = [False] * (m + 1)
        while True:  # @line L4
            used[j0] = True  # @line L5
            i0 = p[j0]
            delta: Number = math.inf
            j1 = 0
            for j in range(1, m + 1):  # @line L6
                if used[j]:
                    continue
                r = a[i0 - 1][j - 1] - u[i0] - v[j]  # @line L7
                if r < minv[j]:  # @line L8
                    minv[j] = r
                    way[j] = j0
                if minv[j] < delta:  # @line L9
                    delta = minv[j]
                    j1 = j
            for j in range(m + 1):  # @line L10
                if used[j]:  # @line L11
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta  # @line L12
            j0 = j1  # @line L13
            if p[j0] == 0:  # @line L14
                break
        while j0 != 0:  # @line L15: flip the alternating path back to the dummy column
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    assign = [0] * n
    for j in range(1, m + 1):  # @line L16
        if p[j] != 0:
            assign[p[j] - 1] = j - 1
    if any(cost[i][assign[i]] == math.inf for i in range(n)):
        return None
    total = sum((cost[i][assign[i]] for i in range(n)), start=0)
    return total, assign
