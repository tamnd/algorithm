# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multidimensional-scaling/. The authors are listed in prov/4X06MR.jsonl.

import math
import random
from fractions import Fraction as F

from multidimensional_scaling import (
    disparities,
    gradient,
    kruskal_mds,
    pav,
    raw_stress,
    stress1,
    stress1_of,
)


def max_min_isotonic(y):
    """The max-min formula of isotonic regression, O(n^3), as a reference."""
    n = len(y)
    return [max(min(sum(y[s:t + 1]) / (t - s + 1) for t in range(i, n)) for s in range(i + 1)) for i in range(n)]


def euclid(points):
    return [[math.dist(p, q) for q in points] for p in points]


def test_pav_matches_max_min_formula():
    rng = random.Random(5)
    for _ in range(200):
        y = [F(rng.randint(-5, 5)) for _ in range(rng.randint(1, 8))]
        assert pav(y) == max_min_isotonic(y)


def test_pav_examples():
    assert pav([1, 3, 2, 4]) == [1, 2.5, 2.5, 4]
    assert pav([3, 2, 1]) == [2, 2, 2]
    assert pav([]) == []


def test_true_configuration_has_zero_stress_under_monotone_transform():
    rng = random.Random(2)
    pts = [(rng.uniform(0, 4), rng.uniform(0, 4)) for _ in range(7)]
    delta = [[math.exp(v) for v in row] for row in euclid(pts)]
    d, dhat = disparities(pts, delta)
    assert stress1(d, dhat) < 1e-12
    assert raw_stress(pts, euclid(pts)) < 1e-20


def test_stress1_scale_and_translation_invariant():
    rng = random.Random(4)
    x = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(6)]
    delta = [[abs(i - j) ** 1.5 for j in range(6)] for i in range(6)]
    s = stress1(*disparities(x, delta))
    y = [(3 * a + 1, 3 * b - 2) for a, b in x]
    assert abs(stress1(*disparities(y, delta)) - s) < 1e-12


def test_gradient_matches_finite_differences():
    rng = random.Random(8)
    x = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(5)]
    delta = [[rng.random() if i != j else 0 for j in range(5)] for i in range(5)]
    delta = [[min(delta[i][j], delta[j][i]) for j in range(5)] for i in range(5)]
    d, dhat = disparities(x, delta)
    g = gradient(x, d, dhat)
    h = 1e-6
    for i in range(5):
        for a in range(2):
            xp = [list(p) for p in x]
            xm = [list(p) for p in x]
            xp[i][a] += h
            xm[i][a] -= h
            fd = (stress1_of(xp, dhat) - stress1_of(xm, dhat)) / (2 * h)
            assert abs(fd - g[i][a]) < 1e-6


def test_stress_never_increases():
    for seed in range(5):
        rng = random.Random(seed)
        pts = [(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(9)]
        delta = [[v ** 2 for v in row] for row in euclid(pts)]
        x0 = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(9)]
        _, hist = kruskal_mds(delta, x0, iters=80)
        assert all(b <= a + 1e-12 for a, b in zip(hist, hist[1:]))
        assert hist[-1] < hist[0]


def test_recovers_rank_order_of_planar_data():
    rng = random.Random(11)
    pts = [(rng.uniform(0, 3), rng.uniform(0, 3)) for _ in range(8)]
    delta = [[math.exp(v) - 1 for v in row] for row in euclid(pts)]
    x0 = [(p[0] + rng.gauss(0, 0.5), p[1] + rng.gauss(0, 0.5)) for p in pts]
    x, hist = kruskal_mds(delta, x0, iters=400)
    assert hist[-1] < 0.01
