# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-shortcut-path-smoothing/. The authors are listed in prov/N97VRM.jsonl.
"""Tests: the path stays free, the length never grows, and it never beats the true shortest path."""

import heapq
import math
import random

from random_shortcut_path_smoothing import path_free, path_length, segment_free, shortcut


def shortest_length(start, goal, obstacles):
    """Exact shortest path length by Dijkstra on the visibility graph of the rectangle corners."""
    nodes = [start, goal]
    for x0, y0, x1, y1 in obstacles:
        nodes += [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    dist = [math.inf] * len(nodes)
    dist[0] = 0.0
    heap = [(0.0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == 1:
            return d
        for v in range(len(nodes)):
            if v != u and segment_free(nodes[u], nodes[v], obstacles):
                nd = d + math.dist(nodes[u], nodes[v])
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
    return math.inf


def staircase(start, goal, rng, n):
    """A free but wasteful path: a random walk of waypoints, kept only where free."""
    return [start] + [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)] + [goal]


def test_segment_test():
    box = [(2, 2, 4, 4)]
    assert not segment_free((0, 3), (6, 3), box)
    assert segment_free((0, 2), (6, 2), box)  # along the border
    assert segment_free((0, 0), (2, 2), box)  # ends at a corner
    assert not segment_free((2, 2), (4, 4), box)  # the diagonal crosses the interior
    assert segment_free((5, 0), (5, 9), box)
    assert not segment_free((3, 3), (3, 3), box)  # a point inside


def test_one_wall():
    walls = [(4, -9, 6, 8)]
    path = [(0, 0), (0, 9), (10, 9), (10, 0)]
    assert path_free(path, walls)
    out = shortcut(path, walls, 300, random.Random(1))
    assert out[0] == (0, 0) and out[-1] == (10, 0)
    assert path_free(out, walls)
    best = shortest_length((0, 0), (10, 0), walls)
    assert abs(best - (2 * math.hypot(4, 8) + 2)) < 1e-12
    assert best - 1e-9 <= path_length(out) <= path_length(path)
    # Measured with this seed: 28 drops to about 20.30 after 300 tries, 2.1 percent above the optimum.
    assert path_length(out) <= 1.03 * best


def test_random_scenes():
    rng = random.Random(2)
    for _ in range(12):
        obstacles = []
        for _ in range(4):
            x, y = rng.uniform(1, 8), rng.uniform(1, 8)
            obstacles.append((x, y, x + rng.uniform(0.5, 2), y + rng.uniform(0.5, 2)))
        start, goal = (0.0, 0.0), (10.0, 10.0)
        # Build a free path by sampling random free waypoint chains.
        path = None
        for _ in range(200):
            cand = staircase(start, goal, rng, 6)
            if path_free(cand, obstacles):
                path = cand
                break
        if path is None:
            continue
        lengths = [path_length(path)]
        cur = path
        for _ in range(10):
            before = len(cur)
            nxt = shortcut(cur, obstacles, 5, rng)
            assert len(nxt) <= before + 5  # at most one new vertex per iteration
            assert path_free(nxt, obstacles)
            assert nxt[0] == start and nxt[-1] == goal
            lengths.append(path_length(nxt))
            cur = nxt
        assert all(b <= a + 1e-9 for a, b in zip(lengths, lengths[1:]))
        assert lengths[-1] >= shortest_length(start, goal, obstacles) - 1e-9


def test_free_line_collapses():
    rng = random.Random(3)
    path = [(0, 0), (1, 5), (2, -3), (3, 4), (4, 0)]
    out = shortcut(path, [], 200, rng)
    # Close to the straight line, but small detours near the ends shrink slowly.
    assert 4 <= path_length(out) < 4.02


def test_same_seed_same_result():
    walls = [(4, -9, 6, 8)]
    path = [(0, 0), (0, 9), (10, 9), (10, 0)]
    assert shortcut(path, walls, 50, random.Random(9)) == shortcut(path, walls, 50, random.Random(9))
