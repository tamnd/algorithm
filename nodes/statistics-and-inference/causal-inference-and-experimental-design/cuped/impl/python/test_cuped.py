# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuped/. The authors are listed in prov/Y9J2V9.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction as Fr

import pytest

from cuped import ancova, cuped, interval, theta_pooled


def test_worked_example():
    xt, yt = [Fr(2), Fr(4), Fr(6)], [Fr(5), Fr(8), Fr(11)]
    xc, yc = [Fr(1), Fr(3), Fr(5)], [Fr(2), Fr(6), Fr(7)]
    w = cuped(yt, xt, yc, xc, "within")
    assert (w.naive_delta, w.theta, w.delta) == (3, Fr(11, 8), Fr(13, 8))
    p = cuped(yt, xt, yc, xc, "pooled")
    assert (p.theta, p.delta) == (Fr(53, 35), Fr(52, 35))
    assert ancova(yt, xt, yc, xc) == [Fr(7, 8), Fr(13, 8), Fr(11, 8)]


def test_within_theta_equals_ancova_coefficient_exactly():
    rng = random.Random(1)
    for _ in range(200):
        nt, nc = rng.randint(2, 7), rng.randint(2, 7)
        xt = [Fr(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(nt)]
        xc = [Fr(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(nc)]
        yt = [Fr(rng.randint(-20, 20)) for _ in range(nt)]
        yc = [Fr(rng.randint(-20, 20)) for _ in range(nc)]
        try:
            res = cuped(yt, xt, yc, xc, "within")
        except ValueError:
            continue
        b = ancova(yt, xt, yc, xc)
        assert res.delta == b[1] and res.theta == b[2]


def test_zero_theta_is_difference_in_means():
    yt, xt, yc, xc = [Fr(3), Fr(5)], [Fr(1), Fr(2)], [Fr(1), Fr(4)], [Fr(0), Fr(7)]
    r = cuped(yt, xt, yc, xc, 0)
    assert r.delta == r.naive_delta == Fr(3, 2) and r.var == r.naive_var


def enumerate_designs(y1, y0, x, n_t):
    """All assignments of n_t of the n units to treatment, each equally likely (complete randomization)."""
    n = len(x)
    for tr in itertools.combinations(range(n), n_t):
        s = set(tr)
        yield ([y1[i] for i in tr], [x[i] for i in tr], [y0[i] for i in range(n) if i not in s], [x[i] for i in range(n) if i not in s])


def test_fixed_theta_is_exactly_unbiased_over_the_randomization():
    """n = 6 units with fixed potential outcomes, 3 treated: averaging over all 20 assignments,
    CUPED with any theta fixed in advance has mean equal to the sample average treatment effect."""
    rng = random.Random(2)
    for _ in range(30):
        x = [Fr(rng.randint(0, 9)) for _ in range(6)]
        y0 = [xi + Fr(rng.randint(-3, 3)) for xi in x]
        y1 = [v + Fr(rng.randint(-2, 6)) for v in y0]
        tau = sum(a - b for a, b in zip(y1, y0)) / 6
        for theta in (Fr(0), Fr(1), Fr(7, 3), Fr(-2)):
            ests = [cuped(*d, theta).delta for d in enumerate_designs(y1, y0, x, 3)]
            assert len(ests) == 20 and sum(ests) / 20 == tau


def test_estimated_theta_bias():
    """With theta estimated from the same data the estimate is not exactly unbiased, but under the sharp
    null (Y(1) = Y(0)) the pooled theta does not depend on the assignment, so the mean is exactly 0."""
    x = [Fr(v) for v in (0, 1, 2, 3, 4, 9)]
    y0 = [Fr(v) for v in (1, 0, 4, 3, 7, 8)]
    y1 = [Fr(v) for v in (1, 6, 4, 3, 7, 20)]  # effects 0, 6, 0, 0, 0, 12: tau = 3
    within = [cuped(*d, "within").delta for d in enumerate_designs(y1, y0, x, 3)]
    assert sum(within) / 20 != 3
    null = [cuped(*d, "pooled").delta for d in enumerate_designs(y0, y0, x, 3)]
    assert sum(null) == 0


def test_variance_identity_exact():
    """With theta the pooled slope, the sample variance of y - theta x is var(y) (1 - r^2) exactly."""
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(3, 12)
        x = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        mx, my = sum(x) / n, sum(y) / n
        sxx = sum((a - mx) ** 2 for a in x)
        syy = sum((b - my) ** 2 for b in y)
        sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
        if sxx == 0 or syy == 0:
            continue
        th = theta_pooled(y, x)
        z = [b - th * a for a, b in zip(x, y)]
        mz = sum(z) / n
        szz = sum((c - mz) ** 2 for c in z)
        assert szz == syy * (1 - sxy * sxy / (sxx * syy))


def test_monte_carlo_variance_reduction_and_coverage():
    """X ~ N(0, 1), Y = 2 + X + 0.75 noise, so rho^2 = 1/1.5625 = 0.64 and the variance factor is 0.36.
    Effect 0.1, 500 units per arm, r = 400 replicates (seed 2026). Checks: the CUPED and naive estimates
    are unbiased within 4 SE; the ratio of the Monte Carlo variances is within 0.36 +- 0.08 (the ratio of
    two sample variances of 400 draws has relative SE about 0.07 each, and they are positively correlated);
    the mean of the per-sample variance ratio is within 0.36 +- 0.01; the 95% interval covers in at least
    0.92 of runs (4 SE below 0.95 is 0.906)."""
    rng = random.Random(2026)
    r, m, tau = 400, 500, 0.1
    cu, nv, ratios, cover = [], [], [], 0
    for _ in range(r):
        def arm(eff):
            xs = [rng.gauss(0, 1) for _ in range(m)]
            return [2 + eff + v + 0.75 * rng.gauss(0, 1) for v in xs], xs
        yt, xt = arm(tau)
        yc, xc = arm(0.0)
        res = cuped(yt, xt, yc, xc, "pooled")
        cu.append(res.delta)
        nv.append(res.naive_delta)
        ratios.append(res.var / res.naive_var)
        lo, hi = interval(res)
        cover += lo <= tau <= hi
    for est in (cu, nv):
        assert abs(statistics.mean(est) - tau) < 4 * statistics.stdev(est) / math.sqrt(r)
    assert abs(statistics.variance(cu) / statistics.variance(nv) - 0.36) < 0.08
    assert abs(statistics.mean(ratios) - 0.36) < 0.01
    assert cover / r >= 0.92


def test_input_checks():
    with pytest.raises(ValueError):
        cuped([1, 2], [1], [1, 2], [1, 2])
    with pytest.raises(ValueError):
        cuped([1], [1], [1, 2], [1, 2])
    with pytest.raises(ValueError):
        cuped([1, 2], [5, 5], [3, 4], [5, 5], "pooled")
