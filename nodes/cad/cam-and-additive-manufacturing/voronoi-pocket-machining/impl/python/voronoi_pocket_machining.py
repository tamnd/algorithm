# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voronoi-pocket-machining/. The authors are listed in prov/MEJQSV.jsonl.

"""Voronoi pocket machining on a convex polygon, with exact arithmetic.

Held's method computes the Voronoi diagram of the pocket boundary once and
reads every offset curve from it. Inside a convex polygon the Voronoi diagram
of the edges is the medial axis, and it is made of straight pieces of angle
bisectors. This module builds it with a wavefront: all edges move inward at
unit speed, and an edge disappears when its two neighbours meet on it. The
time of that event is the clearance (the distance to the boundary) of the
node where it happens.

Each arc of the medial axis is the track of one wavefront vertex. Its
clearance grows linearly from one end to the other, so the offset at distance
d is read from the arcs: one point on each arc whose clearance range holds d.

The pocket must be strictly convex, counterclockwise, with edges of rational
length, so that the unit normals are rational. A nonconvex pocket has
reflex vertices, and its Voronoi diagram then has parabolic arcs and its
offsets have circular arcs; this module does not handle that case.
"""

from fractions import Fraction
from math import isqrt

Point = tuple[Fraction, Fraction]


def _exact_sqrt(q: Fraction) -> Fraction:
    q = Fraction(q)
    rn, rd = isqrt(q.numerator), isqrt(q.denominator)
    if rn * rn != q.numerator or rd * rd != q.denominator:
        raise ValueError("an edge has an irrational length")
    return Fraction(rn, rd)


