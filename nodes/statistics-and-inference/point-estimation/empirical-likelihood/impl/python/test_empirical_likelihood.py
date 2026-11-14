# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-likelihood/. The authors are listed in prov/DSWA0W.jsonl.

import math
import random

from empirical_likelihood import _solve, el_mean_interval, el_mean_stat, el_ratio, el_test
from stdist import chi2_ppf


def scalar_reference(x, mu):
    """-2 log R(mu) by bisection on lambda in the interval where all weights are positive."""
    d = [v - mu for v in x]
    lo, hi = -1.0 / max(d), -1.0 / min(d)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = sum(di / (1 + mid * di) for di in d)  # decreasing in lambda
        if f > 0:
            lo = mid
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    return 2 * sum(math.log1p(lam * di) for di in d)


def test_zero_at_the_sample_mean():
    x = [1.0, 4.0, 2.0, 8.0, 5.0]
    res = el_ratio([[v - 4.0] for v in x])
    assert abs(res.stat) < 1e-14
    assert all(abs(w - 0.2) < 1e-14 for w in res.weights)


def test_scalar_matches_lambda_bisection():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(3, 30)
        x = [rng.expovariate(1.0) for _ in range(n)]
        lo, hi = min(x), max(x)
        mu = lo + (hi - lo) * rng.uniform(0.02, 0.98)
        assert abs(el_mean_stat(x, mu) - scalar_reference(x, mu)) < 1e-8 * max(1.0, scalar_reference(x, mu))


def test_two_points_exact():
    x1, x2 = 1.0, 5.0
    for mu in (1.5, 2.0, 3.0, 4.9):
        w1 = (x2 - mu) / (x2 - x1)
        expect = -2 * (math.log(2 * w1) + math.log(2 * (1 - w1)))
        assert abs(el_mean_stat([x1, x2], mu) - expect) < 1e-10


def test_three_points_against_simplex_search():
    x = [0.0, 1.0, 5.0]
    for mu in (0.5, 1.0, 2.0, 4.0):
        d = [v - mu for v in x]

        def value(t):
            w2 = (-t * d[0] - (1 - t) * d[2]) / (d[1] - d[2])
            w3 = 1 - t - w2
            if t <= 0 or w2 <= 0 or w3 <= 0:
                return -math.inf
            return math.log(3 * t) + math.log(3 * w2) + math.log(3 * w3)

        best = max((value(i / 20000), i / 20000) for i in range(1, 20000))
        h = 1 / 20000
        best = max((value(best[1] - h + 2 * h * i / 20000), 0) for i in range(20001))
        assert abs(el_mean_stat(x, mu) - (-2 * best[0])) < 1e-8


def test_outside_hull_is_infinite():
    x = [1.0, 2.0, 3.0]
    assert el_mean_stat(x, 3.0) == math.inf and el_mean_stat(x, 0.5) == math.inf
    d = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 0.5]]  # 0 is not in the hull
    assert el_ratio(d).stat == math.inf
    d2 = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0], [2.0, 0.5]]
    assert el_ratio(d2).stat < math.inf


def test_affine_invariance():
    rng = random.Random(2)
    x = [rng.gauss(0, 1) for _ in range(25)]
    a, b = 3.0, -2.5
    y = [a + b * v for v in x]
    for mu in (-0.3, 0.0, 0.2):
        assert abs(el_mean_stat(x, mu) - el_mean_stat(y, a + b * mu)) < 1e-9
    d = [[rng.gauss(0.1, 1), rng.gauss(-0.2, 2)] for _ in range(30)]
    m = [[2.0, 1.0], [-1.0, 3.0]]
    dm = [[m[0][0] * u + m[0][1] * v, m[1][0] * u + m[1][1] * v] for u, v in d]
    assert abs(el_ratio(d).stat - el_ratio(dm).stat) < 1e-9


def test_vector_weights_are_optimal():
    rng = random.Random(3)
    n = 12
    d = [[rng.gauss(0.2, 1), rng.gauss(0.1, 1)] for _ in range(n)]
    res = el_ratio(d)
    w = res.weights
    assert abs(sum(w) - 1) < 1e-12
    for j in range(2):
        assert abs(sum(wi * di[j] for wi, di in zip(w, d))) < 1e-12
    base = sum(math.log(n * wi) for wi in w)
    assert abs(-2 * base - res.stat) < 1e-10
    # random feasible directions: project onto {v : sum v = 0, sum v d = 0}
    c = [[1.0] * n, [di[0] for di in d], [di[1] for di in d]]
    cct = [[sum(a * b for a, b in zip(r, s)) for s in c] for r in c]
    for _ in range(200):
        v = [rng.gauss(0, 1) for _ in range(n)]
        coef = _solve(cct, [sum(a * b for a, b in zip(r, v)) for r in c])
        v = [v[i] - sum(coef[k] * c[k][i] for k in range(3)) for i in range(n)]
        eps = 0.5 * min(wi / abs(vi) for wi, vi in zip(w, v) if vi != 0)
        assert sum(math.log(n * (wi + eps * vi)) for wi, vi in zip(w, v)) <= base + 1e-12


def test_interval_ends_and_scan():
    rng = random.Random(4)
    x = [rng.expovariate(0.5) for _ in range(20)]
    lo, hi = el_mean_interval(x)
    c = chi2_ppf(0.95, 1)
    assert abs(el_mean_stat(x, lo) - c) < 1e-6 and abs(el_mean_stat(x, hi) - c) < 1e-6
    grid = [min(x) + (max(x) - min(x)) * i / 4000 for i in range(1, 4000)]
    inside = [mu for mu in grid if el_mean_stat(x, mu) <= c]
    step = (max(x) - min(x)) / 4000
    assert abs(inside[0] - lo) <= step and abs(inside[-1] - hi) <= step


def test_coverage_measured():
    # Measured, not proved: coverage at the true mean for Exp(1) data, n = 40.
    rng = random.Random(5)
    r, n = 1000, 40
    c = chi2_ppf(0.95, 1)
    hits = sum(el_mean_stat([rng.expovariate(1.0) for _ in range(n)], 1.0) <= c for _ in range(r))
    assert 0.90 < hits / r < 0.97
    # mean and variance together for normal data, q = 2
    c2 = chi2_ppf(0.95, 2)
    hits = 0
    for _ in range(300):
        x = [rng.gauss(0, 1) for _ in range(60)]
        stat, crit, rej = el_test(lambda v, t: (v - t[0], (v - t[0]) ** 2 - t[1]), x, (0.0, 1.0))
        assert crit == c2
        hits += not rej
    assert 0.88 < hits / 300 < 0.99
