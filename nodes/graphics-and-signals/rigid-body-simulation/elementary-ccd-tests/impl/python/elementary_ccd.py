# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elementary-ccd-tests/. The authors are listed in prov/RXJ8EY.jsonl.

"""Vertex-face and edge-edge continuous collision tests in 3D.

Each point moves on a line from its position at t = 0 to its position at t = 1. Four points are
coplanar at time t exactly when the triple product f(t) = u(t) . (v(t) x w(t)) is 0, where for a
vertex p and a triangle abc, u = p - a, v = b - a, w = c - a, and for edges ab and cd,
u = c - a, v = b - a, w = d - c. Each of u, v, w is linear in t, so f is a cubic.

The tests find the roots of f in [0, 1] in increasing order: the critical points of f (a quadratic)
split [0, 1] into pieces on which f is monotone, and bisection finds the root of each piece with a
sign change. At each root they check if the vertex is on the triangle, or if the edges meet, with
a distance tolerance delta. The first root that passes is the time of impact.

The cubic works on float or on Fraction input. sturm_count gives the exact number of distinct
roots in an open interval with Fraction arithmetic, which the tests use to check the float roots.

The module is not named after the slug, because a file name that ends in "tests" counts as a
test file.
"""

from __future__ import annotations

import math

Vec = tuple


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _lerp(p0, p1, t):
    return (p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]), p0[2] + t * (p1[2] - p0[2]))


def _pmul(a: list, b: list) -> list:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _padd(a: list, b: list) -> list:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def _psub(a: list, b: list) -> list:
    return _padd(a, [-x for x in b])


def triple_product_cubic(u0, u1, v0, v1, w0, w1) -> list:
    """Coefficients [c0, c1, c2, c3] of f(t) = u(t) . (v(t) x w(t)) for linear u, v, w."""
    U = [[u0[i], u1[i] - u0[i]] for i in range(3)]
    V = [[v0[i], v1[i] - v0[i]] for i in range(3)]
    W = [[w0[i], w1[i] - w0[i]] for i in range(3)]
    f = [0]
    for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        f = _padd(f, _pmul(U[i], _psub(_pmul(V[j], W[k]), _pmul(V[k], W[j]))))
    return (f + [0, 0, 0, 0])[:4]


def vertex_face_cubic(p0, p1, a0, a1, b0, b1, c0, c1) -> list:
    """The coplanarity cubic of a moving vertex p and a moving triangle abc."""
    return triple_product_cubic(_sub(p0, a0), _sub(p1, a1), _sub(b0, a0), _sub(b1, a1), _sub(c0, a0), _sub(c1, a1))


def edge_edge_cubic(a0, a1, b0, b1, c0, c1, d0, d1) -> list:
    """The coplanarity cubic of a moving edge ab and a moving edge cd."""
    return triple_product_cubic(_sub(c0, a0), _sub(c1, a1), _sub(b0, a0), _sub(b1, a1), _sub(d0, c0), _sub(d1, c1))


def poly_eval(c: list, t):
    r = 0
    for x in reversed(c):
        r = r * t + x
    return r


def _quadratic_roots(A: float, B: float, C: float) -> list[float]:
    if A == 0:
        return [] if B == 0 else [-C / B]
    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    q = -(B + math.copysign(math.sqrt(disc), B)) / 2
    roots = [q / A]
    if q != 0:
        roots.append(C / q)
    return sorted(roots)


def cubic_roots_01(c: list, iters: int = 80) -> list[float]:
    """The roots of the cubic c in [0, 1], in increasing order, found in floating point.

    Raises ValueError if c is the zero polynomial (the four points stay coplanar).
    """
    c = [float(x) for x in c]
    if all(x == 0 for x in c):
        raise ValueError("the points are coplanar at all times")
    crit = [t for t in _quadratic_roots(3 * c[3], 2 * c[2], c[1]) if 0 < t < 1]  # @line L2
    pts = [0.0] + crit + [1.0]
    roots: list[float] = []
    for lo, hi in zip(pts, pts[1:]):  # @line L3
        flo, fhi = poly_eval(c, lo), poly_eval(c, hi)
        if flo == 0:
            roots.append(lo)
        elif fhi != 0 and (flo < 0) != (fhi < 0):  # @line L4
            for _ in range(iters):  # bisection on a monotone piece, keeping f(lo) of the sign of f(start)
                mid = (lo + hi) / 2
                if not lo < mid < hi:
                    break
                fm = poly_eval(c, mid)
                if fm == 0:
                    lo = mid
                    break
                if (fm < 0) == (flo < 0):
                    lo, flo = mid, fm
                else:
                    hi = mid
            roots.append(lo)  # the end of the bracket before the root, so the time is not late
    if poly_eval(c, 1.0) == 0:
        roots.append(1.0)
    out: list[float] = []
    for r in roots:
        if not out or r > out[-1]:
            out.append(r)
    return out


