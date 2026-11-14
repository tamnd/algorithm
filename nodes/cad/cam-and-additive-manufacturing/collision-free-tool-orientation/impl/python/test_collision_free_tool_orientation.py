# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-free-tool-orientation/. The authors are listed in prov/E9RNYT.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from collision_free_tool_orientation import (
    box_blocks,
    free_directions,
    grow,
    plan_orientations,
)


def ray_hits_box(p, d, box):
    """Reference: slab test of the ray p + t d, t > 0, against the closed box, exactly."""
    lo, hi = None, None  # the set of t, as an interval
    for k in range(3):
        m0, m1 = box[2 * k], box[2 * k + 1]
        if d[k] == 0:
            if p[k] < m0 or p[k] > m1:
                return False
            continue
        t0, t1 = F(m0 - p[k]) / d[k], F(m1 - p[k]) / d[k]
        if t0 > t1:
            t0, t1 = t1, t0
        lo = t0 if lo is None else max(lo, t0)
        hi = t1 if hi is None else min(hi, t1)
    if hi is None:
        return True  # d = 0 does not happen here
    return lo <= hi and hi > 0


def inside(p, box):
    return all(box[2 * k] <= p[k] <= box[2 * k + 1] for k in range(3))


def random_box(rng):
    x0, y0 = F(rng.randint(-12, 10), 2), F(rng.randint(-12, 10), 2)
    z0 = F(rng.choice([0, 0, rng.randint(0, 8)]), 2)
    return (x0, x0 + F(rng.randint(1, 6), 2), y0, y0 + F(rng.randint(1, 6), 2), z0, z0 + F(rng.randint(1, 10), 2))


def random_center(rng, boxes):
    while True:
        p = (F(rng.randint(-8, 8), 3), F(rng.randint(-8, 8), 3), F(rng.randint(1, 12), 3))
        if not any(inside(p, b) for b in boxes):
            return p


def test_cspace_test_equals_ray_test_random():
    rng = random.Random(11)
    for _ in range(3000):
        box = random_box(rng)
        p = random_center(rng, [box])
        q = (F(rng.randint(-20, 20), rng.randint(1, 6)), F(rng.randint(-20, 20), rng.randint(1, 6)))
        assert box_blocks(p, box, q) == ray_hits_box(p, (q[0], q[1], 1), box)


def test_cspace_test_equals_ray_test_on_edges_and_corners():
    # Directions aimed exactly at corners and edges of a box, where floats would fail.
    rng = random.Random(12)
    count = 0
    for _ in range(400):
        box = random_box(rng)
        p = random_center(rng, [box])
        for cx in box[0:2]:
            for cy in box[2:4]:
                for cz in box[4:6]:
                    if cz <= p[2]:
                        continue
                    t = cz - p[2]
                    for dx, dy in [(0, 0), (F(1, 1000), 0), (0, F(-1, 1000))]:
                        q = ((cx - p[0]) / t + dx, (cy - p[1]) / t + dy)
                        assert box_blocks(p, box, q) == ray_hits_box(p, (q[0], q[1], 1), box)
                        count += 1
    assert count > 500


def test_wall_and_post_example():
    p = (0, 0, 1)
    wall = (2, 3, -5, 5, 0, 6)
    post = (-3, -2, -1, 1, 0, 4)
    assert box_blocks(p, wall, (F(2, 5), 0))  # exactly at the top edge of the wall
    assert not box_blocks(p, wall, (F(2, 5) - F(1, 1000), 0))
    assert box_blocks(p, post, (F(-2, 3), 0))
    assert not box_blocks(p, post, (F(-2, 3) + F(1, 1000), 0))
    assert math.isclose(math.degrees(math.atan(0.4)), 21.80140948635181)
    assert math.isclose(math.degrees(math.atan(2 / 3)), 33.690067525979785)


def grid_of(k):
    return [(a, b) for a in range(-k, k + 1) for b in range(-k, k + 1)]


def test_free_set_equals_direct_ray_tests():
    rng = random.Random(13)
    grid = grid_of(4)
    step = F(1, 4)
    for _ in range(40):
        boxes = [random_box(rng) for _ in range(5)]
        p = random_center(rng, boxes)
        got = free_directions(p, boxes, grid, step)
        want = [g for g in grid if not any(ray_hits_box(p, (g[0] * step, g[1] * step, 1), b) for b in boxes)]
        assert got == want


