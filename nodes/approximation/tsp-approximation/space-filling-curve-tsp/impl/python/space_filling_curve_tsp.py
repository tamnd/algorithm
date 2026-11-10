# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-filling-curve-tsp/. The authors are listed in prov/CF8E6R.jsonl.

import math
from typing import Sequence


def hilbert_index(order: int, x: int, y: int) -> int:
    """The position of the cell (x, y) on the Hilbert curve through the 2^order x 2^order grid.

    The curve starts in the cell (0, 0), visits the four quadrants in the order lower left,
    upper left, upper right, lower right, and ends in the cell (2^order - 1, 0). Iterative.
    """
    size = 1 << order
    d = 0
    s = size >> 1
    while s > 0:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:  # turn the quadrant so that its sub-curve has the standard form
            if rx == 1:
                x = size - 1 - x
                y = size - 1 - y
            x, y = y, x
        s >>= 1
    return d


def grid_cell(
    points: Sequence[tuple[float, float]], order: int, frame: tuple[float, float, float] | None = None
) -> list[tuple[int, int]]:
    """Return the grid cell of each point in the square frame (x0, y0, side).

    When frame is None, the frame is the bounding square of the points: its lower left corner is
    (min x, min y) and its side is the larger of the width and the height.
    """
    if frame is None:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        x0, y0 = min(xs), min(ys)
        side = max(max(xs) - x0, max(ys) - y0)
    else:
        x0, y0, side = frame
    size = 1 << order
    cells = []
    for x, y in points:
        if side == 0:
            cells.append((0, 0))
            continue
        cx = min(size - 1, int((x - x0) / side * size))
        cy = min(size - 1, int((y - y0) / side * size))
        cells.append((cx, cy))
    return cells


def space_filling_curve_tour(
    points: Sequence[tuple[float, float]], order: int = 24, frame: tuple[float, float, float] | None = None
) -> list[int]:
    """Visit the points in the order of their cells on the Hilbert curve.

    Points in one cell keep their input order. Time O(n log n) for the sort and O(n * order) for
    the indices; extra space Theta(n).
    """
    n = len(points)
    if n == 0:
        return []
    cells = grid_cell(points, order, frame)  # @line L1
    keys = [hilbert_index(order, cx, cy) for cx, cy in cells]  # @line L2
    return sorted(range(n), key=lambda i: (keys[i], i))  # @line L3


def euclidean_tour_length(points: Sequence[tuple[float, float]], tour: Sequence[int]) -> float:
    n = len(tour)
    if n < 2:
        return 0.0
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % n]]) for i in range(n))
