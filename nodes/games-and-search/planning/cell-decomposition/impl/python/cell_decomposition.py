# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cell-decomposition/. The authors are listed in prov/9HY0M9.jsonl.

"""Cell decomposition planners for a point robot among convex polygons in the rectangle [0, w] x [0, h].

exact_decomposition cuts the free space into trapezoids with vertical lines through every vertex and every
crossing of two edges. Inside one vertical slab no two edges cross, so the free parts of the slab are
trapezoids. The planner is complete: it finds a path when one exists in the open free space.

approximate_decomposition is the quadtree method. A square is free, full or mixed. Mixed squares are split
until they reach the smallest size. The planner is resolution complete.

Obstacles are convex polygons with counterclockwise vertices inside the rectangle. They may overlap.
"""

import bisect
from collections import deque

EPS = 1e-12


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def point_in_convex(p, poly):
    """True if p is in the closed convex polygon."""
    n = len(poly)
    return all(cross(poly[i], poly[(i + 1) % n], p) >= 0 for i in range(n))


def point_free(p, obstacles):
    return not any(point_in_convex(p, ob) for ob in obstacles)


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


def rect_meets_convex(x0, y0, x1, y1, poly):
    """True if the closed rectangle and the closed convex polygon share a point (separating axes)."""
    rect = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for shape in (rect, poly):
        n = len(shape)
        for i in range(n):
            ax = shape[i][1] - shape[(i + 1) % n][1]
            ay = shape[(i + 1) % n][0] - shape[i][0]
            pa = [ax * x + ay * y for (x, y) in rect]
            pb = [ax * x + ay * y for (x, y) in poly]
            if max(pa) < min(pb) or max(pb) < min(pa):
                return False
    return True


def _edges(obstacles):
    out = []
    for ob in obstacles:
        n = len(ob)
        for i in range(n):
            out.append((ob[i], ob[(i + 1) % n]))
    return out


def _crossing_x(e, f):
    """x of the proper crossing of two segments, or None."""
    (p, q), (r, s) = e, f
    d1, d2 = cross(p, q, r), cross(p, q, s)
    d3, d4 = cross(r, s, p), cross(r, s, q)
    if d1 * d2 < 0 and d3 * d4 < 0:
        t = d3 / (d3 - d4)
        return p[0] + t * (q[0] - p[0])
    return None


def _y_at(line, x):
    (p, q) = line
    if p[0] == q[0]:
        return p[1]
    t = (x - p[0]) / (q[0] - p[0])
    return p[1] + t * (q[1] - p[1])


class ExactDecomposition:
    """Trapezoid cells. Cell i lies in slab slab[i] between the lines lower[i] and upper[i]."""

    def __init__(self, w, h, obstacles):
        self.obstacles = obstacles
        edges = _edges(obstacles)
        xs = {0.0, float(w)}
        for ob in obstacles:
            for v in ob:
                if 0 < v[0] < w:
                    xs.add(float(v[0]))
        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                x = _crossing_x(edges[i], edges[j])
                if x is not None and 0 < x < w:
                    xs.add(x)
        self.xs = sorted(xs)  # @line L1
        bottom = ((0.0, 0.0), (float(w), 0.0))
        top = ((0.0, float(h)), (float(w), float(h)))
        self.slab, self.lower, self.upper = [], [], []
        self.by_slab = []
        for k in range(len(self.xs) - 1):
            a, b = self.xs[k], self.xs[k + 1]
            xm = (a + b) / 2
            lines = [bottom, top]
            for e in edges:
                lo, hi = min(e[0][0], e[1][0]), max(e[0][0], e[1][0])
                if lo < hi and lo <= a and hi >= b:
                    lines.append(e)
            lines.sort(key=lambda ln: _y_at(ln, xm))
            ids = []
            for lo_line, hi_line in zip(lines, lines[1:]):
                ylo, yhi = _y_at(lo_line, xm), _y_at(hi_line, xm)
                if yhi - ylo <= EPS:
                    continue
                if not point_free((xm, (ylo + yhi) / 2), obstacles):
                    continue
                ids.append(len(self.slab))
                self.slab.append(k)
                self.lower.append(lo_line)
                self.upper.append(hi_line)
            self.by_slab.append(ids)
        self.adj = [[] for _ in self.slab]  # @line L2
        for k in range(len(self.xs) - 2):
            x = self.xs[k + 1]
            for i in self.by_slab[k]:
                a0, a1 = _y_at(self.lower[i], x), _y_at(self.upper[i], x)
                for j in self.by_slab[k + 1]:
                    b0, b1 = _y_at(self.lower[j], x), _y_at(self.upper[j], x)
                    lo, hi = max(a0, b0), min(a1, b1)
                    if hi - lo > EPS:  # @line L3
                        door = (x, (lo + hi) / 2)
                        self.adj[i].append((j, door))  # @line L4
                        self.adj[j].append((i, door))

    def locate(self, p):
        """Index of a cell that holds the free point p, or None."""
        if not point_free(p, self.obstacles):
            return None
        k = bisect.bisect_right(self.xs, p[0]) - 1
        k = min(max(k, 0), len(self.xs) - 2)
        for i in self.by_slab[k]:
            if _y_at(self.lower[i], p[0]) - EPS <= p[1] <= _y_at(self.upper[i], p[0]) + EPS:
                return i
        return None

    def plan(self, start, goal):
        """A polyline from start to goal through the cells, or None if no path exists."""
        return _search(self.adj, self.locate(start), self.locate(goal), start, goal, self.center)  # @line L5

    def center(self, i):
        """A point inside cell i: the middle of its cut with the vertical midline of its slab."""
        k = self.slab[i]
        xm = (self.xs[k] + self.xs[k + 1]) / 2
        return (xm, (_y_at(self.lower[i], xm) + _y_at(self.upper[i], xm)) / 2)


