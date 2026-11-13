# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rapidly-exploring-random-tree/. The authors are listed in prov/C6S6KW.jsonl.

"""Rapidly-exploring random tree (LaValle 1998) for a point robot in [0, w] x [0, h].

Obstacles are convex polygons with counterclockwise vertices. Each iteration draws a random point, finds
the nearest tree vertex, and adds a new vertex at most eta away from it, toward the random point, when
the segment is free. The goal point is drawn with probability goal_bias. The search ends when a new
vertex is within goal_radius of the goal and sees it.
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
    """Collision checker that counts its calls."""

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
    """The point on the segment from x toward y at distance min(eta, |xy|) from x."""
    d = math.dist(x, y)
    if d <= eta:
        return y
    return (x[0] + eta * (y[0] - x[0]) / d, x[1] + eta * (y[1] - x[1]) / d)


class Tree:
    def __init__(self, root):
        self.nodes = [root]
        self.parent = [None]

    def nearest(self, p):
        return min(range(len(self.nodes)), key=lambda i: (self.nodes[i][0] - p[0]) ** 2 + (self.nodes[i][1] - p[1]) ** 2)

    def add(self, p, parent):
        self.nodes.append(p)
        self.parent.append(parent)
        return len(self.nodes) - 1

    def path_to(self, i):
        out = []
        while i is not None:
            out.append(self.nodes[i])
            i = self.parent[i]
        return out[::-1]

    def edges(self):
        return [(self.nodes[self.parent[i]], self.nodes[i]) for i in range(1, len(self.nodes))]


def rrt(w, h, obstacles, start, goal, rng, eta=0.5, goal_radius=0.5, goal_bias=0.05, max_iter=3000):
    """Returns (path or None, tree, checker, iterations)."""
    check = Checker(obstacles)
    tree = Tree(start)  # @line L1
    if not (check.point_free(start) and check.point_free(goal)):
        return None, tree, check, 0
    for it in range(1, max_iter + 1):  # @line L2
        x_rand = goal if rng.random() < goal_bias else (rng.uniform(0, w), rng.uniform(0, h))  # @line L3
        i_near = tree.nearest(x_rand)  # @line L4
        x_new = steer(tree.nodes[i_near], x_rand, eta)  # @line L5
        if not check.segment_free(tree.nodes[i_near], x_new):  # @line L6
            continue
        i_new = tree.add(x_new, i_near)  # @line L7
        if math.dist(x_new, goal) <= goal_radius and check.segment_free(x_new, goal):  # @line L8
            if x_new != goal:
                i_new = tree.add(goal, i_new)
            return tree.path_to(i_new), tree, check, it  # @line L9
    return None, tree, check, max_iter  # @line L10
