# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slice-sampling/. The authors are listed in prov/97GJYT.jsonl.

import math
import random
from collections import Counter

import pytest

from slice_sampling import slice_sampling, slice_update, step_out


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
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


class FixedRandom:
    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def test_trace_from_page() -> None:
    # 1 - 0.4 = 0.6 gives y = 0.6 f(x0); then U = 0.3, V = 0.6; then two shrinkage draws
    rng = FixedRandom([0.4, 0.3, 0.6, 0.1, 0.7])
    x1 = slice_update(lambda z: -0.5 * z * z, 0.5, 1.0, 4, rng)
    assert abs(x1 - 0.39) < 1e-12 and rng.values == []


def test_step_out_counts_do_not_depend_on_start() -> None:
    def inside(z):
        return -2.1 < z < 1.0 or 1.5 < z < 3.9

    theta, w = 0.25, 1.0
    starts = [-1.875, -0.5, 0.75, 1.75, 2.5, 3.5]
    for m in (1, 2, 3, 5, 8):
        counts = {}
        for x in starts:
            u = ((x - theta) / w) % 1.0
            counts[x] = Counter(step_out(inside, x, w, m, u, (j + 0.5) / m) for j in range(m))
        for x0 in starts:
            for (lo, hi), n in counts[x0].items():
                assert lo <= x0 < hi
                for x1 in starts:
                    if lo <= x1 < hi:
                        assert counts[x1][(lo, hi)] == n


def test_gaussian_one_dimensional() -> None:
    chain = slice_sampling(lambda x: -0.5 * x[0] ** 2, (4.0,), 1.0, 10, 20_000, random.Random(1))
    xs = [x[0] for x in chain]
    check_mean(xs, 0.0, 1.0)
    check_mean([v * v for v in xs], 1.0, math.sqrt(2.0))


def test_insensitive_to_width() -> None:
    # w far too large still gives correct moments
    chain = slice_sampling(lambda x: -0.5 * x[0] ** 2, (0.0,), 100.0, 3, 10_000, random.Random(2))
    xs = [x[0] for x in chain]
    check_mean(xs, 0.0, 1.0)
    check_mean([v * v for v in xs], 1.0, math.sqrt(2.0))


def test_correlated_gaussian_two_dimensional() -> None:
    rho = 0.8

    def log_f(x):
        return -0.5 * (x[0] ** 2 - 2 * rho * x[0] * x[1] + x[1] ** 2) / (1 - rho * rho)

    chain = slice_sampling(log_f, (0.0, 0.0), 1.0, 10, 20_000, random.Random(3))
    check_mean([x[0] for x in chain], 0.0, 1.0)
    check_mean([x[1] for x in chain], 0.0, 1.0)
    # E[X Y] = rho, Var(X Y) = 1 + rho^2
    check_mean([x[0] * x[1] for x in chain], rho, math.sqrt(1 + rho * rho))


def test_beta_target_with_bounded_support() -> None:
    # Beta(2, 5): mean 2/7, variance 10/392
    def log_f(x):
        z = x[0]
        return math.log(z) + 4 * math.log(1 - z) if 0 < z < 1 else -math.inf

    chain = slice_sampling(log_f, (0.5,), 0.5, 10, 20_000, random.Random(4))
    xs = [x[0] for x in chain]
    assert 0 < min(xs) and max(xs) < 1
    check_mean(xs, 2 / 7, math.sqrt(10 / 392))


def test_bad_inputs() -> None:
    with pytest.raises(ValueError):
        slice_sampling(lambda x: -math.inf, (0.0,), 1.0, 3, 5, random.Random(5))
    with pytest.raises(ValueError):
        slice_sampling(lambda x: 0.0, (0.0,), 0.0, 3, 5, random.Random(5))
