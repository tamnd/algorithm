# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/visibility-graph/. The authors are listed in prov/KH2F9W.jsonl.

"""The visibility graph of polygonal obstacles in the plane, with exact tests.

Obstacles are simple polygons with int or Fraction vertices, given in either
orientation. Their interiors are open and pairwise disjoint, and their
boundaries do not meet. A path may touch obstacle boundaries but may not enter
an interior. Two points see each other when the closed segment between them
misses the interior of every obstacle. The graph is built by testing all pairs
of nodes against all edges, O(n) per pair and O(n^3) time for n vertices,
with exact predicates.
Shortest paths use Dijkstra's algorithm on float lengths.
"""

import heapq
import math
from fractions import Fraction

Point = tuple


def orient(a: Point, b: Point, c: Point):
    """Twice the signed area of the triangle abc: > 0 for a left turn."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _sign(x) -> int:
    return (x > 0) - (x < 0)


def _on_segment(p: Point, a: Point, b: Point) -> bool:
    """p lies on the closed segment ab."""
    return (orient(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def proper_crossing(p: Point, q: Point, a: Point, b: Point) -> bool:
    """The open segments pq and ab cross at one point interior to both."""
    d1 = _sign(orient(p, q, a))
    d2 = _sign(orient(p, q, b))
    d3 = _sign(orient(a, b, p))
    d4 = _sign(orient(a, b, q))
    return d1 * d2 < 0 and d3 * d4 < 0


def strictly_inside(p: Point, poly) -> bool:
    """p lies in the open interior of the simple polygon poly."""
    n = len(poly)
    inside = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if _on_segment(p, a, b):
            return False
        if (a[1] > p[1]) != (b[1] > p[1]):
            # x-coordinate of the crossing of edge ab with the line y = p.y
            if orient(a, b, p) * (b[1] - a[1]) > 0:
                inside = not inside
    return inside


def _in_cone(prev: Point, v: Point, nxt: Point, u: Point, sigma: int) -> bool:
    """The direction u points from the vertex v into the open interior of the polygon.

    prev and nxt are the neighbors of v, and sigma is +1 for a counterclockwise
    polygon and -1 for a clockwise one, so the interior is to the left of each
    edge after the sign change.
    """
    c1 = sigma * ((v[0] - prev[0]) * u[1] - (v[1] - prev[1]) * u[0]) > 0
    c2 = sigma * ((nxt[0] - v[0]) * u[1] - (nxt[1] - v[1]) * u[0]) > 0
    turn = sigma * ((v[0] - prev[0]) * (nxt[1] - v[1]) - (v[1] - prev[1]) * (nxt[0] - v[0]))
    return (c1 and c2) if turn >= 0 else (c1 or c2)


def _area_sign(poly) -> int:
    n = len(poly)
    return _sign(sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n)))


def visible(p: Point, q: Point, obstacles) -> bool:
    """The closed segment pq misses the interior of every obstacle."""
    if p == q:
        return not any(strictly_inside(p, poly) for poly in obstacles)
    d = (q[0] - p[0], q[1] - p[1])
    back = (-d[0], -d[1])
    for poly in obstacles:  # @line L4
        n = len(poly)
        sigma = _area_sign(poly)
        touched = False
        for i in range(n):  # @line L5
            a, b = poly[i], poly[(i + 1) % n]
            if proper_crossing(p, q, a, b):  # @line L6
                return False
            if _on_segment(a, p, q):  # @line L7
                touched = True
                if a != q and _in_cone(poly[i - 1], a, b, d, sigma):  # @line L8
                    return False
                if a != p and _in_cone(poly[i - 1], a, b, back, sigma):  # @line L9
                    return False
        if not touched:
            mid = (Fraction(p[0] + q[0], 2), Fraction(p[1] + q[1], 2))
            if strictly_inside(mid, poly):  # @line L10
                return False
    return True  # @line L11


class VisibilityGraph:
    """Nodes are the obstacle vertices followed by the extra points."""

    def __init__(self, obstacles, points=()):
        self.obstacles = [list(poly) for poly in obstacles]
        nodes = [v for poly in self.obstacles for v in poly] + list(points)
        for v in points:
            if any(strictly_inside(v, poly) for poly in self.obstacles):
                raise ValueError("a point lies inside an obstacle")
        self.nodes = nodes
        self.adj = [[] for _ in nodes]
        for i in range(len(nodes)):  # @line L1
            for j in range(i + 1, len(nodes)):  # @line L2
                if visible(nodes[i], nodes[j], self.obstacles):  # @line L3
                    self._link(i, j)

    def _link(self, i: int, j: int) -> None:
        d = math.dist(self.nodes[i], self.nodes[j])
        self.adj[i].append((j, d))
        self.adj[j].append((i, d))

    def edges(self) -> set:
        """The edges as pairs (i, j) with i < j."""
        return {(i, j) for i in range(len(self.nodes)) for j, _ in self.adj[i] if i < j}

    def edge_count(self) -> int:
        return sum(len(a) for a in self.adj) // 2

    def shortest_path(self, s: Point, t: Point):
        """Length and vertex list of a shortest obstacle-avoiding path from s to t."""
        for v in (s, t):
            if any(strictly_inside(v, poly) for poly in self.obstacles):
                raise ValueError("an end point lies inside an obstacle")
        nodes = self.nodes + [s, t]
        si, ti = len(nodes) - 2, len(nodes) - 1
        extra = {si: [], ti: []}
        for k in (si, ti):
            for j in range(len(nodes)):
                if j != k and visible(nodes[k], nodes[j], self.obstacles):
                    extra[k].append((j, math.dist(nodes[k], nodes[j])))

        def neighbors(u):
            if u in extra:
                return extra[u]
            out = list(self.adj[u])
            for k in (si, ti):
                for j, d in extra[k]:
                    if j == u:
                        out.append((k, d))
            return out

        dist = {si: 0.0}
        prev = {si: None}
        heap = [(0.0, si)]
        done = set()
        while heap:
            d, u = heapq.heappop(heap)
            if u in done:
                continue
            done.add(u)
            if u == ti:
                break
            for v, w in neighbors(u):
                nd = d + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        if ti not in done:
            return math.inf, []
        path = []
        u = ti
        while u is not None:
            path.append(nodes[u])
            u = prev[u]
        return dist[ti], path[::-1]

    def check_invariant(self) -> None:
        """The adjacency lists are symmetric and hold exactly the visible pairs."""
        n = len(self.nodes)
        for i in range(n):
            for j, d in self.adj[i]:
                assert any(k == i and e == d for k, e in self.adj[j])
        for i in range(n):
            linked = {j for j, _ in self.adj[i]}
            for j in range(n):
                if j != i:
                    assert (j in linked) == visible(self.nodes[i], self.nodes[j], self.obstacles)
