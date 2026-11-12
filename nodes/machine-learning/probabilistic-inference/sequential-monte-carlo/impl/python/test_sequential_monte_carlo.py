# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-monte-carlo/.

import itertools
import math
import random

from sequential_monte_carlo import ess, sequential_monte_carlo, systematic_resample

# Two-state hidden Markov model, with a uniform proposal on {0, 1}.
P1, STAY, HIT = 0.25, 0.75, 0.75


def init(rng):
    return 1 if rng.random() < P1 else 0


def uniform_proposal(x, t, rng):
    return 1 if rng.random() < 0.5 else 0


def binary_log_inc(ys):
    def f(x_prev, x, t):
        trans = STAY if x == x_prev else 1 - STAY
        lik = HIT if ys[t - 1] == x else 1 - HIT
        return math.log(lik * trans / 0.5)

    return f


def exact_z(ys):
    total = 0.0
    for path in itertools.product((0, 1), repeat=len(ys) + 1):
        p = P1 if path[0] == 1 else 1 - P1
        for t, y in enumerate(ys, 1):
            p *= STAY if path[t] == path[t - 1] else 1 - STAY
            p *= HIT if y == path[t] else 1 - HIT
        total += p
    return total


class GridRng:
    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop()


def test_sis_likelihood_estimate_is_exactly_unbiased() -> None:
    grid = [(2 * k + 1) / 8 for k in range(4)]
    for n, ys in [(2, [1, 0, 0]), (1, [0, 1, 1, 0])]:
        k = n * (len(ys) + 1)
        total, runs = 0.0, 0
        for u in itertools.product(grid, repeat=k):
            rng = GridRng(u)
            _, log_z, resampled, _ = sequential_monte_carlo(
                init, uniform_proposal, binary_log_inc(ys), len(ys), n, rng, threshold=0.0
            )
            assert not rng.values and resampled == []
            total += math.exp(log_z)
            runs += 1
        assert abs(total / runs - exact_z(ys)) < 1e-12


# Scalar linear Gaussian model with the locally optimal proposal.
A, Q, R = 0.9, 0.5, 1.0
YS = [0.8, 1.5, -0.3, 0.4, 1.1, 2.0, 1.2, -0.5, 0.0, 0.7]


def kalman(ys):
    m, P, log_z, means = 0.0, 1.0, 0.0, []
    for y in ys:
        m, P = A * m, A * A * P + Q
        S = P + R
        log_z += -0.5 * (math.log(2 * math.pi * S) + (y - m) ** 2 / S)
        K = P / S
        m, P = m + K * (y - m), P - K * S * K
        means.append(m)
    return means, log_z


S2 = 1.0 / (1.0 / Q + 1.0 / R)


def optimal_proposal(x, t, rng):
    mean = S2 * (A * x / Q + YS[t - 1] / R)
    return rng.gauss(mean, math.sqrt(S2))


def optimal_log_inc(x_prev, x, t):
    # p(y_t | x_(t-1)) = N(y_t; A x_(t-1), Q + R), which does not depend on x_t.
    v = Q + R
    return -0.5 * (math.log(2 * math.pi * v) + (YS[t - 1] - A * x_prev) ** 2 / v)


def gauss_init(rng):
    return rng.gauss(0.0, 1.0)


def test_adaptive_smc_matches_kalman_means() -> None:
    means, _ = kalman(YS)
    est, _, resampled, _ = sequential_monte_carlo(
        gauss_init, optimal_proposal, optimal_log_inc, len(YS), 5000, random.Random(1)
    )
    assert max(abs(a - b) for a, b in zip(est, means)) < 0.05
    assert 0 < len(resampled) < len(YS)


def test_adaptive_smc_likelihood_is_unbiased() -> None:
    _, log_z = kalman(YS)
    rng = random.Random(2)
    ratios = []
    for _ in range(1000):
        _, lz, _, _ = sequential_monte_carlo(gauss_init, optimal_proposal, optimal_log_inc, len(YS), 10, rng)
        ratios.append(math.exp(lz - log_z))
    mean = sum(ratios) / len(ratios)
    se = math.sqrt(sum((r - mean) ** 2 for r in ratios) / (len(ratios) - 1) / len(ratios))
    assert abs(mean - 1) < 4 * se


def test_resampling_follows_the_threshold() -> None:
    for threshold in (0.0, 0.3, 0.5, 0.9, 1.01):
        _, _, resampled, seen = sequential_monte_carlo(
            gauss_init, optimal_proposal, optimal_log_inc, len(YS), 200, random.Random(3), threshold
        )
        assert resampled == [t for t, e in enumerate(seen, 1) if e < threshold * 200]
        if threshold == 0.0:
            assert resampled == []
        if threshold > 1:
            assert resampled == list(range(1, len(YS) + 1))


def test_ess_and_systematic_resample() -> None:
    assert abs(ess([0.25] * 4) - 4) < 1e-12
    assert ess([1.0, 0.0, 0.0]) == 1
    assert abs(ess([0.5, 0.25, 0.25]) - 1 / 0.375) < 1e-12

    class Fixed:
        def random(self):
            return 0.3

    assert systematic_resample([0.1, 0.2, 0.3, 0.4], Fixed()) == [0, 2, 2, 3]
