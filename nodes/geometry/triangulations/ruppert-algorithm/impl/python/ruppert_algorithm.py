# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ruppert-algorithm/. The authors are listed in prov/A2ZJPV.jsonl.
"""Ruppert's Delaunay refinement with exact rational arithmetic.

The domain is a convex polygon whose angles are all at least 90 degrees,
with optional interior segments and points that touch neither the boundary
nor each other. These are the hypotheses under which Ruppert's algorithm with
the bound B = sqrt(2) on circumradius over shortest edge is proved to stop.
Every triangle of the output then has all angles at least
arcsin(1 / (2 sqrt 2)), about 20.7 degrees.

The triangulation is an ordinary Delaunay triangulation, maintained by
Bowyer-Watson insertion. A subsegment is encroached when a vertex other than
its end points lies inside or on its diametral circle; once no subsegment is
encroached, every subsegment is an edge of the Delaunay triangulation.
"""
from collections import deque
from fractions import Fraction


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def incircle(a, b, c, d):
    """Positive when d is strictly inside the circle through the CCW triangle abc."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    return ((adx * adx + ady * ady) * (bdx * cdy - cdx * bdy)
            - (bdx * bdx + bdy * bdy) * (adx * cdy - cdx * ady)
            + (cdx * cdx + cdy * cdy) * (adx * bdy - bdx * ady))


def circumcenter(a, b, c):
    bx, by = b[0] - a[0], b[1] - a[1]
    cx, cy = c[0] - a[0], c[1] - a[1]
    d = 2 * (bx * cy - by * cx)
    b2, c2 = bx * bx + by * by, cx * cx + cy * cy
    return (a[0] + Fraction(cy * b2 - by * c2) / d, a[1] + Fraction(bx * c2 - cx * b2) / d)


def dist2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def encroaches(p, a, b):
    """Is p inside or on the circle with diameter ab?"""
    return (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0


def ratio2_exceeds(a, b, c, B2):
    """Is (circumradius / shortest edge)^2 greater than B2?"""
    r2 = dist2(circumcenter(a, b, c), a)
    l2 = min(dist2(a, b), dist2(b, c), dist2(c, a))
    return r2 > B2 * l2


def _canon(t):
    k = t.index(min(t))
    return t[k:] + t[:k]


class Mesh:
    """A triangulation stored as a map from each directed edge (u, v) to the apex w of triangle (u, v, w)."""

    def __init__(self):
        self.p = []
        self.opp = {}
        self.last = None

    def add(self, a, b, c):
        self.opp[(a, b)], self.opp[(b, c)], self.opp[(c, a)] = c, a, b
        self.last = (a, b, c)

    def remove(self, a, b, c):
        del self.opp[(a, b)], self.opp[(b, c)], self.opp[(c, a)]

    def has(self, t):
        a, b, c = t
        return self.opp.get((a, b)) == c

    def triangles(self):
        return sorted({_canon((u, v, w)) for (u, v), w in self.opp.items()})

    def locate(self, q):
        t = self.last if self.last is not None and self.has(self.last) else next(
            (u, v, w) for (u, v), w in self.opp.items())
        while True:
            for k in range(3):
                u, v = t[k], t[(k + 1) % 3]
                if orient(self.p[u], self.p[v], q) < 0:
                    w = self.opp.get((v, u))
                    if w is None:
                        raise ValueError("point outside the domain")
                    t = (v, u, w)
                    break
            else:
                return t

    def legalize_all(self):
        stack = list(self.opp)
        while stack:
            u, v = stack.pop()
            w, x = self.opp.get((u, v)), self.opp.get((v, u))
            if w is None or x is None:
                continue
            P = self.p
            if incircle(P[u], P[v], P[w], P[x]) > 0:
                self.remove(u, v, w)
                self.remove(v, u, x)
                self.add(u, x, w)
                self.add(x, v, w)
                stack.extend([(u, x), (x, v), (v, w), (w, u)])

    def insert(self, q):
        """Bowyer-Watson insertion; returns the new vertex and the new triangles."""
        P = self.p
        t0 = self.locate(q)  # @line L11
        bad, seen, todo, rim = [], {_canon(t0)}, [t0], []
        while todo:  # @line L12
            t = todo.pop()
            bad.append(t)
            for k in range(3):
                u, v = t[k], t[(k + 1) % 3]
                w = self.opp.get((v, u))
                if w is not None:
                    key = _canon((v, u, w))
                    if key in seen:
                        continue
                    if incircle(P[v], P[u], P[w], q) > 0:
                        seen.add(key)
                        todo.append((v, u, w))
                        continue
                rim.append((u, v))
        for t in bad:
            self.remove(*t)
        i = len(P)
        P.append(q)
        new = []
        for u, v in rim:
            o = orient(P[u], P[v], q)
            if o > 0:
                self.add(u, v, i)  # @line L13
                new.append((u, v, i))
            elif o < 0 or (u, v) in self.opp or (v, u) in self.opp:
                raise ValueError("cavity is not star-shaped")
        return i, new


def _check_input(boundary, segments, points):
    n = len(boundary)
    if n < 3:
        raise ValueError("the boundary needs at least 3 vertices")
    for i in range(n):
        u, v, w = boundary[i - 1], boundary[i], boundary[(i + 1) % n]
        if orient(u, v, w) <= 0:
            raise ValueError("the boundary must be strictly convex and counterclockwise")
        if (u[0] - v[0]) * (w[0] - v[0]) + (u[1] - v[1]) * (w[1] - v[1]) > 0:
            raise ValueError("every boundary angle must be at least 90 degrees")

    def strictly_inside(q):
        return all(orient(boundary[i], boundary[(i + 1) % n], q) > 0 for i in range(n))

    def touch(a, b, c, d):
        o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
        if o1 * o2 < 0 and o3 * o4 < 0:
            return True

        def on(p, q, r):
            return orient(p, q, r) == 0 and min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) \
                and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
        return on(a, b, c) or on(a, b, d) or on(c, d, a) or on(c, d, b)

    for a, b in segments:
        if a == b or not strictly_inside(a) or not strictly_inside(b):
            raise ValueError("segments must be proper and strictly inside")
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            if touch(*segments[i], *segments[j]):
                raise ValueError("segments must be pairwise disjoint")
    for q in points:
        if not strictly_inside(q):
            raise ValueError("points must be strictly inside")
        for a, b in segments:
            if touch(a, b, q, q):
                raise ValueError("points must not lie on segments")
    allpts = list(boundary) + [p for s in segments for p in s] + list(points)
    if len(set(allpts)) != len(allpts):
        raise ValueError("repeated input points")


def ruppert(boundary, segments=(), points=(), B2=2, max_vertices=5000, trace=None):
    """Refine the domain; returns (points, triangles, subsegments) with exact coordinates.

    B2 is the square of the bound B on circumradius over shortest edge. If trace is
    a list, the steps are appended to it.
    """
    boundary = [(Fraction(x), Fraction(y)) for x, y in boundary]
    segments = [((Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))) for a, b in segments]
    points = [(Fraction(x), Fraction(y)) for x, y in points]
    _check_input(boundary, segments, points)
    if B2 < 2:
        raise ValueError("termination is only guaranteed for B >= sqrt(2)")
    M = Mesh()
    M.p.extend(boundary)
    n = len(boundary)
    for i in range(1, n - 1):
        M.add(0, i, i + 1)
    M.legalize_all()  # @line L1
    sub = set((i, (i + 1) % n) for i in range(n))
    for a, b in segments:
        ia, _ = M.insert(a)
        ib, _ = M.insert(b)
        sub.add((ia, ib))
    for q in points:
        M.insert(q)
    M.legalize_all()

    enc, skinny = deque(), deque(M.triangles())

    def check_sub(s):
        a, b = s
        if any(k != a and k != b and encroaches(M.p[k], M.p[a], M.p[b]) for k in range(len(M.p))):
            enc.append(s)

    def after_insert(i, new):
        skinny.extend(new)
        q = M.p[i]
        for s in sub:
            if i not in s and encroaches(q, M.p[s[0]], M.p[s[1]]):
                enc.append(s)

    def split(s):
        a, b = s
        m = ((M.p[a][0] + M.p[b][0]) / 2, (M.p[a][1] + M.p[b][1]) / 2)
        i, new = M.insert(m)
        if trace is not None:
            trace.append(("split", s, m))
        sub.discard(s)
        sub.add((a, i))
        sub.add((i, b))
        after_insert(i, new)
        check_sub((a, i))
        check_sub((i, b))

    for s in sorted(sub):
        check_sub(s)
    while True:  # @line L2
        if len(M.p) > max_vertices:
            raise RuntimeError("too many vertices")
        if enc:
            s = enc.popleft()
            if s in sub:  # @line L3
                split(s)  # @line L4
            continue
        if not skinny:
            break
        t = skinny.popleft()
        if not M.has(t):
            continue
        a, b, c = (M.p[k] for k in t)
        if not ratio2_exceeds(a, b, c, B2):  # @line L5
            continue
        cc = circumcenter(a, b, c)  # @line L6
        hit = sorted(s for s in sub if encroaches(cc, M.p[s[0]], M.p[s[1]]))
        if hit:  # @line L7
            if trace is not None:
                trace.append(("reject", t, cc, hit))
            for s in hit:
                if s in sub:
                    split(s)  # @line L8
            skinny.append(t)
        else:
            i, new = M.insert(cc)  # @line L9
            if trace is not None:
                trace.append(("insert", t, cc))
            after_insert(i, new)
    return M.p, M.triangles(), sorted(sub)  # @line L10
