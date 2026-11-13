# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bug-algorithms/. The authors are listed in prov/JJWB8E.jsonl.

import math
import random
from collections import deque

from bug_algorithms import World, bug1, bug2, path_length


def hull(points):
    pts = sorted(set(points))
    out = []
    for seq in (pts, pts[::-1]):
        part = []
        for p in seq:
            while len(part) >= 2 and (part[-1][0] - part[-2][0]) * (p[1] - part[-2][1]) - (part[-1][1] - part[-2][1]) * (p[0] - part[-2][0]) <= 0:
                part.pop()
            part.append(p)
        out += part[:-1]
    return out


def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def poly_gap(a, b):
    """Distance of two convex polygons, or 0 if a vertex of one is inside the other."""
    for p, q in ((a, b), (b, a)):
        for v in p:
            if all((q[(i + 1) % len(q)][0] - q[i][0]) * (v[1] - q[i][1]) - (q[(i + 1) % len(q)][1] - q[i][1]) * (v[0] - q[i][0]) >= 0 for i in range(len(q))):
                return 0.0
    return min(seg_dist(v, q[i], q[(i + 1) % len(q)]) for p, q in ((a, b), (b, a)) for v in p for i in range(len(q)))


def random_map(rng, count):
    polys = []
    while len(polys) < count:
        cx, cy, r = rng.uniform(1.5, 8.5), rng.uniform(1.5, 8.5), rng.uniform(0.5, 1.6)
        blob = hull([(cx + r * math.cos(t), cy + r * math.sin(t)) for t in (rng.uniform(0, 2 * math.pi) for _ in range(7))])
        if len(blob) >= 3 and all(poly_gap(blob, p) > 0.3 for p in polys):
            polys.append(blob)
    return [[p] for p in polys]


def clear_point(rng, world):
    while True:
        p = (rng.uniform(0, 10), rng.uniform(0, 10))
        if not world.blocked(p) and world.boundary_distance(p) > 0.2:
            return p


RING_OUTER = [(3.0, 3.0), (7.0, 3.0), (7.0, 7.0), (3.0, 7.0)]
RING_HOLE = [(4.0, 4.0), (4.0, 6.0), (6.0, 6.0), (6.0, 4.0)]
U_SHAPE = [(3.0, 2.0), (7.0, 2.0), (7.0, 8.0), (3.0, 8.0), (3.0, 7.0), (6.0, 7.0), (6.0, 3.0), (3.0, 3.0)]


def grid_reachable(world, s, g, lo=-1.0, hi=11.0, h=0.1):
    """Reference: flood fill over the free points of a grid, with s and g snapped to the grid."""
    n = int(round((hi - lo) / h)) + 1

    def node(p):
        return (round((p[0] - lo) / h), round((p[1] - lo) / h))

    def free(i, j):
        return not world.blocked((lo + i * h, lo + j * h)) and world.boundary_distance((lo + i * h, lo + j * h)) > h

    a, b = node(s), node(g)
    seen, todo = {a}, deque([a])
    while todo:
        i, j = todo.popleft()
        if (i, j) == b:
            return True
        for c in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= c[0] < n and 0 <= c[1] < n and c not in seen and (c == b or free(*c)):
                seen.add(c)
                todo.append(c)
    return False


def assert_free(world, path, step=0.005):
    for p, q in zip(path, path[1:]):
        k = max(1, int(math.dist(p, q) / step))
        for t in range(k + 1):
            x = (p[0] + (q[0] - p[0]) * t / k, p[1] + (q[1] - p[1]) * t / k)
            assert not world.blocked(x), x


def mline_crossings(world, s, g):
    """Number of points where the segment s g meets the boundary of each obstacle."""
    counts = {}
    d = (g[0] - s[0], g[1] - s[1])
    for lp in world.loops:
        for i in range(len(lp.pts)):
            a, b = lp.edge(i)
            e = (b[0] - a[0], b[1] - a[1])
            den = d[0] * e[1] - d[1] * e[0]
            w = (a[0] - s[0], a[1] - s[1])
            if den != 0:
                t = (w[0] * e[1] - w[1] * e[0]) / den
                u = (w[0] * d[1] - w[1] * d[0]) / den
                if 0 <= t <= 1 and 0 <= u < 1:
                    counts[lp.obstacle] = counts.get(lp.obstacle, 0) + 1
    return counts


def check_bounds(world, s, g, p1, p2):
    d = math.dist(s, g)
    total = sum(world.perimeter(i) for i in range(len(world.obstacles)))
    assert path_length(p1) <= d + 1.5 * total + 1e-9
    n = mline_crossings(world, s, g)
    assert path_length(p2) <= d + 0.5 * sum(n[i] * world.perimeter(i) for i in n) + 1e-9


def test_random_maps_reach_the_goal_within_the_bounds():
    rng = random.Random(42)
    for _ in range(12):
        world = World(random_map(rng, rng.randint(2, 6)))
        s, g = clear_point(rng, world), clear_point(rng, world)
        assert grid_reachable(world, s, g)
        p1, ok1 = bug1(world, s, g)
        p2, ok2 = bug2(world, s, g)
        assert ok1 and ok2
        assert p1[-1] == g and p2[-1] == g
        assert_free(world, p1)
        assert_free(world, p2)
        check_bounds(world, s, g, p1, p2)


def test_u_shaped_obstacle():
    world = World([[U_SHAPE]])
    s, g = (4.51, 5.13), (9.02, 5.37)
    assert grid_reachable(world, s, g)
    for planner in (bug1, bug2):
        path, ok = planner(world, s, g)
        assert ok and path[-1] == g
        assert_free(world, path)
    check_bounds(world, s, g, bug1(world, s, g)[0], bug2(world, s, g)[0])


def test_goal_inside_a_ring_is_reported_unreachable():
    world = World([[RING_OUTER, RING_HOLE]])
    s, g = (0.13, 0.41), (5.07, 4.89)
    assert not grid_reachable(world, s, g)
    for planner in (bug1, bug2):
        path, ok = planner(world, s, g)
        assert not ok
        assert_free(world, path)


def test_start_inside_a_ring_is_reported_unreachable():
    world = World([[RING_OUTER, RING_HOLE], [[(8.0, 8.0), (9.0, 8.0), (8.5, 9.0)]]])
    s, g = (5.07, 4.89), (9.6, 9.7)
    assert not grid_reachable(world, s, g)
    for planner in (bug1, bug2):
        path, ok = planner(world, s, g)
        assert not ok
        assert_free(world, path)
