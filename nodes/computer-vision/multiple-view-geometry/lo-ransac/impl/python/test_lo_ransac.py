# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lo-ransac/. The authors are listed in prov/BQXMXZ.jsonl.

import itertools
import math
import random

from lo_ransac import fit_line_lsq, inliers, line_through, lo_ransac, local_opt, point_line_distance, ransac_trials

YS = [0.05, -0.05, 0.04, -0.03, 0.0, 0.05, -0.05, 0.02, -0.04, 0.03]
EXAMPLE = [(float(x), y) for x, y in enumerate(YS)] + [(2.0, 3.0), (5.0, -2.0), (7.0, 4.0), (8.0, -3.0)]


def planted(rng, n_in, n_out, sigma, a=0.5, b=2.0, gap=1.0):
    pts = []
    for _ in range(n_in):
        x = rng.uniform(0.0, 10.0)
        pts.append((x, a * x + b + rng.gauss(0.0, sigma)))
    true_line = line_through([(0.0, b), (1.0, a + b)])
    while len(pts) < n_in + n_out:
        q = (rng.uniform(0.0, 10.0), rng.uniform(-5.0, 12.0))
        if point_line_distance(true_line, q) > gap:
            pts.append(q)
    return pts, true_line


def test_example_local_step():
    line = line_through([EXAMPLE[3], EXAMPLE[4]])
    inl = inliers(line, EXAMPLE, 0.08)
    assert inl == [1, 3, 4, 5, 7]
    wide = inliers(line, EXAMPLE, math.sqrt(2.0) * 0.08)
    assert wide == [1, 2, 3, 4, 5, 6, 7]
    refit = fit_line_lsq([EXAMPLE[i] for i in wide])
    assert inliers(refit, EXAMPLE, 0.08) == list(range(10))
    _, lo_inl = local_opt(line, inl, EXAMPLE, 0.08, random.Random(0))
    assert lo_inl == list(range(10))
    assert ransac_trials(0.99, 5 / 14, 2) == 34 and ransac_trials(0.99, 10 / 14, 2) == 7


def test_example_pairs():
    counts = [len(inliers(line_through([EXAMPLE[i], EXAMPLE[j]]), EXAMPLE, 0.08))
              for i, j in itertools.combinations(range(14), 2)]
    assert len(counts) == 91 and counts.count(10) == 4 and max(counts) == 10


def test_example_run():
    model, inl, t, runs = lo_ransac(EXAMPLE, 0.08, random.Random(1))
    assert inl == list(range(10)) and t == 7 and 1 <= runs <= t
    assert max(point_line_distance(model, EXAMPLE[i]) for i in inl) <= 0.08


def test_local_opt_never_loses():
    for seed in range(5):
        rng = random.Random(seed)
        data, _ = planted(rng, 40, 30, sigma=0.1, gap=0.5)
        for _ in range(10):
            i, j = rng.sample(range(len(data)), 2)
            line = line_through([data[i], data[j]])
            inl = inliers(line, data, 0.25)
            _, lo_inl = local_opt(line, inl, data, 0.25, random.Random(seed))
            assert len(lo_inl) >= len(inl)
            assert lo_inl == sorted(lo_inl)


def test_noisy_data():
    for seed in range(4):
        data, true_line = planted(random.Random(20 + seed), 25, 15, sigma=0.1, gap=0.6)
        model, inl, t, runs = lo_ransac(data, 0.25, random.Random(seed))
        assert all(i < 25 for i in inl) and len(inl) >= 23
        assert runs <= t
        a = math.atan2(abs(model[0] * true_line[1] - model[1] * true_line[0]),
                       abs(model[0] * true_line[0] + model[1] * true_line[1]))
        assert a < math.radians(2.0)


def test_degenerate():
    assert lo_ransac([(1.0, 1.0)] * 4, 0.1, random.Random(0), max_trials=10) == (None, [], 10, 0)
    assert lo_ransac([(0.0, 0.0)], 0.1, random.Random(0)) == (None, [], 0, 0)
