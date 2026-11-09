# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-walk-point-location/. The authors are listed in prov/47K91B.jsonl.

"""Point location in a triangulation by walking from triangle to triangle.

Input: a list of triangles (each a triple of integer points) that triangulates a convex region
edge to edge. Two walks are implemented.

The straight walk follows the segment from the centroid s of the start triangle to the query
point q and crosses the edges that the segment crosses. A vertex on the line through s and q is
treated as lying to the left of the directed line s q, which is the same as moving the line an
infinitely small distance to the right. So the walk never passes through a vertex.

The visibility walk moves from the current triangle to a neighbor across an edge whose line
strictly separates the triangle from q. The deterministic version tests the edges in their
stored order and can loop in a triangulation that is not Delaunay. The stochastic version starts
the test at a random edge of each triangle and ends with probability 1.

A query returns one of
    ("vertex", p)        q is the vertex p
    ("edge", (a, b))     q is in the relative interior of the edge ab, with a < b in lexicographic order
    ("triangle", i)      q is in the open triangle i
    ("outside",)         q is outside the region
"""

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of p, q, r: positive for a counterclockwise turn."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def in_closed(t, q: Point) -> bool:
    a, b, c = t
    return orient(a, b, q) >= 0 and orient(b, c, q) >= 0 and orient(c, a, q) >= 0


def classify(pts, index, q):
    """The answer for a point q in the closed triangle pts."""
    for p in pts:
        if q == p:
            return ("vertex", p)
    for k in range(3):
        a, b = pts[k], pts[(k + 1) % 3]
        if orient(a, b, q) == 0:
            return ("edge", (a, b) if a < b else (b, a))
    return ("triangle", index)


class WalkLoops(RuntimeError):
    """The deterministic visibility walk came back to a triangle, so it loops forever."""


class Triangulation:
    def __init__(self, triangles) -> None:
        self.tris = []
        for t in triangles:
            a, b, c = t
            o = orient(a, b, c)
            if o == 0:
                raise ValueError("degenerate triangle")
            self.tris.append((a, b, c) if o > 0 else (a, c, b))
        # owner[(u, w)] is the triangle whose counterclockwise boundary has the directed edge u -> w
        self.owner = {}
        for i, t in enumerate(self.tris):
            for k in range(3):
                e = (t[k], t[(k + 1) % 3])
                if e in self.owner:
                    raise ValueError("two triangles have the same directed edge")
                self.owner[e] = i
        self.steps = 0
        self.path: list[int] = []  # the triangles visited by the last walk

    def neighbor(self, u: Point, w: Point):
        """The triangle on the other side of the edge u -> w, or None on the boundary."""
        return self.owner.get((w, u))

    def straight_walk(self, q: Point, start: int = 0):
        self.steps = 0
        t = start
        self.path = [t]
        a, b, c = self.tris[t]
        if in_closed((a, b, c), q):  # @line L1
            return classify((a, b, c), t, q)
        # scaled coordinates: S = 3 s, Q = 3 q, so that the centroid s is an integer point
        S = (a[0] + b[0] + c[0], a[1] + b[1] + c[1])
        Q = (3 * q[0], 3 * q[1])

        def left(p: Point) -> bool:
            """Side of p for the directed line s q, moved to the right by an infinitely small distance."""
            return orient(S, Q, (3 * p[0], 3 * p[1])) >= 0

        pts = self.tris[t]
        u = w = None
        for k in range(3):  # @line L2
            if not left(pts[k]) and left(pts[(k + 1) % 3]):
                u, w = pts[k], pts[(k + 1) % 3]
                break
        while True:  # @line L3
            t = self.neighbor(u, w)  # @line L4
            self.steps += 1
            if t is None:
                return ("outside",)
            self.path.append(t)
            pts = self.tris[t]
            if in_closed(pts, q):  # @line L5
                return classify(pts, t, q)
            i = pts.index(w)
            v = pts[(i + 2) % 3]  # the counterclockwise order of t is w, u, v
            if left(v):  # @line L6
                w = v
            else:
                u = v

    def _visibility(self, q: Point, start: int, first_edge, max_steps):
        self.steps = 0
        t = start
        self.path = [t]
        seen = {t}
        while True:  # @line L7
            pts = self.tris[t]
            k0 = first_edge()
            for j in range(3):  # @line L8
                k = (k0 + j) % 3
                a, b = pts[k], pts[(k + 1) % 3]
                if orient(a, b, q) < 0:
                    break
            else:
                return classify(pts, t, q)
            t = self.neighbor(a, b)  # @line L9
            self.steps += 1
            if t is None:
                return ("outside",)
            self.path.append(t)
            if max_steps is None:
                if t in seen:
                    raise WalkLoops("the visibility walk loops")
                seen.add(t)
            elif self.steps > max_steps:
                raise RuntimeError("the walk took more than max_steps steps")

    def visibility_walk(self, q: Point, start: int = 0):
        """Deterministic: test the edges in their stored order. Raises WalkLoops on a loop."""
        return self._visibility(q, start, lambda: 0, None)

    def stochastic_walk(self, q: Point, rng, start: int = 0, max_steps: int = 10**6):
        """Start the test at a random edge of each triangle."""
        return self._visibility(q, start, lambda: rng.randrange(3), max_steps)


def incircle(a: Point, b: Point, c: Point, d: Point) -> int:
    """Positive if d is strictly inside the circle through the counterclockwise triangle a, b, c."""
    rows = [(p[0] - d[0], p[1] - d[1]) for p in (a, b, c)]
    m = [(x, y, x * x + y * y) for x, y in rows]
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def lawson_delaunay(triangles):
    """Flip edges that are not locally Delaunay until none is left (Lawson's flip algorithm)."""
    tris = [t if orient(*t) > 0 else (t[0], t[2], t[1]) for t in triangles]
    changed = True
    while changed:
        changed = False
        owner = {}
        for i, t in enumerate(tris):
            for k in range(3):
                owner[(t[k], t[(k + 1) % 3])] = i
        for (u, w), i in owner.items():
            j = owner.get((w, u))
            if j is None or j < i:
                continue
            t, s = tris[i], tris[j]
            c = t[(t.index(u) + 2) % 3]  # t is u, w, c
            d = s[(s.index(w) + 2) % 3]  # s is w, u, d
            if incircle(u, w, c, d) > 0:
                tris[i] = (c, u, d)
                tris[j] = (d, w, c)
                changed = True
                break
    return tris
