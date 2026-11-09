# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chew-second-algorithm/. The authors are listed in prov/R64BJ4.jsonl.
"""Chew's second Delaunay refinement algorithm with exact rational arithmetic.

The domain is a strictly convex polygon whose angles are all at least 60
degrees, with optional interior segments and points that touch neither the
boundary nor each other. The mesh is a constrained Delaunay triangulation in
which every segment is a chain of edges. A skinny triangle gets a vertex at its
circumcenter, unless a subsegment lies between the triangle and the
circumcenter. Then that subsegment is split at its midpoint, after the free
vertices inside its diametral circle that can see the midpoint are deleted.

With B^2 >= 5/4 the algorithm is proved to stop, and every triangle has
circumradius at most B times its shortest edge, so every angle is at least
arcsin(1 / (2B)), about 26.57 degrees for B^2 = 5/4.
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


def ratio2_exceeds(a, b, c, B2):
    """Is (circumradius / shortest edge)^2 greater than B2?"""
    r2 = dist2(circumcenter(a, b, c), a)
    l2 = min(dist2(a, b), dist2(b, c), dist2(c, a))
    return r2 > B2 * l2


def _cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def first_meet(x, c, p, q):
    """The smallest s in [0, 1] with x + s (c - x) on the closed segment pq, or None."""
    d = (c[0] - x[0], c[1] - x[1])
    e = (q[0] - p[0], q[1] - p[1])
    w = (p[0] - x[0], p[1] - x[1])
    den = _cross(d, e)
    if den != 0:
        s, u = Fraction(_cross(w, e)) / den, Fraction(_cross(w, d)) / den
        return s if 0 <= s <= 1 and 0 <= u <= 1 else None
    if _cross(w, d) != 0:
        return None
    dd = d[0] * d[0] + d[1] * d[1]
    sp = Fraction(w[0] * d[0] + w[1] * d[1]) / dd
    sq = Fraction((q[0] - x[0]) * d[0] + (q[1] - x[1]) * d[1]) / dd
    lo, hi = max(min(sp, sq), 0), min(max(sp, sq), 1)
    return lo if lo <= hi else None


def open_meets(a, b, p, q):
    """Does the open segment ab meet the closed segment pq?"""
    d = (b[0] - a[0], b[1] - a[1])
    e = (q[0] - p[0], q[1] - p[1])
    w = (p[0] - a[0], p[1] - a[1])
    den = _cross(d, e)
    if den != 0:
        s, u = Fraction(_cross(w, e)) / den, Fraction(_cross(w, d)) / den
        return 0 < s < 1 and 0 <= u <= 1
    if _cross(w, d) != 0:
        return False
    dd = d[0] * d[0] + d[1] * d[1]
    sp = Fraction(w[0] * d[0] + w[1] * d[1]) / dd
    sq = Fraction((q[0] - a[0]) * d[0] + (q[1] - a[1]) * d[1]) / dd
    return min(sp, sq) < 1 and max(sp, sq) > 0


def earclip(P, poly):
    """Triangulate the simple CCW polygon poly (a list of indices into P) by ear clipping."""
    poly, tris = list(poly), []
    while len(poly) > 3:
        n = len(poly)
        for k in range(n):
            u, v, w = poly[k - 1], poly[k], poly[(k + 1) % n]
            a, b, c = P[u], P[v], P[w]
            if orient(a, b, c) <= 0:
                continue
            if any(z not in (u, v, w) and orient(a, b, P[z]) >= 0 and orient(b, c, P[z]) >= 0
                   and orient(c, a, P[z]) >= 0 for z in poly):
                continue
            tris.append((u, v, w))
            del poly[k]
            break
        else:
            raise ValueError("no ear found")
    if orient(P[poly[0]], P[poly[1]], P[poly[2]]) <= 0:
        raise ValueError("degenerate polygon")
    tris.append(tuple(poly))
    return tris


def _key(u, v):
    return (u, v) if u < v else (v, u)


class Mesh:
    """A constrained triangulation: a map from each directed edge (u, v) to the apex w of
    triangle (u, v, w), and a set of constrained edges (the subsegments)."""

    def __init__(self):
        self.p, self.alive = [], []
        self.opp, self.cons = {}, set()
        self.dirty, self.created = [], []

    def add(self, a, b, c):
        self.opp[(a, b)], self.opp[(b, c)], self.opp[(c, a)] = c, a, b
        self.dirty.extend(((a, b), (b, c), (c, a)))
        self.created.append((a, b, c))

    def remove(self, a, b, c):
        del self.opp[(a, b)], self.opp[(b, c)], self.opp[(c, a)]

    def has(self, t):
        return self.opp.get((t[0], t[1])) == t[2]

    def triangles(self):
        out = set()
        for (u, v), w in self.opp.items():
            t = (u, v, w)
            k = t.index(min(t))
            out.add(t[k:] + t[:k])
        return sorted(out)

    def new_vertex(self, q):
        self.p.append(q)
        self.alive.append(True)
        return len(self.p) - 1

    def legalize(self):
        P = self.p
        while self.dirty:
            u, v = self.dirty.pop()
            w, x = self.opp.get((u, v)), self.opp.get((v, u))
            if w is None or x is None or _key(u, v) in self.cons:
                continue
            if incircle(P[u], P[v], P[w], P[x]) > 0:  # @line L12
                self.remove(u, v, w)
                self.remove(v, u, x)
                self.add(u, x, w)
                self.add(x, v, w)

    def locate(self, q):
        P = self.p
        for (u, v), w in self.opp.items():
            if orient(P[u], P[v], q) >= 0 and orient(P[v], P[w], q) >= 0 and orient(P[w], P[u], q) >= 0:
                return (u, v, w)
        raise ValueError("point outside the domain")

    def insert(self, q):
        """Insert a point that is not a vertex; returns its index."""
        P = self.p
        t = self.locate(q)  # @line L10
        on = [k for k in range(3) if orient(P[t[k]], P[t[(k + 1) % 3]], q) == 0]
        i = self.new_vertex(q)
        if not on:
            a, b, c = t
            self.remove(a, b, c)
            for u, v in ((a, b), (b, c), (c, a)):
                self.add(u, v, i)  # @line L11
        else:
            k = on[0]
            u, v, w = t[k], t[(k + 1) % 3], t[(k + 2) % 3]
            x = self.opp.get((v, u))
            self.remove(u, v, w)
            self.add(v, w, i)
            self.add(w, u, i)
            if x is not None:
                self.remove(v, u, x)
                self.add(u, x, i)
                self.add(x, v, i)
            if _key(u, v) in self.cons:
                self.cons.discard(_key(u, v))
                self.cons.add(_key(u, i))
                self.cons.add(_key(i, v))
        self.legalize()
        return i

    def delete(self, v):
        """Delete an interior vertex that is on no constrained edge."""
        nxt = {w: z for (u, w), z in self.opp.items() if u == v}
        start = next(iter(nxt))
        poly = [start]
        while nxt[poly[-1]] != start:
            poly.append(nxt[poly[-1]])
        for a in poly:
            self.remove(v, a, nxt[a])
        for t in earclip(self.p, poly):  # @line L13
            self.add(*t)
        self.alive[v] = False
        self.legalize()

    def insert_segment(self, a, b):
        """Make the segment ab, which passes through no other vertex, a constrained edge."""
        P = self.p
        self.cons.add(_key(a, b))
        if (a, b) in self.opp or (b, a) in self.opp:
            return
        t = next((a, v, w) for (u, v), w in self.opp.items()
                 if u == a and orient(P[a], P[v], P[b]) > 0 and orient(P[a], P[w], P[b]) < 0)
        self.remove(*t)
        r, l = t[1], t[2]
        right, left = [r], [l]
        while True:
            z = self.opp[(l, r)]
            self.remove(l, r, z)
            if z == b:
                break
            if orient(P[a], P[b], P[z]) > 0:
                left.append(z)
                l = z
            else:
                right.append(z)
                r = z
        for poly in ([a, b] + left[::-1], [b, a] + right):
            for tri in earclip(P, poly):
                self.add(*tri)
        self.legalize()


def _check_input(boundary, segments, points):
    n = len(boundary)
    if n < 3:
        raise ValueError("the boundary needs at least 3 vertices")
    for i in range(n):
        u, v, w = boundary[i - 1], boundary[i], boundary[(i + 1) % n]
        if orient(u, v, w) <= 0:
            raise ValueError("the boundary must be strictly convex and counterclockwise")
        dot = (u[0] - v[0]) * (w[0] - v[0]) + (u[1] - v[1]) * (w[1] - v[1])
        if dot > 0 and 4 * dot * dot > dist2(u, v) * dist2(w, v):
            raise ValueError("every boundary angle must be at least 60 degrees")

    def strictly_inside(q):
        return all(orient(boundary[i], boundary[(i + 1) % n], q) > 0 for i in range(n))

    for a, b in segments:
        if a == b or not strictly_inside(a) or not strictly_inside(b):
            raise ValueError("segments must be proper and strictly inside")
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            (a, b), (c, d) = segments[i], segments[j]
            if open_meets(a, b, c, d) or open_meets(c, d, a, b) or len({a, b, c, d}) < 4 \
                    or any(open_meets(p, q, r, r) for p, q, r in ((a, b, c), (a, b, d), (c, d, a), (c, d, b))):
                raise ValueError("segments must be pairwise disjoint")
    for q in points:
        if not strictly_inside(q):
            raise ValueError("points must be strictly inside")
        if any(q in (a, b) or open_meets(a, b, q, q) for a, b in segments):
            raise ValueError("points must not lie on segments")
    allpts = list(boundary) + [p for s in segments for p in s] + list(points)
    if len(set(allpts)) != len(allpts):
        raise ValueError("repeated input points")


def chew(boundary, segments=(), points=(), B2=Fraction(5, 4), max_vertices=4000, trace=None):
    """Refine the domain; returns (points, triangles, subsegments) with exact coordinates.

    B2 is the square of the bound B on circumradius over shortest edge. If trace is a
    list, the steps are appended to it.
    """
    boundary = [(Fraction(x), Fraction(y)) for x, y in boundary]
    segments = [((Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))) for a, b in segments]
    points = [(Fraction(x), Fraction(y)) for x, y in points]
    _check_input(boundary, segments, points)
    if B2 < Fraction(5, 4):
        raise ValueError("termination is only guaranteed for B >= sqrt(5) / 2")
    M = Mesh()
    n = len(boundary)
    for q in boundary:
        M.new_vertex(q)
    M.cons = {_key(i, (i + 1) % n) for i in range(n)}
    for i in range(1, n - 1):
        M.add(0, i, i + 1)
    M.legalize()
    fixed = set(range(n))
    ends = [(M.insert(a), M.insert(b)) for a, b in segments]
    fixed.update(v for e in ends for v in e)
    fixed.update(M.insert(q) for q in points)
    for a, b in ends:
        M.insert_segment(a, b)  # @line L1
    queue = deque(M.triangles())
    M.created = []

    def split(s, t):
        a, b = s
        P = M.p
        m = ((P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2)  # @line L6
        h2 = dist2(m, P[a])
        doomed = [v for v in range(len(P)) if M.alive[v] and v not in fixed and dist2(P[v], m) < h2
                  and not any(open_meets(m, P[v], P[x], P[y]) for x, y in M.cons)]
        for v in doomed:
            M.delete(v)  # @line L7
        i = M.insert(m)  # @line L8
        fixed.add(i)
        if trace is not None:
            trace.append(("split", t, s, m, [P[v] for v in doomed]))

    while True:  # @line L2
        if len(M.p) > max_vertices:
            raise RuntimeError("too many vertices")
        queue.extend(M.created)
        M.created = []
        if not queue:
            break
        t = queue.popleft()
        if not M.has(t):
            continue
        a, b, c = (M.p[k] for k in t)
        if not ratio2_exceeds(a, b, c, B2):
            continue
        cc = circumcenter(a, b, c)  # @line L3
        x = ((a[0] + b[0] + c[0]) / 3, (a[1] + b[1] + c[1]) / 3)
        hits = [(s, e) for e in M.cons for s in (first_meet(x, cc, M.p[e[0]], M.p[e[1]]),) if s is not None]
        if not hits:  # @line L4
            M.insert(cc)  # @line L5
            if trace is not None:
                trace.append(("insert", t, cc))
        else:
            split(min(hits)[1], t)
            queue.append(t)
    keep = [v for v in range(len(M.p)) if M.alive[v]]
    new = {v: k for k, v in enumerate(keep)}
    tris = sorted(tuple(new[v] for v in t) for t in M.triangles())
    subs = sorted(_key(new[u], new[v]) for u, v in M.cons)
    return [M.p[v] for v in keep], tris, subs  # @line L9