def test_grown_boxes_keep_the_tool_clear():
    # A direction that is free for boxes grown by r keeps the whole ray at
    # least r away from the boxes (checked on samples along the ray).
    rng = random.Random(14)
    r = F(1, 2)
    grid = grid_of(4)
    step = F(1, 4)
    for _ in range(20):
        boxes = [random_box(rng) for _ in range(4)]
        grown = [grow(b, r) for b in boxes]
        p = random_center(rng, grown)
        for g in free_directions(p, grown, grid, step):
            d = (float(g[0] * step), float(g[1] * step), 1.0)
            for k in range(1, 200):
                t = k * 0.1
                x = [float(p[i]) + t * d[i] for i in range(3)]
                for b in boxes:
                    dist2 = sum(max(float(b[2 * i]) - x[i], 0.0, x[i] - float(b[2 * i + 1])) ** 2 for i in range(3))
                    assert dist2 >= float(r) ** 2 - 1e-9


def brute_force(points, boxes, grid, step, pref, w):
    free = [free_directions(p, boxes, grid, step) for p in points]
    best = None
    for choice in itertools.product(*free):
        c = sum(w * ((g[0] - pr[0]) ** 2 + (g[1] - pr[1]) ** 2) for g, pr in zip(choice, pref))
        c += sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in zip(choice, choice[1:]))
        if best is None or c < best:
            best = c
    return best


@pytest.mark.parametrize("seed", range(6))
def test_dynamic_program_equals_brute_force(seed):
    rng = random.Random(100 + seed)
    grid = grid_of(2)
    step = F(1, 2)
    while True:
        boxes = [random_box(rng) for _ in range(4)]
        points = [random_center(rng, boxes) for _ in range(3)]
        if all(free_directions(p, boxes, grid, step) for p in points):
            break
    pref = [(rng.randint(-2, 2), rng.randint(-2, 2)) for _ in points]
    w = rng.choice([1, 2, 5])
    cost, path = plan_orientations(points, boxes, grid, step, pref, w)
    assert cost == brute_force(points, boxes, grid, step, pref, w)
    # the returned path is free and has the returned cost
    for p, g in zip(points, path):
        assert g in free_directions(p, boxes, grid, step)
    c = sum(w * ((g[0] - pr[0]) ** 2 + (g[1] - pr[1]) ** 2) for g, pr in zip(path, pref))
    c += sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in zip(path, path[1:]))
    assert c == cost


def test_path_along_a_wall():
    # The example of the page: the tool moves toward a wall with a preferred lead q = (1/2, 0).
    wall = (4, 5, -10, 10, 0, 6)
    points = [(0, 0, 1), (1, 0, 1), (2, 0, 1), (3, 0, 1)]
    grid = [(a, 0) for a in range(-4, 5)]
    step = F(1, 8)
    pref = [(4, 0)] * 4
    free = [free_directions(p, [wall], grid, step) for p in points]
    assert [max(g[0] for g in f) for f in free] == [4, 4, 3, 1]
    cost, path = plan_orientations(points, [wall], grid, step, pref, w=1)
    assert path == [(4, 0), (4, 0), (3, 0), (1, 0)]
    assert cost == 0 + 0 + (1 + 1) + (9 + 4)
    # with a smaller weight on the preference, the path tilts back earlier
    cost, path = plan_orientations(points, [wall], grid, step, pref, w=F(1, 4))
    assert path == [(3, 0), (3, 0), (2, 0), (1, 0)]
    assert cost == F(1 + 1 + 4 + 9, 4) + (0 + 1 + 1)
    assert cost == brute_force(points, [wall], grid, step, pref, F(1, 4))


def test_no_free_direction():
    box = (-5, 5, -5, 5, 0, 10)
    with pytest.raises(ValueError):
        plan_orientations([(0, 0, 11)], [(-5, 5, -5, 5, 11, 20)], grid_of(1), F(1), [(0, 0)])
    assert free_directions((0, 0, 11), [box], grid_of(1), F(1)) == grid_of(1)
