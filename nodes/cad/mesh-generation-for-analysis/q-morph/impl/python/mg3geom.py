# SPDX-License-Identifier: MIT
# Shared helper of the mg3 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small exact tools for triangle and tetrahedral meshes, used by the mg3 pages.

Points are tuples of int, fractions.Fraction or float. Every predicate here is
exact when the coordinates are int or Fraction. A float converts to a Fraction
without rounding, so exact() followed by a predicate gives the exact sign for
the float points as they are stored. Nothing here builds a mesh; each page
builds its own.
"""

import math
from fractions import Fraction
from typing import Dict, Iterable, List, Sequence, Tuple

Point = Tuple


def exact(p: Point) -> Tuple[Fraction, ...]:
    """The point p with each coordinate converted to Fraction, without rounding."""
    return tuple(Fraction(c) for c in p)


def to_grid(x: float, bits: int = 20) -> Fraction:
    """The nearest multiple of 2**-bits to x, as a Fraction."""
    return Fraction(round(x * (1 << bits)), 1 << bits)


def orient2d(a: Point, b: Point, c: Point):
    """Twice the signed area of the triangle a, b, c; positive if counterclockwise."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def incircle(a: Point, b: Point, c: Point, d: Point):
    """Positive if d is inside the circle through a, b, c (a, b, c counterclockwise),
    zero if on it, negative if outside."""
    rows = []
    for p in (a, b, c):
        dx, dy = p[0] - d[0], p[1] - d[1]
        rows.append((dx, dy, dx * dx + dy * dy))
    (a0, a1, a2), (b0, b1, b2), (c0, c1, c2) = rows
    return a0 * (b1 * c2 - b2 * c1) - a1 * (b0 * c2 - b2 * c0) + a2 * (b0 * c1 - b1 * c0)


def orient3d(a: Point, b: Point, c: Point, d: Point):
    """Six times the signed volume of the tetrahedron a, b, c, d.

    Positive if d lies on the side of the plane abc toward which (b - a) x (c - a)
    points, that is, if a, b, c look clockwise from d."""
    u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    w = (d[0] - a[0], d[1] - a[1], d[2] - a[2])
    return (u[0] * (v[1] * w[2] - v[2] * w[1])
            - u[1] * (v[0] * w[2] - v[2] * w[0])
            + u[2] * (v[0] * w[1] - v[1] * w[0]))


def twice_area(poly: Sequence[Point]):
    """Twice the signed area of a polygon by the shoelace formula."""
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def segments_cross(a: Point, b: Point, c: Point, d: Point) -> bool:
    """True if the open segments ab and cd cross at one point inside both."""
    return (orient2d(a, b, c) * orient2d(a, b, d) < 0
            and orient2d(c, d, a) * orient2d(c, d, b) < 0)


def edge_map(cells: Iterable[Sequence[int]]) -> Dict[Tuple[int, int], int]:
    """Map each directed edge (i, j) of a list of counterclockwise polygons
    (triangles or quads, given by vertex indices) to the index of its cell.
    Raises ValueError if a directed edge is used twice."""
    m: Dict[Tuple[int, int], int] = {}
    for k, cell in enumerate(cells):
        n = len(cell)
        for s in range(n):
            e = (cell[s], cell[(s + 1) % n])
            if e in m:
                raise ValueError("directed edge %r used twice" % (e,))
            m[e] = k
    return m


def boundary_edges(cells: Iterable[Sequence[int]]) -> List[Tuple[int, int]]:
    """The directed edges whose reverse is not an edge of any cell."""
    m = edge_map(cells)
    return [e for e in m if (e[1], e[0]) not in m]


def is_valid_planar_mesh(points: Sequence[Point], cells: Sequence[Sequence[int]]) -> bool:
    """Exact check that every cell is a strictly convex counterclockwise polygon
    and that no directed edge is used twice. With the area sum of the caller,
    this shows a conforming mesh of a simply covered region."""
    try:
        edge_map(cells)
    except ValueError:
        return False
    for cell in cells:
        n = len(cell)
        for s in range(n):
            a, b, c = points[cell[s]], points[cell[(s + 1) % n]], points[cell[(s + 2) % n]]
            if orient2d(a, b, c) <= 0:
                return False
    return True


def mean_ratio(a: Point, b: Point, c: Point) -> float:
    """The mean ratio 4 sqrt(3) A / (sum of squared edge lengths) of a triangle,
    in floats; 1 for the equilateral triangle, 0 for a flat one, negative if the
    triangle is clockwise."""
    s = sum(float((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) for p, q in ((a, b), (b, c), (c, a)))
    return 2.0 * math.sqrt(3.0) * float(orient2d(a, b, c)) / s
