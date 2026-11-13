# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-roadmap/. The authors are listed in prov/S30SPN.jsonl.

import math
import random
from collections import deque

from probabilistic_roadmap import Roadmap, point_in_convex, segment_meets_convex

SIZE = 10.0


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def wall_map(rng, gap):
    """A wall across the square at x near 5, made of rectangles, with one gap of width 1 or none."""
    obs = []
    cut = rng.uniform(2.0, 7.0)
    if gap:
        obs.append(rect(4.5, 0.0, 5.5, cut))
        obs.append(rect(4.5, cut + 1.0, 5.5, SIZE))
    else:
        obs.append(rect(4.5, 0.0, 5.5, cut + 0.2))
        obs.append(rect(4.4, cut, 5.6, SIZE))
    obs.append([(1.5, 6.0), (3.0, 6.5), (2.0, 8.0)])
    obs.append([(7.0, 2.0), (8.5, 2.5), (8.0, 4.0), (6.8, 3.2)])
    return obs


def point_free(p, obstacles):
    return not any(point_in_convex(p, ob) for ob in obstacles)


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


def assert_segments_free(segments, obstacles, step=0.002):
    for p, q in segments:
        k = max(1, int(math.dist(p, q) / step))
        for t in range(k + 1):
            x = (p[0] + (q[0] - p[0]) * t / k, p[1] + (q[1] - p[1]) * t / k)
            assert point_free(x, obstacles), (p, q, x)


START, GOAL = (1.0, 1.0), (9.0, 9.0)


def test_every_roadmap_edge_is_collision_free():
    rng = random.Random(3)
    obs = wall_map(rng, gap=True)
    for every_pair in (False, True):
        rm = Roadmap(SIZE, SIZE, obs, 150, 1.5, random.Random(17), every_pair=every_pair)
        assert_segments_free(rm.edges(), obs)


def test_finds_a_path_exactly_when_grid_search_does():
    rng = random.Random(8)
    for trial in range(6):
        obs = wall_map(rng, gap=trial % 2 == 0)
        exists = grid_path_exists(obs, START, GOAL)
        assert exists == (trial % 2 == 0)
        rm = Roadmap(SIZE, SIZE, obs, 500, 1.5, random.Random(100 + trial))
        path = rm.query(START, GOAL)
        assert (path is not None) == exists
        if path is not None:
            assert path[0] == START and path[-1] == GOAL
            assert_segments_free(list(zip(path, path[1:])), obs)


def test_forest_mode_builds_a_forest():
    obs = wall_map(random.Random(3), gap=True)
    rm = Roadmap(SIZE, SIZE, obs, 200, 1.5, random.Random(5))
    edges = len(rm.edges())
    roots = len({rm.sets.find(i) for i in range(len(rm.nodes))})
    assert edges == len(rm.nodes) - roots
    full = Roadmap(SIZE, SIZE, obs, 200, 1.5, random.Random(5), every_pair=True)
    assert len(full.edges()) > edges