def closest_point_on_triangle(p, a, b, c):
    """The point of the triangle abc closest to p, by its Voronoi regions."""
    ab, ac, ap = _sub(b, a), _sub(c, a), _sub(p, a)
    d1, d2 = _dot(ab, ap), _dot(ac, ap)
    if d1 <= 0 and d2 <= 0:
        return a
    bp = _sub(p, b)
    d3, d4 = _dot(ab, bp), _dot(ac, bp)
    if d3 >= 0 and d4 <= d3:
        return b
    vc = d1 * d4 - d3 * d2
    if vc <= 0 and d1 >= 0 and d3 <= 0:
        return _lerp(a, b, d1 / (d1 - d3))
    cp = _sub(p, c)
    d5, d6 = _dot(ab, cp), _dot(ac, cp)
    if d6 >= 0 and d5 <= d6:
        return c
    vb = d5 * d2 - d1 * d6
    if vb <= 0 and d2 >= 0 and d6 <= 0:
        return _lerp(a, c, d2 / (d2 - d6))
    va = d3 * d6 - d5 * d4
    if va <= 0 and d4 - d3 >= 0 and d5 - d6 >= 0:
        return _lerp(b, c, (d4 - d3) / ((d4 - d3) + (d5 - d6)))
    s = va + vb + vc
    v, w = vb / s, vc / s
    return (a[0] + ab[0] * v + ac[0] * w, a[1] + ab[1] * v + ac[1] * w, a[2] + ab[2] * v + ac[2] * w)


def closest_points_segments(p1, q1, p2, q2):
    """Closest points of the segments p1q1 and p2q2."""
    d1, d2, r = _sub(q1, p1), _sub(q2, p2), _sub(p1, p2)
    a, e, f = _dot(d1, d1), _dot(d2, d2), _dot(d2, r)

    def clamp(x):
        return 0 if x < 0 else 1 if x > 1 else x

    if a == 0 and e == 0:
        s = t = 0
    elif a == 0:
        s, t = 0, clamp(f / e)
    else:
        cc = _dot(d1, r)
        if e == 0:
            s, t = clamp(-cc / a), 0
        else:
            b = _dot(d1, d2)
            denom = a * e - b * b
            s = clamp((b * f - cc * e) / denom) if denom != 0 else 0
            t = (b * s + f) / e
            if t < 0:
                s, t = clamp(-cc / a), 0
            elif t > 1:
                s, t = clamp((b - cc) / a), 1
    return _lerp(p1, q1, s), _lerp(p2, q2, t)


def _dist(p, q) -> float:
    return math.sqrt(float(_dot(_sub(p, q), _sub(p, q))))


def vertex_face_ccd(p0, p1, a0, a1, b0, b1, c0, c1, delta: float = 1e-9):
    """The first time in [0, 1] at which the moving vertex is on the moving triangle, or None."""
    c = vertex_face_cubic(p0, p1, a0, a1, b0, b1, c0, c1)  # @line L1
    for t in cubic_roots_01(c):  # @line L5
        p, a, b, cc = (_lerp(x0, x1, t) for x0, x1 in ((p0, p1), (a0, a1), (b0, b1), (c0, c1)))
        if _dist(p, closest_point_on_triangle(p, a, b, cc)) <= delta:  # @line L6
            return t  # @line L7
    return None  # @line L8


def edge_edge_ccd(a0, a1, b0, b1, c0, c1, d0, d1, delta: float = 1e-9):
    """The first time in [0, 1] at which the moving edges ab and cd meet, or None."""
    c = edge_edge_cubic(a0, a1, b0, b1, c0, c1, d0, d1)
    for t in cubic_roots_01(c):
        a, b, cc, d = (_lerp(x0, x1, t) for x0, x1 in ((a0, a1), (b0, b1), (c0, c1), (d0, d1)))
        x, y = closest_points_segments(a, b, cc, d)
        if _dist(x, y) <= delta:
            return t
    return None


def sturm_count(c: list, lo, hi) -> int:
    """The exact number of distinct real roots of the polynomial c in the open interval (lo, hi).

    Use Fraction coefficients and bounds, with lo and hi not roots. c must not be zero.
    """
    def trim(p):
        p = list(p)
        while p and p[-1] == 0:
            p.pop()
        return p

    def rem(a, b):
        a = list(a)
        while len(a) >= len(b):
            k = a[-1] / b[-1]
            shift = len(a) - len(b)
            for i in range(len(b)):
                a[shift + i] -= k * b[i]
            a.pop()
            a = trim(a)
            if not a:
                break
        return a

    p0 = trim(c)
    seq = [p0, trim([i * p0[i] for i in range(1, len(p0))])]
    while seq[-1]:
        r = rem(seq[-2], seq[-1])
        if not r:
            break
        seq.append([-x for x in r])

    def changes(x):
        signs = [s for s in (poly_eval(p, x) for p in seq if p) if s != 0]
        return sum(1 for u, v in zip(signs, signs[1:]) if (u < 0) != (v < 0))

    return changes(lo) - changes(hi)
