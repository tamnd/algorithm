# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gjk-algorithm/. The authors are listed in prov/QSXJNC.jsonl.
"""Exact Gilbert-Johnson-Keerthi distance algorithm in the plane.

P and Q are finite nonempty lists of points with int or Fraction coordinates;
the convex sets are their convex hulls. M = conv(P) - conv(Q) is the
Minkowski difference. The result is the squared distance between the hulls,
as an exact Fraction, together with the point v of M nearest to the origin.
The distance is sqrt of the squared distance; v / |v| is a separating
direction when the distance is positive.
"""

from dataclasses import dataclass, field
from fractions import Fraction

Point = tuple[Fraction, Fraction]


def _sub(a, b) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def support(points, d):
    """A point of the list with the largest dot product with d (the first one on ties)."""
    best = points[0]
    bv = _dot(best, d)
    for p in points[1:]:
        pv = _dot(p, d)
        if pv > bv:
            best, bv = p, pv
    return best


def _closest_on_segment(a, b):
    """The point of segment ab nearest to the origin, and the smallest subset that holds it."""
    ab = _sub(b, a)
    den = _dot(ab, ab)
    if den == 0:
        return a, [a]
    t = Fraction(-_dot(a, ab)) / den
    if t <= 0:
        return a, [a]
    if t >= 1:
        return b, [b]
    return (a[0] + t * ab[0], a[1] + t * ab[1]), [a, b]


def closest_on_simplex(w):
    """The point of conv(w) nearest to the origin for 1 to 3 points, and a smallest subset."""
    if len(w) == 1:
        return w[0], list(w)
    if len(w) == 2:
        return _closest_on_segment(w[0], w[1])
    a, b, c = w
    area = _cross(_sub(b, a), _sub(c, a))
    if area != 0:
        s1 = _cross(_sub(b, a), _sub((0, 0), a))
        s2 = _cross(_sub(c, b), _sub((0, 0), b))
        s3 = _cross(_sub(a, c), _sub((0, 0), c))
        if all(s * area >= 0 for s in (s1, s2, s3)):
            return (Fraction(0), Fraction(0)), [a, b, c]
    best = None
    for x, y in ((a, b), (b, c), (c, a)):
        v, sub = _closest_on_segment(x, y)
        if best is None or _dot(v, v) < _dot(best[0], best[0]):
            best = (v, sub)
    return best


@dataclass
class GJKResult:
    dist2: Fraction
    v: Point
    iterations: int
    trace: list = field(default_factory=list)


def gjk_distance(p_pts, q_pts, keep_trace=False) -> GJKResult:
    """Squared distance between conv(p_pts) and conv(q_pts), exactly."""
    if not p_pts or not q_pts:
        raise ValueError("both point lists must be nonempty")
    pp = [(Fraction(x), Fraction(y)) for x, y in p_pts]
    qq = [(Fraction(x), Fraction(y)) for x, y in q_pts]
    v = _sub(pp[0], qq[0])  # @line L1
    w_set = [v]
    trace = []
    it = 0
    while True:  # @line L2
        it += 1
        if v == (0, 0):  # @line L3
            return GJKResult(Fraction(0), v, it, trace)
        w = _sub(support(pp, (-v[0], -v[1])), support(qq, v))  # @line L4
        if keep_trace:
            trace.append((v, w, list(w_set)))
        if _dot(v, v) - _dot(v, w) <= 0:  # @line L5
            return GJKResult(_dot(v, v), v, it, trace)
        w_set = w_set + [w]  # @line L6
        v, w_set = closest_on_simplex(w_set)  # @line L7
        w_set = list(w_set)  # @line L8 (the subset from closest_on_simplex)


def intersects(p_pts, q_pts) -> bool:
    return gjk_distance(p_pts, q_pts).dist2 == 0
