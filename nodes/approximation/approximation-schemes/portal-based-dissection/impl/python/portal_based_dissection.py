# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/portal-based-dissection/. The authors are listed in prov/4X3G6D.jsonl.

"""The randomly shifted dissection of Arora, with portals, and the snapping of a tour to the portals.

A point (p, q) with integers 0 <= p, q < L stands for the centre (p + 1/2, q + 1/2) of a unit cell, so no point lies
on a grid line. The dissection lines are the integer lines. With the shift (a, b), the root square is
[-a, 2L - a) x [-b, 2L - b), and the squares of depth i have side 2L / 2^i. The dynamic program over the squares is
not implemented here; this module builds the dissection and measures what the portals cost."""

import random
from fractions import Fraction
from math import comb, floor
from typing import Optional, Sequence

Point = tuple[int, int]


def perturb(points: Sequence[tuple[float, float]], eps: float) -> tuple[list[Point], int]:
    """Move each point to a grid cell of side eps * L0 / (8n), L0 the side of the bounding box; merge duplicates."""
    n = len(points)
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    side = max(max(xs) - min(xs), max(ys) - min(ys)) or 1.0
    gap = eps * side / (8 * n)
    cells = sorted({(floor((x - min(xs)) / gap), floor((y - min(ys)) / gap)) for x, y in points})  # @line L1
    size = 1
    while size <= max(max(c) for c in cells):
        size *= 2
    return cells, size


def random_shift(size: int, rng: random.Random) -> tuple[int, int]:
    return rng.randrange(size), rng.randrange(size)  # @line L2


def depth_count(size: int) -> int:
    """The number of levels D = log2(2L): the squares of depth D have side 1."""
    return (2 * size).bit_length() - 1


def line_level(c: int, shift: int, size: int) -> int:
    """The level i of the line at c: the least i such that the line is a side of the squares of depth i."""
    x = c + shift
    assert 0 < x < 2 * size
    v = (x & -x).bit_length() - 1  # the power of 2 that divides x exactly
    return depth_count(size) - v  # @line L3


def portal_gap(level: int, size: int, m: int) -> Fraction:
    return Fraction(2 * size, 2 ** level * m)  # @line L4


def nearest_portal(t: Fraction, offset: int, gap: Fraction) -> tuple[Fraction, Fraction]:
    """Portals lie at -offset + k * gap; return the nearest one to t and its distance."""
    k = (t + offset) / gap
    lo = floor(k)
    best = min((lo, lo + 1), key=lambda j: abs(k - j))
    portal = -offset + best * gap
    return portal, abs(t - portal)


def crossings(p: Point, q: Point) -> list[tuple[str, int, Fraction]]:
    """The crossings of the segment between the centres of p and q with the integer lines.

    ('x', c, y) is a crossing of the vertical line x = c at height y; ('y', c, x) of the horizontal line y = c."""
    (x1, y1), (x2, y2) = p, q
    out = []
    for c in range(min(x1, x2) + 1, max(x1, x2) + 1):
        out.append(("x", c, y1 + Fraction(1, 2) + Fraction((c - x1 - Fraction(1, 2)) * (y2 - y1), x2 - x1)))
    for c in range(min(y1, y2) + 1, max(y1, y2) + 1):
        out.append(("y", c, x1 + Fraction(1, 2) + Fraction((c - y1 - Fraction(1, 2)) * (x2 - x1), y2 - y1)))
    return out


def snap_tour(points: Sequence[Point], tour: Sequence[int], size: int, m: int, shift: tuple[int, int],
              stats: Optional[dict] = None) -> Fraction:
    """The extra length when every crossing of the tour is moved to the nearest portal of its line.

    The tour walks along the line from the crossing to the portal and back, which adds twice the distance."""
    a, b = shift
    extra, count, worst = Fraction(0), 0, Fraction(0)
    for k in range(len(tour)):
        p, q = points[tour[k]], points[tour[(k + 1) % len(tour)]]
        for axis, c, t in crossings(p, q):
            level = line_level(c, a if axis == "x" else b, size)
            gap = portal_gap(level, size, m)
            _, d = nearest_portal(t, b if axis == "x" else a, gap)
            extra += 2 * d  # @line L5
            count += 1
            worst = max(worst, 2 * d / gap)
    if stats is not None:
        stats.update(crossings=count, worst=worst)
    return extra


def quadtree_size(points: Sequence[Point], size: int, shift: tuple[int, int]) -> tuple[int, int]:
    """The number of squares of the quadtree and its depth; a square with two or more points is split into four."""
    a, b = shift
    nodes, depth = 0, 0
    stack = [(-a, -b, 2 * size, 0, list(points))]
    while stack:
        x0, y0, side, d, pts = stack.pop()
        nodes += 1
        depth = max(depth, d)
        if len(pts) <= 1:
            continue
        half = side // 2
        for dx in (0, half):
            for dy in (0, half):
                inner = [p for p in pts if x0 + dx <= p[0] < x0 + dx + half and y0 + dy <= p[1] < y0 + dy + half]
                stack.append((x0 + dx, y0 + dy, half, d + 1, inner))
    return nodes, depth


def interface_count(m: int, r: int) -> int:
    """The ways to choose at most r crossing portals on each of the four sides, each side with m + 1 portals."""
    return sum(comb(m + 1, j) for j in range(r + 1)) ** 4
