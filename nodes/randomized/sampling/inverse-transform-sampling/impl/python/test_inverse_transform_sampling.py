# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-transform-sampling/. The authors are listed in prov/FC22KF.jsonl.

import bisect
import math
import random
from fractions import Fraction

import pytest

from inverse_transform_sampling import (
    cauchy,
    discrete_inverse,
    discrete_inverse_float,
    exponential,
    generalized_inverse,
    inverse_transform,
    prefix_sums,
)


class FixedInt:
    def __init__(self, t):
        self.t = t

    def randrange(self, n):
        assert 0 <= self.t < n
        return self.t


def exact_law(weights, sampler):
    prefix = prefix_sums(weights)
    W = prefix[-1]
    counts = [0] * len(weights)
    for t in range(W):  # every value of the random integer once
        counts[sampler(prefix, FixedInt(t))] += 1
    return [Fraction(c, W) for c in counts]


def test_example() -> None:
    # Weights 1, 0, 2, 3, 2: prefix sums 1, 1, 3, 6, 8.
    prefix = prefix_sums([1, 0, 2, 3, 2])
    assert prefix == [1, 1, 3, 6, 8]
    got = [discrete_inverse(prefix, FixedInt(t)) for t in range(8)]
    assert got == [0, 2, 2, 3, 3, 3, 4, 4]
    # Exponential with rate 2 at U = 0.5: ln 2 / 2.
    class Half:
        def random(self):
            return 0.5

    assert abs(inverse_transform(lambda u: -math.log1p(-u) / 2, Half()) - math.log(2) / 2) < 1e-15


def test_exact_law_small_cases() -> None:
    rng = random.Random(1)
    cases = [[1], [1, 1], [0, 3, 0, 1], [5, 0], [1, 0, 2, 3, 2]]
    for _ in range(300):
        n = rng.randint(1, 7)
        w = [rng.randint(0, 6) for _ in range(n)]
        if sum(w) > 0:
            cases.append(w)
    for w in cases:
        W = sum(w)
        assert exact_law(w, discrete_inverse) == [Fraction(x, W) for x in w]


def test_wrong_variant_fails() -> None:
    # Searching with "prefix >= t" instead of "prefix > t" is off by one.
    def wrong(prefix, rng):
        t = rng.randrange(prefix[-1])
        return bisect.bisect_left(prefix, t)

    w = [1, 2, 3]
    assert exact_law(w, wrong) != [Fraction(x, 6) for x in w]


def test_generalized_inverse_lemma() -> None:
    # F has jumps and a flat part (the value 3 has probability 0).
    values = [1, 2, 3, 4]
    cdf = [Fraction(1, 4), Fraction(1, 2), Fraction(1, 2), Fraction(1)]
    grid = [Fraction(j, 24) for j in range(1, 25)]
    for u in grid:
        g = generalized_inverse(values, cdf, u)
        for x, fx in zip(values, cdf):
            assert (g <= x) == (u <= fx)
    # The set {u : F^{-1}(u) = x_i} is the interval (F(x_{i-1}), F(x_i)].
    for u in grid:
        g = generalized_inverse(values, cdf, u)
        i = values.index(g)
        lo = cdf[i - 1] if i > 0 else Fraction(0)
        assert lo < u <= cdf[i]
    assert all(generalized_inverse(values, cdf, u) != 3 for u in grid)


def phi_exp(rate):
    return lambda x: 1.0 - math.exp(-rate * x) if x > 0 else 0.0


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


def test_continuous_ks_and_moments() -> None:
    rng = random.Random(42)
    m = 40000
    xs = [exponential(2.0, rng) for _ in range(m)]
    assert ks_statistic(xs, phi_exp(2.0)) < ks_threshold(m)
    assert abs(sum(xs) / m - 0.5) < 6 * 0.5 / math.sqrt(m)
    ys = [cauchy(rng) for _ in range(m)]
    assert ks_statistic(ys, lambda t: 0.5 + math.atan(t) / math.pi) < ks_threshold(m)


def test_continuous_wrong_variant_fails() -> None:
    # Multiplying by the rate instead of dividing gives mean 2, not 1/2.
    rng = random.Random(43)
    m = 20000
    xs = [inverse_transform(lambda u: -2.0 * math.log1p(-u), rng) for _ in range(m)]
    assert ks_statistic(xs, phi_exp(2.0)) > ks_threshold(m)


def test_float_discrete_chi_squared() -> None:
    rng = random.Random(7)
    p = [0.1, 0.2, 0.3, 0.4]
    m = 40000
    counts = [0] * 4
    for _ in range(m):
        counts[discrete_inverse_float(p, rng)] += 1
    chi2 = sum((c - m * q) ** 2 / (m * q) for c, q in zip(counts, p))
    assert chi2 < 40.0  # 3 degrees of freedom; Pr[chi2 > 40] < 1e-8


def test_errors() -> None:
    with pytest.raises(ValueError):
        prefix_sums([0, 0])
    with pytest.raises(ValueError):
        prefix_sums([1, -1])
