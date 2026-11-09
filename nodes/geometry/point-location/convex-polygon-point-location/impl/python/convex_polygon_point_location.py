# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-polygon-point-location/. The authors are listed in prov/QBH461.jsonl.

"""Point location in a convex polygon by binary search over the wedges around an interior point.

The polygon is a list of integer vertices in counterclockwise order. It must be convex, with at
least three vertices that are not collinear and no repeated vertex. Collinear vertices on an
edge are allowed. The center c is the centroid of v0, v1 and the first vertex vk that is not on
the line v0 v1, so c lies strictly inside. To stay in integers, every predicate that involves c
works with the scaled vectors 3 p - (v0 + v1 + vk).

A query returns one of
    ("vertex", i)   q is the vertex i
    ("edge", i)     q is in the relative interior of the edge from vertex i to vertex i + 1
    ("inside", i)   q is in the open interior, in wedge i
    ("outside", i)  q is outside, in wedge i
Wedge i is bounded by the rays from c through vertex i (included) and vertex i + 1 (excluded).
The center c itself is in wedge 0 by convention.
"""

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of p, q, r: positive for a counterclockwise turn."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class ConvexPolygonLocator:
    def __init__(self, vertices: list[Point]) -> None:
        n = len(vertices)
        if n < 3:
            raise ValueError("a convex polygon needs at least three vertices")
        v0, v1 = vertices[0], vertices[1]
        k = next((j for j in range(2, n) if orient(v0, v1, vertices[j]) != 0), None)
        if k is None:
            raise ValueError("all vertices are collinear")
        self.v = vertices
        self.n = n
        self.s = (v0[0] + v1[0] + vertices[k][0], v0[1] + v1[1] + vertices[k][1])  # 3 c
        self.u = self._vec(v0)  # the direction of angle 0
        self.tests = 0

    def _vec(self, p: Point) -> Point:
        """3 (p - c), an exact integer vector."""
        return (3 * p[0] - self.s[0], 3 * p[1] - self.s[1])

    def _half(self, w: Point) -> int:
        """0 for angles in [0, pi) from the direction u, 1 for [pi, 2 pi)."""
        u = self.u
        cr = u[0] * w[1] - u[1] * w[0]
        if cr > 0 or (cr == 0 and u[0] * w[0] + u[1] * w[1] > 0):
            return 0
        return 1

    def _angle_le(self, a: Point, b: Point) -> bool:
        """True if the angle of a around c is at most the angle of b, both measured from u."""
        wa, wb = self._vec(a), self._vec(b)
        ha, hb = self._half(wa), self._half(wb)
        if ha != hb:
            return ha < hb
        return wa[0] * wb[1] - wa[1] * wb[0] >= 0

    def locate(self, q: Point):
        v, n = self.v, self.n
        if 3 * q[0] == self.s[0] and 3 * q[1] == self.s[1]:  # @line L1
            return ("inside", 0)
        lo, hi = 0, n  # @line L2
        while hi - lo > 1:  # @line L3
            mid = (lo + hi) // 2  # @line L4
            self.tests += 1
            if self._angle_le(v[mid], q):  # @line L5
                lo = mid
            else:
                hi = mid
        i = lo
        j = (i + 1) % n
        o = orient(v[i], v[j], q)  # @line L6
        if o > 0:
            return ("inside", i)  # @line L7
        if o < 0:
            return ("outside", i)  # @line L8
        return ("vertex", i) if q == v[i] else ("edge", i)  # @line L9


def reference(vertices: list[Point], q: Point):
    """Linear-scan classification with the same wedge convention, for testing."""
    loc = ConvexPolygonLocator(vertices)
    n = len(vertices)
    for i, p in enumerate(vertices):
        if q == p:
            return ("vertex", i)
    for i in range(n):
        a, b = vertices[i], vertices[(i + 1) % n]
        if orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return ("edge", i)
    inside = all(orient(vertices[i], vertices[(i + 1) % n], q) > 0 for i in range(n))
    tag = "inside" if inside else "outside"
    w = loc._vec(q)
    if w == (0, 0):
        return (tag, 0)
    for i in range(n):
        a, b = loc._vec(vertices[i]), loc._vec(vertices[(i + 1) % n])
        # each wedge is narrower than pi, so it is the set where q is left of ray a (or on it, same way) and right of ray b
        on_a = a[0] * w[1] - a[1] * w[0]
        on_b = b[0] * w[1] - b[1] * w[0]
        if on_b < 0 and (on_a > 0 or (on_a == 0 and a[0] * w[0] + a[1] * w[1] > 0)):
            return (tag, i)
    raise AssertionError("no wedge found")
