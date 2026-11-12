# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/catmull-rom-spline/. The authors are listed in prov/SBH6DE.jsonl.

"""Catmull-Rom splines: uniform (matrix form) and nonuniform (Barry-Goldman pyramid).

A point is a tuple of numbers; use fractions.Fraction for exact results. The
control points are P[0..n]; the curve runs from P[1] to P[n-1], so P[0] and
P[n] only set the end tangents. Segment i (1 <= i <= n-2) joins P[i] to P[i+1]
and uses P[i-1], P[i], P[i+1], P[i+2].
Cost: O(d) per point in the uniform form and O(d) (a pyramid of 6 lerps) in
the nonuniform form, for d coordinates.
"""

import math
from bisect import bisect_right
from typing import List, Sequence, Tuple

Point = Tuple

# 2 * M, the uniform Catmull-Rom basis matrix in the power basis (rows: 1, u, u^2, u^3).
M2 = ((0, 2, 0, 0), (-1, 0, 1, 0), (2, -5, 4, -1), (-1, 3, -3, 1))


def _comb(ws, pts):
    return tuple(sum(w * p[k] for w, p in zip(ws, pts)) for k in range(len(pts[0])))


def uniform_segment(p0: Point, p1: Point, p2: Point, p3: Point, u, order: int = 0) -> Point:
    """Uniform Catmull-Rom segment from p1 (u = 0) to p2 (u = 1), or its derivative in u."""
    pts = (p0, p1, p2, p3)
    coeffs = [tuple(x / 2 for x in _comb(r, pts)) for r in M2]
    out = [0] * len(p0)
    for j in range(order, 4):
        f = 1
        for q in range(j - order + 1, j + 1):
            f *= q
        w = f * u ** (j - order)
        out = [o + w * c for o, c in zip(out, coeffs[j])]
    return tuple(out)


def uniform_tangents(points: Sequence[Point]) -> List[Point]:
    """Tangents (P[i+1] - P[i-1]) / 2 at the inner points P[1..n-1]."""
    return [tuple((b - a) / 2 for a, b in zip(points[i - 1], points[i + 1])) for i in range(1, len(points) - 1)]


def alpha_knots(points: Sequence[Point], alpha: float, t0: float = 0.0) -> List[float]:
    """Knots with t[i+1] - t[i] = |P[i+1] - P[i]| ** alpha: 0 uniform, 1/2 centripetal, 1 chordal.

    Precondition: no two consecutive points are equal when alpha > 0.
    """
    ts = [t0]
    for a, b in zip(points, points[1:]):
        d = math.sqrt(sum((y - x) ** 2 for x, y in zip(a, b)))
        if alpha > 0 and d == 0:
            raise ValueError("consecutive points coincide")
        ts.append(ts[-1] + d ** alpha)
    return ts


def _lerp(a: Point, b: Point, ta, tb, t) -> Point:
    s = (t - ta) / (tb - ta)
    return tuple(x + s * (y - x) for x, y in zip(a, b))


def barry_goldman(p: Sequence[Point], ts: Sequence, t) -> Point:
    """The Barry-Goldman pyramid on one segment: p[0..3] at knots ts[0..3], t in [ts[1], ts[2]].

    Precondition: ts strictly increasing.
    """
    a1 = _lerp(p[0], p[1], ts[0], ts[1], t)
    a2 = _lerp(p[1], p[2], ts[1], ts[2], t)
    a3 = _lerp(p[2], p[3], ts[2], ts[3], t)
    b1 = _lerp(a1, a2, ts[0], ts[2], t)
    b2 = _lerp(a2, a3, ts[1], ts[3], t)
    return _lerp(b1, b2, ts[1], ts[2], t)


def nonuniform_tangent(p: Sequence[Point], ts: Sequence) -> Point:
    """dC/dt at ts[1] of the nonuniform Catmull-Rom curve through p[0], p[1], p[2]."""
    h0 = ts[1] - ts[0]
    h1 = ts[2] - ts[1]
    return tuple(
        (b - a) / h0 - (c - a) / (h0 + h1) + (c - b) / h1 for a, b, c in zip(p[0], p[1], p[2])
    )


def catmull_rom_curve(points: Sequence[Point], knots: Sequence, t) -> Point:
    """Evaluate the Catmull-Rom curve with the given knots at t in [knots[1], knots[n-1]].

    Precondition: len(points) == len(knots) >= 4 and knots strictly increasing.
    """
    n = len(points) - 1
    if n < 3 or len(knots) != n + 1:
        raise ValueError("need at least four points and one knot per point")
    if any(b <= a for a, b in zip(knots, knots[1:])):
        raise ValueError("knots must increase strictly")
    i = bisect_right(knots, t) - 1
    i = min(max(i, 1), n - 2)
    return barry_goldman(points[i - 1 : i + 3], knots[i - 1 : i + 3], t)
