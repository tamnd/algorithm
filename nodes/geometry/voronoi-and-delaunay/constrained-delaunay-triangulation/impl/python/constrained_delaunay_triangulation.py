# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constrained-delaunay-triangulation/. The authors are listed in prov/MHT5ZY.jsonl.

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


def crosses(a: Point, b: Point, c: Point, d: Point) -> bool:
    """True if the open segments ab and cd cross at one point inside both."""
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def inside_closed(a: Point, b: Point, c: Point, p: Point) -> bool:
    """True if p lies in the closed counterclockwise triangle abc."""
    return orient(a, b, p) >= 0 and orient(b, c, p) >= 0 and orient(c, a, p) >= 0


def between(p: Point, a: Point, b: Point) -> bool:
    """True if p lies strictly inside the segment ab."""
    return orient(a, b, p) == 0 and (p[0] - a[0]) * (p[0] - b[0]) + (p[1] - a[1]) * (p[1] - b[1]) < 0


class ConstrainedDelaunayTriangulation:
    """Constrained Delaunay triangulation of integer points and non-crossing segments between them.

    Every segment is an edge (split at the points that lie on it), and every other edge is locally
    Delaunay: the vertex opposite to it is not strictly inside the circumcircle of the triangle on its other
    side. The build first makes a maximal set of non-crossing edges that starts with the segment pieces (so
    a triangulation that holds them), then runs Lawson flips on the edges that are not segments.
    insert_point and insert_segment mark the structure as stale; the next query rebuilds it.
    Cost: O(n^3) for the maximal edge set (O(n^2) candidate edges, each tested against O(n) points and edges)
    and O(n^2) flips, so O(n^3) worst case for n points; Chew's algorithm takes O(n log n). Space O(n^2) for
    the candidate list.
    """

    def __init__(self, points: list[Point] = (), segments: list[tuple[Point, Point]] = ()) -> None:
        self.points: list[Point] = []
        self.segments: list[tuple[Point, Point]] = []
        self.stale = True
        for p in points:
            self.insert_point(p)
        for p, q in segments:
            self.insert_segment(p, q)

    def insert_point(self, p: Point) -> bool:
        """Add the point p; return False if it is already present."""
        if p in self.points:
            return False
        self.points.append(p)
        self.stale = True
        return True

    def _pieces(self, segments) -> set[tuple[Point, Point]]:
        """The segments split at the points inside them, as sorted point pairs."""
        out = set()
        for p, q in segments:
            inner = sorted([r for r in self.points if between(r, p, q)] + [p, q])
            out.update(zip(inner, inner[1:]))
        return out

    def insert_segment(self, p: Point, q: Point) -> bool:
        """Add the segment pq between two present points; return False if it is not new, is a single point,
        or crosses a segment that is already present."""
        if p == q or p not in self.points or q not in self.points:
            return False
        old = self._pieces(self.segments)
        new = self._pieces([(p, q)])
        if new <= old:
            return False
        if any(crosses(a, b, c, d) for a, b in new for c, d in old):
            return False
        self.segments.append((p, q))
        self.stale = True
        return True

    def _build(self) -> None:
        P = self.points
        n = len(P)
        index = {p: i for i, p in enumerate(P)}
        fixed = {frozenset((index[a], index[b])) for a, b in self._pieces(self.segments)}  # @line L1
        candidates = [tuple(sorted(s)) for s in fixed]
        candidates += [tuple(sorted(t[k:] + t[:k])[:2]) for t in delaunay_indices(P) for k in range(3)]
        candidates += [(i, j) for i in range(n) for j in range(i + 1, n)]
        chosen: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()
        for a, b in candidates:  # @line L2
            if (a, b) in seen:
                continue
            seen.add((a, b))
            if any(between(r, P[a], P[b]) for r in P):  # @line L3
                continue
            if any(crosses(P[a], P[b], P[c], P[d]) for c, d in chosen):
                continue
            chosen.append((a, b))  # @line L4
        nbr: dict[int, list[int]] = {i: [] for i in range(n)}
        for a, b in chosen:
            nbr[a].append(b)
            nbr[b].append(a)
        edge: dict[tuple[int, int], tuple[int, int, int]] = {}
        for a, b in chosen:  # @line L5
            for u, v in ((a, b), (b, a)):
                for w in nbr[u]:
                    if w in nbr[v] and orient(P[u], P[v], P[w]) > 0 and not any(
                            r not in (P[u], P[v], P[w]) and inside_closed(P[u], P[v], P[w], r) for r in P):
                        edge[(u, v)] = edge[(v, w)] = edge[(w, u)] = (u, v, w)

        def add(t: tuple[int, int, int]) -> None:
            u, v, w = t
            edge[(u, v)] = edge[(v, w)] = edge[(w, u)] = t

        def remove(t: tuple[int, int, int]) -> None:
            u, v, w = t
            del edge[(u, v)], edge[(v, w)], edge[(w, u)]

        def apex(a: int, b: int) -> int:
            return next(v for v in edge[(a, b)] if v not in (a, b))

        stack = [e for e in edge if frozenset(e) not in fixed]  # @line L6
        while stack:  # @line L7
            a, b = stack.pop()
            if (a, b) not in edge or (b, a) not in edge or frozenset((a, b)) in fixed:
                continue
            c, d = apex(a, b), apex(b, a)
            if incircle(P[a], P[b], P[c], P[d]) > 0:  # @line L8
                remove(edge[(a, b)])
                remove(edge[(b, a)])
                add((a, d, c))
                add((d, b, c))
                stack += [(a, d), (d, b), (b, c), (c, a)]  # @line L9
        self._tris = sorted({min((P[t[k]], P[t[k - 2]], P[t[k - 1]]) for k in range(3)) for t in edge.values()})  # @line L10
        self._edge, self._fixed = edge, fixed
        self.stale = False

    def triangles(self) -> list[tuple[Point, Point, Point]]:
        """The triangles as counterclockwise point triples, sorted."""
        if self.stale:
            self._build()
        return list(self._tris)

    def constraint_edges(self) -> list[tuple[Point, Point]]:
        """The pieces of the segments, which are all edges of the triangulation, sorted."""
        return sorted(self._pieces(self.segments))

    def check_invariant(self) -> None:
        """Segment pieces are edges; every other interior edge is locally Delaunay."""
        if self.stale:
            self._build()
        P, edge = self.points, self._edge
        if not edge:
            return
        for s in self._fixed:
            u, v = tuple(s)
            assert (u, v) in edge or (v, u) in edge, "a segment is missing"
        for (a, b), t in edge.items():
            if (b, a) in edge and frozenset((a, b)) not in self._fixed:
                c = next(v for v in t if v not in (a, b))
                d = next(v for v in edge[(b, a)] if v not in (a, b))
                assert incircle(P[a], P[b], P[c], P[d]) <= 0, "edge not locally Delaunay"
