# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/little-algorithm/. The authors are listed in prov/10HFCT.jsonl.
"""Little's branch and bound for the asymmetric traveling salesman problem.

A node is a reduced cost matrix together with the arcs that are already in the
tour. Its lower bound is the sum of all reductions made so far. The search
branches on a zero entry (i, j) of largest penalty: one child excludes the arc
(i, j) and the other includes it.
"""

from __future__ import annotations

import heapq
import math
from typing import Optional, Sequence

INF = math.inf
Matrix = list[list[float]]


def reduce_rows(m: Matrix, which: Sequence[int], cols: Sequence[int]) -> float:
    """Subtract from each row in which its minimum over cols, in place. Return the total."""
    total = 0.0
    for i in which:
        h = min(m[i][j] for j in cols)
        if h == INF:
            return INF
        if h > 0:
            for j in cols:
                m[i][j] -= h
            total += h
    return total


def reduce_cols(m: Matrix, rows: Sequence[int], which: Sequence[int]) -> float:
    """Subtract from each column in which its minimum over rows, in place. Return the total."""
    total = 0.0
    for j in which:
        h = min(m[i][j] for i in rows)
        if h == INF:
            return INF
        if h > 0:
            for i in rows:
                m[i][j] -= h
            total += h
    return total


def reduce_matrix(m: Matrix, rows: Sequence[int], cols: Sequence[int]) -> float:
    """Reduce all rows, then all columns, in place. Return the total."""
    h = reduce_rows(m, rows, cols)
    return h if h == INF else h + reduce_cols(m, rows, cols)


def penalty_choice(m: Matrix, rows: Sequence[int], cols: Sequence[int]) -> tuple[int, int, float]:
    """Return the zero entry (i, j) with the largest penalty and the penalty.

    The penalty of a zero (i, j) is the smallest other entry of row i plus the
    smallest other entry of column j. Ties go to the smallest (i, j).
    """
    best: Optional[tuple[int, int, float]] = None
    for i in rows:
        for j in cols:
            if m[i][j] != 0:
                continue
            a = min((m[i][k] for k in cols if k != j), default=INF)
            b = min((m[k][j] for k in rows if k != i), default=INF)
            theta = a + b
            if best is None or theta > best[2]:
                best = (i, j, theta)
    assert best is not None
    return best


def little(
    cost: Sequence[Sequence[float]],
    stats: Optional[dict[str, int]] = None,
    trace: Optional[list[tuple[str, float]]] = None,
) -> tuple[float, Optional[list[int]]]:
    """Solve the TSP on the n x n matrix cost; cost[i][j] = inf forbids arc i -> j.

    Return (length, tour), where tour lists the cities from city 0, or
    (inf, None) if there is no tour. The diagonal is ignored.
    """
    n = len(cost)
    if stats is not None:
        stats.update(nodes=0, expanded=0)
    if n == 0:
        return 0.0, []
    if n == 1:
        return 0.0, [0]
    m0: Matrix = [[INF if i == j else float(cost[i][j]) for j in range(n)] for i in range(n)]
    lb0 = reduce_matrix(m0, range(n), range(n))  # @line L1
    z = INF  # @line L2
    best: Optional[dict[int, int]] = None
    heap: list = []
    tick = 0
    if lb0 < z:
        heapq.heappush(heap, (lb0, tick, m0, list(range(n)), list(range(n)), {}))
        if stats is not None:
            stats["nodes"] += 1
    while heap:  # @line L3
        lb, _, m, rows, cols, succ = heapq.heappop(heap)  # @line L4
        if trace is not None:
            trace.append(("pop", lb))
        if lb >= z:  # @line L5
            break
        if len(succ) == n:  # @line L6
            z, best = lb, succ  # @line L7
            continue
        if stats is not None:
            stats["expanded"] += 1
        i, j, theta = penalty_choice(m, rows, cols)  # @line L8
        # Exclude child: forbid i -> j and reduce row i and column j again.
        if lb + theta < z:  # @line L9
            mx = [row[:] for row in m]
            mx[i][j] = INF
            extra = reduce_rows(mx, [i], cols) + reduce_cols(mx, rows, [j])
            tick += 1
            heapq.heappush(heap, (lb + extra, tick, mx, rows, cols, succ))  # @line L10
            if stats is not None:
                stats["nodes"] += 1
        # Include child: take i -> j, delete row i and column j, block the subtour.
        mi = [row[:] for row in m]  # @line L11
        rows2 = [r for r in rows if r != i]
        cols2 = [c for c in cols if c != j]
        succ2 = dict(succ)
        succ2[i] = j
        if len(succ2) < n - 1:  # @line L12
            pred = {v: u for u, v in succ2.items()}
            s = i
            while s in pred:
                s = pred[s]
            e = j
            while e in succ2:
                e = succ2[e]
            mi[e][s] = INF
        extra = reduce_matrix(mi, rows2, cols2) if rows2 else 0.0  # @line L13
        if lb + extra < z:  # @line L14
            tick += 1
            heapq.heappush(heap, (lb + extra, tick, mi, rows2, cols2, succ2))
            if stats is not None:
                stats["nodes"] += 1
    if best is None:  # @line L15
        return INF, None
    tour = [0]
    while len(tour) < n:
        tour.append(best[tour[-1]])
    return z, tour


def tour_length(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    """Length of the closed tour that visits the cities in this order."""
    n = len(tour)
    return sum(cost[tour[k]][tour[(k + 1) % n]] for k in range(n)) if n > 1 else 0.0
