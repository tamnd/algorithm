# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rrt-star/. The authors are listed in prov/4RBAE6.jsonl.

"""RRT* (Karaman and Frazzoli 2011, Algorithm 6) for a point robot in [0, w] x [0, h] with path length cost.

Each iteration steers the nearest vertex toward a random point. If the new segment is free, the new vertex
takes as parent the neighbor within radius r(n) = min(gamma (log n / n)^(1/2), eta) that gives it the least
cost. Then each neighbor whose cost drops when it goes through the new vertex is rewired to it.
Obstacles are convex polygons with counterclockwise vertices. A uniform grid of cell size eta answers the
nearest and near queries.
"""

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
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.calls = 0

    def point_free(self, p):
        self.calls += 1
        return not any(point_in_convex(p, ob) for ob in self.obstacles)

    def segment_free(self, p, q):
        self.calls += 1
        return not any(segment_meets_convex(p, q, ob) for ob in self.obstacles)


def steer(x, y, eta):
    d = math.dist(x, y)
    if d <= eta:
        return y
    return (x[0] + eta * (y[0] - x[0]) / d, x[1] + eta * (y[1] - x[1]) / d)


def gamma_star(free_measure, d=2):
    """The Karaman-Frazzoli threshold (2 (1 + 1/d))^(1/d) (free_measure / zeta_d)^(1/d)."""
    zeta = math.pi ** (d / 2) / math.gamma(d / 2 + 1)
    return (2 * (1 + 1 / d)) ** (1 / d) * (free_measure / zeta) ** (1 / d)


class RRTStar:
    def __init__(self, w, h, obstacles, start, rng, eta=1.0, gamma=None):
        self.w, self.h = w, h
        self.rng = rng
        self.check = Checker(obstacles)
        self.eta = eta
        self.gamma = gamma if gamma is not None else 1.1 * gamma_star(w * h)
        self.nodes = [start]  # @line L1
        self.parent = [None]
        self.cost = [0.0]
        self.children = [[]]
        self.cells = {}
        self._index(0)

    def _key(self, p):
        return (int(p[0] // self.eta), int(p[1] // self.eta))

    def _index(self, i):
        self.cells.setdefault(self._key(self.nodes[i]), []).append(i)

    def nearest(self, p):
        cx, cy = self._key(p)
        best, bd = None, math.inf
        span = int(max(self.w, self.h) / self.eta) + 2
        for r in range(span + 1):
            for a in range(cx - r, cx + r + 1):
                for b in range(cy - r, cy + r + 1):
                    if max(abs(a - cx), abs(b - cy)) != r:
                        continue
                    for i in self.cells.get((a, b), ()):
                        d = math.dist(self.nodes[i], p)
                        if d < bd:
                            best, bd = i, d
            if best is not None and bd <= r * self.eta:
                break
        return best

    def near(self, p, radius):
        cx, cy = self._key(p)
        k = int(math.ceil(radius / self.eta))
        out = []
        for a in range(cx - k, cx + k + 1):
            for b in range(cy - k, cy + k + 1):
                for i in self.cells.get((a, b), ()):
                    if math.dist(self.nodes[i], p) <= radius:
                        out.append(i)
        return out

    def radius(self):
        n = len(self.nodes)
        if n < 2:
            return self.eta
        return min(self.gamma * math.sqrt(math.log(n) / n), self.eta)

    def _set_parent(self, j, i):
        old = self.parent[j]
        if old is not None:
            self.children[old].remove(j)
        self.parent[j] = i
        self.children[i].append(j)
        delta = self.cost[i] + math.dist(self.nodes[i], self.nodes[j]) - self.cost[j]
        stack = [j]
        while stack:
            u = stack.pop()
            self.cost[u] += delta
            stack.extend(self.children[u])

    def step(self):  # @line L2
        """One iteration of Algorithm 6. Returns the index of the new vertex or None."""
        x_rand = (self.rng.uniform(0, self.w), self.rng.uniform(0, self.h))  # @line L3
        i_nearest = self.nearest(x_rand)  # @line L4
        x_new = steer(self.nodes[i_nearest], x_rand, self.eta)  # @line L5
        if not self.check.segment_free(self.nodes[i_nearest], x_new):  # @line L6
            return None
        radius = self.radius()  # @line L7
        near = self.near(x_new, radius)
        i_min = i_nearest  # @line L8
        c_min = self.cost[i_nearest] + math.dist(self.nodes[i_nearest], x_new)
        free_to = {i_nearest: True}
        for i in near:  # @line L9
            c = self.cost[i] + math.dist(self.nodes[i], x_new)
            if c < c_min:
                free_to[i] = self.check.segment_free(self.nodes[i], x_new)
                if free_to[i]:
                    i_min, c_min = i, c
        k = len(self.nodes)
        self.nodes.append(x_new)  # @line L10
        self.parent.append(None)
        self.cost.append(c_min)
        self.children.append([])
        self._index(k)
        self.parent[k] = i_min
        self.children[i_min].append(k)
        for i in near:  # @line L11
            if i == i_min:
                continue
            c = c_min + math.dist(x_new, self.nodes[i])
            if c < self.cost[i]:  # @line L12
                ok = free_to.get(i)
                if ok is None:
                    ok = self.check.segment_free(x_new, self.nodes[i])
                if ok:
                    self._set_parent(i, k)  # @line L13
        return k

    def best_cost(self, goal, goal_radius):
        """Least cost(v) + |v goal| over vertices v within goal_radius that see the goal, or inf."""
        best = math.inf
        for i in self.near(goal, goal_radius):  # @line L14
            c = self.cost[i] + math.dist(self.nodes[i], goal)
            if c < best and self.check.segment_free(self.nodes[i], goal):
                best = c
        return best

    def path_to(self, i):
        out = []
        while i is not None:
            out.append(self.nodes[i])
            i = self.parent[i]
        return out[::-1]

    def edges(self):
        return [(self.nodes[self.parent[i]], self.nodes[i]) for i in range(1, len(self.nodes))]
