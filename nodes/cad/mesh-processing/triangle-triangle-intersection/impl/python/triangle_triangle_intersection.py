# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-triangle-intersection/. The authors are listed in prov/QR3KY9.jsonl.

"""Exact test whether two closed triangles in 3D intersect.

The method is the plane-side and interval method of Moller (1997). Every
sign is computed exactly: coordinates are int or fractions.Fraction, and the
interval ends on the common line are Fractions. Triangles must not be
degenerate (their three vertices must not be collinear).
"""

from fractions import Fraction
from typing import Sequence, Union

Num = Union[int, Fraction]
Point = Sequence[Num]
Triangle = Sequence[Point]


def sub(a: Point, b: Point) -> tuple[Num, Num, Num]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Point, b: Point) -> tuple[Num, Num, Num]:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a: Point, b: Point) -> Num:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normal(t: Triangle) -> tuple[Num, Num, Num]:
    return cross(sub(t[1], t[0]), sub(t[2], t[0]))


def orient3d(a: Point, b: Point, c: Point, d: Point) -> Num:
    """det[b - a, c - a, d - a]: positive when d is on the side of the normal of (a, b, c)."""
    return dot(cross(sub(b, a), sub(c, a)), sub(d, a))


def sign(x: Num) -> int:
    return (x > 0) - (x < 0)


def orient2d(a: Sequence[Num], b: Sequence[Num], c: Sequence[Num]) -> int:
    return sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def on_segment(a: Sequence[Num], b: Sequence[Num], c: Sequence[Num]) -> bool:
    """For collinear a, b, c: is c on the closed segment ab?"""
    return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])


def segments_meet_2d(a, b, c, d) -> bool:
    """Do the closed segments ab and cd of the plane meet?"""
    o1, o2, o3, o4 = orient2d(a, b, c), orient2d(a, b, d), orient2d(c, d, a), orient2d(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return ((o1 == 0 and on_segment(a, b, c)) or (o2 == 0 and on_segment(a, b, d))
            or (o3 == 0 and on_segment(c, d, a)) or (o4 == 0 and on_segment(c, d, b)))


def in_triangle_2d(p, t) -> bool:
    """Is p in the closed, non-degenerate triangle t of the plane?"""
    s = [orient2d(t[i], t[(i + 1) % 3], p) for i in range(3)]
    return min(s) >= 0 or max(s) <= 0


def coplanar_tri_tri(p: Triangle, q: Triangle) -> bool:
    """Two triangles in one plane: project to the axis plane where the normal is largest."""
    n = normal(p)
    k = max(range(3), key=lambda i: abs(n[i]))  # @line L13
    keep = [i for i in range(3) if i != k]
    p2 = [(v[keep[0]], v[keep[1]]) for v in p]
    q2 = [(v[keep[0]], v[keep[1]]) for v in q]
    for i in range(3):  # @line L14
        for j in range(3):
            if segments_meet_2d(p2[i], p2[(i + 1) % 3], q2[j], q2[(j + 1) % 3]):
                return True
    return in_triangle_2d(p2[0], q2) or in_triangle_2d(q2[0], p2)  # @line L15


def span(t: Triangle, s: Sequence[Num], d: Point) -> tuple[Fraction, Fraction]:
    """The projections on d of the part of t that lies in the plane of the other triangle.

    s[i] is the signed side of vertex i of t. The signs are not all equal and non-zero.
    """
    x = [Fraction(dot(d, t[i])) for i in range(3) if s[i] == 0]  # @line L9
    for i in range(3):  # @line L10
        j = (i + 1) % 3
        if s[i] * s[j] < 0:
            di, dj = dot(d, t[i]), dot(d, t[j])
            x.append(Fraction(di) + Fraction(dj - di) * Fraction(s[i], 1) / (s[i] - s[j]))  # @line L11
    return min(x), max(x)  # @line L12


def tri_tri(p: Triangle, q: Triangle) -> bool:
    """Return True when the closed triangles p and q share at least one point.

    Precondition: neither triangle is degenerate. Coordinates are int or
    Fraction. Time O(1); every decision is an exact sign.
    """
    dq = [orient3d(p[0], p[1], p[2], q[i]) for i in range(3)]  # @line L1
    if min(dq) > 0 or max(dq) < 0:  # @line L2
        return False
    dp = [orient3d(q[0], q[1], q[2], p[i]) for i in range(3)]  # @line L3
    if min(dp) > 0 or max(dp) < 0:  # @line L4
        return False
    if dq == [0, 0, 0]:  # @line L5
        return coplanar_tri_tri(p, q)
    d = cross(normal(p), normal(q))  # @line L6
    a, b = span(p, dp, d)  # @line L7
    c, e = span(q, dq, d)
    return max(a, c) <= min(b, e)  # @line L8


def orient3d_float(a: Point, b: Point, c: Point, d: Point) -> float:
    """The same determinant in floating point, to show how its sign can be wrong."""
    fa, fb, fc, fd = ([float(x) for x in v] for v in (a, b, c, d))
    return orient3d(fa, fb, fc, fd)  # type: ignore[arg-type]
