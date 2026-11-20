# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-method/. The authors are listed in prov/2Q63VY.jsonl.
import math
import random

import pytest

from morris_method import grid_effects, morris, trajectory


def ishigami_unit(u):
    x = [-math.pi + 2 * math.pi * v for v in u]
    return math.sin(x[0]) + 7 * math.sin(x[1]) ** 2 + 0.1 * x[2] ** 4 * math.sin(x[0])


def test_trajectory_moves_each_coordinate_once_on_the_grid():
    rng = random.Random(4)
    p, d = 6, 5
    delta = p / (2 * (p - 1))
    for _ in range(50):
        points, order = trajectory(d, p, rng)
        assert len(points) == d + 1 and sorted(order) == list(range(d))
        for k, i in enumerate(order):
            diff = [b - a for a, b in zip(points[k], points[k + 1])]
            assert all(abs(diff[j]) < 1e-12 for j in range(d) if j != i)
            assert abs(abs(diff[i]) - delta) < 1e-12
        for pt in points:
            for v in pt:
                assert -1e-12 <= v <= 1 + 1e-12
                assert abs(v * (p - 1) - round(v * (p - 1))) < 1e-9


def test_hand_example():
    # f = x1 + x1 x2 with p = 4: EE_1 = 1 + x2 and EE_2 = x1
    f = lambda x: x[0] + x[0] * x[1]  # noqa: E731
    e1 = grid_effects(f, 2, 4, 0)
    e2 = grid_effects(f, 2, 4, 1)
    assert abs(sum(e1) / len(e1) - 1.5) < 1e-12
    assert abs(sum(e2) / len(e2) - 0.5) < 1e-12


def test_linear_model_gives_the_coefficients_with_zero_spread():
    c = [2.0, -1.0, 0.5, 0.0]
    f = lambda x: sum(ci * xi for ci, xi in zip(c, x))  # noqa: E731
    res = morris(f, 4, 12, 4, random.Random(7))
    assert res["runs"] == 12 * 5
    for i in range(4):
        assert abs(res["mu"][i] - c[i]) < 1e-12
        assert abs(res["mu_star"][i] - abs(c[i])) < 1e-12
        assert res["sigma"][i] < 1e-12


def test_mu_star_matches_the_grid_enumeration():
    # each elementary effect of a random trajectory is a uniform draw from the grid list
    rng = random.Random(1991)
    r = 1500
    res = morris(ishigami_unit, 3, r, 4, rng)
    for i in range(3):
        grid = [abs(v) for v in grid_effects(ishigami_unit, 3, 4, i)]
        exact = sum(grid) / len(grid)
        spread = math.sqrt(sum((v - exact) ** 2 for v in grid) / len(grid))
        assert abs(res["mu_star"][i] - exact) < 4 * spread / math.sqrt(r) + 1e-12
    assert abs(sum(abs(v) for v in grid_effects(ishigami_unit, 3, 4, 1)) / 32 - 7.875) < 1e-12


def test_odd_number_of_levels_is_rejected():
    with pytest.raises(ValueError):
        trajectory(3, 5, random.Random(0))
