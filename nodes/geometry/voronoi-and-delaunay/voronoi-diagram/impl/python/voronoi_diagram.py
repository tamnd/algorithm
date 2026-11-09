# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voronoi-diagram/. The authors are listed in prov/6MC1K7.jsonl.

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


class VoronoiDiagram:
    """The Voronoi diagram of a set of integer sites, built as the dual of a Delaunay triangulation.

    Vertices are exact points (pairs of Fractions). A vertex shared by four or more cocircular sites is one
    vertex, and the Delaunay edges inside such a cocircular polygon give no Voronoi edge. Edges are stored as
    {frozenset({p, q}): (end, end)}, ends sorted, None for an end at infinity.
    insert marks the diagram as stale; the next query rebuilds it.
    Cost: build O(n^2) worst case with the Bowyer-Watson core used here (O(n log n) with an optimal
    Delaunay algorithm); cell(p) O(deg p); nearest(q) O(n) worst case by a greedy walk; space O(n).
    """

    def __init__(self, points: list[Point] = ()) -> None:
        self.sites: list[Point] = []
        self.index: dict[Point, int] = {}
        self.stale = True
        for p in points:
            self.insert(p)

    def insert(self, p: Point) -> bool:
        """Add the site p; return False if it is already a site."""
        if p in self.index:
            return False
        self.index[p] = len(self.sites)
        self.sites.append(p)
        self.stale = True
        return True

    def _build(self) -> None:
        pts = self.sites
        tris = delaunay_indices(pts)  # @line L1
        self.fan: dict[int, dict[int, tuple[int, int, int]]] = {i: {} for i in range(len(pts))}
        self.center: dict[tuple[int, int, int], tuple[Fraction, Fraction]] = {}
        opposite: dict[tuple[int, int], tuple[int, int, int]] = {}
        for t in tris:
            self.center[t] = circumcenter(*(pts[i] for i in t))  # @line L2
            a, b, c = t
            for u, v in ((a, b), (b, c), (c, a)):
                opposite[(u, v)] = t
            self.fan[a][b], self.fan[b][c], self.fan[c][a] = t, t, t
        self._vertices = sorted(set(self.center.values()))  # @line L3
        self._edges: dict[frozenset, tuple] = {}
        self.adj: dict[int, set[int]] = {i: set() for i in range(len(pts))}
        for (u, v), t in opposite.items():  # @line L4
            self.adj[u].add(v)
            self.adj[v].add(u)
            t2 = opposite.get((v, u))
            if t2 is None:  # a hull edge: a ray from the center of t, away from the hull
                ends = (self.center[t], None)  # @line L5
            elif u < v:
                c1, c2 = self.center[t], self.center[t2]
                if c1 == c2:  # @line L6
                    continue
                ends = tuple(sorted((c1, c2)))
            else:
                continue
            self._edges[frozenset((pts[u], pts[v]))] = ends  # @line L7
        if not tris and len(pts) >= 2:  # collinear sites: parallel lines between neighbors on the line
            order = sorted(range(len(pts)), key=lambda i: pts[i])
            for u, v in zip(order, order[1:]):
                self._edges[frozenset((pts[u], pts[v]))] = (None, None)
                self.adj[u].add(v)
                self.adj[v].add(u)
        self.stale = False

    def _fresh(self) -> None:
        if self.stale:
            self._build()

    def vertices(self) -> list[tuple[Fraction, Fraction]]:
        """The Voronoi vertices, sorted."""
        self._fresh()
        return list(self._vertices)

    def edges(self) -> dict[frozenset, tuple]:
        """The Voronoi edges of positive length, keyed by the pair of sites."""
        self._fresh()
        return dict(self._edges)

    def cell(self, p: Point) -> tuple[list[tuple[Fraction, Fraction]], bool]:
        """The vertices of the cell of site p in counterclockwise order, and whether the cell is bounded."""
        self._fresh()
        i = self.index[p]
        succ = {a: t for a, t in self.fan[i].items()}
        nxt = {}
        for a, t in succ.items():
            b = t[(t.index(i) + 2) % 3]
            nxt[a] = b
        starts = [a for a in nxt if a not in set(nxt.values())]
        bounded = not starts and bool(nxt)
        out: list[tuple[Fraction, Fraction]] = []
        if nxt:
            a = starts[0] if starts else next(iter(nxt))
            for _ in range(len(nxt)):
                c = self.center[succ[a]]
                if not out or out[-1] != c:
                    out.append(c)
                a = nxt[a]
                if a not in nxt:
                    break
            if bounded and len(out) > 1 and out[0] == out[-1]:
                out.pop()
        return out, bounded

    def neighbors(self, p: Point) -> list[Point]:
        """The sites whose cells share an edge of positive length with the cell of p."""
        self._fresh()
        return sorted(q for key in self._edges if p in key for q in key if q != p)

    def nearest(self, q: tuple) -> Point:
        """A site nearest to q (exact), by a greedy walk on the Delaunay graph."""
        self._fresh()
        pts = self.sites
        d = lambda i: (pts[i][0] - q[0]) ** 2 + (pts[i][1] - q[1]) ** 2
        cur = 0
        while True:
            better = min(self.adj[cur], key=d, default=cur)
            if d(better) >= d(cur):
                return pts[cur]
            cur = better
