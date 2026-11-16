# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preemptive-ransac/. The authors are listed in prov/86C9V2.jsonl.

import math
import random

from preemptive_ransac import (line_through, make_hypotheses, point_line_distance, preemption,
                               preemptive_ransac, total_scorings)

EXAMPLE = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (0, 4), (1, 3), (4, 0)]
PAIRS = [((0, 0), (3, 3)), ((0, 4), (4, 0)), ((1, 1), (1, 3)), ((0, 0), (4, 0)),
         ((0, 4), (4, 4)), ((1, 3), (3, 3)), ((0, 0), (1, 3)), ((1, 1), (0, 4))]
HYPS = [line_through(p) for p in PAIRS]


def full_cost(h, data, thr):
    return sum(min(point_line_distance(h, x) ** 2, thr * thr) for x in data)


def planted(rng, n_in, n_out, sigma=0.05):
    true_line = line_through([(0.0, 2.0), (1.0, 2.5)])
    pts = []
    for _ in range(n_in):
        x = rng.uniform(0.0, 10.0)
        pts.append((x, 0.5 * x + 2.0 + rng.gauss(0.0, sigma)))
    while len(pts) < n_in + n_out:
        q = (rng.uniform(0.0, 10.0), rng.uniform(-5.0, 12.0))
        if point_line_distance(true_line, q) > 0.5:
            pts.append(q)
    return pts, true_line


def test_preemption_function():
    assert [preemption(i, 8, 2) for i in range(1, 9)] == [8, 4, 4, 2, 2, 1, 1, 0]
    assert total_scorings(8, 8, 2) == 20
    assert total_scorings(500, 500, 100) == 96315
    assert total_scorings(500, 500, 100) == sum(500 >> (i // 100) for i in range(1, 501))
    assert total_scorings(500, 500, 100) <= 2 * 100 * 500


def test_example_trace():
    h, cost, count = preemptive_ransac(EXAMPLE, 0.1, M=8, B=2, rng=random.Random(2), hypotheses=HYPS)
    assert h == HYPS[0] and abs(cost - 0.01) < 1e-12 and count == 20
    # another order of the observations keeps the wrong line
    h, cost, count = preemptive_ransac(EXAMPLE, 0.1, M=8, B=2, rng=random.Random(3), hypotheses=HYPS)
    assert h == HYPS[1] and count == 20
    assert full_cost(HYPS[0], EXAMPLE, 0.1) < full_cost(HYPS[1], EXAMPLE, 0.1)


def test_no_preemption_is_full_scoring():
    for seed in range(3):
        data, _ = planted(random.Random(seed), 30, 30)
        hyps = make_hypotheses(data, 40, random.Random(seed))
        h, cost, count = preemptive_ransac(data, 0.15, M=40, B=1000, rng=random.Random(seed), hypotheses=hyps)
        costs = [full_cost(g, data, 0.15) for g in hyps]
        assert count == 40 * 60
        assert abs(cost - min(costs)) < 1e-9
        assert abs(full_cost(h, data, 0.15) - min(costs)) < 1e-9


def test_scorings_match_formula():
    data, _ = planted(random.Random(5), 250, 250)
    _, _, count = preemptive_ransac(data, 0.15, M=500, B=100, rng=random.Random(1))
    assert count == total_scorings(500, 500, 100) == 96315


def test_planted_line():
    for seed in range(3):
        data, true_line = planted(random.Random(10 + seed), 100, 100)
        h, _, _ = preemptive_ransac(data, 0.15, M=100, B=20, rng=random.Random(seed))
        ang = math.atan2(abs(h[0] * true_line[1] - h[1] * true_line[0]),
                         abs(h[0] * true_line[0] + h[1] * true_line[1]))
        assert ang < math.radians(3.0) and abs(h[2] - true_line[2]) < 0.3


def test_empty():
    assert preemptive_ransac([], 0.1, M=4, B=2, rng=random.Random(0)) == (None, math.inf, 0)
