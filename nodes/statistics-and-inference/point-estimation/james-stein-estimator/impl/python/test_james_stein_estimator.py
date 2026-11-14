# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/james-stein-estimator/. The authors are listed in prov/CYEN4M.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from james_stein_estimator import (
    inverse_moment_noncentral_chi2,
    james_stein,
    james_stein_risk,
    james_stein_toward_mean,
    stein_unbiased_risk_estimate,
)


def loss(est, theta):
    return math.fsum((a - b) ** 2 for a, b in zip(est, theta))


def simpson_inverse_moment(p, lam, n=4000):
    """E[1/W] = integral over (0, 1) of w^(p-3) exp(-lam (1 - w^2) / 2) dw, by Simpson's rule.

    This follows from E[1/W] = integral over t > 0 of E[exp(-t W)] dt and the
    moment generating function of the noncentral chi-squared law, with the
    change of variable w = (1 + 2t)^(-1/2). It is independent of the Poisson series.
    """
    h = 1.0 / n

    def f(w):
        return w ** (p - 3) * math.exp(-lam * (1.0 - w * w) / 2.0)

    s = f(0.0) + f(1.0)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(i * h)
    return s * h / 3.0


def test_page_example():
    x = [2, -1, F(1, 2), F(3, 2), F(-1, 2)]
    s = sum(t * t for t in x)
    assert s == F(31, 4)
    c = 1 - 3 / s
    assert c == F(19, 31)
    got = james_stein([float(t) for t in x])
    for g, t in zip(got, x):
        assert g == pytest.approx(float(c * t), abs=1e-15)


def test_risk_at_zero_is_two_exactly():
    for p in range(3, 12):
        # At theta = 0, ||X||^2 is central chi-squared with p degrees of freedom and E[1/W] = 1/(p - 2).
        exact = p - (p - 2) ** 2 * F(1, p - 2)
        assert exact == 2
        assert james_stein_risk(0.0, p) == pytest.approx(2.0, abs=1e-12)


def test_series_against_quadrature():
    for p in (3, 4, 5, 10):
        for lam in (0.0, 0.5, 5.0, 30.0, 200.0):
            a = inverse_moment_noncentral_chi2(p, lam)
            b = simpson_inverse_moment(p, lam)
            assert a == pytest.approx(b, rel=1e-6)


def test_exact_risk_below_p_and_increasing():
    for p in (3, 5, 10):
        prev = 0.0
        for lam in (0.0, 0.1, 1.0, 5.0, 25.0, 100.0, 1e4):
            r = james_stein_risk(lam, p)
            assert 2.0 - 1e-12 <= r < p
            assert r >= prev
            prev = r
        # For large lam, E[1/W] is close to 1/(p - 2 + lam).
        lam = 1e6
        approx = p - (p - 2) ** 2 / (p - 2 + lam)
        assert james_stein_risk(lam, p) == pytest.approx(approx, rel=1e-6)


def test_sigma2_scaling():
    p = 6
    for lam in (0.0, 3.0, 40.0):
        for s2 in (0.25, 4.0):
            assert james_stein_risk(lam * s2, p, s2) == pytest.approx(s2 * james_stein_risk(lam, p), rel=1e-12)
    x = [1.0, -2.0, 0.5, 3.0, 0.0, -1.5]
    for k in (0.5, 3.0):
        a = james_stein([k * t for t in x], sigma2=k * k * 2.0)
        b = james_stein(x, sigma2=2.0)
        for u, v in zip(a, b):
            assert u == pytest.approx(k * v, rel=1e-12, abs=1e-12)


def test_monte_carlo_risk_matches_exact():
    rng = random.Random(20240601)
    p, n = 5, 20000
    for lam in (0.0, 5.0, 25.0):
        theta = [math.sqrt(lam)] + [0.0] * (p - 1)
        losses = []
        sures = []
        for _ in range(n):
            x = [t + rng.gauss(0.0, 1.0) for t in theta]
            losses.append(loss(james_stein(x), theta))
            sures.append(stein_unbiased_risk_estimate(x))
        exact = james_stein_risk(lam, p)
        for sample in (losses, sures):
            mean = math.fsum(sample) / n
            se = math.sqrt(math.fsum((t - mean) ** 2 for t in sample) / (n - 1) / n)
            assert abs(mean - exact) < 4.0 * se
        assert exact < p


def test_positive_part_beats_plain_in_simulation():
    rng = random.Random(77)
    p, n = 5, 20000
    for lam in (0.0, 2.0, 10.0):
        theta = [math.sqrt(lam / p)] * p
        diffs = []
        for _ in range(n):
            x = [t + rng.gauss(0.0, 1.0) for t in theta]
            diffs.append(loss(james_stein(x), theta) - loss(james_stein(x, positive_part=True), theta))
        mean = math.fsum(diffs) / n
        se = math.sqrt(math.fsum((t - mean) ** 2 for t in diffs) / (n - 1) / n)
        assert mean > -3.0 * se
        if lam == 0.0:
            assert mean > 4.0 * se


def test_toward_mean_risk_three_at_constant_theta():
    rng = random.Random(7)
    p, n = 6, 20000
    theta = [3.0] * p
    losses = [loss(james_stein_toward_mean([t + rng.gauss(0.0, 1.0) for t in theta]), theta) for _ in range(n)]
    mean = math.fsum(losses) / n
    se = math.sqrt(math.fsum((t - mean) ** 2 for t in losses) / (n - 1) / n)
    # The mean direction is not shrunk (risk 1); the other p - 1 directions are plain James-Stein at 0 (risk 2).
    exact = 1.0 + james_stein_risk(0.0, p - 1)
    assert exact == pytest.approx(3.0, abs=1e-12)
    assert abs(mean - exact) < 4.0 * se


def test_target_is_translation_equivariant():
    x = [1.0, 4.0, -2.0, 0.5]
    m = [0.5, 1.0, 1.0, -1.0]
    a = [3.0, -1.0, 2.0, 7.0]
    left = james_stein([u + v for u, v in zip(x, a)], target=[u + v for u, v in zip(m, a)])
    right = [u + v for u, v in zip(james_stein(x, target=m), a)]
    for u, v in zip(left, right):
        assert u == pytest.approx(v, rel=1e-12, abs=1e-12)


def test_edges():
    with pytest.raises(ValueError):
        james_stein([1.0, 2.0])
    with pytest.raises(ValueError):
        james_stein([1.0, 2.0, 3.0], sigma2=0.0)
    with pytest.raises(ValueError):
        james_stein([1.0, 2.0, 3.0], target=[0.0])
    with pytest.raises(ValueError):
        james_stein_toward_mean([1.0, 2.0, 3.0])
    assert james_stein([0.0, 0.0, 0.0]) == [0.0, 0.0, 0.0]
    assert james_stein([1.0, 1.0, 1.0], target=[1.0, 1.0, 1.0]) == [1.0, 1.0, 1.0]
    # ||x||^2 = 0.75 < p - 2 = 1: the plain factor is negative, the positive part gives the target.
    x = [0.5, 0.5, 0.5]
    plain = james_stein(x)
    assert plain[0] == pytest.approx(0.5 * (1.0 - 1.0 / 0.75))
    assert plain[0] < 0.0
    assert james_stein(x, positive_part=True) == [0.0, 0.0, 0.0]
    assert james_stein_toward_mean([2.0, 2.0, 2.0, 2.0]) == [2.0, 2.0, 2.0, 2.0]
