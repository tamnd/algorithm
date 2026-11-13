# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rrt-star/. The authors are listed in prov/4RBAE6.jsonl.

import heapq
import math
import random
from collections import deque

from rrt_star import RRTStar, gamma_star, point_in_convex, segment_meets_convex

SIZE = 10.0


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def point_free(p, obstacles):
    return not any(point_in_convex(p, ob) for ob in obstacles)


def crosses_interior(p, q, poly):
    """True if the open segment pq passes through the interior of the convex polygon."""
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        num = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        den = (b[0] - a[0]) * dy - (b[1] - a[1]) * dx
        if den == 0:
            if num <= 0:
                return False
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t1 - t0 <= 1e-9:
        return False
    m = (p[0] + dx * (t0 + t1) / 2, p[1] + dy * (t0 + t1) / 2)
    return all((poly[(i + 1) % n][0] - poly[i][0]) * (m[1] - poly[i][1]) - (poly[(i + 1) % n][1] - poly[i][1]) * (m[0] - poly[i][0]) > 1e-9 for i in range(n))


def visibility_shortest_path(obstacles, s, g):
    """Reference: Dijkstra on the visibility graph of the start, the goal and the obstacle vertices."""
    pts = [s, g] + [v for ob in obstacles for v in ob]
    dist = [math.inf] * len(pts)
    dist[0] = 0.0
    heap = [(0.0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v in range(len(pts)):
            if v != u and not any(crosses_interior(pts[u], pts[v], ob) for ob in obstacles):
                nd = d + math.dist(pts[u], pts[v])
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
    return dist[1]


def grid_path_exists(obstacles, start, goal, h=0.2):
    """Reference: breadth-first search on the grid of cell centers, with exact segment tests."""
    n = int(round(SIZE / h))

    def seg_free(p, q):
        return not any(segment_meets_convex(p, q, ob) for ob in obstacles)

    def pt(i, j):
        return ((i + 0.5) * h, (j + 0.5) * h)

    def attach(p):
        i, j = min(int(p[0] / h), n - 1), min(int(p[1] / h), n - 1)
        return (i, j) if seg_free(p, pt(i, j)) else None

    s, g = attach(start), attach(goal)
    if s is None or g is None:
        return False
    seen, todo = {s}, deque([s])
    while todo:
        i, j = todo.popleft()
        if (i, j) == g:
            return True
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n and (a, b) not in seen and seg_free(pt(i, j), pt(a, b)):
                seen.add((a, b))
                todo.append((a, b))
    return False


def assert_segments_free(segments, obstacles, step=0.01):
    for p, q in segments:
        k = max(1, int(math.dist(p, q) / step))
        for t in range(k + 1):
            x = (p[0] + (q[0] - p[0]) * t / k, p[1] + (q[1] - p[1]) * t / k)
            assert point_free(x, obstacles), (p, q, x)


BLOCK = [rect(4, 3, 6, 7)]
START, GOAL = (1.0, 5.0), (9.0, 5.0)


def test_gamma_star_in_the_plane():
    assert abs(gamma_star(1.0) - math.sqrt(3 / math.pi)) < 1e-12


def test_cost_never_increases_and_approaches_the_optimum():
    c_star = visibility_shortest_path(BLOCK, START, GOAL)
    assert abs(c_star - (2 + 2 * math.sqrt(13))) < 1e-9
    tree = RRTStar(SIZE, SIZE, BLOCK, START, random.Random(0))
    last = math.inf
    for it in range(1, 4001):
        tree.step()
        if it % 50 == 0:
            c = tree.best_cost(GOAL, 1.0)
            assert c <= last + 1e-12
            last = c
    assert c_star - 1e-9 <= last <= 1.02 * c_star
    for i in range(1, len(tree.nodes)):
        p = tree.parent[i]
        assert abs(tree.cost[i] - tree.cost[p] - math.dist(tree.nodes[i], tree.nodes[p])) < 1e-9
    assert_segments_free(tree.edges(), BLOCK)


def test_two_obstacles_against_the_visibility_graph():
    obs = [rect(3, 0.5, 4, 6), [(6, 4), (7.5, 4), (7, 9.5)]]
    s, g = (1.0, 2.0), (9.0, 6.0)
    c_star = visibility_shortest_path(obs, s, g)
    tree = RRTStar(SIZE, SIZE, obs, s, random.Random(1))
    for _ in range(3000):
        tree.step()
    c = tree.best_cost(g, 1.0)
    assert c_star - 1e-9 <= c <= 1.05 * c_star
    assert_segments_free(tree.edges(), obs)


def test_finds_a_path_exactly_when_grid_search_does():
    walls = {True: [rect(4.5, 0.0, 5.5, 4.0), rect(4.5, 5.0, 5.5, SIZE)], False: [rect(4.5, 0.0, 5.5, 4.2), rect(4.4, 4.0, 5.6, SIZE)]}
    for gap, obs in walls.items():
        exists = grid_path_exists(obs, START, GOAL)
        assert exists == gap
        tree = RRTStar(SIZE, SIZE, obs, START, random.Random(7))
        for _ in range(1500):
            tree.step()
        assert (tree.best_cost(GOAL, 1.0) < math.inf) == exists
        assert_segments_free(tree.edges(), obs)
