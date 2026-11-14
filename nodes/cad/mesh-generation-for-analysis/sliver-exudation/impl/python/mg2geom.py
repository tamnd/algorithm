# SPDX-License-Identifier: MIT
# Shared helper of the mg2 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small exact geometric tools used by the mg2 pages.

Points are tuples of int or fractions.Fraction. Every predicate returns an
exact value when the coordinates are int or Fraction, so its sign is the true
sign. A float converts to a Fraction without rounding (exact()), so the sign
is then exact for the float point as it is stored. The angle functions return
floats and are used only to report or to compare with a stated bound.
"""

import math
from fractions import Fraction
from typing import Sequence, Tuple

Point = Tuple


def exact(p: Point) -> Tuple[Fraction, ...]:
    """The point p with each coordinate converted to Fraction, without rounding."""
    return tuple(Fraction(c) for c in p)


def sub(a: Point, b: Point) -> tuple:
    return tuple(x - y for x, y in zip(a, b))


def dot(a: Point, b: Point):
    return sum(x * y for x, y in zip(a, b))


def cross(a: Point, b: Point) -> tuple:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dist2(a: Point, b: Point):
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def det3(r0: Sequence, r1: Sequence, r2: Sequence):
    return dot(r0, cross(r1, r2))


def det4(m: Sequence[Sequence]):
    """Determinant of a 4 by 4 matrix by cofactor expansion along the first row."""
    total = 0
    for j in range(4):
        minor = [[m[i][k] for k in range(4) if k != j] for i in range(1, 4)]
        term = m[0][j] * det3(minor[0], minor[1], minor[2])
        total += term if j % 2 == 0 else -term
    return total


def orient2d(a: Point, b: Point, c: Point):
    """Twice the signed area of the triangle a, b, c; positive if counterclockwise."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def orient3d(a: Point, b: Point, c: Point, d: Point):
    """Six times the signed volume of the tetrahedron a, b, c, d.

    It is det[b - a, c - a, d - a]: positive when d lies on the side of the
    plane abc from which a, b, c appear clockwise.
    """
    return det3(sub(b, a), sub(c, a), sub(d, a))


def insphere(a: Point, b: Point, c: Point, d: Point, e: Point):
    """Positive if e lies inside the sphere through a, b, c, d, zero on it.

    The value is det of the rows (p - e, |p - e|^2) for p = a, b, c, d,
    divided by nothing, times the sign of orient3d(a, b, c, d), so the result
    does not depend on the order of a, b, c, d. The tetrahedron must not be flat.
    """
    rows = []
    for p in (a, b, c, d):
        v = sub(p, e)
        rows.append([v[0], v[1], v[2], dot(v, v)])
    o = orient3d(a, b, c, d)
    if o == 0:
        raise ValueError("flat tetrahedron")
    val = -det4(rows)
    return val if o > 0 else -val


def circumcenter3(a: Point, b: Point, c: Point, d: Point) -> tuple:
    """Exact circumcenter of a tetrahedron, by Cramer's rule on 2 (p - a) . x = |p - a|^2."""
    u, v, w = sub(b, a), sub(c, a), sub(d, a)
    det = det3(u, v, w)
    if det == 0:
        raise ValueError("flat tetrahedron")
    bu, bv, bw = Fraction(dot(u, u)), Fraction(dot(v, v)), Fraction(dot(w, w))
    # x = (bu (v x w) + bv (w x u) + bw (u x v)) / (2 det)
    cvw, cwu, cuv = cross(v, w), cross(w, u), cross(u, v)
    x = tuple((bu * cvw[k] + bv * cwu[k] + bw * cuv[k]) / (2 * det) for k in range(3))
    return tuple(a[k] + x[k] for k in range(3))


def tri_circumcenter3(a: Point, b: Point, c: Point) -> tuple:
    """Exact circumcenter of a triangle in space (the center of its smallest circumscribed sphere)."""
    u, v = sub(b, a), sub(c, a)
    n = cross(u, v)
    nn = Fraction(dot(n, n))
    if nn == 0:
        raise ValueError("flat triangle")
    t1 = cross(n, u)
    t2 = cross(v, n)
    uu, vv = dot(u, u), dot(v, v)
    # x = (|u|^2 (v x n) + |v|^2 (n x u)) / (2 |n|^2)
    return tuple(a[k] + (uu * t2[k] + vv * t1[k]) / (2 * nn) for k in range(3))


def radius_edge2(a: Point, b: Point, c: Point, d: Point) -> Fraction:
    """Exact square of the radius-edge ratio R / l_min of a tetrahedron."""
    cc = circumcenter3(a, b, c, d)
    r2 = dist2(cc, a)
    pts = (a, b, c, d)
    lmin2 = min(dist2(pts[i], pts[j]) for i in range(4) for j in range(i + 1, 4))
    return Fraction(r2) / Fraction(lmin2)


def _angle(u: Sequence[float], v: Sequence[float]) -> float:
    nu = math.sqrt(sum(x * x for x in u))
    nv = math.sqrt(sum(x * x for x in v))
    c = sum(x * y for x, y in zip(u, v)) / (nu * nv)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def triangle_angles_deg(a: Point, b: Point, c: Point) -> list:
    """The three plane angles of a triangle in degrees, in 2D or 3D (floats)."""
    p = [tuple(float(x) for x in q) for q in (a, b, c)]
    out = []
    for i in range(3):
        o, s, t = p[i], p[(i + 1) % 3], p[(i + 2) % 3]
        out.append(_angle(sub(s, o), sub(t, o)))
    return out


def dihedral_angles_deg(a: Point, b: Point, c: Point, d: Point) -> list:
    """The six dihedral angles of a tetrahedron in degrees (floats).

    The angle at edge pq is the angle between the two faces pqr and pqs,
    measured inside the tetrahedron.
    """
    p = [tuple(float(x) for x in q) for q in (a, b, c, d)]
    out = []
    for i in range(4):
        for j in range(i + 1, 4):
            k, m = [t for t in range(4) if t not in (i, j)]
            e = sub(p[j], p[i])
            ee = dot(e, e)
            # components of p_k - p_i and p_m - p_i orthogonal to the edge
            u = sub(p[k], p[i])
            v = sub(p[m], p[i])
            u = tuple(u[t] - dot(u, e) / ee * e[t] for t in range(3))
            v = tuple(v[t] - dot(v, e) / ee * e[t] for t in range(3))
            out.append(_angle(u, v))
    return out