def cross(o: Point, a: Point, b: Point) -> Fraction:
    """The orientation test: positive for a left turn, zero when collinear."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def half_planes(poly):
    """Edge i goes from vertex i to vertex i + 1; it is a x + b y <= c with a unit normal."""
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
        length = _exact_sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        a, b = (y1 - y0) / length, -(x1 - x0) / length
        out.append((a, b, a * x0 + b * y0))
    return pts, out


def _meet(planes, i, j, k):
    """The point and time where the moved lines of edges i, j and k meet (Cramer's rule)."""
    rows = [planes[i], planes[j], planes[k]]
    m = [[a, b, Fraction(1)] for a, b, _ in rows]
    rhs = [c for _, _, c in rows]

    def det(q):
        return (q[0][0] * (q[1][1] * q[2][2] - q[1][2] * q[2][1])
                - q[0][1] * (q[1][0] * q[2][2] - q[1][2] * q[2][0])
                + q[0][2] * (q[1][0] * q[2][1] - q[1][1] * q[2][0]))

    d = det(m)
    sol = []
    for col in range(3):
        q = [row[:] for row in m]
        for r in range(3):
            q[r][col] = rhs[r]
        sol.append(det(q) / d)
    return (sol[0], sol[1]), sol[2]


class Arc:
    """The track of the wavefront vertex between edges left and right."""

    __slots__ = ("left", "right", "p0", "t0", "p1", "t1", "next")

    def __init__(self, left, right, p0, t0):
        self.left, self.right = left, right
        self.p0, self.t0 = p0, t0
        self.p1 = self.t1 = None
        self.next = None  # the arc that starts where this one ends

    def at(self, d) -> list[Point]:
        """The points of the arc with clearance d."""
        if not (self.t0 <= d <= self.t1):
            return []
        if self.t1 == self.t0:
            return [self.p0, self.p1]
        lam = (d - self.t0) / (self.t1 - self.t0)
        return [(self.p0[0] + lam * (self.p1[0] - self.p0[0]), self.p0[1] + lam * (self.p1[1] - self.p0[1]))]


def medial_axis(poly):
    """The medial axis of a convex polygon as a list of arcs, and its deepest node.

    The first n arcs start at the polygon vertices: arc i starts at vertex
    i + 1, between edges i and i + 1. Every arc ends at a node, and arc.next is
    the arc that leaves that node (None at the deepest node).
    """
    pts, planes = half_planes(poly)
    n = len(pts)
    front = list(range(n))  # @line L1
    arcs = []
    live = {}  # (left, right) -> Arc
    for i in range(n):
        a = Arc(i, (i + 1) % n, pts[(i + 1) % n], Fraction(0))
        arcs.append(a)
        live[(i, (i + 1) % n)] = a
    while len(front) > 3:  # @line L2
        best = None
        m = len(front)
        for pos in range(m):  # @line L3
            p, e, q = front[pos - 1], front[pos], front[(pos + 1) % m]
            point, t = _meet(planes, p, e, q)
            if best is None or t < best[0]:
                best = (t, pos, point)
        t, pos, point = best  # @line L4
        p, e, q = front[pos - 1], front[pos], front[(pos + 1) % m]
        a1, a2 = live.pop((p, e)), live.pop((e, q))  # @line L5
        new = Arc(p, q, point, t)  # @line L6
        for a in (a1, a2):
            a.p1, a.t1, a.next = point, t, new
        arcs.append(new)
        live[(p, q)] = new
        front.pop(pos)  # @line L7
    point, t = _meet(planes, *front)  # @line L8
    for a in live.values():
        a.p1, a.t1 = point, t
    return arcs, (point, t)


def convex_hull(points: list[Point]) -> list[Point]:
    """Andrew's monotone chain; collinear points are dropped. Exact for rationals."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    return hull if len(hull) > 2 else [pts[0], pts[-1]]


def offset_from_axis(arcs, d) -> list[Point]:
    """The offset at distance d, read from the medial axis.

    Inside a convex pocket the points of clearance d on the arcs are the
    vertices of the offset, so the offset is their convex hull.
    """
    d = Fraction(d)
    found = []
    for a in arcs:  # @line L10
        found.extend(a.at(d))
    return convex_hull(found)  # @line L11


def spine(arcs, start=0):
    """The chain of arcs from polygon vertex start + 1 to the deepest node."""
    chain = []
    a = arcs[start]
    while a is not None:
        chain.append(a)
        a = a.next
    return chain


def point_on_spine(chain, d) -> Point:
    """The point of clearance d on a chain whose clearance does not decrease."""
    for a in chain:
        if a.t0 <= d <= a.t1:
            return a.at(d)[0]
    raise ValueError("no point of this clearance on the chain")


def voronoi_pocket(poly, r, s):
    """Loops at d = r, r + s, ... and the links between them along the medial axis.

    Returns (loops, links). Each loop is (d, polygon) and starts at the point
    where the spine meets it. Link k goes from loop k to loop k + 1 along the
    spine, so it stays at clearance at least r.
    """
    r, s = Fraction(r), Fraction(s)
    if r <= 0 or s <= 0:
        raise ValueError("r and s must be positive")
    arcs, (_, deepest) = medial_axis(poly)  # @line L9
    chain = spine(arcs)
    loops, links = [], []
    d = r
    while d <= deepest:  # @line L12
        loop = offset_from_axis(arcs, d)
        loops.append((d, _start_at(loop, point_on_spine(chain, d))))
        nd = d + s
        if nd <= deepest:  # @line L13
            pts = [point_on_spine(chain, d)]
            for a in chain:
                if d < a.t1 and a.t1 < nd:
                    pts.append(a.p1)
            pts.append(point_on_spine(chain, nd))
            links.append(pts)
        d = nd
    return loops, links


def _start_at(loop, p):
    """Rotate a closed loop so that it starts at p, inserting p on an edge if needed."""
    if p in loop:
        k = loop.index(p)
        return loop[k:] + loop[:k]
    m = len(loop)
    for i in range(m):
        a, b = loop[i], loop[(i + 1) % m]
        if cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            return [p] + loop[i + 1:] + loop[:i + 1]
    raise ValueError("the point is not on the loop")
