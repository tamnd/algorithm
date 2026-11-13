# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-roadmap/. The authors are listed in prov/S30SPN.jsonl.

"""Probabilistic roadmap (Kavraki, Svestka, Latombe and Overmars 1996) for a point robot in [0, w] x [0, h].

Obstacles are convex polygons with counterclockwise vertices. The local planner is the straight segment,
checked exactly against each polygon. The learning phase samples free points and links each one to the
neighbors within radius r. In the default mode a link is tried only when the two points lie in different
components, so the roadmap is a forest, as in the 1996 paper. With every_pair=True all free links inside
the radius are added (the simplified PRM). The query phase links start and goal and runs Dijkstra.
"""

import heapq
import math


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def point_in_convex(p, poly):
    n = len(poly)
    return all(cross(poly[i], poly[(i + 1) % n], p) >= 0 for i in range(n))


def segment_meets_convex(p, q, poly):
    """True if the closed segment pq meets the closed convex polygon (Cyrus-Beck clipping)."""
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        num = cross(a, b, p)
        den = (b[0] - a[0]) * dy - (b[1] - a[1]) * dx
        if den == 0:
            if num < 0:
                return False
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return False
    return True


class Checker:
    """Collision checker that counts its calls, the main cost of a sampling planner."""

    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.calls = 0

    def point_free(self, p):
        self.calls += 1
        return not any(point_in_convex(p, ob) for ob in self.obstacles)

    def segment_free(self, p, q):
        self.calls += 1
        return not any(segment_meets_convex(p, q, ob) for ob in self.obstacles)


class DisjointSet:
    def __init__(self):
        self.parent = []

    def add(self):
        self.parent.append(len(self.parent))
        return len(self.parent) - 1

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)


class Roadmap:
    def __init__(self, w, h, obstacles, n, radius, rng, every_pair=False):
        self.check = Checker(obstacles)
        self.nodes, self.adj = [], []  # @line L1
        self.sets = DisjointSet()
        self.radius = radius
        self.every_pair = every_pair
        while len(self.nodes) < n:  # @line L2
            p = (rng.uniform(0, w), rng.uniform(0, h))  # @line L3
            if self.check.point_free(p):  # @line L4
                self._insert(p)

    def _insert(self, p):
        i = len(self.nodes)
        near = sorted((math.dist(p, q), j) for j, q in enumerate(self.nodes) if math.dist(p, q) <= self.radius)
        self.nodes.append(p)  # @line L5
        self.adj.append([])
        self.sets.add()
        for d, j in near:  # @line L6
            if not self.every_pair and self.sets.find(i) == self.sets.find(j):  # @line L7
                continue
            if self.check.segment_free(p, self.nodes[j]):  # @line L8
                self.adj[i].append((j, d))
                self.adj[j].append((i, d))
                self.sets.union(i, j)
        return i

    def edges(self):
        return [(self.nodes[i], self.nodes[j]) for i in range(len(self.nodes)) for j, _ in self.adj[i] if i < j]

    def _visible(self, p):
        """The roadmap nodes within the radius that a free segment links to p, nearest first, as (j, d)."""
        near = sorted((math.dist(p, q), j) for j, q in enumerate(self.nodes) if math.dist(p, q) <= self.radius)
        return [(j, d) for d, j in near if self.check.segment_free(p, self.nodes[j])]

    def _attach(self, start, goal):
        """A node a seen by start and a node b seen by goal in the same component, nearest first, or None."""
        by_comp = {}
        for j, d in self._visible(goal):
            by_comp.setdefault(self.sets.find(j), (j, d))
        for j, d in self._visible(start):
            c = self.sets.find(j)
            if c in by_comp:
                return (j, d), by_comp[c]
        return None

    def query(self, start, goal):
        """Shortest roadmap path from start to goal as a list of points, or None."""
        if not (self.check.point_free(start) and self.check.point_free(goal)):
            return None
        if math.dist(start, goal) <= self.radius and self.check.segment_free(start, goal):
            return [start, goal]
        pair = self._attach(start, goal)  # @line L9
        if pair is None:  # @line L10
            return None
        a, b = pair
        dist = {a[0]: a[1]}
        prev = {a[0]: None}
        heap = [(a[1], a[0])]
        while heap:  # @line L11
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            if u == b[0]:
                break
            for v, w in self.adj[u]:
                if d + w < dist.get(v, math.inf):
                    dist[v] = d + w
                    prev[v] = u
                    heapq.heappush(heap, (d + w, v))
        path = [goal]
        u = b[0]
        while u is not None:
            path.append(self.nodes[u])
            u = prev[u]
        path.append(start)
        return path[::-1]
