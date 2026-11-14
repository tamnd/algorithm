# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contour-parallel-toolpath/. The authors are listed in prov/DWDHQ8.jsonl.

"""Contour-parallel toolpath for a convex pocket, with exact offsets.

The pocket P is a convex polygon given by its vertices in counterclockwise
order. Every edge must have a rational length, so that its unit normal is
rational and every offset is a polygon with rational vertices. Edge
directions such as (3, 4), (5, 12), (8, 15) and the axis directions qualify.

The offset of P at distance d is the set of points of P whose distance to the
boundary is at least d. For a convex polygon it is the intersection of the
half-planes of the edges, each one moved inward by d. The tool center runs
along the boundaries of the offsets at d = r, r + s, r + 2s, ... until the
offset is empty. Here r is the tool radius and s is the step-over.

All coordinates are int or Fraction. Every sign test is exact.
"""

from fractions import Fraction
from math import isqrt

Point = tuple[Fraction, Fraction]
HalfPlane = tuple[Fraction, Fraction, Fraction]  # a x + b y <= c, with a^2 + b^2 = 1


def _exact_sqrt(q: Fraction) -> Fraction:
    """The square root of a nonnegative rational, or ValueError if it is not rational."""
    q = Fraction(q)
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn != n or rd * rd != d:
        raise ValueError("an edge has an irrational length")
    return Fraction(rn, rd)


def cross(o: Point, a: Point, b: Point) -> Fraction:
    """The orientation test: positive if o, a, b turn left, zero if collinear."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def half_planes(poly: list[Point]) -> list[HalfPlane]:
    """The edge half-planes of a convex counterclockwise polygon, with unit outward normals."""
    pts = [(Fraction(x), Fraction(y)) for x, y in poly]
    n = len(pts)
    if n < 3:
        raise ValueError("a pocket needs at least 3 vertices")
    for i in range(n):
        if cross(pts[i], pts[(i + 1) % n], pts[(i + 2) % n]) <= 0:
            raise ValueError("the polygon is not strictly convex and counterclockwise")
    out = []
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        length = _exact_sqrt(dx * dx + dy * dy)
        a, b = dy / length, -dx / length
        out.append((a, b, a * x0 + b * y0))
    return out


def depth(planes: list[HalfPlane], p: Point) -> Fraction:
    """Signed distance from p to the boundary of the convex polygon: positive inside."""
    return min(c - a * p[0] - b * p[1] for a, b, c in planes)


def clip(poly: list[Point], a: Fraction, b: Fraction, c: Fraction) -> list[Point]:
    """Sutherland-Hodgman clip of a convex polygon by the closed half-plane a x + b y <= c."""
    out: list[Point] = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = c - a * p[0] - b * p[1]
        fq = c - a * q[0] - b * q[1]
        if fp >= 0:
            out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    clean: list[Point] = []
    for v in out:
        if not clean or clean[-1] != v:
            clean.append(v)
    if len(clean) > 1 and clean[0] == clean[-1]:
        clean.pop()
    return clean


def offset(poly: list[Point], d) -> list[Point]:
    """The inward offset of the convex polygon at distance d >= 0.

    The result is a convex polygon, a segment (2 points), a point (1 point) or
    empty. Collinear vertices are removed.
    """
    pts = [(Fraction(x), Fraction(y)) for x, y in poly]
    d = Fraction(d)
    q = pts
    for a, b, c in half_planes(pts):
        q = clip(q, a, b, c - d)
        if not q:
            return []
    if len(q) <= 2:
        return q
    keep = [q[i] for i in range(len(q)) if cross(q[i - 1], q[i], q[(i + 1) % len(q)]) != 0]
    if not keep:  # every vertex is collinear: the offset is a segment
        lo, hi = min(q), max(q)
        return [lo, hi] if lo != hi else [lo]
    return keep


def contour_parallel(poly: list[Point], r, s) -> list[tuple[Fraction, list[Point]]]:
    """The loops of a contour-parallel toolpath, from the outside in.

    Each loop is (d, Q): the tool center runs once around the closed polygon Q,
    the offset of the pocket at distance d. A segment or a point is a loop of
    zero area. The first loop is at d = r and each next one is s further in.
    """
    r, s = Fraction(r), Fraction(s)
    if r <= 0 or s <= 0:
        raise ValueError("r and s must be positive")
    loops = []
    d = r  # @line L1
    while True:  # @line L2
        q = offset(poly, d)  # @line L3
        if not q:  # @line L4
            break
        loops.append((d, q))  # @line L5
        d += s  # @line L6
    # The loops are returned in order; a link joins each loop to the next.
    return loops  # @line L7


def loop_segments(q: list[Point]) -> list[tuple[Point, Point]]:
    """The segments of one closed loop. A point gives one degenerate segment."""
    if len(q) == 1:
        return [(q[0], q[0])]
    if len(q) == 2:
        return [(q[0], q[1])]
    return [(q[i], q[(i + 1) % len(q)]) for i in range(len(q))]


def loop_lengths(loops) -> list[Fraction | None]:
    """The length of each loop when it is rational, else None for that loop.

    A segment loop is run out and back, so its length is twice the segment.
    """
    out: list[Fraction | None] = []
    for _, q in loops:
        total = Fraction(0)
        ok = True
        for p, t in loop_segments(q):
            dx, dy = t[0] - p[0], t[1] - p[1]
            try:
                total += _exact_sqrt(dx * dx + dy * dy)
            except ValueError:
                ok = False
        if len(q) == 2:
            total *= 2
        out.append(total if ok else None)
    return out
