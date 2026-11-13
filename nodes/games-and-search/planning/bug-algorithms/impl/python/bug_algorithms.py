# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bug-algorithms/. The authors are listed in prov/JJWB8E.jsonl.

"""Bug1 and Bug2 (Lumelsky and Stepanov 1987) for a point robot with contact sensing in the plane.

An obstacle is a list of boundary loops: the outer polygon, then the holes. A hole lets an obstacle enclose
a region, for example a ring around the goal. Obstacles are closed and pairwise disjoint. The robot follows
a loop in the order of its vertices. The planners return (path, reached), where path is a polyline.
"""

import bisect
import math

EPS = 1e-9


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def _inside_polygon(p, poly):
    """Even-odd ray test for a simple polygon."""
    inside = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                inside = not inside
    return inside


def _dist_to_segment(p, a, b):
    d = _sub(b, a)
    t = max(0.0, min(1.0, ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / (d[0] ** 2 + d[1] ** 2)))
    return math.hypot(p[0] - a[0] - t * d[0], p[1] - a[1] - t * d[1]), t


class Loop:
    def __init__(self, obstacle, pts):
        self.obstacle = obstacle
        self.pts = pts
        self.cum = [0.0]
        for i in range(len(pts)):
            self.cum.append(self.cum[-1] + math.dist(pts[i], pts[(i + 1) % len(pts)]))
        self.perimeter = self.cum[-1]

    def edge(self, i):
        return self.pts[i], self.pts[(i + 1) % len(self.pts)]

    def point_at(self, s):
        s %= self.perimeter
        i = min(bisect.bisect_right(self.cum, s) - 1, len(self.pts) - 1)
        a, b = self.edge(i)
        t = (s - self.cum[i]) / (self.cum[i + 1] - self.cum[i])
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

    def walk(self, s, length, forward=True):
        """Points met when moving length along the loop from arc position s, without the first point."""
        out = []
        p = self.perimeter
        if forward:
            k = bisect.bisect_right(self.cum, s % p)
            base = s - (s % p)
            while True:
                if k > len(self.pts):
                    k, base = 1, base + p
                v = base + self.cum[k]
                if v >= s + length - EPS:
                    break
                out.append(self.pts[k % len(self.pts)])
                k += 1
        else:
            k = bisect.bisect_left(self.cum, s % p) - 1
            base = s - (s % p)
            while True:
                if k < 0:
                    k, base = len(self.pts) - 1, base - p
                v = base + self.cum[k]
                if v <= s - length + EPS:
                    break
                out.append(self.pts[k])
                k -= 1
        out.append(self.point_at(s + length if forward else s - length))
        return out


class World:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.loops = [Loop(i, pts) for i, ob in enumerate(obstacles) for pts in ob]

    def perimeter(self, i):
        return sum(lp.perimeter for lp in self.loops if lp.obstacle == i)

    def boundary_distance(self, p):
        return min(_dist_to_segment(p, *lp.edge(i))[0] for lp in self.loops for i in range(len(lp.pts)))

    def blocked(self, p):
        """True if p is in the interior of an obstacle."""
        for ob in self.obstacles:
            if _inside_polygon(p, ob[0]) and not any(_inside_polygon(p, h) for h in ob[1:]):
                return self.boundary_distance(p) > 1e-7
        return False

    def first_hit(self, p, g):
        """First point after p where the segment p g meets a boundary: (t, loop, arc) or None."""
        best = None
        d = _sub(g, p)
        for lp in self.loops:
            for i in range(len(lp.pts)):
                a, b = lp.edge(i)
                e = _sub(b, a)
                den = _cross(d, e)
                if den == 0:
                    continue
                w = _sub(a, p)
                t = _cross(w, e) / den
                u = _cross(w, d) / den
                if EPS < t <= 1 and -EPS <= u <= 1 + EPS and (best is None or t < best[0]):
                    u = min(max(u, 0.0), 1.0)
                    best = (t, lp, lp.cum[i] + u * (lp.cum[i + 1] - lp.cum[i]))
        return best

    def can_head_to(self, p, g):
        d = math.dist(p, g)
        if d < EPS:
            return True
        step = min(1e-6, d / 2)
        return not self.blocked((p[0] + step * (g[0] - p[0]) / d, p[1] + step * (g[1] - p[1]) / d))


def path_length(path):
    return sum(math.dist(a, b) for a, b in zip(path, path[1:]))


def bug1(world, start, goal, max_hits=1000):
    """Bug1: circle each obstacle that is hit, then leave from the boundary point closest to the goal."""
    path, p = [start], start  # @line L1
    for _ in range(max_hits):  # @line L2
        hit = world.first_hit(p, goal)  # @line L3
        if hit is None:  # @line L4
            path.append(goal)
            return path, True
        _, lp, a = hit
        h = lp.point_at(a)  # @line L5
        path.append(h)
        path += lp.walk(a, lp.perimeter)  # @line L6
        best_s, best_d = a, math.dist(h, goal)
        for i in range(len(lp.pts)):
            d, t = _dist_to_segment(goal, *lp.edge(i))
            if d < best_d - EPS:
                best_d, best_s = d, lp.cum[i] + t * (lp.cum[i + 1] - lp.cum[i])
        ahead = (best_s - a) % lp.perimeter  # @line L7
        if ahead <= lp.perimeter - ahead:
            path += lp.walk(a, ahead, forward=True)
        else:
            path += lp.walk(a, lp.perimeter - ahead, forward=False)
        p = lp.point_at(best_s)  # @line L9
        if not world.can_head_to(p, goal):  # @line L8
            return path, False
    return path, False


def _mline_crossings(lp, i, s, g):
    """Points where edge i of the loop meets the segment s g, as (u along the edge, point)."""
    a, b = lp.edge(i)
    d, e = _sub(g, s), _sub(b, a)
    den = _cross(e, d)
    if den == 0:
        return []
    w = _sub(s, a)
    u = _cross(w, d) / den
    t = _cross(w, e) / den
    if -EPS <= u <= 1 + EPS and -EPS <= t <= 1 + EPS:
        return [(min(max(u, 0.0), 1.0), (a[0] + u * e[0], a[1] + u * e[1]))]
    return []


def bug2(world, start, goal, max_hits=1000):
    """Bug2: follow the boundary until the robot meets the start-goal line closer to the goal, then leave."""
    path, p = [start], start  # @line L10
    for _ in range(max_hits):  # @line L11
        hit = world.first_hit(p, goal)  # @line L12
        if hit is None:  # @line L13
            path.append(goal)
            return path, True
        _, lp, a = hit
        h = lp.point_at(a)  # @line L14
        path.append(h)
        dh = math.dist(h, goal)
        per, n = lp.perimeter, len(lp.pts)
        leave = None
        k = min(bisect.bisect_right(lp.cum, a % per) - 1, n - 1)
        for step in range(n + 1):  # @line L15
            i = (k + step) % n
            for u, q in _mline_crossings(lp, i, start, goal):
                s = lp.cum[i] + u * (lp.cum[i + 1] - lp.cum[i])
                if (step == 0 and s < a % per) or (step == n and s >= a % per):
                    continue
                off = (s - a) % per
                if off <= 1e-7 or off >= per - 1e-7:
                    continue
                if math.dist(q, goal) < dh - 1e-7 and world.can_head_to(q, goal):
                    if leave is None or off < leave[0]:
                        leave = (off, q)
            if leave is not None:
                break
        if leave is None:  # @line L16
            path += lp.walk(a, per)
            return path, False
        path += lp.walk(a, leave[0])
        p = leave[1]  # @line L17
    return path, False
