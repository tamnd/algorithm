# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ratio-of-uniforms/. The authors are listed in prov/3SHGH5.jsonl.

import math
import random

from ratio_of_uniforms import (
    SQRT_2_OVER_E,
    ratio_of_uniforms,
    ratio_of_uniforms_counted,
    rou_cauchy,
    rou_exponential,
    rou_normal,
    rou_normal_counted,
)


def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def ks_statistic(xs, cdf) -> float:
    xs = sorted(xs)
    m = len(xs)
    d = 0.0
    for i, x in enumerate(xs):
        c = cdf(x)
        d = max(d, (i + 1) / m - c, c - i / m)
    return d


def ks_threshold(m: int, alpha: float = 1e-9) -> float:
    # Dvoretzky-Kiefer-Wolfowitz with Massart's constant: Pr[D > t] <= 2 exp(-2 m t^2).
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * m))


class Fixed:
    def __init__(self, vals):
        self.vals = list(vals)

    def random(self):
        return self.vals.pop(0)


def gauss(x: float) -> float:
    return math.exp(-0.5 * x * x)


def test_example() -> None:
    b = SQRT_2_OVER_E
    # random() = r gives U = 1 - r and V = b (2 r' - 1).
    # Try 1: U = 0.2, V = 0.8: X = 4 > sqrt(-4 ln 0.2), reject.
    # Try 2: U = 0.5, V = 0.3: X = 0.6, accept.
    vals = [0.8, (0.8 / b + 1) / 2, 0.5, (0.3 / b + 1) / 2]
    x, tries = rou_normal_counted(Fixed(vals))
    assert tries == 2 and abs(x - 0.6) < 1e-12
    x, tries = ratio_of_uniforms_counted(gauss, 1.0, -b, b, Fixed(vals))
    assert tries == 2 and abs(x - 0.6) < 1e-12


def test_normal_ks_and_moments() -> None:
    rng = random.Random(1977)
    m = 40000
    xs = [rou_normal(rng) for _ in range(m)]
    assert ks_statistic(xs, phi) < ks_threshold(m)
    mean = sum(xs) / m
    var = sum(x * x for x in xs) / m
    assert abs(mean) < 0.03 and abs(var - 1) < 0.05


def test_generic_matches_normal_and_acceptance_rate() -> None:
    rng = random.Random(3)
    m = 40000
    b = SQRT_2_OVER_E
    xs, total = [], 0
    for _ in range(m):
        x, t = ratio_of_uniforms_counted(gauss, 1.0, -b, b, rng)
        xs.append(x)
        total += t
    assert ks_statistic(xs, phi) < ks_threshold(m)
    # Acceptance probability: (integral of h / 2) / box area = sqrt(pi e) / 4.
    p = math.sqrt(math.pi * math.e) / 4
    assert abs(p - 0.7306) < 1e-4
    sd = math.sqrt((1 - p) / p ** 2 / m)
    assert abs(total / m - 1 / p) < 6 * sd


def test_cauchy_and_exponential() -> None:
    rng = random.Random(8)
    m = 40000
    xs = [rou_cauchy(rng) for _ in range(m)]
    assert ks_statistic(xs, lambda t: 0.5 + math.atan(t) / math.pi) < ks_threshold(m)
    ys = [rou_exponential(rng) for _ in range(m)]
    assert min(ys) >= 0.0
    assert ks_statistic(ys, lambda t: 1.0 - math.exp(-t) if t > 0 else 0.0) < ks_threshold(m)
    assert abs(sum(ys) / m - 1.0) < 0.03


def test_wrong_variant_fails() -> None:
    # Testing U <= h(X) instead of U^2 <= h(X) gives density proportional to h^2,
    # here N(0, 1/2).
    rng = random.Random(4)
    m = 20000
    b = SQRT_2_OVER_E
    xs = []
    while len(xs) < m:
        u = 1.0 - rng.random()
        v = b * (2.0 * rng.random() - 1.0)
        if u <= gauss(v / u):
            xs.append(v / u)
    assert ks_statistic(xs, phi) > ks_threshold(m)
    assert ks_statistic(xs, lambda t: phi(t * math.sqrt(2.0))) < ks_threshold(m)


def test_box_too_small_fails() -> None:
    # A box that misses part of C cuts off the tails.
    rng = random.Random(6)
    m = 40000
    xs = [ratio_of_uniforms(gauss, 1.0, -0.3, 0.3, rng) for _ in range(m)]
    assert ks_statistic(xs, phi) > ks_threshold(m)
