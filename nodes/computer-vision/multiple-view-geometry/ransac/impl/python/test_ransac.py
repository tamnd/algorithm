# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ransac/. The authors are listed in prov/648BZZ.jsonl.

import itertools
import math
import random

from ransac import (canonical_line, consensus_size, fit_line_lsq, line_through,
                    point_line_distance, ransac, ransac_trials)


def planted(rng, n_in, n_out, a=0.5, b=2.0, sigma=0.0, gap=1.0):
    """Inliers on y = a x + b (with optional noise), outliers at least gap away from the line."""
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


def test_trial_counts():
    assert [ransac_trials(0.99, 0.5, s) for s in (2, 3, 4, 5, 7, 8)] == [17, 35, 72, 146, 588, 1177]
    assert ransac_trials(0.99, 0.8, 4) == 9
    assert ransac_trials(0.95, 0.5, 2) == 11
    assert ransac_trials(0.99, 1.0, 4) == 1
    assert ransac_trials(0.99, 0.0, 4) == math.inf


def test_page_example():
    data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (0, 4), (1, 3), (4, 0)]
    model, inl, _ = ransac(data, 0.1, random.Random(1))
    assert inl == [0, 1, 2, 3, 4]
    assert max(point_line_distance(model, data[i]) for i in inl) < 1e-12
    # the competing line x + y = 4 has 4 points
    assert consensus_size(line_through([(0, 4), (4, 0)]), data, 0.1) == 4


def test_planted_inliers_found_exactly():
    rng = random.Random(7)
    data, true_line = planted(rng, 60, 40)
    model, inl, _ = ransac(data, 0.05, random.Random(11))
    assert inl == list(range(60))
    assert line_angle(model, true_line) < 1e-9
    assert abs(model[2] - true_line[2]) < 1e-9


def test_matches_exhaustive_consensus():
    for seed in range(5):
        rng = random.Random(100 + seed)
        data, _ = planted(rng, 12, 10, gap=0.5)
        best = max(consensus_size(line_through(pq), data, 0.05)
                   for pq in itertools.combinations(data, 2) if line_through(pq) is not None)
        _, inl, _ = ransac(data, 0.05, random.Random(seed), p=0.999)
        assert len(inl) == best


def test_noisy_inliers():
    rng = random.Random(3)
    data, true_line = planted(rng, 50, 50, sigma=0.05, gap=0.5)
    model, inl, _ = ransac(data, 0.15, random.Random(5))
    assert set(range(50)) - set(inl) == set() or len(set(range(50)) - set(inl)) <= 1
    assert all(i < 50 for i in inl)
    assert line_angle(model, true_line) < math.radians(1.0)


def test_degenerate_data():
    model, inl, t = ransac([(1.0, 1.0)] * 5, 0.1, random.Random(0), max_trials=20)
    assert model is None and inl == [] and t == 20
    assert ransac([(0.0, 0.0)], 0.1, random.Random(0)) == (None, [], 0)


def test_fit_line_lsq():
    pts = [(x, 2.0 * x - 1.0) for x in range(6)]
    l = fit_line_lsq(pts)
    assert max(point_line_distance(l, q) for q in pts) < 1e-12
    assert canonical_line((-1.0, 0.0, 3.0)) == (1.0, 0.0, -3.0)
