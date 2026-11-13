# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/configuration-space/. The authors are listed in prov/RXK2FN.jsonl.

"""Configuration space obstacles for a translating convex robot, and the torus of a two-link arm.

A convex polygon is a list of (x, y) vertices in counterclockwise order. The robot is given in its own
frame, with the reference point at the origin. A placement q = (qx, qy) moves every robot point p to p + q.
Coordinates may be int, float or fractions.Fraction. With Fraction all tests are exact.
"""

import math
from collections import deque


def cross(o, a, b):
    """Twice the signed area of the triangle o, a, b."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Counterclockwise convex hull without collinear points (Andrew's monotone chain)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def reflect(poly):
    """The robot reflected through its reference point, -R. A point reflection keeps the orientation."""
    return [(-x, -y) for (x, y) in poly]


def _start(poly):
    """Index of the lowest vertex, and the leftmost of those."""
    return min(range(len(poly)), key=lambda i: (poly[i][1], poly[i][0]))


def minkowski_sum(a, b):
    """Minkowski sum of two convex polygons by the merge of their edge sequences in angle order."""
    a = convex_hull(a)
    b = convex_hull(b)
    ia, ib = _start(a), _start(b)
    a = a[ia:] + a[:ia]
    b = b[ib:] + b[:ib]
    n, m = len(a), len(b)
    out = []
    i = j = 0
    while i < n or j < m:
        out.append((a[i % n][0] + b[j % m][0], a[i % n][1] + b[j % m][1]))
        ea = (a[(i + 1) % n][0] - a[i % n][0], a[(i + 1) % n][1] - a[i % n][1])
        eb = (b[(j + 1) % m][0] - b[j % m][0], b[(j + 1) % m][1] - b[j % m][1])
        turn = ea[0] * eb[1] - ea[1] * eb[0]
        if j >= m or (i < n and turn > 0):
            i += 1
        elif i >= n or turn < 0:
            j += 1
        else:
            i += 1
            j += 1
    return convex_hull(out)


def c_obstacle(obstacle, robot):
    """The C-obstacle of a convex obstacle for a translating convex robot: obstacle plus (-robot)."""
    return minkowski_sum(obstacle, reflect(robot))


def place(robot, q):
    """The robot moved to the placement q."""
    return [(x + q[0], y + q[1]) for (x, y) in robot]


def point_in_convex(p, poly):
    """True if p is in the closed convex polygon (counterclockwise)."""
    n = len(poly)
    return all(cross(poly[i], poly[(i + 1) % n], p) >= 0 for i in range(n))


def convex_intersect(a, b):
    """True if two closed convex polygons share a point. Separating axis test on all edge normals."""
    for poly in (a, b):
        n = len(poly)
        for i in range(n):
            ex = poly[(i + 1) % n][0] - poly[i][0]
            ey = poly[(i + 1) % n][1] - poly[i][1]
            ax, ay = -ey, ex
            pa = [ax * x + ay * y for (x, y) in a]
            pb = [ax * x + ay * y for (x, y) in b]
            if max(pa) < min(pb) or max(pb) < min(pa):
                return False
    return True


def collides(robot, q, obstacles):
    """Brute force: place the robot at q and test it against each obstacle in the workspace."""
    body = place(robot, q)
    return any(convex_intersect(body, ob) for ob in obstacles)


def in_c_obstacles(q, cobs):
    """True if the placement q lies in one of the C-obstacles."""
    return any(point_in_convex(q, c) for c in cobs)


def arm_points(theta1, theta2, l1, l2):
    """Joint and tip positions of a planar two-link arm with its base at the origin."""
    elbow = (l1 * math.cos(theta1), l1 * math.sin(theta1))
    tip = (elbow[0] + l2 * math.cos(theta1 + theta2), elbow[1] + l2 * math.sin(theta1 + theta2))
    return (0.0, 0.0), elbow, tip


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


def arm_free_grid(k, l1, l2, obstacles):
    """Free cells of a k by k grid on the torus of joint angles. Cell (i, j) has angles 2 pi i / k and 2 pi j / k."""
    free = [[False] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            base, elbow, tip = arm_points(2 * math.pi * i / k, 2 * math.pi * j / k, l1, l2)
            hit = any(segment_meets_convex(base, elbow, ob) or segment_meets_convex(elbow, tip, ob) for ob in obstacles)
            free[i][j] = not hit
    return free


def grid_components(free, wrap):
    """Number of 4-connected components of free cells. With wrap the grid is a torus, else a square."""
    k = len(free)
    seen = [[False] * k for _ in range(k)]
    count = 0
    for si in range(k):
        for sj in range(k):
            if not free[si][sj] or seen[si][sj]:
                continue
            count += 1
            seen[si][sj] = True
            todo = deque([(si, sj)])
            while todo:
                i, j = todo.popleft()
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    a, b = i + di, j + dj
                    if wrap:
                        a, b = a % k, b % k
                    elif not (0 <= a < k and 0 <= b < k):
                        continue
                    if free[a][b] and not seen[a][b]:
                        seen[a][b] = True
                        todo.append((a, b))
    return count
