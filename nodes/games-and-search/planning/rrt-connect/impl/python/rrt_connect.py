# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rrt-connect/. The authors are listed in prov/2V2P6G.jsonl.

"""RRT-Connect (Kuffner and LaValle 2000) for a point robot in [0, w] x [0, h].

Two trees grow, one from the start and one from the goal. Each iteration extends one tree one step toward
a random point. If that step adds a vertex, the other tree runs CONNECT: it takes steps toward the new
vertex until it reaches it or is blocked. Then the two trees swap roles. Obstacles are convex polygons.
"""

import math

TRAPPED, ADVANCED, REACHED = "trapped", "advanced", "reached"


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


def extend(tree, x, eta, check):
    """One step of the tree toward x. Returns (status, index of the new vertex or None)."""
    i_near = tree.nearest(x)  # @line L1
    x_new = steer(tree.nodes[i_near], x, eta)  # @line L2
    if not check.segment_free(tree.nodes[i_near], x_new):  # @line L3
        return TRAPPED, None
    i_new = tree.add(x_new, i_near)  # @line L4
    return (REACHED if x_new == x else ADVANCED), i_new  # @line L5


def connect(tree, x, eta, check):
    """Repeat extend toward x while it advances."""
    while True:
        status, i = extend(tree, x, eta, check)  # @line L6
        if status != ADVANCED:
            return status, i  # @line L7


def rrt_connect(w, h, obstacles, start, goal, rng, eta=0.5, max_iter=3000):
    """Returns (path or None, tree from start, tree from goal, checker, iterations)."""
    check = Checker(obstacles)
    ta, tb = Tree(start), Tree(goal)  # @line L8
    if not (check.point_free(start) and check.point_free(goal)):
        return None, ta, tb, check, 0
    a, b = ta, tb
    for it in range(1, max_iter + 1):  # @line L9
        x_rand = (rng.uniform(0, w), rng.uniform(0, h))  # @line L10
        status, i_new = extend(a, x_rand, eta, check)  # @line L11
        if status != TRAPPED:
            status_b, j = connect(b, a.nodes[i_new], eta, check)  # @line L12
            if status_b == REACHED:
                pa, pb = a.path_to(i_new), b.path_to(j)  # @line L13
                if a is ta:
                    return pa + pb[::-1][1:], ta, tb, check, it
                return pb + pa[::-1][1:], ta, tb, check, it
        a, b = b, a  # @line L14
    return None, ta, tb, check, max_iter  # @line L15
