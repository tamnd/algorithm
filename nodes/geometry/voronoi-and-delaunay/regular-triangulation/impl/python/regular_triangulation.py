# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regular-triangulation/. The authors are listed in prov/BBD60J.jsonl.

Point = tuple[int, int]
GHOST = -1


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def power_test(a: Point, wa: int, b: Point, wb: int, c: Point, wc: int, d: Point, wd: int) -> int:
    """For a, b, c counterclockwise: 1 if the lifted point (d, |d|^2 - wd) is strictly below the plane through
    the lifted a, b, c, 0 on it, -1 above. With all weights zero this is the incircle test."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    az = adx * adx + ady * ady - wa + wd
    bz = bdx * bdx + bdy * bdy - wb + wd
    cz = cdx * cdx + cdy * cdy - wc + wd
    det = az * (bdx * cdy - cdx * bdy) + bz * (cdx * ady - adx * cdy) + cz * (adx * bdy - bdx * ady)
    return (det > 0) - (det < 0)


class RegularTriangulation:
    """The regular (weighted Delaunay) triangulation of integer sites with integer weights.

    It is the projection of the lower convex hull of the lifted points (x, y, x^2 + y^2 - w). A site whose
    lifted point is strictly above that hull is redundant and is not a vertex. Built online by the
    weighted Bowyer-Watson method with ghost triangles: the triangles whose plane passes strictly above the
    new lifted point are removed and the hole is filled from the new site. Sites whose lifted point lies
    exactly on the hull may or may not be vertices (the triangulation is then not unique).
    Cost: insert O(n) in this form (a linear scan finds the first conflict), so O(n^2) for n sites;
    with a history DAG and random order the expected total is O(n log n). Space O(n).
    """

    def __init__(self, sites: list[tuple[Point, int]] = ()) -> None:
        self.pts: list[Point] = []
        self.w: list[int] = []
        self.index: dict[Point, int] = {}
        self.tri: dict[int, tuple[int, int, int]] = {}
        self.edge: dict[tuple[int, int], int] = {}
        self.count = 0
        self.started = False
        for p, w in sites:
            self.insert(p, w)

    def _add(self, t: tuple[int, int, int]) -> None:
        u, v, x = t
        if u == GHOST:
            u, v, x = v, x, u
        elif v == GHOST:
            u, v, x = x, u, v
        self.tri[self.count] = (u, v, x)
        self.edge[(u, v)] = self.edge[(v, x)] = self.edge[(x, u)] = self.count
        self.count += 1

    def _height(self, k: int) -> int:
        p = self.pts[k]
        return p[0] * p[0] + p[1] * p[1] - self.w[k]

    def _conflict(self, t: tuple[int, int, int], i: int) -> bool:
        u, v, x = t
        P, p = self.pts, self.pts[i]
        if x != GHOST:
            return power_test(P[u], self.w[u], P[v], self.w[v], P[x], self.w[x], p, self.w[i]) > 0
        o = orient(P[u], P[v], p)
        if o != 0:
            return o > 0
        # p is on the line of the hull edge: conflict iff its lifted point is below the lifted line
        dot = (p[0] - P[u][0]) * (P[v][0] - P[u][0]) + (p[1] - P[u][1]) * (P[v][1] - P[u][1])
        ln = (P[v][0] - P[u][0]) ** 2 + (P[v][1] - P[u][1]) ** 2
        return self._height(i) * ln < (ln - dot) * self._height(u) + dot * self._height(v)

    def _start(self) -> None:
        P = self.pts
        n = len(P)
        third = next((k for k in range(2, n) if orient(P[0], P[1], P[k]) != 0), None)
        if third is None:
            return
        a, b, c = (0, 1, third) if orient(P[0], P[1], P[third]) > 0 else (0, third, 1)
        for t in ((a, b, c), (b, a, GHOST), (c, b, GHOST), (a, c, GHOST)):
            self._add(t)
        self.started = True
        for i in range(n):
            if i not in (a, b, c):
                self._insert_index(i)

    def insert(self, p: Point, w: int) -> bool:
        """Add the site p with weight w; return False if p is already a site."""
        if p in self.index:  # @line L1
            return False
        self.index[p] = len(self.pts)
        self.pts.append(p)
        self.w.append(w)
        if not self.started:
            self._start()  # @line L2
        else:
            self._insert_index(len(self.pts) - 1)
        return True

    def _insert_index(self, i: int) -> None:
        start = next((tid for tid, t in self.tri.items() if self._conflict(t, i)), None)  # @line L3
        if start is None:
            return  # @line L4
        cavity, stack = {start}, [start]
        while stack:  # @line L5
            u, v, x = self.tri[stack.pop()]
            for a, b in ((u, v), (v, x), (x, u)):
                nb = self.edge[(b, a)]
                if nb not in cavity and self._conflict(self.tri[nb], i):
                    cavity.add(nb)
                    stack.append(nb)
        bound = [(a, b) for tid in cavity for a, b in zip(self.tri[tid], self.tri[tid][1:] + self.tri[tid][:1])
                 if self.edge[(b, a)] not in cavity]  # @line L6
        for tid in cavity:  # @line L7
            u, v, x = self.tri.pop(tid)
            del self.edge[(u, v)], self.edge[(v, x)], self.edge[(x, u)]
        for a, b in bound:  # @line L8
            self._add((a, b, i))

    def triangles(self) -> list[tuple[Point, Point, Point]]:
        """The triangles as counterclockwise triples of sites, sorted; [] while the sites are collinear."""
        P = self.pts
        return sorted((P[u], P[v], P[x]) for u, v, x in self.tri.values() if x != GHOST)

    def vertices(self) -> list[Point]:
        """The sites that are vertices of the triangulation, sorted."""
        return sorted({self.pts[k] for t in self.tri.values() for k in t if k != GHOST})

    def check_invariant(self) -> None:
        """Every edge is locally regular, and the ghost triangles close the border into a sphere."""
        P = self.pts
        for (a, b), tid in self.edge.items():
            assert self.edge[(b, a)] != tid
            t1, t2 = self.tri[tid], self.tri[self.edge[(b, a)]]
            if GHOST in (a, b) or GHOST in t1 or GHOST in t2:
                continue
            d = next(k for k in t2 if k not in (a, b))
            assert not self._conflict(t1, d), "edge not locally regular"
        for u, v, x in self.tri.values():
            if x != GHOST:
                assert orient(P[u], P[v], P[x]) > 0
