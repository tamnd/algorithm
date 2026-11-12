# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-filter/.

import itertools
import math
import random

from particle_filter import bootstrap_filter, multinomial_resample

# A two-state hidden Markov model. All probabilities are multiples of 1/4,
# so a grid of 4 uniform values per draw gives the exact law of the filter.
P1, STAY, HIT = 0.25, 0.75, 0.75


def init(rng):
    return 1 if rng.random() < P1 else 0


def move(x, t, rng):
    return x if rng.random() < STAY else 1 - x


def loglik(y, x, t):
    return math.log(HIT if y == x else 1 - HIT)


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
    """Returns a fixed list of values; used to enumerate all runs."""

    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop()


def draws(n, T):
    return n + n + 2 * n * (T - 1)


def test_likelihood_estimate_is_exactly_unbiased() -> None:
    grid = [(2 * k + 1) / 8 for k in range(4)]
    for n, ys in [(1, [1, 0, 0]), (2, [1, 0]), (1, [0, 1, 1, 0])]:
        k = draws(n, len(ys))
        runs = 0
        mean = 0.0
        for u in itertools.product(grid, repeat=k):
            rng = GridRng(u)
            _, log_z = bootstrap_filter(init, move, loglik, ys, n, rng)
            assert not rng.values
            mean += math.exp(log_z)
            runs += 1
        mean /= runs
        assert abs(mean - exact_z(ys)) < 1e-12


def test_log_likelihood_estimate_is_biased_down() -> None:
    grid = [(2 * k + 1) / 8 for k in range(4)]
    ys = [1, 0]
    logs = [bootstrap_filter(init, move, loglik, ys, 2, GridRng(u))[1] for u in itertools.product(grid, repeat=8)]
    assert sum(logs) / len(logs) < math.log(exact_z(ys))


# A scalar linear Gaussian model, where the Kalman filter is exact.
A, Q, R = 0.9, 0.5, 1.0


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


def gauss_init(rng):
    return rng.gauss(0.0, 1.0)


def gauss_move(x, t, rng):
    return A * x + rng.gauss(0.0, math.sqrt(Q))


def gauss_loglik(y, x, t):
    return -0.5 * (math.log(2 * math.pi * R) + (y - x) ** 2 / R)


YS = [0.8, 1.5, -0.3, 0.4, 1.1]


def test_likelihood_estimate_unbiased_on_a_gaussian_model() -> None:
    _, log_z = kalman(YS)
    rng = random.Random(7)
    ratios = [math.exp(bootstrap_filter(gauss_init, gauss_move, gauss_loglik, YS, 20, rng)[1] - log_z) for _ in range(2000)]
    mean = sum(ratios) / len(ratios)
    se = math.sqrt(sum((r - mean) ** 2 for r in ratios) / (len(ratios) - 1) / len(ratios))
    assert abs(mean - 1) < 4 * se


def test_filtered_mean_converges_to_the_kalman_mean() -> None:
    means, _ = kalman(YS)
    errors = []
    for n in (100, 1000, 10000):
        err = 0.0
        for seed in range(3):
            est, _ = bootstrap_filter(gauss_init, gauss_move, gauss_loglik, YS, n, random.Random(seed))
            err += max(abs(a - b) for a, b in zip(est, means))
        errors.append(err / 3)
    assert errors[0] > errors[1] > errors[2]
    assert errors[2] < 0.03


def test_multinomial_resample_counts() -> None:
    rng = random.Random(1)
    w = [0.1, 0.2, 0.3, 0.4]
    counts = [0] * 4
    for _ in range(2000):
        for a in multinomial_resample(w, 4, rng):
            counts[a] += 1
    for i in range(4):
        assert abs(counts[i] / 8000 - w[i]) < 0.02
