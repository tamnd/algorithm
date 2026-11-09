# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-gradient-descent/. The authors are listed in prov/BTB2HV.jsonl.

import math
import random

from stochastic_gradient_descent import average, minibatch, sgd

TOL = 1e-9


def test_step_one_over_k_gives_the_running_mean() -> None:
    # f(x, xi) = (x - xi)^2 / 2: SGD with step 1/(k+1) returns the mean of the samples seen so far.
    seen: list[float] = []

    def oracle(x: list[float], rng: random.Random) -> list[float]:
        xi = rng.gauss(3.0, 2.0)
        seen.append(xi)
        return [x[0] - xi]

    xs = sgd(oracle, [100.0], lambda k: 1.0 / (k + 1), 50, random.Random(61))
    for k in range(1, 51):
        assert abs(xs[k][0] - sum(seen[:k]) / k) <= 1e-12 * (1 + abs(xs[k][0]))


def exact_expected_errors(d: list[float], e0: list[float], s2: float, steps: list[float]) -> list[float]:
    """E||x_k - x*||^2 for F = sum d_i (x_i - c_i)^2 / 2 with independent N(0, s2) noise per coordinate.

    Per coordinate, e_(k+1) = (1 - eta d_i)^2 e_k + eta^2 s2 holds exactly.
    """
    e, out = list(e0), [sum(e0)]
    for eta in steps:
        e = [(1 - eta * di) ** 2 * ei + eta * eta * s2 for di, ei in zip(d, e)]
        out.append(sum(e))
    return out


def test_strongly_convex_rate_exact_expectation_and_monte_carlo() -> None:
    n, s = 3, 0.5
    d = [1.0, 2.0, 4.0]
    c = [1.0, -2.0, 0.5]
    mu, lf = min(d), max(d)
    sigma2 = n * s * s
    k0 = math.ceil(2 * lf / mu)  # k0 >= 2 kappa, so the first step is at most 1/L
    x0 = [3.0, 1.0, -2.0]
    a0 = sum((a - b) ** 2 for a, b in zip(x0, c))
    nu = max(k0 * a0, 4 * sigma2 / mu**2)
    iters = 60
    steps = [2.0 / (mu * (k + k0)) for k in range(iters)]
    assert steps[0] <= 1 / lf + TOL
    exact = exact_expected_errors(d, [(a - b) ** 2 for a, b in zip(x0, c)], s * s, steps)
    for k, e in enumerate(exact):
        assert e <= nu / (k + k0) + TOL  # the theorem, checked on the exact expectation

    def oracle(x: list[float], r: random.Random) -> list[float]:
        return [di * (xi - ci) + r.gauss(0, s) for di, xi, ci in zip(d, x, c)]

    seeds = 400
    total = [0.0] * (iters + 1)
    sq = [0.0] * (iters + 1)
    for t in range(seeds):
        xs = sgd(oracle, x0, lambda k: steps[k], iters, random.Random(5000 + t))
        for k, x in enumerate(xs):
            v = sum((a - b) ** 2 for a, b in zip(x, c))
            total[k] += v
            sq[k] += v * v
    for k in range(iters + 1):
        mean = total[k] / seeds
        sd = math.sqrt(max(sq[k] / seeds - mean * mean, 0.0))
        # The Monte Carlo mean agrees with the exact expectation within 5 standard errors.
        assert abs(mean - exact[k]) <= 5 * sd / math.sqrt(seeds) + 1e-12


def test_constant_step_noise_ball() -> None:
    d = [0.5, 1.0, 3.0]
    mu, lf = min(d), max(d)
    s2 = 0.3
    sigma2 = len(d) * s2
    for eta in (0.05, 0.1, 1.0 / lf):
        e0 = [4.0, 1.0, 9.0]
        exact = exact_expected_errors(d, e0, s2, [eta] * 300)
        for k, e in enumerate(exact):
            assert e <= (1 - mu * eta) ** k * sum(e0) + eta * sigma2 / mu + TOL
        # The ball does not vanish: the coordinate with d_i = mu tends to eta s2 / (mu (2 - eta mu)).
        assert exact[-1] >= 0.99 * eta * s2 / (mu * (2 - eta * mu))


def test_convex_nonsmooth_averaged_rate() -> None:
    # f(x, xi) = |x - xi|, xi ~ U(0, 1), on X = [-1, 2]. F(x) = x^2 - x + 1/2 on [0, 1], F* = 1/4.
    def big_f(x: float) -> float:
        if x <= 0:
            return 0.5 - x
        if x >= 1:
            return x - 0.5
        return x * x - x + 0.5

    def oracle(x: list[float], r: random.Random) -> list[float]:
        xi = r.random()
        return [1.0 if x[0] > xi else -1.0]

    clip = lambda v: [min(max(v[0], -1.0), 2.0)]  # noqa: E731
    x0, g_bound, iters = [2.0], 1.0, 400
    r = abs(x0[0] - 0.5)
    eta = r / (g_bound * math.sqrt(iters))
    seeds = 300
    gap = 0.0
    for t in range(seeds):
        xs = sgd(oracle, x0, eta, iters, random.Random(7000 + t), clip)
        gap += big_f(average(xs[:iters])[0]) - 0.25
    # The bound R G / sqrt(K) holds for the expectation; the mean of 300 runs gets 10% slack.
    assert gap / seeds <= 1.1 * r * g_bound / math.sqrt(iters)


def test_minibatch_is_unbiased_with_smaller_variance() -> None:
    def sample(x: list[float], r: random.Random) -> list[float]:
        return [x[0] + r.gauss(0, 1)]

    rng = random.Random(64)
    single = [sample([2.0], rng)[0] for _ in range(4000)]
    batch = [minibatch(sample, 8)([2.0], rng)[0] for _ in range(4000)]
    m1, m8 = sum(single) / 4000, sum(batch) / 4000
    v1 = sum((a - m1) ** 2 for a in single) / 4000
    v8 = sum((a - m8) ** 2 for a in batch) / 4000
    assert abs(m1 - 2.0) <= 0.1 and abs(m8 - 2.0) <= 0.05
    assert abs(v8 * 8 - v1) <= 0.25 * v1


def test_zero_iterations() -> None:
    assert sgd(lambda x, r: x, [1.0], 0.1, 0, random.Random(0)) == [[1.0]]
