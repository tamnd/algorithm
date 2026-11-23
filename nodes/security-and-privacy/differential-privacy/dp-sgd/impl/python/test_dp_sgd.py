# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dp-sgd/. The authors are listed in prov/X5S7AN.jsonl.

import math
import random

import pytest

from dp_sgd import (
    clip,
    dp_sgd,
    epsilon_for,
    log_a,
    logistic_gradient,
    logistic_loss,
    norm,
    rdp_sampled_gaussian,
)


def blobs(n, rng):
    """Two Gaussian blobs in the plane with a bias coordinate; labels -1 and +1."""
    data = []
    for i in range(n):
        y = 1 if i % 2 == 0 else -1
        data.append(((rng.gauss(1.5 * y, 1.0), rng.gauss(0.5 * y, 1.0), 1.0), y))
    return data


def mean_loss(theta, data):
    return sum(logistic_loss(theta, x, y) for x, y in data) / len(data)


def test_check_values():
    eps, order = epsilon_for(1, 2, 1, 1e-5)
    assert abs(eps - 2.52629) < 1e-5 and order == 11
    # The bound at integer orders is above the best real order, 2.5243.
    best_real = min(a / 8 + math.log(1e5) / (a - 1) for a in (1 + i / 1000 for i in range(1, 60000)))
    assert abs(best_real - 2.5243) < 1e-4 and eps >= best_real
    # Abadi et al. report epsilon = 1.26 for q = 0.01, sigma = 4, delta = 1e-5 and 10000 steps.
    eps, order = epsilon_for(0.01, 4, 10000, 1e-5)
    assert abs(eps - 1.26) < 0.01 and order == 20
    assert abs(epsilon_for(0.01, 1.0, 1000, 1e-5)[0] - 2.5383) < 1e-4
    assert abs(epsilon_for(0.01, 1.1, 10000, 1e-5)[0] - 6.2798) < 1e-4


def test_full_batch_is_the_gaussian_mechanism():
    for sigma in (0.5, 1.0, 2.0, 5.0):
        for alpha in range(2, 30):
            assert abs(rdp_sampled_gaussian(1, sigma, alpha) - alpha / (2 * sigma ** 2)) < 1e-12


def test_bad_input():
    with pytest.raises(ValueError):
        log_a(0.1, 1.0, 1)
    with pytest.raises(ValueError):
        epsilon_for(0.1, 1.0, 10, 0.0)
    with pytest.raises(ValueError):
        dp_sgd([((1.0,), 1)], 0.0, 1.0, 1.0, 0.1, 1, random.Random(0))


def test_clipping_bounds_the_add_remove_sensitivity():
    rng = random.Random(2)
    for _ in range(500):
        d = rng.randint(1, 8)
        c = rng.uniform(0.1, 3.0)
        theta = [rng.uniform(-3, 3) for _ in range(d)]
        data = [([rng.uniform(-4, 4) for _ in range(d)], rng.choice((-1, 1))) for _ in range(rng.randint(0, 10))]
        extra = ([rng.uniform(-4, 4) for _ in range(d)], rng.choice((-1, 1)))
        g = logistic_gradient(theta, *extra)
        gc = clip(g, c)
        assert norm(gc) <= c * (1 + 1e-12)
        if norm(g) <= c:
            assert gc == g
        s1 = [0.0] * d
        for x, y in data:
            s1 = [a + b for a, b in zip(s1, clip(logistic_gradient(theta, x, y), c))]
        s2 = [a + b for a, b in zip(s1, gc)]
        assert norm([a - b for a, b in zip(s2, s1)]) <= c * (1 + 1e-9)


def test_gradient_against_finite_differences():
    rng = random.Random(3)
    for _ in range(500):
        d = rng.randint(1, 8)
        theta = [rng.uniform(-2, 2) for _ in range(d)]
        x = [rng.uniform(-2, 2) for _ in range(d)]
        y = rng.choice((-1, 1))
        g = logistic_gradient(theta, x, y)
        for i in range(d):
            h = 1e-6
            up = theta[:]
            dn = theta[:]
            up[i] += h
            dn[i] -= h
            fd = (logistic_loss(up, x, y) - logistic_loss(dn, x, y)) / (2 * h)
            assert abs(fd - g[i]) < 1e-6


def simpson_a(q, sigma, alpha, steps=1200):
    """Independent oracle: A_alpha = E_{z ~ N(0, sigma^2)} [((1 - q) + q exp((2z - 1) / (2 sigma^2)))^alpha]."""
    lo, hi = -12 * sigma, 12 * sigma + 2 * alpha
    h = (hi - lo) / steps

    def f(z):
        dens = math.exp(-z * z / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))
        return dens * ((1 - q) + q * math.exp((2 * z - 1) / (2 * sigma ** 2))) ** alpha

    s = f(lo) + f(hi)
    for i in range(1, steps):
        s += (4 if i % 2 else 2) * f(lo + i * h)
    return s * h / 3


def test_binomial_formula_against_numerical_integration():
    rng = random.Random(4)
    for _ in range(500):
        q = rng.uniform(0.001, 0.5)
        sigma = rng.uniform(0.9, 3.0)
        alpha = rng.randint(2, 8)
        exact = math.exp(log_a(q, sigma, alpha))
        assert abs(simpson_a(q, sigma, alpha) - exact) <= 1e-6 * exact


def test_epsilon_is_monotone():
    e = [epsilon_for(0.02, 1.2, t, 1e-5)[0] for t in (10, 100, 1000, 5000)]
    assert e == sorted(e)
    e = [epsilon_for(0.02, s, 1000, 1e-5)[0] for s in (0.8, 1.0, 2.0, 4.0)]
    assert e == sorted(e, reverse=True)
    e = [epsilon_for(0.02, 1.2, 1000, dl)[0] for dl in (1e-3, 1e-5, 1e-7)]
    assert e == sorted(e)
    e = [epsilon_for(q, 1.2, 1000, 1e-5)[0] for q in (0.001, 0.01, 0.1, 1.0)]
    assert e == sorted(e)


def test_training_lowers_the_loss():
    rng = random.Random(5)
    data = blobs(200, rng)
    start = mean_loss([0.0, 0.0, 0.0], data)
    theta = dp_sgd(data, q=0.1, sigma=1.0, c=1.0, eta=0.5, steps=200, rng=rng)
    assert mean_loss(theta, data) < start - 0.2
    # The same seed gives the same model.
    a = dp_sgd(data, 0.1, 1.0, 1.0, 0.5, 20, random.Random(7))
    b = dp_sgd(data, 0.1, 1.0, 1.0, 0.5, 20, random.Random(7))
    assert a == b
