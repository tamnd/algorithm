# SPDX-License-Identifier: MIT
# Shared helper of the mg1 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small exact tools for planar grids and triangulations, used by the mg1 pages.

Points are tuples of int, fractions.Fraction or float. Every predicate here is
exact when the coordinates are int or Fraction. A float coordinate converts to
a Fraction without rounding, so exact() followed by a predicate gives the exact
sign for the float points as they are stored.
"""

from fractions import Fraction
from typing import Iterable, Sequence, Tuple

Point = Tuple


def exact(p: Point) -> Tuple[Fraction, ...]:
    """The point p with each coordinate converted to Fraction, without rounding."""
    return tuple(Fraction(c) for c in p)


def orient2d(a: Point, b: Point, c: Point):
    """Twice the signed area of the triangle a, b, c; positive if counterclockwise."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def twice_area(poly: Sequence[Point]):
    """Twice the signed area of a polygon by the shoelace formula."""
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def quad_corner_values(q: Sequence[Point]) -> list:
    """The four values ORIENT2D(q[k-1], q[k], q[k+1]) of a quadrilateral q[0..3].

    They are the Jacobian determinants of the bilinear map of the cell at its
    corners. All four are positive exactly when the quadrilateral is strictly
    convex and counterclockwise.
    """
    return [orient2d(q[k - 1], q[k], q[(k + 1) % 4]) for k in range(4)]


def grid_cells(grid: Sequence[Sequence[Point]]) -> Iterable:
    """Yield ((i, j), corners) for each cell of a grid x[i][j], corners counterclockwise for u right, v up."""
    for i in range(len(grid) - 1):
        for j in range(len(grid[0]) - 1):
            yield (i, j), (grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1])


def in_closed_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    """True if p lies in the closed counterclockwise triangle a, b, c."""
    return orient2d(a, b, p) >= 0 and orient2d(b, c, p) >= 0 and orient2d(c, a, p) >= 0


def segments_cross(a: Point, b: Point, c: Point, d: Point) -> bool:
    """True if the closed segments ab and cd share a point other than a common endpoint.

    Segments that share exactly one endpoint and are not collinear return False.
    Cost O(1); exact for int and Fraction.
    """
    shared = {a, b} & {c, d}
    o1, o2 = orient2d(a, b, c), orient2d(a, b, d)
    o3, o4 = orient2d(c, d, a), orient2d(c, d, b)
    if o1 == 0 and o2 == 0:
        # collinear: overlap in more than a shared endpoint?
        k = 0 if a[0] != b[0] else 1
        lo1, hi1 = sorted((a[k], b[k]))
        lo2, hi2 = sorted((c[k], d[k]))
        lo, hi = max(lo1, lo2), min(hi1, hi2)
        if lo < hi:
            return True
        return lo == hi and not shared
    if shared:
        # two segments that are not collinear meet in at most one point
        return False
    return o1 * o2 <= 0 and o3 * o4 <= 0
