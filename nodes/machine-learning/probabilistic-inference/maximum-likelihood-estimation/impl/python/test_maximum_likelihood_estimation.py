# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-estimation/. The authors are listed in prov/8RHNEA.jsonl.

import math
import random
from fractions import Fraction as F
from math import comb

from maximum_likelihood_estimation import (
    bernoulli_mle,
    exp_family_mle_1d,
    gaussian_loglik,
    gaussian_mle,
    mixture_loglik,
    neyman_scott_expected_s2,
    neyman_scott_mle,
    poisson_mle,
)


def test_gaussian_closed_form_is_the_maximum() -> None:
    xs = [2.1, 1.3, 3.0, 2.6, 0.4]
    mu, var = gaussian_mle(xs)
    best = gaussian_loglik(xs, mu, var)
    for dm in (-0.1, -0.01, 0.01, 0.1):
        for dv in (0.9, 0.99, 1.0, 1.01, 1.1):
            if (dm, dv) != (0, 1.0):
                assert gaussian_loglik(xs, mu + dm, var * dv) < best
    assert gaussian_mle([F(1), F(2), F(6)]) == (F(3), F(14, 3))


def test_moment_matching_and_invariance() -> None:
    # Bernoulli in the natural parameter eta = logit(theta): A(eta) = log(1 + e^eta)
    xs = [1, 1, 0, 1, 1, 0, 1, 1]
    sig = lambda e: 1 / (1 + math.exp(-e))
    eta = exp_family_mle_1d(sum(xs) / len(xs), sig, lambda e: sig(e) * (1 - sig(e)))
    th = float(bernoulli_mle(xs))
    assert abs(eta - math.log(th / (1 - th))) < 1e-12  # invariance: MLE of logit is logit of MLE
    # Poisson: A(eta) = e^eta, so the MLE matches the mean: e^eta = mean
    ys = [3, 1, 4, 1, 5, 9, 2, 6]
    eta = exp_family_mle_1d(sum(ys) / len(ys), math.exp, math.exp, eta0=1.0)
    assert abs(math.exp(eta) - float(poisson_mle(ys))) < 1e-12


def test_invariance_on_a_grid() -> None:
    # maximize the Bernoulli likelihood over theta and over tau = theta^3
    s, f = 6, 2
    grid = [(i + 0.5) / 100000 for i in range(100000)]
    th = max(grid, key=lambda t: s * math.log(t) + f * math.log(1 - t))
    tau = max(grid, key=lambda u: s * math.log(u ** (1 / 3)) + f * math.log(1 - u ** (1 / 3)))
    assert abs(th - 0.75) < 1e-4 and abs(tau - 0.75 ** 3) < 1e-4


def test_bernoulli_mle_attains_cramer_rao_bound() -> None:
    theta, n = F(3, 10), 12
    mean = var = F(0)
    for s in range(n + 1):
        p = comb(n, s) * theta ** s * (1 - theta) ** (n - s)
        mean += p * F(s, n)
    for s in range(n + 1):
        p = comb(n, s) * theta ** s * (1 - theta) ** (n - s)
        var += p * (F(s, n) - mean) ** 2
    fisher = 1 / (theta * (1 - theta))
    assert mean == theta and var == 1 / (n * fisher)


def test_neyman_scott_bias_is_exact() -> None:
    noise = {F(-1): F(1, 4), F(0): F(1, 2), F(1): F(1, 4)}  # mean 0, variance 1/2
    s2 = F(1, 2)
    for k, m in [(1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (1, 4)]:
        means = [F(5 * i - 3) for i in range(k)]
        assert neyman_scott_expected_s2(noise, means, m) == F(m - 1, m) * s2


def test_neyman_scott_is_inconsistent() -> None:
    rng = random.Random(1948)
    groups = []
    for i in range(20000):
        mu = rng.uniform(-50, 50)
        groups.append([rng.gauss(mu, 1.0), rng.gauss(mu, 1.0)])
    _, s2 = neyman_scott_mle(groups)
    # more strata do not help: the estimate goes to sigma^2 / 2, not sigma^2
    assert abs(s2 - 0.5) < 0.03


def test_mixture_likelihood_is_unbounded() -> None:
    xs = [-1.2, 0.3, 0.8, 1.9, 2.4]
    values = [mixture_loglik(xs, [0.5, 0.5], [xs[0], 1.0], [10.0 ** -e, 1.0]) for e in range(1, 8)]
    assert all(b > a + 2 for a, b in zip(values, values[1:]))
