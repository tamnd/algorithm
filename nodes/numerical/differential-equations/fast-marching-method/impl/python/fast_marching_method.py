# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-marching-method/. The authors are listed in prov/XZFJD7.jsonl.

"""Fast marching method for the eikonal equation |grad T| = s on a 2D grid.

First-order Godunov upwind discretization on a uniform grid with spacing h; grid
points are accepted in increasing order of T, as in Dijkstra's algorithm.
"""

import heapq
import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple

INF = math.inf
FAR, TRIAL, KNOWN = 0, 1, 2


@dataclass
class FMMResult:
    """Arrival times T[i][j] (inf where unreachable), acceptance order, heap pushes."""

    T: List[List[float]]
    order: List[Tuple[int, int]]
    pushes: int


def upwind_update(c: float, a: float, b: float) -> float:
    """Largest root t of max(t - a, 0)^2 + max(t - b, 0)^2 = c^2, c = s h > 0.

    a and b are the smaller neighbour values in the two grid directions (inf if none).
    """
    if a > b:
        a, b = b, a
    if a == INF:
        return INF
    if b - a >= c:
        return a + c
    return 0.5 * (a + b + math.sqrt(2.0 * c * c - (b - a) * (b - a)))


def _neighbour_mins(T, state, i, j, only_known):
    """Smallest neighbour value in x and in y, using Known points only if asked."""
    rows, cols = len(T), len(T[0])

    def val(p, q):
        if 0 <= p < rows and 0 <= q < cols and (not only_known or state[p][q] == KNOWN):
            return T[p][q]
        return INF

    return min(val(i, j - 1), val(i, j + 1)), min(val(i - 1, j), val(i + 1, j))


def fast_marching(s: Sequence[Sequence[float]], h: float,
                  sources: Sequence[Tuple[int, int]]) -> FMMResult:
    """Solve the discrete eikonal equation with slowness s[i][j] (inf marks an obstacle).

    Sources get T = 0. Cost: O(N log N) for N grid points, N accepted points and at
    most 4N heap pushes; O(N) space.
    """
    if not h > 0:
        raise ValueError("h must be positive")
    rows = len(s)
    cols = len(s[0]) if rows else 0
    if any(len(r) != cols for r in s):
        raise ValueError("s must be a rectangular grid")
    for i in range(rows):
        for j in range(cols):
            if not s[i][j] > 0:
                raise ValueError("slowness must be positive (inf for obstacles)")
    T = [[INF] * cols for _ in range(rows)]  # @line L1
    state = [[FAR] * cols for _ in range(rows)]
    heap: List[Tuple[float, int, int]] = []
    pushes = 0
    for (i, j) in sources:  # @line L2
        if not (0 <= i < rows and 0 <= j < cols):
            raise ValueError("source outside the grid")
        if s[i][j] == INF:
            raise ValueError("source on an obstacle")
        T[i][j] = 0.0
        state[i][j] = TRIAL
        heapq.heappush(heap, (0.0, i, j))
        pushes += 1
    order: List[Tuple[int, int]] = []
    while heap:  # @line L3
        tau, i, j = heapq.heappop(heap)  # @line L4
        if state[i][j] == KNOWN or tau > T[i][j]:  # @line L5
            continue
        state[i][j] = KNOWN  # @line L6
        order.append((i, j))
        for p, q in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):  # @line L7
            if 0 <= p < rows and 0 <= q < cols and state[p][q] != KNOWN and s[p][q] < INF:
                a, b = _neighbour_mins(T, state, p, q, True)
                t = upwind_update(s[p][q] * h, a, b)  # @line L8
                if t < T[p][q]:  # @line L9
                    T[p][q] = t
                    state[p][q] = TRIAL
                    heapq.heappush(heap, (t, p, q))
                    pushes += 1
    return FMMResult(T, order, pushes)  # @line L10


def discrete_residual(T, s, h, sources) -> float:
    """Max over non-source points of |T - update(all neighbours)| where T is finite."""
    src = set(sources)
    worst = 0.0
    state = None
    for i in range(len(T)):
        for j in range(len(T[0])):
            if (i, j) in src or s[i][j] == INF:
                continue
            a, b = _neighbour_mins(T, state, i, j, False)
            u = upwind_update(s[i][j] * h, a, b)
            if T[i][j] == INF or u == INF:
                if T[i][j] != u:
                    return INF
                continue
            worst = max(worst, abs(T[i][j] - u))
    return worst
