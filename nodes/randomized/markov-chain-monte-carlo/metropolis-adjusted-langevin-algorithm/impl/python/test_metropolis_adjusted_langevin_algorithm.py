# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metropolis-adjusted-langevin-algorithm/. The authors are listed in prov/CGM810.jsonl.

import math
import random
from statistics import NormalDist

import pytest

from metropolis_adjusted_langevin_algorithm import (
    log_proposal,
    metropolis_adjusted_langevin_algorithm,
    unadjusted_langevin,
)


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n
    if var == 0:
        return 1.0

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / max(tau, 1e-9)


def check_mean(xs, mu, sd):
    # the sample mean has standard error about sd / sqrt(ESS)
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


def std_normal(x):
    return -0.5 * sum(v * v for v in x)


def std_normal_grad(x):
    return [-v for v in x]


def quartic(x):
    return -sum(v**4 for v in x) / 4


def quartic_grad(x):
    return [-(v**3) for v in x]


def test_trace_from_page() -> None:
    h = 0.5
    r1 = math.exp(std_normal((1.1743,)) + log_proposal(std_normal_grad, (1.1743,), (1.0,), h)
                  - std_normal((1.0,)) - log_proposal(std_normal_grad, (1.0,), (1.1743,), h))
    assert abs(r1 - 0.9766) < 1e-3
    y2 = 1.1743 * (1 - h / 2) + math.sqrt(h) * (-1.2)
    assert abs(y2 - 0.0322) < 1e-3


def test_detailed_balance_identity() -> None:
    # pi(x) q(y | x) alpha(x, y) = pi(y) q(x | y) alpha(y, x) for random pairs
    rng = random.Random(1)
    for _ in range(200):
        x = (rng.uniform(-2, 2),)
        y = (rng.uniform(-2, 2),)
        h = rng.uniform(0.05, 1.5)
        a = quartic(x) + log_proposal(quartic_grad, x, y, h)
        b = quartic(y) + log_proposal(quartic_grad, y, x, h)
        lhs = a + min(0.0, b - a)
        rhs = b + min(0.0, a - b)
        assert abs(lhs - rhs) < 1e-12


def test_standard_normal_moments() -> None:
    rng = random.Random(2)
    chain, acc = metropolis_adjusted_langevin_algorithm(std_normal, std_normal_grad, [3.0], 0.8, 6000, rng)
    xs = [x[0] for x in chain[100:]]
    check_mean(xs, 0.0, 1.0)
    check_mean([x * x for x in xs], 1.0, math.sqrt(2))
    assert acc / 6000 > 0.8


def test_quartic_target_moments() -> None:
    # pi(x) proportional to exp(-x^4 / 4): E x^2 = 2 Gamma(3/4) / Gamma(1/4) and E x^4 = 1
    m2 = 2 * math.gamma(0.75) / math.gamma(0.25)
    m4 = 1.0
    rng = random.Random(3)
    chain, _ = metropolis_adjusted_langevin_algorithm(quartic, quartic_grad, [0.0], 0.3, 8000, rng)
    xs = [x[0] for x in chain]
    check_mean(xs, 0.0, math.sqrt(m2))
    check_mean([x * x for x in xs], m2, math.sqrt(m4 - m2 * m2))


def test_correlated_gaussian() -> None:
    rho = 0.9
    det_s = 1 - rho * rho

    def log_t(q):
        return -(q[0] ** 2 - 2 * rho * q[0] * q[1] + q[1] ** 2) / (2 * det_s)

    def grad(q):
        return [-(q[0] - rho * q[1]) / det_s, -(q[1] - rho * q[0]) / det_s]

    rng = random.Random(4)
    chain, _ = metropolis_adjusted_langevin_algorithm(log_t, grad, [0.0, 0.0], 0.15, 8000, rng)
    for i in range(2):
        xs = [x[i] for x in chain]
        check_mean(xs, 0.0, 1.0)
    check_mean([x[0] * x[1] for x in chain], rho, math.sqrt(1 + rho * rho))


def test_acceptance_near_limit_in_high_dimension() -> None:
    # Roberts and Rosenthal: h = l^2 d^(-1/3); on N(0, I_d) the rate tends to 2 Phi(-l^3 / 8)
    d, ell = 400, 1.65
    h = ell * ell * d ** (-1 / 3)
    rng = random.Random(5)
    x0 = [rng.gauss(0.0, 1.0) for _ in range(d)]
    _, acc = metropolis_adjusted_langevin_algorithm(std_normal, std_normal_grad, x0, h, 1500, rng)
    limit = 2 * NormalDist().cdf(-(ell**3) / 8)
    assert abs(limit - 0.574) < 0.001
    assert abs(acc / 1500 - limit) < 0.08


def test_unadjusted_langevin_is_biased() -> None:
    # on N(0, 1) the unadjusted chain has stationary variance 1 / (1 - h / 4)
    rng = random.Random(6)
    h = 1.0
    chain = unadjusted_langevin(std_normal_grad, [0.0], h, 20000, rng)
    xs = [x[0] for x in chain]
    v = sum(x * x for x in xs) / len(xs)
    assert abs(v - 4 / 3) < 0.1
    chain, _ = metropolis_adjusted_langevin_algorithm(std_normal, std_normal_grad, [0.0], h, 20000, rng)
    v = sum(x[0] ** 2 for x in chain) / len(chain)
    assert abs(v - 1.0) < 0.1


def test_bad_inputs() -> None:
    rng = random.Random(7)
    with pytest.raises(ValueError):
        metropolis_adjusted_langevin_algorithm(std_normal, std_normal_grad, [0.0], 0.0, 10, rng)
    with pytest.raises(ValueError):
        metropolis_adjusted_langevin_algorithm(lambda x: -math.inf, std_normal_grad, [0.0], 0.1, 10, rng)
