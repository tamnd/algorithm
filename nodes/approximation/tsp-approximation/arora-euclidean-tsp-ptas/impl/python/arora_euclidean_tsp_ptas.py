# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-euclidean-tsp-ptas/. The authors are listed in prov/CVQVJX.jsonl.
"""Checked parts of Arora's scheme in the plane: the grid step, the shifted quadtree and the portals.

What the code covers: the snapping to a grid, the random shift, the levels of the grid lines, the
quadtree, and the extra cost of moving every crossing of a tour to the nearest portal. The dynamic
program over the squares is NOT implemented. arora_tour replaces it by a brute force over the city
orders, which gives the same guarantee as the portal lemma on the page but takes exponential time.
The limit of r crossings per side and the patching lemma are not implemented either.
"""

import itertools
import math
import random
from typing import Sequence

Point = tuple[float, float]


def snap(points: Sequence[Point], c: float) -> tuple[list[tuple[int, int]], float, int]:
    """Move the points to a grid of spacing delta = L0 / (8 c n) and scale by 1 / delta.

    Return (integer points, delta, L), with L the least power of 2 above every coordinate.
    """
    n = len(points)
    x0, y0 = min(p[0] for p in points), min(p[1] for p in points)
    side = max(max(p[0] for p in points) - x0, max(p[1] for p in points) - y0)
    if side == 0:
        return [(0, 0)] * n, 1.0, 1
    delta = side / (8 * c * n)
    grid = [(round((p[0] - x0) / delta), round((p[1] - y0) / delta)) for p in points]
    top = max(max(g) for g in grid)
    return grid, delta, 1 << top.bit_length()


def line_level(k: int, shift: int, L: int) -> int:
    """The level of the grid line between the integers k and k + 1, for 0 <= k <= L - 2.

    The dissection square has side 2L and its low corner at -shift - 1/2, so that line is at
    distance k + shift + 1 from the corner. Its level is the least i with (2L / 2^i) dividing that.
    """
    dist, i = k + shift + 1, 1
    while dist % ((2 * L) >> i):
        i += 1
    return i


def detour(tour: Sequence[tuple[int, int]], a: int, b: int, L: int, m: int) -> float:
    """The extra length if each crossing of a grid line by the tour goes to the nearest portal and back.

    A line of level i carries the portals of the squares of side 2L / 2^i, spaced 2L / (2^i m).
    """
    total = 0.0
    n = len(tour)
    for idx in range(n):
        p, q = tour[idx], tour[(idx + 1) % n]
        for axis, shift_along, shift_across in ((0, b, a), (1, a, b)):
            lo, hi = sorted((p[axis], q[axis]))
            for k in range(lo, hi):
                t = (k + 0.5 - p[axis]) / (q[axis] - p[axis])
                along = p[1 - axis] + t * (q[1 - axis] - p[1 - axis]) + shift_along + 0.5
                spacing = 2 * L / ((1 << line_level(k, shift_across, L)) * m)
                total += 2 * abs(along - spacing * round(along / spacing))
    return total


def quadtree(points: Sequence[tuple[int, int]], a: int, b: int, L: int) -> tuple[int, int]:
    """Split the shifted square of side 2L until each square holds at most one distinct point.

    Return (the number of non-empty squares, the largest depth).
    """
    count, deepest = 0, 0
    stack = [(-a - 0.5, -b - 0.5, 2.0 * L, 0, sorted(set(points)))]
    while stack:
        x, y, side, depth, inside = stack.pop()
        count += 1
        deepest = max(deepest, depth)
        if len(inside) <= 1:
            continue
        half = side / 2
        for dx in (0, half):
            for dy in (0, half):
                part = [p for p in inside if x + dx < p[0] < x + dx + half and y + dy < p[1] < y + dy + half]
                if part:
                    stack.append((x + dx, y + dy, half, depth + 1, part))
    return count, deepest


def portal_count(L: int, c: float) -> int:
    """m: the least power of 2 with m >= 2 sqrt(2) c log2(2L)."""
    need = 2 * math.sqrt(2) * c * math.log2(2 * L)
    return 1 << max(0, math.ceil(math.log2(need)))


def length(points: Sequence[Point], order: Sequence[int]) -> float:
    n = len(order)
    return sum(math.dist(points[order[i]], points[order[(i + 1) % n]]) for i in range(n))


def arora_tour(points: Sequence[Point], c: float = 1.0, rng: random.Random | None = None, shift=None):
    """Return (order, (a, b), m) for the scheme with ratio 1 + 1/c in expectation; small n only."""
    n = len(points)
    if n <= 3:
        return list(range(n)), (0, 0), 1
    grid, _, L = snap(points, c)  # @line L1
    rng = rng or random.Random(0)
    a, b = shift if shift is not None else (rng.randrange(L), rng.randrange(L))  # @line L2
    quadtree(grid, a, b, L)  # @line L3
    m = portal_count(L, c)  # @line L4
    best, best_order = math.inf, None
    for rest in itertools.permutations(range(1, n)):  # @line L5 (brute force here, not the DP)
        order = [0, *rest]
        pts = [grid[i] for i in order]
        value = length(pts, range(n)) + detour(pts, a, b, L, m)
        if value < best:
            best, best_order = value, order
    return best_order, (a, b), m  # @line L6
