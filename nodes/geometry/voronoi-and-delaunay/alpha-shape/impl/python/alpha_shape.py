# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-shape/. The authors are listed in prov/NVRCS8.jsonl.

from fractions import Fraction

Point = tuple[int, int]
GHOST = -1


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def incircle(a: Point, b: Point, c: Point, d: Point) -> int:
    """For a, b, c counterclockwise: 1 if d is strictly inside their circumcircle, 0 on it, -1 outside."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    det = ((adx * adx + ady * ady) * (bdx * cdy - cdx * bdy)
           + (bdx * bdx + bdy * bdy) * (cdx * ady - adx * cdy)
           + (cdx * cdx + cdy * cdy) * (adx * bdy - bdx * ady))
    return (det > 0) - (det < 0)


def delaunay_indices(pts: list[Point]) -> list[tuple[int, int, int]]:
    """A Delaunay triangulation of distinct points (Bowyer-Watson with ghost triangles), as counterclockwise
    index triples; [] if the points are collinear. O(n^2) worst case."""
    n = len(pts)
    third = next((k for k in range(2, n) if orient(pts[0], pts[1], pts[k]) != 0), None)
    if third is None:
        return []
    a, b, c = (0, 1, third) if orient(pts[0], pts[1], pts[third]) > 0 else (0, third, 1)
    tri: dict[int, tuple[int, int, int]] = {}
    edge: dict[tuple[int, int], int] = {}
    counter = [0]

    def add(t: tuple[int, int, int]) -> None:
        u, v, w = t
        if u == GHOST:
            u, v, w = v, w, u
        elif v == GHOST:
            u, v, w = w, u, v
        tri[counter[0]] = (u, v, w)
        edge[(u, v)] = edge[(v, w)] = edge[(w, u)] = counter[0]
        counter[0] += 1

    def conflict(t: tuple[int, int, int], p: Point) -> bool:
        u, v, w = t
        if w != GHOST:
            return incircle(pts[u], pts[v], pts[w], p) > 0
        o = orient(pts[u], pts[v], p)
        if o != 0:
            return o > 0
        return (p[0] - pts[u][0]) * (p[0] - pts[v][0]) + (p[1] - pts[u][1]) * (p[1] - pts[v][1]) < 0

    for t in ((a, b, c), (b, a, GHOST), (c, b, GHOST), (a, c, GHOST)):
        add(t)
    for i in range(n):
        if i in (a, b, c):
            continue
        p = pts[i]
        start = next(tid for tid, t in tri.items() if conflict(t, p))
        cavity, stack = {start}, [start]
        while stack:
            u, v, w = tri[stack.pop()]
            for x, y in ((u, v), (v, w), (w, u)):
                nb = edge[(y, x)]
                if nb not in cavity and conflict(tri[nb], p):
                    cavity.add(nb)
                    stack.append(nb)
        bound = [(x, y) for tid in cavity for x, y in zip(tri[tid], tri[tid][1:] + tri[tid][:1])
                 if edge[(y, x)] not in cavity]
        for tid in cavity:
            u, v, w = tri.pop(tid)
            del edge[(u, v)], edge[(v, w)], edge[(w, u)]
        for x, y in bound:
            add((x, y, i))
    return [t for t in tri.values() if t[2] != GHOST]


def circumcenter(a: Point, b: Point, c: Point) -> tuple[Fraction, Fraction]:
    """Exact circumcenter of three points that are not collinear."""
    bx, by = b[0] - a[0], b[1] - a[1]
    cx, cy = c[0] - a[0], c[1] - a[1]
    d = 2 * (bx * cy - by * cx)
    return (a[0] + Fraction(cy * (bx * bx + by * by) - by * (cx * cx + cy * cy), d),
            a[1] + Fraction(bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by), d))


def dist2(p: tuple, q: tuple):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


class AlphaShape:
    """The alpha complex of a set of integer points, as a filtration of its Delaunay triangulation.

    Here alpha is a squared radius. Each Delaunay simplex gets the smallest alpha at which it enters the
    complex: 0 for a vertex, the squared circumradius for a triangle, and for an edge pq either |pq|^2 / 4
    (when no point lies strictly inside the circle with diameter pq; the two opposite vertices decide this)
    or the smallest value of its triangles. complex(alpha) is the set of simplices with value <= alpha.
    insert marks the structure as stale; the next query rebuilds it.
    Cost: build O(n^2) worst case with this Delaunay code (O(n log n) with an optimal one) plus O(n) for
    the values; complex(alpha) O(n) and O(log n + k) with the sorted filtration; space O(n).
    """

    def __init__(self, points: list[Point] = ()) -> None:
        self.points: list[Point] = []
        self.stale = True
        for p in points:
            self.insert(p)

    def insert(self, p: Point) -> bool:
        """Add the point p; return False if it is already present."""
        if p in self.points:
            return False
        self.points.append(p)
        self.stale = True
        return True

    def _build(self) -> None:
        P = self.points
        tris = delaunay_indices(P)  # @line L1
        value: dict[frozenset, Fraction] = {frozenset([i]): Fraction(0) for i in range(len(P))}  # @line L2
        opposite: dict[frozenset, list[int]] = {}
        for a, b, c in tris:
            o = circumcenter(P[a], P[b], P[c])
            value[frozenset((a, b, c))] = dist2(o, P[a])  # @line L3
            for u, v, w in ((a, b, c), (b, c, a), (c, a, b)):
                opposite.setdefault(frozenset((u, v)), []).append(w)
        if not tris:  # collinear points: the Delaunay triangulation is the path in sorted order
            order = sorted(range(len(P)), key=lambda i: P[i])
            for u, v in zip(order, order[1:]):
                opposite[frozenset((u, v))] = []
        for e, opp in opposite.items():  # @line L4
            u, v = tuple(e)
            mid2 = (P[u][0] + P[v][0], P[u][1] + P[v][1])  # twice the midpoint
            r2 = dist2(P[u], P[v])  # four times the squared radius of the diametral circle
            gabriel = all(dist2((2 * P[w][0], 2 * P[w][1]), mid2) >= r2 for w in opp)  # @line L5
            if gabriel:
                value[e] = Fraction(r2, 4)  # @line L6
            else:
                value[e] = min(value[frozenset((u, v, w))] for w in opp)  # @line L7
        self._filtration = sorted((val, tuple(sorted(P[i] for i in s))) for s, val in value.items())  # @line L8
        self.stale = False

    def filtration(self) -> list[tuple[Fraction, tuple]]:
        """All Delaunay simplices (sorted tuples of points) with their alpha values, sorted by value."""
        if self.stale:
            self._build()
        return list(self._filtration)

    def complex(self, alpha) -> set[tuple]:
        """The simplices of the alpha complex for the squared radius alpha."""
        return {s for v, s in self.filtration() if v <= alpha}

    def boundary(self, alpha) -> set[tuple]:
        """The edges of the alpha complex with at most one triangle of the complex on them."""
        cx = self.complex(alpha)
        count = {s: 0 for s in cx if len(s) == 2}
        for s in cx:
            if len(s) == 3:
                for e in ((s[0], s[1]), (s[0], s[2]), (s[1], s[2])):
                    count[e] += 1
        return {e for e, k in count.items() if k <= 1}

    def check_invariant(self) -> None:
        """Every face of a simplex enters no later than the simplex."""
        val = {s: v for v, s in self.filtration()}
        for s, v in val.items():
            for k in range(len(s)):
                if len(s) > 1:
                    assert val[s[:k] + s[k + 1:]] <= v
