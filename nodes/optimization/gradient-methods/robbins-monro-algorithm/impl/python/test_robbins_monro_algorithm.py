# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robbins-monro-algorithm/. The authors are listed in prov/WZNBN6.jsonl.

import math
import random

from robbins_monro_algorithm import quantile_observer, robbins_monro

TOL = 1e-9
UNIT = lambda v: [min(max(v[0], 0.0), 1.0)]  # noqa: E731


def test_quantile_example_trace() -> None:
    samples = iter([0.81, 0.12, 0.47, 0.09, 0.66, 0.33, 0.21, 0.95])
    observe = quantile_observer(0.25, lambda r: next(samples))
    xs = robbins_monro(observe, [0.5], lambda n: 1.0 / (n + 2), 8, random.Random(0), UNIT)
    want = [0.5, 0.625, 0.375, 0.4375, 0.2875, 0.32917, 0.36488, 0.27113, 0.29891]
    for x, w in zip(xs, want):
        assert abs(x[0] - w) <= 5e-6


def test_quantile_mean_square_rate_monte_carlo() -> None:
    # h(x) = x - alpha on X = [0, 1] for xi ~ U(0, 1): mu = 1, B = 0, A = max(alpha^2, (1 - alpha)^2).
    alpha, x0, n0, iters, seeds = 0.25, 0.5, 2, 200, 400
    big_a = max(alpha**2, (1 - alpha) ** 2)
    nu = max(n0 * (x0 - alpha) ** 2, 4 * big_a)
    observe = quantile_observer(alpha, lambda r: r.random())
    total = [0.0] * (iters + 1)
    for t in range(seeds):
        xs = robbins_monro(observe, [x0], lambda n: 2.0 / (n + n0), iters, random.Random(900 + t), UNIT)
        for n, x in enumerate(xs):
            total[n] += (x[0] - alpha) ** 2
    for n in range(iters + 1):
        # The theorem bounds the expectation; the mean of 400 runs gets 10% slack.
        assert total[n] / seeds <= 1.1 * nu / (n + n0)


def linear_field_moments(m: list[list[float]], d0: list[float], s: float, steps: list[float]) -> list[float]:
    """Exact E||x_n - x*||^2 for H(x) = M (x - x*) + s z, z ~ N(0, I): mean and covariance recursions."""
    mean, cov = list(d0), [[0.0, 0.0], [0.0, 0.0]]
    out = [sum(v * v for v in mean)]
    for a in steps:
        t = [[(1.0 if i == j else 0.0) - a * m[i][j] for j in range(2)] for i in range(2)]
        mean = [sum(t[i][j] * mean[j] for j in range(2)) for i in range(2)]
        tc = [[sum(t[i][k] * cov[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        cov = [[sum(tc[i][k] * t[j][k] for k in range(2)) + (a * a * s * s if i == j else 0.0) for j in range(2)] for i in range(2)]
        out.append(sum(v * v for v in mean) + cov[0][0] + cov[1][1])
    return out


ROTATION = [[1.0, 1.0], [-1.0, 1.0]]  # not a gradient field; <M d, d> = |d|^2 and |M d|^2 = 2 |d|^2


def test_rate_on_a_non_gradient_field_exact_and_monte_carlo() -> None:
    root, x0, s = [1.0, -1.0], [3.0, 2.0], 0.7
    mu, big_b, big_a = 1.0, 2.0, 2 * s * s
    n0 = max(2, math.ceil(2 * big_b / mu**2))
    d0 = [a - b for a, b in zip(x0, root)]
    e0 = sum(v * v for v in d0)
    nu = max(n0 * e0, 4 * big_a / mu**2)
    iters = 80
    steps = [2.0 / (mu * (n + n0)) for n in range(iters)]
    exact = linear_field_moments(ROTATION, d0, s, steps)
    for n, e in enumerate(exact):
        assert e <= nu / (n + n0) + TOL

    def observe(x: list[float], r: random.Random) -> list[float]:
        d = [a - b for a, b in zip(x, root)]
        return [sum(ROTATION[i][j] * d[j] for j in range(2)) + s * r.gauss(0, 1) for i in range(2)]

    seeds = 300
    total, sq = [0.0] * (iters + 1), [0.0] * (iters + 1)
    for t in range(seeds):
        xs = robbins_monro(observe, x0, lambda n: steps[n], iters, random.Random(3000 + t))
        for n, x in enumerate(xs):
            v = sum((a - b) ** 2 for a, b in zip(x, root))
            total[n] += v
            sq[n] += v * v
    for n in range(iters + 1):
        mean = total[n] / seeds
        sd = math.sqrt(max(sq[n] / seeds - mean * mean, 0.0))
        assert abs(mean - exact[n]) <= 5 * sd / math.sqrt(seeds) + 1e-12


def test_mean_square_convergence_with_slow_steps() -> None:
    # a_n = (n + 1)^(-0.6): sum a_n diverges, sum a_n^2 converges, so Theorem 1 gives e_n -> 0.
    steps = [0.5 * (n + 1) ** -0.6 for n in range(20000)]
    exact = linear_field_moments(ROTATION, [2.0, 1.0], 0.7, steps)
    assert exact[-1] <= 1e-3 * exact[0]
    assert exact[2000] > exact[-1]


def test_step_conditions_are_needed() -> None:
    # Without noise and with sum a_n finite, x_n = prod (1 - a_j) stays above 1/2: no convergence to 0.
    xs = robbins_monro(lambda x, r: [x[0]], [1.0], lambda n: 1.0 / (n + 2) ** 2, 5000, random.Random(0))
    assert all(x[0] >= 0.5 - TOL for x in xs)
    # With a constant step a, sum a_n^2 diverges. On the rotation field T = I - a M has T T^T = ((1 - a)^2 + a^2) I,
    # so the stationary covariance is c I with c = a s^2 / (2 (1 - a)), and E||x_n - x*||^2 tends to a s^2 / (1 - a) > 0.
    a, s = 0.2, 0.7
    exact = linear_field_moments(ROTATION, [2.0, 1.0], s, [a] * 2000)
    assert abs(exact[-1] - a * s * s / (1 - a)) <= 1e-12


def test_zero_iterations() -> None:
    assert robbins_monro(lambda x, r: x, [1.0, 2.0], lambda n: 0.1, 0, random.Random(0)) == [[1.0, 2.0]]
