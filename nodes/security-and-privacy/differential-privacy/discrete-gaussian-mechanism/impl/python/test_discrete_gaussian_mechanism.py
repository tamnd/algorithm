# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-gaussian-mechanism/. The authors are listed in prov/70PG4J.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from discrete_gaussian_mechanism import (
    acceptance_exponent,
    bernoulli,
    bernoulli_exp_neg,
    discrete_gaussian,
    discrete_gaussian_delta,
    discrete_gaussian_mechanism,
    discrete_laplace,
    laplace_scale_for,
)

BETA = 1e-6  # failure probability for each Hoeffding or DKW margin


def margin(n):
    return math.sqrt(math.log(2 / BETA) / (2 * n))


def gauss_pmf(sigma2, lo, hi):
    """The discrete Gaussian pmf on [lo, hi], normalized over a wide range."""
    s = float(sigma2)
    wide = int(60 * math.sqrt(s)) + 60
    total = math.fsum(math.exp(-(y * y) / (2 * s)) for y in range(-wide, wide + 1))
    return {y: math.exp(-(y * y) / (2 * s)) / total for y in range(lo, hi + 1)}


def hockey_stick(epsilon, sigma2, sensitivity):
    """sum_y (p(y) - e^epsilon p(y - Delta))_+ by brute force over a wide range."""
    s = float(sigma2)
    wide = int(60 * math.sqrt(s) + epsilon * s + 2 * sensitivity) + 60
    w = {y: math.exp(-(y * y) / (2 * s)) for y in range(-wide - sensitivity, wide + 1)}
    total = math.fsum(w[y] for y in range(-wide, wide + 1))
    terms = (w[y] - math.exp(epsilon) * w[y - sensitivity] for y in range(-wide, wide + 1))
    return math.fsum(max(0.0, d) for d in terms) / total


def test_worked_example():
    # sigma^2 = 4: t = floor(2) + 1 = 3, and Y = 2 is kept with probability exp(-1/18).
    assert laplace_scale_for(4) == 3
    assert acceptance_exponent(2, 4, 3) == Fraction(1, 18)
    assert acceptance_exponent(0, 4, 3) == Fraction(2, 9)
    assert acceptance_exponent(-5, 4, 3) == Fraction(121, 72)
    assert discrete_gaussian_delta(1.0, 4) == pytest.approx(0.0072488, abs=1e-7)


def test_scale_edges():
    assert laplace_scale_for(1) == 2
    assert laplace_scale_for(Fraction(9, 4)) == 2
    assert laplace_scale_for(Fraction(1, 4)) == 1
    assert laplace_scale_for(Fraction(99, 100)) == 1
    assert laplace_scale_for(10**12) == 10**6 + 1


def test_bad_input():
    rng = random.Random(1)
    with pytest.raises(TypeError):
        discrete_gaussian(4.0, rng)
    with pytest.raises(ValueError):
        discrete_gaussian(0, rng)
    with pytest.raises(ValueError):
        bernoulli_exp_neg(Fraction(-1, 2), rng)
    with pytest.raises(ValueError):
        discrete_laplace(0, rng)
    with pytest.raises(ValueError):
        bernoulli(Fraction(3, 2), rng)


def test_bernoulli_edges():
    rng = random.Random(2)
    assert all(bernoulli(Fraction(0), rng) == 0 for _ in range(100))
    assert all(bernoulli(Fraction(1), rng) == 1 for _ in range(100))
    assert all(bernoulli_exp_neg(0, rng) == 1 for _ in range(100))


def test_bernoulli_exp_neg_frequencies():
    rng = random.Random(3)
    n = 2500
    for gamma in [Fraction(1, 3), Fraction(1), Fraction(5, 2), Fraction(7)]:
        hits = sum(bernoulli_exp_neg(gamma, rng) for _ in range(n))
        assert abs(hits / n - math.exp(-float(gamma))) <= margin(n)


def test_discrete_laplace_frequencies():
    rng = random.Random(4)
    n = 4000
    t = 2
    counts = Counter(discrete_laplace(t, rng) for _ in range(n))
    r = math.exp(-1 / t)
    for y in range(-6, 7):
        want = (1 - r) / (1 + r) * r ** abs(y)
        assert abs(counts[y] / n - want) <= margin(n)


@pytest.mark.parametrize("sigma2,seed", [(4, 5), (Fraction(1, 3), 6), (Fraction(50, 7), 7)])
def test_discrete_gaussian_against_exact_pmf(sigma2, seed):
    rng = random.Random(seed)
    n = 2000
    samples = [discrete_gaussian(sigma2, rng) for _ in range(n)]
    counts = Counter(samples)
    width = int(6 * math.sqrt(float(sigma2))) + 2
    pmf = gauss_pmf(sigma2, -width, width)
    cdf_got = cdf_want = 0.0
    for y in range(-width, width + 1):
        assert abs(counts[y] / n - pmf[y]) <= margin(n)
        cdf_got += counts[y] / n
        cdf_want += pmf[y]
        assert abs(cdf_got - cdf_want) <= margin(n)  # the DKW inequality
    # Variance at most sigma^2 (Canonne, Kamath and Steinke, Corollary 17), up to sampling error.
    var = sum(y * y for y in samples) / n
    assert var <= float(sigma2) * (1 + 0.2) + 0.05


def test_mechanism_adds_the_noise():
    for seed in range(20):
        a = discrete_gaussian_mechanism(10, Fraction(5, 2), random.Random(seed))
        b = discrete_gaussian(Fraction(5, 2), random.Random(seed))
        assert a == 10 + b


def test_delta_decreases_and_matches_known_values():
    values = [discrete_gaussian_delta(e / 4, 4) for e in range(0, 17)]
    assert all(x >= y for x, y in zip(values, values[1:]))
    assert discrete_gaussian_delta(0.5, 4) == pytest.approx(0.0540072, abs=1e-7)
    assert discrete_gaussian_delta(2.0, 4) == pytest.approx(1.07409e-05, rel=1e-4)
    # More noise gives a smaller delta.
    assert discrete_gaussian_delta(1.0, 16) < discrete_gaussian_delta(1.0, 4)


def test_random_delta_against_hockey_stick():
    rng = random.Random(2020)
    for _ in range(500):
        sigma2 = Fraction(rng.randint(1, 240), rng.randint(4, 8))
        epsilon = rng.uniform(0.0, 3.0)
        sensitivity = rng.randint(1, 3)
        got = discrete_gaussian_delta(epsilon, sigma2, sensitivity)
        assert got == pytest.approx(hockey_stick(epsilon, sigma2, sensitivity), rel=1e-7, abs=1e-12)


def test_random_rejection_identity_exact():
    # Line L4 must make Laplace weight times acceptance proportional to the Gaussian weight:
    # -|y|/t - gamma(y) = -y^2/(2 sigma^2) - sigma^2/(2 t^2), exactly.
    rng = random.Random(70)
    for _ in range(500):
        sigma2 = Fraction(rng.randint(1, 500), rng.randint(1, 9))
        t = laplace_scale_for(sigma2)
        assert (t - 1) ** 2 <= sigma2 < t * t
        y = rng.randint(-60, 60)
        lhs = -Fraction(abs(y), t) - acceptance_exponent(y, sigma2, t)
        rhs = -Fraction(y * y) / (2 * sigma2) - sigma2 / (2 * t * t)
        assert lhs == rhs
