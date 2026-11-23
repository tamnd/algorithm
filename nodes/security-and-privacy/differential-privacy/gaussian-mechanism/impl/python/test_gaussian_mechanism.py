# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-mechanism/. The authors are listed in prov/B229GK.jsonl.

import math
import random

import pytest

import dpkit
from gaussian_mechanism import (
    analytic_delta,
    analytic_sigma,
    classical_sigma,
    gaussian_log_density,
    gaussian_mechanism,
    normal_cdf,
)


def simpson(g, a, b, n=1200):
    h = (b - a) / n
    s = g(a) + g(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * g(a + i * h)
    return s * h / 3


def hockey_stick_by_integration(sens, sigma, eps):
    """Oracle: integrate max(0, p - e^eps q) for p = N(0, s^2), q = N(Delta, s^2).

    The integrand is positive exactly left of the point where the log ratio equals eps.
    """
    p = lambda y: math.exp(gaussian_log_density(y, 0.0, sigma))
    q = lambda y: math.exp(gaussian_log_density(y, sens, sigma))
    cut = sens / 2 - eps * sigma * sigma / sens
    g = lambda y: max(0.0, p(y) - math.exp(eps) * q(y))
    return simpson(g, cut - 14 * sigma, cut)


def test_check_values():
    assert abs(classical_sigma(1, 0.5, 1e-5) - 9.6896) < 5e-5
    assert abs(analytic_delta(1, 1, 1) - 0.126937) < 5e-7
    assert abs(analytic_delta(1, 2, 1) - 0.0068296) < 5e-8
    # mu-GDP with mu = Delta / sigma = 1 gives the same delta at epsilon = 1.
    assert analytic_delta(3, 3, 1) == pytest.approx(0.126937, abs=5e-7)
    assert normal_cdf(0) == 0.5


def test_analytic_delta_matches_numeric_integration():
    rng = random.Random(21)
    for _ in range(500):
        sens = rng.uniform(0.2, 3.0)
        sigma = rng.uniform(0.3, 4.0) * sens
        eps = rng.uniform(0.0, 3.0)
        want = hockey_stick_by_integration(sens, sigma, eps)
        assert abs(analytic_delta(sens, sigma, eps) - want) < 1e-8


def test_analytic_delta_falls_with_sigma():
    for eps in (0.0, 0.5, 2.0):
        prev = 1.0
        for k in range(1, 60):
            d = analytic_delta(1.0, 0.1 * k, eps)
            assert d <= prev
            prev = d


def test_analytic_sigma_is_tight_and_beats_classical():
    rng = random.Random(4)
    for _ in range(500):
        eps = rng.uniform(0.01, 0.99)
        delta = 10 ** rng.uniform(-9, -1)
        sens = rng.uniform(0.5, 2.0)
        s = analytic_sigma(sens, eps, delta)
        assert analytic_delta(sens, s, eps) <= delta
        assert analytic_delta(sens, s * (1 - 1e-6), eps) > delta
        assert s <= classical_sigma(sens, eps, delta)


def test_classical_formula_fails_outside_its_range():
    # A measurement: with epsilon = 10 the classical sigma gives a larger delta than asked.
    s = math.sqrt(2 * math.log(1.25 / 1e-3)) / 10
    assert analytic_delta(1, s, 10) > 1e-3
    with pytest.raises(ValueError):
        classical_sigma(1, 10, 1e-3)


def test_privacy_loss_is_gaussian_by_monte_carlo():
    # L = ln p(Y) / q(Y) with Y ~ p is N(mu^2 / 2, mu^2), mu = Delta / sigma.
    # delta(eps) = E[max(0, 1 - e^(eps - L))], a mean of [0, 1] values.
    rng = random.Random(31)
    n = 2000
    for sens, sigma, eps in ((1.0, 1.0, 1.0), (1.0, 2.0, 0.5), (2.0, 1.5, 0.2)):
        total = 0.0
        for _ in range(n):
            y = rng.gauss(0.0, sigma)
            loss = gaussian_log_density(y, 0.0, sigma) - gaussian_log_density(y, sens, sigma)
            total += max(0.0, 1 - math.exp(eps - loss))
        assert abs(total / n - analytic_delta(sens, sigma, eps)) <= dpkit.hoeffding_margin(n, 1e-6)


def test_log_ratio_is_unbounded_so_no_pure_dp():
    sigma = 1.0
    px = lambda z: gaussian_log_density(z, 0.0, sigma)
    py = lambda z: gaussian_log_density(z, 1.0, sigma)
    narrow = dpkit.log_ratio_grid(px, py, [i / 10 for i in range(-30, 31)])
    wide = dpkit.log_ratio_grid(px, py, [i / 10 for i in range(-300, 301)])
    assert abs(narrow - 3.5) < 1e-9
    assert abs(wide - 30.5) < 1e-9


def test_sampler_tail_and_coordinates():
    rng = random.Random(55)
    n = 2000
    eps, delta = 1.0, 1e-5
    sigma = analytic_sigma(1.0, eps, delta)
    t = 1.5 * sigma
    hits = 0
    for _ in range(n):
        y = gaussian_mechanism(None, lambda _: [0.0], 1.0, eps, delta, rng)
        hits += abs(y[0]) > t
    assert abs(hits / n - math.erfc(t / (sigma * math.sqrt(2)))) <= dpkit.hoeffding_margin(n, 1e-6)
    out = gaussian_mechanism([1.0, 2.0, 3.0], lambda v: v, 1.0, 0.5, 1e-5, rng, analytic=False)
    assert len(out) == 3


def test_edge_cases():
    rng = random.Random(0)
    with pytest.raises(ValueError):
        classical_sigma(1, 0.5, 0)
    with pytest.raises(ValueError):
        analytic_sigma(1, 1, 1)
    with pytest.raises(ValueError):
        analytic_delta(0, 1, 1)
    assert gaussian_mechanism(None, lambda _: [], 1.0, 1.0, 1e-5, rng) == []
    # At epsilon = 0, sigma = Delta / (2 delta) is enough (Balle and Wang, Theorem 2).
    assert analytic_delta(1, 1 / (2 * 0.01), 0) <= 0.01