def _search(adj, s, g, start, goal, center):
    """Breadth-first search on the cell graph. The path enters and leaves each cell through doors."""
    if s is None or g is None:  # @line L6
        return None
    parent = {s: None}
    todo = deque([s])
    while todo:  # @line L7
        u = todo.popleft()
        if u == g:
            break
        for v, door in adj[u]:
            if v not in parent:
                parent[v] = (u, door)
                todo.append(v)
    if g not in parent:  # @line L8
        return None
    steps = []
    u = g
    while parent[u] is not None:
        u, door = parent[u]
        steps.append((u, door))
    steps.reverse()
    path = [start]
    for k, (u, door) in enumerate(steps):
        if k > 0:
            path.append(center(u))
        path.append(door)
    path.append(goal)
    return path  # @line L9


class ApproximateDecomposition:
    """Quadtree cells of the square [0, size]^2. Only free leaf squares are kept."""

    def __init__(self, size, obstacles, min_size):
        self.obstacles = obstacles
        self.cells = []
        self.mixed = 0
        todo = [(0.0, 0.0, float(size))]
        while todo:
            x, y, s = todo.pop()
            hits = [ob for ob in obstacles if rect_meets_convex(x, y, x + s, y + s, ob)]
            if not hits:  # @line L10
                self.cells.append((x, y, s))
                continue
            corners = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
            if any(all(point_in_convex(c, ob) for c in corners) for ob in hits):  # @line L11
                continue
            if s / 2 < min_size:  # @line L12
                self.mixed += 1
                continue
            t = s / 2
            todo.extend([(x, y, t), (x + t, y, t), (x, y + t, t), (x + t, y + t, t)])  # @line L13
        self.adj = [[] for _ in self.cells]
        left, bottom = {}, {}
        for i, (x, y, s) in enumerate(self.cells):
            left.setdefault(x, []).append(i)
            bottom.setdefault(y, []).append(i)
        for i, (x, y, s) in enumerate(self.cells):
            for j in left.get(x + s, []):
                _, y2, s2 = self.cells[j]
                lo, hi = max(y, y2), min(y + s, y2 + s2)
                if hi > lo:
                    door = (x + s, (lo + hi) / 2)
                    self.adj[i].append((j, door))
                    self.adj[j].append((i, door))
            for j in bottom.get(y + s, []):
                x2, _, s2 = self.cells[j]
                lo, hi = max(x, x2), min(x + s, x2 + s2)
                if hi > lo:
                    door = ((lo + hi) / 2, y + s)
                    self.adj[i].append((j, door))
                    self.adj[j].append((i, door))

    def locate(self, p):
        for i, (x, y, s) in enumerate(self.cells):
            if x <= p[0] <= x + s and y <= p[1] <= y + s:
                return i
        return None

    def plan(self, start, goal):
        return _search(self.adj, self.locate(start), self.locate(goal), start, goal, self.center)

    def center(self, i):
        x, y, s = self.cells[i]
        return (x + s / 2, y + s / 2)
