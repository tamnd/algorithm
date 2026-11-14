# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tukey-median/. The authors are listed in prov/ES2QKG.jsonl.

from fractions import Fraction
from functools import cmp_to_key
from math import ceil


def _half(v):
    """0 for the angles in [0, pi), 1 for the angles in [pi, 2 pi)."""
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _angle_cmp(a, b):
    """Exact comparison of the polar angles of two nonzero vectors."""
    ha, hb = _half(a), _half(b)
    if ha != hb:
        return ha - hb
    c = _cross(a, b)
    return -1 if c > 0 else (1 if c < 0 else 0)


def _in_half_turn(a, v):
    """True when the angle of v is in [angle(a), angle(a) + pi)."""
    c = _cross(a, v)
    return c > 0 or (c == 0 and _dot(a, v) > 0)


def depth(x, points):
    """Halfspace depth of x in a planar sample, in O(n log n) exact steps.

    The depth is the least number of sample points in a closed halfplane
    that contains x. The coordinates can be int or Fraction.
    """
    k0 = sum(1 for p in points if p[0] == x[0] and p[1] == x[1])  # @line L1
    d = [(p[0] - x[0], p[1] - x[1]) for p in points
         if p[0] != x[0] or p[1] != x[1]]  # @line L2
    m = len(d)
    if m == 0:
        return k0
    d.sort(key=cmp_to_key(_angle_cmp))  # @line L3
    best, e = m, 0  # @line L4
    for j in range(m):  # @line L5
        if j > 0 and _angle_cmp(d[j - 1], d[j]) == 0:
            continue  # only the first vector of a group of equal angle
        e = max(e, j)  # @line L6
        while e < j + m and _in_half_turn(d[j], d[e % m]):  # @line L7
            e += 1
        best = min(best, e - j, m - (e - j))  # @line L8
    return k0 + best  # @line L9


def _collinear(points):
    a = points[0]
    b = next((p for p in points if p != a), None)
    if b is None:
        return True
    ab = (b[0] - a[0], b[1] - a[1])
    return all(_cross(ab, (p[0] - a[0], p[1] - a[1])) == 0 for p in points)


def _median_on_line(points):
    """Deepest point and its depth when all points lie on one line."""
    n = len(points)
    a = points[0]
    b = next((p for p in points if p != a), a)
    v = (b[0] - a[0], b[1] - a[1])
    if v == (0, 0):
        return (Fraction(a[0]), Fraction(a[1])), n
    t = sorted(Fraction(_dot(v, (p[0] - a[0], p[1] - a[1]))) / _dot(v, v)
               for p in points)
    mid = (t[(n - 1) // 2] + t[n // 2]) / 2
    point = (a[0] + mid * v[0], a[1] + mid * v[1])
    dep = min(sum(1 for s in t if s <= mid), sum(1 for s in t if s >= mid))
    return point, dep


def _clip(poly, u, q):
    """Clip a convex polygon (a list of vertices) to the halfplane u.x <= q."""
    out = []
    k = len(poly)
    for i in range(k):
        p, r = poly[i], poly[(i + 1) % k]
        fp, fr = _dot(u, p) - q, _dot(u, r) - q
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fr) or (fr < 0 < fp):
            t = fp / (fp - fr)
            out.append((p[0] + t * (r[0] - p[0]), p[1] + t * (r[1] - p[1])))
    clean = []
    for p in out:
        if not clean or clean[-1] != p:
            clean.append(p)
    while len(clean) > 1 and clean[0] == clean[-1]:
        clean.pop()
    return clean


def _directions(points):
    """The critical directions: both normals of each line through two points."""
    seen = set()
    dirs = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            a, b = points[i], points[j]
            if a == b:
                continue
            for u in ((a[1] - b[1], b[0] - a[0]), (b[1] - a[1], a[0] - b[0])):
                key = (Fraction(u[0]), Fraction(u[1]))
                g = max(abs(key[0]), abs(key[1]))
                key = (key[0] / g, key[1] / g)
                if key not in seen:
                    seen.add(key)
                    dirs.append(u)
    return dirs


def depth_region(points, k, dirs=None, proj=None):
    """The depth region D_k = {x : depth(x) >= k} as a list of polygon vertices."""
    if dirs is None:
        dirs = _directions(points)
    if proj is None:
        proj = [sorted((_dot(u, p) for p in points), reverse=True) for u in dirs]
    xs = [Fraction(p[0]) for p in points]
    ys = [Fraction(p[1]) for p in points]
    region = [(min(xs), min(ys)), (max(xs), min(ys)),
              (max(xs), max(ys)), (min(xs), max(ys))]  # @line L19
    for u, pr in zip(dirs, proj):  # @line L20
        q = pr[k - 1]  # @line L21
        region = _clip(region, u, q)  # @line L22
        if not region:  # @line L23
            return []
    return region  # @line L24


def centroid(poly):
    """Centre of gravity of a convex polygon, segment or point (exact)."""
    k = len(poly)
    area2 = Fraction(0)
    cx = cy = Fraction(0)
    for i in range(k):
        p, r = poly[i], poly[(i + 1) % k]
        c = _cross(p, r)
        area2 += c
        cx += (p[0] + r[0]) * c
        cy += (p[1] + r[1]) * c
    if area2 != 0:
        return (cx / (3 * area2), cy / (3 * area2))
    lo = min(poly)
    hi = max(poly)
    return ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2)


def tukey_median(points):
    """Return (median, max_depth) for a planar sample, in exact arithmetic.

    The median is the centre of gravity of the deepest depth region.
    """
    points = [(Fraction(p[0]), Fraction(p[1])) for p in points]
    n = len(points)
    if n == 0:
        raise ValueError("empty sample")
    if _collinear(points):  # @line L10
        return _median_on_line(points)
    dirs = _directions(points)  # @line L11
    proj = [sorted((_dot(u, p) for p in points), reverse=True) for u in dirs]  # @line L12
    lo, hi = ceil(n / 3), n  # @line L13
    while lo < hi:  # @line L14
        k = (lo + hi + 1) // 2  # @line L15
        if depth_region(points, k, dirs, proj):  # @line L16
            lo = k
        else:
            hi = k - 1
    region = depth_region(points, lo, dirs, proj)  # @line L17
    return centroid(region), lo  # @line L18
