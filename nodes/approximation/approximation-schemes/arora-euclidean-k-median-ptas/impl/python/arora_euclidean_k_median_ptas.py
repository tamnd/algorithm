# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-euclidean-k-median-ptas/. The authors are listed in prov/PXSWAG.jsonl.

"""Parts of the Arora-Raghavan-Rao scheme for Euclidean k-median that can be checked on small inputs.

A point (p, q) with integers 0 <= p, q < L stands for the centre (p + 1/2, q + 1/2) of a unit cell; candidate centres
are such points too. With the shift (a, b) the root square is [-a, 2L - a) x [-b, 2L - b). The module computes the
cost of serving each point along a path that crosses grid lines only at portals, and the rounded distance profiles
that form the states of the dynamic program. The dynamic program itself is not implemented."""

import random
from fractions import Fraction
from math import dist, floor
from typing import Sequence

Point = tuple[int, int]


def snap_to_grid(points: Sequence[tuple[float, float]], gap: float) -> tuple[list[Point], int]:
    """Move each point to a cell of side gap (by at most gap / sqrt 2 from the cell centre) and merge duplicates.

    Returns the cells, with the multiplicity lost, and the grid side L, a power of 2."""
    x0, y0 = min(p[0] for p in points), min(p[1] for p in points)
    cells = sorted({(floor((x - x0) / gap), floor((y - y0) / gap)) for x, y in points})  # @line L1
    size = 1
    while size <= max(max(c) for c in cells):
        size *= 2
    return cells, size


def child_counts(j: int) -> list[tuple[int, int, int, int]]:
    """The ways to split j centres among the four children of a square."""
    return [(a, b, c, j - a - b - c) for a in range(j + 1) for b in range(j + 1 - a)  # @line L5
            for c in range(j + 1 - a - b)]


def best_over_shifts(points: Sequence[Point], centres: Sequence[Point], size: int, m: int) -> tuple[float, tuple]:
    """The least portal-respecting cost of the given centres over all L^2 shifts, and a shift that reaches it."""
    return min((portal_cost(points, centres, size, m, (a, b)), (a, b))  # @line L7
               for a in range(size) for b in range(size))


def random_shift(size: int, rng: random.Random) -> tuple[int, int]:
    return rng.randrange(size), rng.randrange(size)  # @line L2


def depth_count(size: int) -> int:
    return (2 * size).bit_length() - 1


def line_level(c: int, shift: int, size: int) -> int:
    x = c + shift
    return depth_count(size) - ((x & -x).bit_length() - 1)


def detour(p: Point, q: Point, size: int, m: int, shift: tuple[int, int]) -> Fraction:
    """The extra length when each crossing of the segment pq with a grid line moves to the nearest portal and back."""
    (x1, y1), (x2, y2) = p, q
    extra = Fraction(0)
    for axis, lo, hi, u1, v1, u2, v2, own, other in (("x", x1, x2, x1, y1, x2, y2, shift[0], shift[1]),
                                                     ("y", y1, y2, y1, x1, y2, x2, shift[1], shift[0])):
        for c in range(min(lo, hi) + 1, max(lo, hi) + 1):
            t = v1 + Fraction(1, 2) + (c - u1 - Fraction(1, 2)) * Fraction(v2 - v1, u2 - u1)
            gap = Fraction(2 * size, 2 ** line_level(c, own, size) * m)
            k = (t + other) / gap
            extra += 2 * min(k - floor(k), floor(k) + 1 - k) * gap
    return extra


def portal_cost(points: Sequence[Point], centres: Sequence[Point], size: int, m: int,
                shift: tuple[int, int]) -> float:
    """Each point is served by the centre with the least length of a portal-respecting path through snapped crossings."""
    return sum(min(dist(p, c) + float(detour(p, c, size, m, shift)) for c in centres) for p in points)  # @line L6


def boundary_portals(x0: int, y0: int, side: int, m: int) -> list[tuple[Fraction, Fraction]]:
    """The 4m portals of a square, in order around the boundary, with gap side / m; the corners are portals."""
    g = Fraction(side, m)
    out = []
    for j in range(m):
        out.append((x0 + j * g, Fraction(y0)))
    for j in range(m):
        out.append((Fraction(x0 + side), y0 + j * g))
    for j in range(m):
        out.append((x0 + side - j * g, Fraction(y0 + side)))
    for j in range(m):
        out.append((Fraction(x0), y0 + side - j * g))
    return out  # @line L3


def distance_profile(portals: Sequence[tuple[Fraction, Fraction]], centres: Sequence[Point], gap: Fraction) -> list[int]:
    """For each portal, the distance to the nearest centre, in whole gaps (rounded down)."""
    cs = [(c[0] + 0.5, c[1] + 0.5) for c in centres]
    g = float(gap)
    return [floor(min(dist((float(px), float(py)), c) for c in cs) / g + 1e-9) for px, py in portals]  # @line L4


def is_smooth(profile: Sequence[int]) -> bool:
    """Adjacent portals are one gap apart, so their rounded distances differ by at most 1, around the cycle."""
    return all(abs(profile[i] - profile[i - 1]) <= 1 for i in range(len(profile)))


def smooth_profile_bound(length: int, top: int) -> int:
    """The number of cyclic profiles with values in 0..top and steps in {-1, 0, 1} is at most this."""
    return (top + 1) * 3 ** (length - 1)
