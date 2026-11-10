# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-walk-metropolis/. The authors are listed in prov/C4EVM2.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from random_walk_metropolis import cycle_transition_matrix, random_walk_metropolis


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


def test_trace_from_page() -> None:
    # ratios of the example table
    assert abs(math.exp(std_normal((1.2,)) - std_normal((0.0,))) - 0.487) < 1e-3
    assert abs(math.exp(std_normal((3.12,)) - std_normal((1.2,))) - 0.0158) < 1e-3
    assert abs(math.exp(std_normal((-0.6,)) - std_normal((-1.2,))) - 1.716) < 1e-3


def test_one_dimensional_gaussian_moments() -> None:
    chain, _ = random_walk_metropolis(std_normal, (3.0,), 2.4, 60_000, random.Random(1))
    xs = [x[0] for x in chain[1000:]]
    check_mean(xs, 0.0, 1.0)
    # E X^2 = 1 and Var X^2 = 2
    check_mean([v * v for v in xs], 1.0, math.sqrt(2.0))


def test_two_dimensional_correlated_gaussian() -> None:
    # covariance [[4, 1.2], [1.2, 1]], correlation 0.6
    a, b, c = 4.0, 1.2, 1.0
    det = a * c - b * b

    def log_t(x):
        u, v = x[0] - 1.0, x[1] + 2.0
        return -0.5 * (c * u * u - 2 * b * u * v + a * v * v) / det

    chain, acc = random_walk_metropolis(log_t, (1.0, -2.0), 1.5, 80_000, random.Random(2))
    assert 0.15 < acc / len(chain) < 0.7
    us = [x[0] for x in chain]
    vs = [x[1] for x in chain]
    check_mean(us, 1.0, 2.0)
    check_mean(vs, -2.0, 1.0)
    # E[(U - 1)(V + 2)] = 1.2, and Var of the product is a c + b^2 = 5.44
    check_mean([(u - 1.0) * (v + 2.0) for u, v in zip(us, vs)], 1.2, math.sqrt(a * c + b * b))


@pytest.mark.parametrize("sigma", [1.0, 5.0])
def test_acceptance_rate_formula(sigma) -> None:
    rng = random.Random(3)
    x0 = (rng.gauss(0.0, 1.0),)  # start in stationarity
    chain, _ = random_walk_metropolis(std_normal, x0, sigma, 60_000, rng)
    moved = [1.0 if chain[t] != chain[t - 1] else 0.0 for t in range(1, len(chain))]
    exact = 2 / math.pi * math.atan(2 / sigma)
    check_mean(moved, exact, math.sqrt(exact * (1 - exact)))


def test_truncated_target_rejects_outside() -> None:
    # half-normal on x > 0 has mean sqrt(2 / pi) and standard deviation sqrt(1 - 2 / pi)
    def log_t(x):
        return -0.5 * x[0] * x[0] if x[0] > 0 else -math.inf

    chain, _ = random_walk_metropolis(log_t, (1.0,), 1.5, 60_000, random.Random(4))
    xs = [x[0] for x in chain]
    assert min(xs) > 0
    check_mean(xs, math.sqrt(2 / math.pi), math.sqrt(1 - 2 / math.pi))


def test_cycle_matrix_exact() -> None:
    w = [F(1), F(3), F(2), F(5), F(4)]
    p = cycle_transition_matrix(w)
    z = sum(w)
    pi = [v / z for v in w]
    n = len(w)
    assert all(sum(row) == 1 and min(row) >= 0 for row in p)
    assert all(pi[x] * p[x][y] == pi[y] * p[y][x] for x in range(n) for y in range(n))
    assert all(sum(pi[x] * p[x][y] for x in range(n)) == pi[y] for y in range(n))
    assert p[0] == [F(0), F(1, 2), F(0), F(0), F(1, 2)]
    assert p[1] == [F(1, 6), F(1, 2), F(1, 3), F(0), F(0)]


def test_bad_inputs() -> None:
    with pytest.raises(ValueError):
        random_walk_metropolis(lambda x: -math.inf, (0.0,), 1.0, 5, random.Random(5))
    with pytest.raises(ValueError):
        random_walk_metropolis(std_normal, (0.0,), 0.0, 5, random.Random(5))
    assert random_walk_metropolis(std_normal, (0.0,), 1.0, 0, random.Random(5)) == ([], 0)
