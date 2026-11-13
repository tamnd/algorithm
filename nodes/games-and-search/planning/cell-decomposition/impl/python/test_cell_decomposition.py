# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cell-decomposition/. The authors are listed in prov/9HY0M9.jsonl.

import math
import random
from collections import deque

from cell_decomposition import (
    ApproximateDecomposition,
    ExactDecomposition,
    point_free,
    point_in_convex,
    segment_meets_convex,
)

SIZE = 10.0


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


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def poly_dist(a, b):
    """Distance of two disjoint convex polygons: the closest pair is a vertex and an edge."""
    best = math.inf
    for p, q in ((a, b), (b, a)):
        for v in p:
            for i in range(len(q)):
                best = min(best, seg_dist(v, q[i], q[(i + 1) % len(q)]))
    return best


def overlap(a, b):
    """True if two closed convex polygons share a point: an edge of one meets the other."""
    return any(segment_meets_convex(a[i], a[(i + 1) % len(a)], b) for i in range(len(a))) or point_in_convex(b[0], a)


def make_map(rng, gap, enclose):
    """A wall of overlapping rectangles at x near 5, with a gap or not, and random convex blobs.

    Two obstacles either overlap or stay at least 0.5 apart, so every passage is at least 0.5 wide.
    """
    obs = []
    y = 0.0
    gap_at = rng.uniform(2.0, 7.0) if gap else None
    while y < SIZE:
        top = min(SIZE, y + rng.uniform(1.0, 2.5))
        if gap_at is not None and y <= gap_at < top:
            obs.append(rect(4.6 + rng.uniform(-0.2, 0.2), y, 5.4, gap_at))
            y = gap_at + rng.uniform(0.8, 1.2)
            gap_at = None
            continue
        obs.append(rect(4.6 + rng.uniform(-0.2, 0.2), max(0.0, y - 0.3), 5.4 + rng.uniform(-0.2, 0.2), top))
        y = top
    if enclose:
        obs += [rect(0.5, 0.5, 3.0, 1.0), rect(2.5, 0.5, 3.0, 3.0), rect(0.5, 2.5, 3.0, 3.0), rect(0.5, 0.5, 1.0, 3.0)]
    tries = 0
    while tries < 400 and len(obs) < 14:
        tries += 1
        cx, cy, r = rng.uniform(1.5, 8.5), rng.uniform(1.5, 8.5), rng.uniform(0.4, 1.0)
        pts = [(cx + r * math.cos(t), cy + r * math.sin(t)) for t in sorted(rng.uniform(0, 2 * math.pi) for _ in range(6))]
        blob = hull(pts)
        if len(blob) < 3:
            continue
        if any(not overlap(blob, ob) and poly_dist(blob, ob) < 0.5 for ob in obs):
            continue
        obs.append(blob)
    return obs


def grid_path_exists(obstacles, start, goal, h=0.1):
    """Reference: breadth-first search on the grid of cell centers with step h."""
    n = int(round(SIZE / h))
    boxes = [(min(x for x, _ in ob), min(y for _, y in ob), max(x for x, _ in ob), max(y for _, y in ob), ob) for ob in obstacles]

    def seg_free(p, q):
        x0, x1 = min(p[0], q[0]), max(p[0], q[0])
        y0, y1 = min(p[1], q[1]), max(p[1], q[1])
        return not any(bx0 <= x1 and x0 <= bx1 and by0 <= y1 and y0 <= by1 and segment_meets_convex(p, q, ob) for bx0, by0, bx1, by1, ob in boxes)

    def pt(i, j):
        return ((i + 0.5) * h, (j + 0.5) * h)

    free = [[point_free(pt(i, j), obstacles) for j in range(n)] for i in range(n)]

    def attach(p):
        i, j = min(int(p[0] / h), n - 1), min(int(p[1] / h), n - 1)
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                if 0 <= a < n and 0 <= b < n and free[a][b] and seg_free(p, pt(a, b)):
                    return (a, b)
        return None

    s, g = attach(start), attach(goal)
    if s is None or g is None:
        return False
    seen = {s}
    todo = deque([s])
    while todo:
        i, j = todo.popleft()
        if (i, j) == g:
            return True
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n and free[a][b] and (a, b) not in seen and seg_free(pt(i, j), pt(a, b)):
                seen.add((a, b))
                todo.append((a, b))
    return False


def assert_path_free(path, obstacles, start, goal, step=1e-3):
    assert path[0] == start and path[-1] == goal
    for p, q in zip(path, path[1:]):
        k = max(1, int(math.dist(p, q) / step))
        for t in range(k + 1):
            x = (p[0] + (q[0] - p[0]) * t / k, p[1] + (q[1] - p[1]) * t / k)
            assert point_free(x, obstacles), (p, q, x)


def test_exact_decomposition_agrees_with_grid_search():
    rng = random.Random(11)
    start, goal = (2.0, 1.75), (8.5, 8.0)
    found = missed = 0
    for trial in range(8):
        obs = make_map(rng, gap=trial % 2 == 0, enclose=trial % 4 == 3)
        if not (point_free(start, obs) and point_free(goal, obs)):
            continue
        dec = ExactDecomposition(SIZE, SIZE, obs)
        path = dec.plan(start, goal)
        assert (path is not None) == grid_path_exists(obs, start, goal)
        if path is None:
            missed += 1
        else:
            found += 1
            assert_path_free(path, obs, start, goal)
    assert found >= 2 and missed >= 2


def test_approximate_decomposition_is_sound_and_finds_wide_passages():
    rng = random.Random(5)
    start, goal = (2.0, 1.75), (8.5, 8.0)
    for trial in range(4):
        obs = make_map(rng, gap=trial % 2 == 0, enclose=False)
        if not (point_free(start, obs) and point_free(goal, obs)):
            continue
        quad = ApproximateDecomposition(SIZE, obs, SIZE / 64)
        path = quad.plan(start, goal)
        exact = ExactDecomposition(SIZE, SIZE, obs).plan(start, goal)
        if path is not None:
            assert exact is not None
            assert_path_free(path, obs, start, goal)
        assert (path is not None) == (exact is not None)


def test_single_square_obstacle_cells():
    obs = [rect(4.0, 4.0, 6.0, 6.0)]
    dec = ExactDecomposition(SIZE, SIZE, obs)
    assert dec.xs == [0.0, 4.0, 6.0, 10.0]
    assert len(dec.slab) == 4
    path = dec.plan((1.0, 5.0), (9.0, 5.0))
    assert_path_free(path, obs, (1.0, 5.0), (9.0, 5.0))
