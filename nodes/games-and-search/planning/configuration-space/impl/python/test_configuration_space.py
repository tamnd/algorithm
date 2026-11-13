# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/configuration-space/. The authors are listed in prov/RXK2FN.jsonl.

import random
from fractions import Fraction

from configuration_space import (
    arm_free_grid,
    c_obstacle,
    collides,
    convex_hull,
    grid_components,
    in_c_obstacles,
    minkowski_sum,
    point_in_convex,
)


def random_convex(rng, cx, cy, size, k):
    pts = [(cx + rng.randint(-size, size), cy + rng.randint(-size, size)) for _ in range(k)]
    hull = convex_hull(pts)
    while len(hull) < 3:
        pts.append((cx + rng.randint(-size, size), cy + rng.randint(-size, size)))
        hull = convex_hull(pts)
    return hull


def grid(lo, hi, steps):
    h = Fraction(hi - lo, steps)
    return [lo + i * h for i in range(steps + 1)]


def test_square_robot_triangle_obstacle():
    robot = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tri = [(3, 2), (5, 2), (4, 4)]
    assert c_obstacle(tri, robot) == [(2, 1), (5, 1), (5, 2), (4, 4), (3, 4), (2, 2)]


def test_minkowski_sum_equals_hull_of_pairwise_sums():
    rng = random.Random(1)
    for _ in range(200):
        a = random_convex(rng, 0, 0, 6, rng.randint(3, 9))
        b = random_convex(rng, 0, 0, 6, rng.randint(3, 9))
        ref = convex_hull([(p[0] + q[0], p[1] + q[1]) for p in a for q in b])
        assert minkowski_sum(a, b) == ref


def test_c_obstacles_match_brute_force_on_a_grid():
    rng = random.Random(7)
    xs = grid(-2, 12, 56)
    for _ in range(4):
        robot = random_convex(rng, 0, 0, 2, rng.randint(3, 6))
        obstacles = [random_convex(rng, rng.randint(2, 8), rng.randint(2, 8), 2, rng.randint(3, 6)) for _ in range(3)]
        cobs = [c_obstacle(ob, robot) for ob in obstacles]
        for x in xs:
            for y in xs:
                q = (x, y)
                assert in_c_obstacles(q, cobs) == collides(robot, q, obstacles)


def test_reference_point_inside_robot_means_obstacle_inside_c_obstacle():
    rng = random.Random(3)
    for _ in range(50):
        robot = random_convex(rng, 0, 0, 3, 6)
        if not point_in_convex((0, 0), robot):
            continue
        ob = random_convex(rng, 5, 5, 3, 6)
        cob = c_obstacle(ob, robot)
        assert all(point_in_convex(v, cob) for v in ob)


def test_arm_free_space_is_one_piece_on_the_torus():
    obstacles = [[(0.6, 0.6), (1.6, 0.6), (1.6, 1.6), (0.6, 1.6)]]
    free = arm_free_grid(72, 1.0, 1.0, obstacles)
    assert sum(map(sum, free)) == 4498
    assert grid_components(free, wrap=True) == 1
    assert grid_components(free, wrap=False) == 3
