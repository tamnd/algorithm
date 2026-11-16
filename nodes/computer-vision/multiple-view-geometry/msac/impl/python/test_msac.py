# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/msac/. The authors are listed in prov/S7R7BT.jsonl.

import itertools
import math
import random

from msac import fit_line_lsq, line_through, msac, msac_cost, point_line_distance, ransac_trials

EXAMPLE = [(0, 0), (1, 0.1), (2, 0), (3, 0.1), (4, 0), (1, 2), (3, -2)]


def planted(rng, n_in, n_out, a=0.5, b=2.0, sigma=0.0, gap=1.0):
    pts = []
    for _ in range(n_in):
        x = rng.uniform(0.0, 10.0)
        pts.append((x, a * x + b + (rng.gauss(0.0, sigma) if sigma else 0.0)))
    true_line = line_through([(0.0, b), (1.0, a + b)])
    while len(pts) < n_in + n_out:
        q = (rng.uniform(0.0, 10.0), rng.uniform(-5.0, 12.0))
        if point_line_distance(true_line, q) > gap:
            pts.append(q)
    return pts, true_line


def line_angle(l1, l2):
    return math.atan2(abs(l1[0] * l2[1] - l1[1] * l2[0]), abs(l1[0] * l2[0] + l1[1] * l2[1]))


def test_example_costs():
    y0 = line_through([(0, 0), (4, 0)])
    y01 = line_through([(1, 0.1), (3, 0.1)])
    assert abs(msac_cost(y0, EXAMPLE, 0.25) - 0.145) < 1e-12
    assert abs(msac_cost(y01, EXAMPLE, 0.25) - 0.155) < 1e-12
    # both lines have the same 5 inliers, so RANSAC cannot tell them apart
    for line in (y0, y01):
        assert [i for i, x in enumerate(EXAMPLE) if point_line_distance(line, x) <= 0.25] == [0, 1, 2, 3, 4]
    assert ransac_trials(0.99, 5 / 7, 2) == 7


def test_example_run():
    model, inl, cost, _ = msac(EXAMPLE, 0.25, random.Random(1))
    assert inl == [0, 1, 2, 3, 4]
    assert abs(cost - 0.145) < 1e-12
    assert abs(model[0]) < 1e-12 and abs(model[1] - 1.0) < 1e-12 and abs(model[2] + 0.04) < 1e-12
    best = min(msac_cost(line_through(pq), EXAMPLE, 0.25)
               for pq in itertools.combinations(EXAMPLE, 2) if line_through(pq) is not None)
    assert abs(cost - best) < 1e-12


def test_cost_is_least_among_sampled_models():
    for seed in range(4):
        data, _ = planted(random.Random(seed), 30, 30, sigma=0.05, gap=0.5)
        seen = []

        def solver(sample):
            line = line_through(sample)
            if line is not None:
                seen.append(msac_cost(line, data, 0.15))
            return line

        _, _, cost, t = msac(data, 0.15, random.Random(50 + seed), fit_minimal=solver)
        assert len(seen) == t
        assert cost == min(seen)


def test_outliers_are_truncated():
    line = line_through([(0, 0), (1, 0)])
    near = [(0, 0), (1, 0), (2, 5)]
    far = [(0, 0), (1, 0), (2, 500)]
    assert msac_cost(line, near, 0.5) == msac_cost(line, far, 0.5) == 0.25


def test_planted_line():
    data, true_line = planted(random.Random(3), 50, 50, sigma=0.05, gap=0.5)
    model, inl, _, _ = msac(data, 0.15, random.Random(5))
    assert all(i < 50 for i in inl) and len(inl) >= 49
    assert line_angle(model, true_line) < math.radians(1.0)


def test_exact_data():
    data, true_line = planted(random.Random(7), 40, 60)
    model, inl, cost, _ = msac(data, 0.05, random.Random(2))
    assert inl == list(range(40))
    assert abs(cost - 60 * 0.05 ** 2) < 1e-9
    assert line_angle(model, true_line) < 1e-9


def test_degenerate():
    assert msac([(1.0, 1.0)] * 4, 0.1, random.Random(0), max_trials=10)[:3] == (None, [], math.inf)
    assert msac([(0.0, 0.0)], 0.1, random.Random(0)) == (None, [], math.inf, 0)
    assert fit_line_lsq([(1.0, 1.0)]) is None
