# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expanding-polytope-algorithm/. The authors are listed in prov/PP6HVM.jsonl.

"""The expanding polytope algorithm (EPA) for two convex polygons in the plane.

Shapes are given only by support functions: support(d) returns a point of the shape that is
extreme in the direction d. A small 2D GJK (gjk_triangle) finds a triangle of support points of
the Minkowski difference A - B that contains the origin. EPA then grows a convex polygon inside
A - B: it takes the edge closest to the origin, asks for the support point of A - B along the
normal of that edge, and inserts it, until the support point is at most eps beyond the edge.

The result is the penetration depth d, the unit normal n from B to A (moving A by d n makes the
shapes touch), and a point on A and a point on B whose difference is the deepest point.
With exact arithmetic, the returned depth d satisfies d <= depth <= d + eps. Floats are used.
"""

from __future__ import annotations

import math
from typing import Callable

Vec = tuple[float, float]
Support = Callable[[Vec], Vec]


def _sub(p: Vec, q: Vec) -> Vec:
    return (p[0] - q[0], p[1] - q[1])


def _dot(u: Vec, v: Vec) -> float:
    return u[0] * v[0] + u[1] * v[1]


def _cross(u: Vec, v: Vec) -> float:
    return u[0] * v[1] - u[1] * v[0]


def polygon_support(P: list[Vec]) -> Support:
    """The support function of the convex hull of the points P (a linear scan)."""

    def s(d: Vec) -> Vec:
        return max(P, key=lambda p: p[0] * d[0] + p[1] * d[1])

    return s


def _diff_support(sa: Support, sb: Support, d: Vec) -> tuple[Vec, Vec, Vec]:
    a = sa(d)
    b = sb((-d[0], -d[1]))
    return (a[0] - b[0], a[1] - b[1]), a, b


def gjk_triangle(sa: Support, sb: Support, max_iter: int = 100):
    """A counterclockwise triangle of (w, a, b) support triples of A - B that contains the origin.

    Returns None if A and B are disjoint or only touch (the origin is on the boundary of A - B).
    This is the boolean part of GJK in 2D.
    """
    d = (1.0, 0.0)
    simplex = [_diff_support(sa, sb, d)]
    w = simplex[0][0]
    if w == (0.0, 0.0):
        return None  # the origin is a support point, so it is on the boundary
    d = (-w[0], -w[1])
    for _ in range(max_iter):
        t = _diff_support(sa, sb, d)
        if _dot(t[0], d) < 0:
            return None  # the support point does not pass the origin: a separating direction
        simplex.append(t)
        a = t[0]
        ao = (-a[0], -a[1])
        if len(simplex) == 2:
            b = simplex[0][0]
            ab = _sub(b, a)
            perp = (-ab[1], ab[0])
            if _dot(perp, ao) < 0:
                perp = (ab[1], -ab[0])
            d = perp
            continue
        c, b = simplex[0][0], simplex[1][0]
        ab, ac = _sub(b, a), _sub(c, a)
        side = _cross(ab, ac)
        if side == 0:
            return None  # a, b, c on one line through the origin: the shapes only touch
        ab_out = (ab[1], -ab[0]) if side > 0 else (-ab[1], ab[0])  # normal of ab away from c
        ac_out = (-ac[1], ac[0]) if side > 0 else (ac[1], -ac[0])  # normal of ac away from b
        if _dot(ab_out, ao) > 0:
            simplex = [simplex[1], simplex[2]]
            d = ab_out
        elif _dot(ac_out, ao) > 0:
            simplex = [simplex[0], simplex[2]]
            d = ac_out
        else:
            if side > 0:  # a, b, c is counterclockwise, so c, b, a is clockwise
                simplex = [simplex[2], simplex[1], simplex[0]]
            return simplex
    raise RuntimeError("GJK did not converge")


def epa(sa: Support, sb: Support, eps: float = 1e-10, max_iter: int = 200):
    """Penetration depth and normal of two overlapping convex shapes.

    Returns (depth, normal, point_on_a, point_on_b, iterations), or None if the shapes are disjoint.
    Shapes that only touch give None or a depth of 0.
    """
    tri = gjk_triangle(sa, sb)
    if tri is None:
        return None
    poly = list(tri)  # @line L1
    for it in range(1, max_iter + 1):  # @line L2
        best = None
        for i in range(len(poly)):  # @line L3
            p, q = poly[i][0], poly[(i + 1) % len(poly)][0]
            e = _sub(q, p)
            length = math.hypot(e[0], e[1])
            n = (e[1] / length, -e[0] / length)  # outward for a counterclockwise polygon
            dist = _dot(n, p)
            if best is None or dist < best[0]:  # @line L4
                best = (dist, n, i)
        dist, n, i = best
        t = _diff_support(sa, sb, n)  # @line L5
        if _dot(n, t[0]) - dist <= eps:  # @line L6
            p, q = poly[i], poly[(i + 1) % len(poly)]
            e = _sub(q[0], p[0])
            lam = -_dot(p[0], e) / _dot(e, e)  # the foot of the perpendicular from the origin
            lam = min(1.0, max(0.0, lam))
            pa = (p[1][0] + lam * (q[1][0] - p[1][0]), p[1][1] + lam * (q[1][1] - p[1][1]))
            pb = (p[2][0] + lam * (q[2][0] - p[2][0]), p[2][1] + lam * (q[2][1] - p[2][1]))
            return dist, (-n[0], -n[1]), pa, pb, it
        poly.insert(i + 1, t)  # @line L7
    raise RuntimeError("EPA did not converge; eps is too small for the arithmetic")
