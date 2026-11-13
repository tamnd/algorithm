# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subdivision-surface-intersection/. The authors are listed in prov/V3H0YK.jsonl.

"""Intersection of two tensor-product Bezier patches by recursive subdivision, exactly.

A patch is a control net net[i][j] of 3D points with int or Fraction
coordinates, i = 0..p in the u direction and j = 0..q in the v direction,
together with its parameter rectangle (u0, u1, v0, v1) in the original
patch. The method discards a pair of patches whose bounding boxes of the
control points do not overlap, splits a patch that is not flat into four
quarters by de Casteljau's algorithm at the midpoints, and intersects the
corner triangles of two flat patches. All arithmetic is exact, so every
box test and every sign in the triangle test is decided without error.

The result is a list of leaves. A leaf is a pair of parameter rectangles,
one in each patch, whose boxes overlap, together with the segments where
the corner triangles of the two flat pieces meet. A leaf that was reached at
max_depth without being flat has no segments and is flagged.
"""

from fractions import Fraction

Vec = tuple
HALF = Fraction(1, 2)


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec, b: Vec):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def lerp(a: Vec, b: Vec, t) -> Vec:
    return tuple(a[k] + t * (b[k] - a[k]) for k in range(3))


def casteljau_split(points: list, t=HALF):
    """Split a Bezier curve at t; return the control points of the two halves."""
    left, right = [points[0]], [points[-1]]
    cur = list(points)
    while len(cur) > 1:
        cur = [lerp(cur[i], cur[i + 1], t) for i in range(len(cur) - 1)]
        left.append(cur[0])
        right.append(cur[-1])
    return left, right[::-1]


def evaluate(net: list, u, v) -> Vec:
    """De Casteljau evaluation of the patch at (u, v) in [0, 1]^2."""

    def point(points, t):
        cur = list(points)
        while len(cur) > 1:
            cur = [lerp(cur[i], cur[i + 1], t) for i in range(len(cur) - 1)]
        return cur[0]

    return point([point(row, v) for row in net], u)


def split_u(net: list):
    cols = [casteljau_split([net[i][j] for i in range(len(net))]) for j in range(len(net[0]))]
    left = [[cols[j][0][i] for j in range(len(cols))] for i in range(len(net))]
    right = [[cols[j][1][i] for j in range(len(cols))] for i in range(len(net))]
    return left, right


def split_v(net: list):
    halves = [casteljau_split(row) for row in net]
    return [h[0] for h in halves], [h[1] for h in halves]


def quarters(patch):
    """The four quarters of a patch (net, rect) at the midpoints of its rectangle."""
    net, (u0, u1, v0, v1) = patch
    um, vm = (u0 + u1) / 2, (v0 + v1) / 2
    lo, hi = split_u(net)
    out = []
    for half, (a, b) in ((lo, (u0, um)), (hi, (um, u1))):
        n0, n1 = split_v(half)
        out.append((n0, (a, b, v0, vm)))
        out.append((n1, (a, b, vm, v1)))
    return out


def box(net: list):
    pts = [p for row in net for p in row]
    return tuple(min(p[k] for p in pts) for k in range(3)), tuple(max(p[k] for p in pts) for k in range(3))


def boxes_overlap(a, b) -> bool:
    return all(a[0][k] <= b[1][k] and b[0][k] <= a[1][k] for k in range(3))


def diagonal2(bx):
    return sum((bx[1][k] - bx[0][k]) ** 2 for k in range(3))


def is_flat(net: list, eps) -> bool:
    """True when every control point is within eps of the plane of three corners."""
    a, b, c = net[0][0], net[-1][0], net[0][-1]
    n = cross(sub(b, a), sub(c, a))
    nn = dot(n, n)
    if nn == 0:
        return False
    return all(dot(n, sub(p, a)) ** 2 <= eps * eps * nn for row in net for p in row)


def corner_triangles(net: list):
    a, b, c, d = net[0][0], net[-1][0], net[-1][-1], net[0][-1]
    return [(a, b, c), (a, c, d)]


def plane_cut(tri, n, o):
    """The points where the edges of tri meet the plane n . (x - o) = 0."""
    s = [dot(n, sub(p, o)) for p in tri]
    pts = [tri[i] for i in range(3) if s[i] == 0]
    for i in range(3):
        j = (i + 1) % 3
        if (s[i] < 0 < s[j]) or (s[j] < 0 < s[i]):
            pts.append(lerp(tri[i], tri[j], s[i] / (s[i] - s[j])))
    return s, pts


def triangle_triangle(t1, t2):
    """The segment where two triangles meet, None, or "coplanar"."""
    n1 = cross(sub(t1[1], t1[0]), sub(t1[2], t1[0]))
    n2 = cross(sub(t2[1], t2[0]), sub(t2[2], t2[0]))
    s2, cut2 = plane_cut(t2, n1, t1[0])
    if all(x > 0 for x in s2) or all(x < 0 for x in s2):
        return None
    if all(x == 0 for x in s2):
        return "coplanar"
    s1, cut1 = plane_cut(t1, n2, t2[0])
    if all(x > 0 for x in s1) or all(x < 0 for x in s1):
        return None
    D = cross(n1, n2)
    i1 = sorted(cut1, key=lambda p: dot(D, p))
    i2 = sorted(cut2, key=lambda p: dot(D, p))
    lo = max(i1[0], i2[0], key=lambda p: dot(D, p))
    hi = min(i1[-1], i2[-1], key=lambda p: dot(D, p))
    if dot(D, lo) > dot(D, hi):
        return None
    return (lo, hi)


def intersect(P, Q, eps, max_depth: int = 40, depth: int = 0, out=None):
    """All leaves of the subdivision of the pair of patches P and Q, each (net, rect)."""
    if out is None:
        out = []
    bp, bq = box(P[0]), box(Q[0])
    if not boxes_overlap(bp, bq):  # @line L1
        return out
    flat_p, flat_q = is_flat(P[0], eps), is_flat(Q[0], eps)
    if depth >= max_depth and not (flat_p and flat_q):
        out.append({"rects": (P[1], Q[1]), "segments": [], "flat": False})
        return out
    if not flat_p and (flat_q or diagonal2(bp) >= diagonal2(bq)):  # @line L2
        for Pk in quarters(P):  # @line L3
            intersect(Pk, Q, eps, max_depth, depth + 1, out)
        return out
    if not flat_q:  # @line L4
        for Qk in quarters(Q):  # @line L5
            intersect(P, Qk, eps, max_depth, depth + 1, out)
        return out
    segments, coplanar = [], False
    for t1 in corner_triangles(P[0]):  # @line L6
        for t2 in corner_triangles(Q[0]):
            s = triangle_triangle(t1, t2)
            if s == "coplanar":
                coplanar = True
            elif s is not None:
                segments.append(s)
    out.append({"rects": (P[1], Q[1]), "segments": segments, "flat": True, "coplanar": coplanar})  # @line L7
    return out


def patch(net: list):
    """Wrap a control net as a patch over the unit square."""
    one = Fraction(1)
    return ([[tuple(Fraction(x) for x in p) for p in row] for row in net], (Fraction(0), one, Fraction(0), one))
