# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/advancing-front-mesh-generation/. The authors are listed in prov/NKGVJD.jsonl.

"""Advancing front triangulation of a simple polygon in the plane.

All points are tuples of Fraction, and every decision that affects validity
(orientation, containment, crossing, the minimum distance of a new point) is
made with exact rational arithmetic. Floats are used only to propose the ideal
point, which is then rounded to a rational grid; a bad proposal is rejected by
the exact tests, never accepted.

The method has no quality guarantee. The triangles are valid and tile the
polygon, but their angles are only measured, see min_angle_degrees().
"""

import math
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg1geom import in_closed_triangle, orient2d, segments_cross, twice_area

Point = Tuple[Fraction, Fraction]
Triangle = Tuple[Point, Point, Point]


def _d2(p: Point, q: Point) -> Fraction:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def _split_side(a: Point, b: Point, h: Fraction) -> List[Point]:
    """Points a = q_0, ..., q_k (b excluded) cutting ab into k equal parts, k the least with k h >= |ab|."""
    k = max(1, math.ceil(math.sqrt(float(_d2(a, b))) / float(h)))
    while k > 1 and (k - 1) ** 2 * h * h >= _d2(a, b):
        k -= 1
    while k * k * h * h < _d2(a, b):
        k += 1
    return [(a[0] + (b[0] - a[0]) * Fraction(t, k), a[1] + (b[1] - a[1]) * Fraction(t, k)) for t in range(k)]


def _ideal_point(a: Point, b: Point, h: Fraction) -> Tuple[Point, float]:
    """The point left of ab at distance delta from a and b, rounded to the grid of step h / 64."""
    ab = math.sqrt(float(_d2(a, b)))
    delta = min(max(float(h), 0.55 * ab), 2.0 * ab)
    height = math.sqrt(max(delta * delta - ab * ab / 4, 0.0))
    mx, my = float(a[0] + b[0]) / 2, float(a[1] + b[1]) / 2
    nx, ny = -float(b[1] - a[1]) / ab, float(b[0] - a[0]) / ab
    g = Fraction(h) / 64
    gf = float(g)
    return (Fraction(round((mx + height * nx) / gf)) * g, Fraction(round((my + height * ny) / gf)) * g), delta


def advancing_front(polygon: Sequence[Point], h) -> Tuple[List[Triangle], List[Point]]:
    """Triangulate a simple counterclockwise polygon with target edge length h.

    Precondition: polygon is a list of at least 3 distinct points with int or
    Fraction coordinates, simple and counterclockwise; h > 0 (int or Fraction).
    Returns (triangles, vertices); each triangle is counterclockwise.
    Cost: O(n^3) exact operations in the worst case for n vertices of the
    output, from the fallback search; usually O(n f) for a front of size f.
    """
    pts = [(Fraction(p[0]), Fraction(p[1])) for p in polygon]
    h = Fraction(h)
    if len(pts) < 3 or h <= 0 or twice_area(pts) <= 0:
        raise ValueError("need a counterclockwise polygon with at least 3 vertices and h > 0")
    loop: List[Point] = []
    for i in range(len(pts)):
        loop += _split_side(pts[i], pts[(i + 1) % len(pts)], h)
    front: Dict[Tuple[Point, Point], None] = {}
    for i in range(len(loop)):  # @line L1
        front[(loop[i], loop[(i + 1) % len(loop)])] = None
    vertices: List[Point] = list(loop)  # @line L2
    hmin2 = min([h * h] + [_d2(a, b) for a, b in front]) / 4
    triangles: List[Triangle] = []

    def valid(a: Point, b: Point, c: Point, new: bool, fverts) -> bool:
        if orient2d(a, b, c) <= 0:  # @line L12
            return False
        if new and any(_d2(c, v) < hmin2 for v in vertices):  # @line L13
            return False
        if any(v not in (a, b, c) and in_closed_triangle(v, a, b, c) for v in fverts):  # @line L14
            return False
        for e in front:  # @line L15
            s = set(e)
            if s != {b, c} and segments_cross(b, c, e[0], e[1]):
                return False
            if s != {c, a} and segments_cross(c, a, e[0], e[1]):
                return False
        return True  # @line L16

    while front:  # @line L3
        a, b = min(front, key=lambda e: _d2(e[0], e[1]))  # @line L4
        p, delta = _ideal_point(a, b, h)  # @line L5
        fverts = {v for e in front for v in e}
        left = [v for v in fverts if orient2d(a, b, v) > 0]
        r2 = (0.8 * delta) ** 2
        near = sorted((v for v in left if float(_d2(v, p)) < r2), key=lambda v: (_d2(v, p), v))  # @line L6
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        candidates = [(v, False) for v in near] + [(p, p not in fverts)]
        candidates += [(v, False) for v in sorted(left, key=lambda v: (_d2(v, mid), v))]  # @line L7
        c = None
        for v, new in candidates:  # @line L8
            if v in (a, b):
                continue
            if valid(a, b, v, new, fverts):
                c = v
                break
        if c is None:
            raise RuntimeError("no valid triangle on a front edge; the input is not a simple polygon")
        triangles.append((a, b, c))  # @line L9
        if c not in fverts and c not in vertices:
            vertices.append(c)
        del front[(a, b)]  # @line L10
        if (b, c) in front:
            del front[(b, c)]
        else:
            front[(c, b)] = None
        if (c, a) in front:
            del front[(c, a)]
        else:
            front[(a, c)] = None
    return triangles, vertices  # @line L11


def min_angle_degrees(triangles: Sequence[Triangle]) -> float:
    """The smallest angle over all triangles, in degrees (a float measurement)."""
    best = 180.0
    for t in triangles:
        for k in range(3):
            p, q, r = [tuple(map(float, x)) for x in (t[k], t[(k + 1) % 3], t[(k + 2) % 3])]
            u = (q[0] - p[0], q[1] - p[1])
            v = (r[0] - p[0], r[1] - p[1])
            ang = math.degrees(math.atan2(abs(u[0] * v[1] - u[1] * v[0]), u[0] * v[0] + u[1] * v[1]))
            best = min(best, ang)
    return best
