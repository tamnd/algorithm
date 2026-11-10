# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-partitioning-tsp/. The authors are listed in prov/56Q4XY.jsonl.

import math
from typing import Sequence

Point = tuple[float, float]


def tour_length(points: Sequence[Point], tour: Sequence[int]) -> float:
    n = len(tour)
    if n < 2:
        return 0.0
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % n]]) for i in range(n))


def held_karp_tour(points: Sequence[Point], ids: Sequence[int]) -> list[int]:
    """An optimal tour of the points with the given ids, by the Held-Karp dynamic program.

    Time O(t^2 2^t) and space O(t 2^t) for t = len(ids). The tour starts at ids[0].
    """
    t = len(ids)
    if t <= 3:
        return list(ids)
    d = [[math.dist(points[a], points[b]) for b in ids] for a in ids]
    full = 1 << (t - 1)  # subsets of the cities 1 .. t-1; city 0 is the start
    best = [[math.inf] * t for _ in range(full)]
    back = [[-1] * t for _ in range(full)]
    for j in range(1, t):
        best[1 << (j - 1)][j] = d[0][j]
    for mask in range(1, full):
        for j in range(1, t):
            here = best[mask][j]
            if here == math.inf:
                continue
            for k in range(1, t):
                bit = 1 << (k - 1)
                if mask & bit:
                    continue
                value = here + d[j][k]
                if value < best[mask | bit][k]:
                    best[mask | bit][k] = value
                    back[mask | bit][k] = j
    mask = full - 1
    last = min(range(1, t), key=lambda j: best[mask][j] + d[j][0])
    order = []
    while last != -1 and mask:
        order.append(last)
        prev = back[mask][last]
        mask ^= 1 << (last - 1)
        last = prev
    return [ids[0]] + [ids[j] for j in reversed(order)]


def bounding_square(points: Sequence[Point]) -> tuple[float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x0, y0 = min(xs), min(ys)
    return x0, y0, max(max(xs) - x0, max(ys) - y0)


def grid_cells(points: Sequence[Point], k: int) -> dict[tuple[int, int], list[int]]:
    """Put each point in one cell of the k x k grid on the bounding square (half-open cells)."""
    x0, y0, side = bounding_square(points)
    cells: dict[tuple[int, int], list[int]] = {}
    for i, (x, y) in enumerate(points):
        if side == 0:
            col = row = 0
        else:
            col = min(k - 1, int((x - x0) / side * k))
            row = min(k - 1, int((y - y0) / side * k))
        cells.setdefault((col, row), []).append(i)
    return cells


def snake_order(cells: dict[tuple[int, int], list[int]], k: int) -> list[tuple[int, int]]:
    """The nonempty cells row by row, left to right in even rows and right to left in odd rows."""
    order = []
    for row in range(k):
        cols = range(k) if row % 2 == 0 else range(k - 1, -1, -1)
        order.extend((col, row) for col in cols if (col, row) in cells)
    return order


def karp_partition_tour(points: Sequence[Point], k: int, max_cell: int = 12) -> list[int]:
    """Cut the bounding square into k x k cells, solve each cell exactly, and join the cell tours.

    The cells are taken in snake order. Each cell tour is cut open before the point that is
    nearest to the end of the tour so far, and it is added as a path from that point.
    Raise ValueError if a cell holds more than max_cell points.
    """
    if not points:
        return []
    cells = grid_cells(points, k)  # @line L1
    tour: list[int] = []
    for cell in snake_order(cells, k):  # @line L2
        ids = cells[cell]
        if len(ids) > max_cell:
            raise ValueError(f"cell {cell} holds {len(ids)} points, more than {max_cell}")
        cycle = held_karp_tour(points, ids)  # @line L3
        start = 0
        if tour:
            start = min(range(len(cycle)), key=lambda i: math.dist(points[tour[-1]], points[cycle[i]]))
        tour.extend(cycle[start:] + cycle[:start])  # @line L4
    return tour  # @line L5


def cell_tours_length(points: Sequence[Point], k: int) -> float:
    """The sum over the nonempty cells of the optimal tour length of the cell."""
    cells = grid_cells(points, k)
    return sum(tour_length(points, held_karp_tour(points, ids)) for ids in cells.values())
