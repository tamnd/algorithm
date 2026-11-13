# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potential-field-method/. The authors are listed in prov/6TE8NF.jsonl.

import math
import random

from potential_field_method import Field, descend, distance_to_convex, inside_convex


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


CUP = [rect(3, 5, 7, 5.5), rect(3, 3, 3.5, 5.5), rect(6.5, 3, 7, 5.5)]


def path_is_free(path, obstacles):
    for p, q in zip(path, path[1:]):
        for t in range(11):
            x = (p[0] + (q[0] - p[0]) * t / 10, p[1] + (q[1] - p[1]) * t / 10)
            if any(inside_convex(x, ob) for ob in obstacles):
                return False
    return True


def test_reaches_goal_among_two_obstacles():
    obs = [rect(3, 2, 4, 4), [(6, 5), (8, 5.5), (6.5, 7)]]
    path, status = descend(Field((9, 9), obs), (1, 1))
    assert status == "goal"
    assert math.dist(path[-1], (9, 9)) < 1e-3
    assert path_is_free(path, obs)


def test_start_beside_the_cup_reaches_goal():
    path, status = descend(Field((5, 8), CUP), (1, 1))
    assert status == "goal"
    assert path_is_free(path, CUP)


def test_cup_traps_the_robot_in_a_true_local_minimum():
    field = Field((5, 8), CUP)
    path, status = descend(field, (5.0, 1.0))
    assert status == "stuck"
    q = path[-1]
    assert math.dist(q, (5, 8)) > 3
    # The analytic minimum on the axis x = 5 solves 8 - y = (1/r - 1)/r^2 with r = 5 - y.
    lo, hi = 3.5, 4.99
    for _ in range(100):
        y = (lo + hi) / 2
        r = 5 - y
        if -(8 - y) + (1 / r - 1) / r ** 2 > 0:
            hi = y
        else:
            lo = y
    assert abs(q[0] - 5) < 1e-6 and abs(q[1] - y) < 1e-4
    u = field.potential(q)
    rng = random.Random(2024)
    for _ in range(2000):
        r = rng.uniform(1e-3, 0.3)
        t = rng.uniform(0, 2 * math.pi)
        assert field.potential((q[0] + r * math.cos(t), q[1] + r * math.sin(t))) > u
    assert path_is_free(path, CUP)


def test_gradient_matches_finite_differences():
    field = Field((5, 8), CUP)
    rng = random.Random(9)
    h = 1e-6
    for _ in range(200):
        q = (rng.uniform(0, 10), rng.uniform(0, 10))
        if min(distance_to_convex(q, ob)[0] for ob in CUP) < 0.05:
            continue
        gx, gy = field.gradient(q)
        fx = (field.potential((q[0] + h, q[1])) - field.potential((q[0] - h, q[1]))) / (2 * h)
        fy = (field.potential((q[0], q[1] + h)) - field.potential((q[0], q[1] - h))) / (2 * h)
        assert abs(gx - fx) < 1e-4 * max(1, abs(fx)) and abs(gy - fy) < 1e-4 * max(1, abs(fy))
