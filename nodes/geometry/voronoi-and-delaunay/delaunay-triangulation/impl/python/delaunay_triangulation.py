# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delaunay-triangulation/. The authors are listed in prov/SGPK44.jsonl.

import random

Point = tuple[int, int]
Triangle = tuple[int, int, int]
GHOST = -1  # the vertex at infinity


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


class DelaunayTriangulation:
    """A Delaunay triangulation under insertion, with a history DAG for point location.

    Vertices are integer points. Every triangle ever created is a node of the history DAG; a destroyed
    triangle points to the triangles that replaced it. Outside the hull there are ghost triangles (a, b, GHOST),
    one for each hull edge b -> a; the region of a ghost is the part of the wedge from the fixed inner point o
    between the rays to b and to a that lies strictly outside the line ab. While all points are collinear
    they wait in a list and there is no triangle.
    Cost, for points in general position inserted in random order: O(log n) expected time per insertion on
    average and O(n) expected nodes in the DAG, so O(n log n) expected time in total. In the worst case an
    insertion makes O(n) flips and a location visits O(n^2) DAG nodes.
    """

    def __init__(self) -> None:
        self.pts: list[Point] = []
        self.index: dict[Point, int] = {}
        self.pending: list[int] = []
        self.tri: list[Triangle] = []
        self.children: list[list[int]] = []
        self.edge: dict[tuple[int, int], int] = {}
        self.roots: list[int] = []
        self.o3: Point = (0, 0)  # three times the inner point o

    # ----- geometry of the DAG regions -----
    def _orient_o(self, a: int, q: Point) -> int:
        ax, ay = 3 * self.pts[a][0] - self.o3[0], 3 * self.pts[a][1] - self.o3[1]
        qx, qy = 3 * q[0] - self.o3[0], 3 * q[1] - self.o3[1]
        d = ax * qy - ay * qx
        return (d > 0) - (d < 0)

    def _region_contains(self, tid: int, q: Point) -> bool:
        u, v, w = self.tri[tid]
        p = self.pts
        if w != GHOST:
            return orient(p[u], p[v], q) >= 0 and orient(p[v], p[w], q) >= 0 and orient(p[w], p[u], q) >= 0
        return orient(p[u], p[v], q) > 0 and self._orient_o(v, q) >= 0 and self._orient_o(u, q) <= 0

    def _conflict(self, tid: int, q: Point) -> bool:
        u, v, w = self.tri[tid]
        p = self.pts
        if w != GHOST:
            return incircle(p[u], p[v], p[w], q) > 0
        o = orient(p[u], p[v], q)
        if o != 0:
            return o > 0
        return (q[0] - p[u][0]) * (q[0] - p[v][0]) + (q[1] - p[u][1]) * (q[1] - p[v][1]) < 0

    # ----- triangle bookkeeping -----
    def _add(self, t: Triangle) -> int:
        u, v, w = t
        if u == GHOST:
            u, v, w = v, w, u
        elif v == GHOST:
            u, v, w = w, u, v
        tid = len(self.tri)
        self.tri.append((u, v, w))
        self.children.append([])
        self.edge[(u, v)] = self.edge[(v, w)] = self.edge[(w, u)] = tid
        return tid

    def _kill(self, tids: list[int], new: list[int]) -> None:
        for tid in tids:
            u, v, w = self.tri[tid]
            for e in ((u, v), (v, w), (w, u)):
                if self.edge.get(e) == tid:
                    del self.edge[e]
            self.children[tid] = new
        for tid in new:
            u, v, w = self.tri[tid]
            self.edge[(u, v)] = self.edge[(v, w)] = self.edge[(w, u)] = tid

    def _start(self, i: int, j: int, k: int) -> None:
        if orient(self.pts[i], self.pts[j], self.pts[k]) < 0:
            j, k = k, j
        p = self.pts
        self.o3 = (p[i][0] + p[j][0] + p[k][0], p[i][1] + p[j][1] + p[k][1])
        self.roots = [self._add(t) for t in ((i, j, k), (j, i, GHOST), (k, j, GHOST), (i, k, GHOST))]

    # ----- operations -----
    def locate(self, q: Point) -> int:
        """Return the id of a live triangle (maybe a ghost) whose region holds q. Needs a first triangle."""
        cur = next(t for t in self.roots if self._region_contains(t, q))  # @line L1
        while self.children[cur]:  # @line L2
            cur = next(t for t in self.children[cur] if self._region_contains(t, q))  # @line L3
        return cur  # @line L4

    def insert(self, q: Point) -> bool:
        """Insert the point q; return False if it was already a vertex. Keeps the Delaunay property."""
        if q in self.index:
            return False
        i = len(self.pts)
        self.pts.append(q)
        self.index[q] = i
        if not self.roots:
            self.pending.append(i)
            pend = self.pending
            if len(pend) >= 3 and orient(self.pts[pend[0]], self.pts[pend[1]], q) != 0:
                self.pending = []
                self._start(pend[0], pend[1], i)
                for j in pend[2:-1]:
                    self._insert_index(j)
            return True
        self._insert_index(i)
        return True

    def _insert_index(self, i: int) -> None:
        p = self.pts
        q = p[i]
        t = self.locate(q)  # @line L5
        u, v, w = self.tri[t]
        stack: list[tuple[int, int]] = []
        on_edge = None
        if w != GHOST:
            for x, y in ((u, v), (v, w), (w, u)):
                if orient(p[x], p[y], q) == 0:
                    on_edge = (x, y)
        if on_edge is None:  # @line L6
            new = [self._add((u, v, i)), self._add((v, w, i)), self._add((w, u, i))]
            self._kill([t], new)
            stack = [(u, v), (v, w), (w, u)]
        else:  # @line L7
            x, y = on_edge
            z = next(c for c in (u, v, w) if c not in (x, y))
            t2 = self.edge[(y, x)]
            r = next(c for c in self.tri[t2] if c not in (x, y))
            new1 = [self._add((x, i, z)), self._add((i, y, z))]
            new2 = [self._add((y, i, r)), self._add((i, x, r))]
            self._kill([t], new1)
            self._kill([t2], new2)
            stack = [(z, x), (y, z), (r, y), (x, r)]
        while stack:  # @line L8
            x, y = stack.pop()
            t1 = self.edge.get((x, y))
            if t1 is None or i not in self.tri[t1]:
                continue
            t2 = self.edge[(y, x)]
            r = next(c for c in self.tri[t2] if c not in (x, y))
            if self._conflict(t2, q):  # @line L9
                new = [self._add((i, x, r)), self._add((i, r, y))]  # @line L10
                self._kill([t1, t2], new)
                stack += [(x, r), (r, y)]  # @line L11

    def triangles(self) -> list[tuple[Point, Point, Point]]:
        """The real triangles, each counterclockwise, sorted."""
        out = []
        for tid, (u, v, w) in enumerate(self.tri):
            if not self.children[tid] and w != GHOST:
                out.append((self.pts[u], self.pts[v], self.pts[w]))
        return sorted(out)

    def find_triangle(self, q: Point) -> tuple[Point, Point, Point] | None:
        """A triangle of the triangulation that holds q (closed), or None if q is outside the hull."""
        if not self.roots:
            return None
        u, v, w = self.tri[self.locate(q)]
        if w == GHOST:
            return None
        return (self.pts[u], self.pts[v], self.pts[w])

    def check_invariant(self) -> None:
        """Every edge between two live triangles is locally Delaunay, and the live triangles are consistent."""
        live = [tid for tid in range(len(self.tri)) if not self.children[tid]]
        for tid in live:
            u, v, w = self.tri[tid]
            for x, y in ((u, v), (v, w), (w, u)):
                assert self.edge[(x, y)] == tid
                nb = self.edge[(y, x)]
                r = next(c for c in self.tri[nb] if c not in (x, y))
                assert not self._conflict(tid, self.pts[r]) if r != GHOST else True
            if w != GHOST:
                assert orient(self.pts[u], self.pts[v], self.pts[w]) > 0


def delaunay_triangulation(points: list[Point], seed: int = 0) -> list[tuple[Point, Point, Point]]:
    """Randomized incremental construction: insert the points in a random order. Expected O(n log n) time."""
    order = list(dict.fromkeys(points))
    random.Random(seed).shuffle(order)
    dt = DelaunayTriangulation()
    for q in order:
        dt.insert(q)
    return dt.triangles()
