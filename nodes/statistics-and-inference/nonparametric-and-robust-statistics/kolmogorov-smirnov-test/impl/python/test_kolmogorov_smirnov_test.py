# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kolmogorov-smirnov-test/. The authors are listed in prov/DWDQWW.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from kolmogorov_smirnov_test import (
    kolmogorov_cdf, kolmogorov_sf, ks_1samp, ks_2samp, ks_2samp_stat, ks_statistic, smirnov_sf,
)

X = [0.42, 0.06, 1.95, 0.88, 0.13, 3.10, 0.27, 0.71, 0.09, 0.35]


def exp_cdf(v: float) -> float:
    return 1.0 - math.exp(-v) if v > 0 else 0.0


def box_probability(lo: list[Fraction], hi: list[Fraction]) -> Fraction:
    """P(lo_i < U_(i) < hi_i for all i) for the order statistics of n uniforms, exactly.

    The density of the order statistics is n! on 0 < u_1 < ... < u_n < 1. Integrate
    u_1, then u_2, ... as piecewise polynomials in exact Fractions."""
    n = len(lo)
    pts = sorted(set([Fraction(0), Fraction(1)] + lo + hi))
    pieces = len(pts) - 1

    def value(p: list[Fraction], u: Fraction) -> Fraction:
        return sum(c * u**i for i, c in enumerate(p))

    def inside(i: int, t: int) -> bool:
        return lo[i] <= pts[t] and pts[t + 1] <= hi[i]

    f = [[Fraction(1)] if inside(0, t) else [Fraction(0)] for t in range(pieces)]
    for i in range(1, n + 1):
        g, acc = [], Fraction(0)
        for t in range(pieces):  # g(u) = integral of f from 0 to u
            p = [Fraction(0)] + [c / (j + 1) for j, c in enumerate(f[t])]
            p[0] += acc - value(p, pts[t])
            g.append(p)
            acc = value(p, pts[t + 1])
        if i == n:
            return acc * math.factorial(n)
        f = [g[t] if inside(i, t) else [Fraction(0)] for t in range(pieces)]
    return Fraction(1)


def exact_two_sided(n: int, d: Fraction) -> Fraction:
    """P(D_n < d): i/n - d < U_(i) < (i - 1)/n + d for every i."""
    lo = [max(Fraction(0), Fraction(i, n) - d) for i in range(1, n + 1)]
    hi = [min(Fraction(1), Fraction(i - 1, n) + d) for i in range(1, n + 1)]
    return box_probability(lo, hi)


def exact_one_sided(n: int, d: Fraction) -> Fraction:
    """P(D_n^+ < d): U_(i) > i/n - d for every i."""
    lo = [max(Fraction(0), Fraction(i, n) - d) for i in range(1, n + 1)]
    return box_probability(lo, [Fraction(1)] * n)


def test_page_example() -> None:
    d, d_plus, d_minus = ks_statistic(X, exp_cdf)
    assert (round(d, 4), round(d_plus, 4), round(d_minus, 4)) == (0.2570, 0.2570, 0.0582)
    assert ks_1samp(X, exp_cdf)[1] == pytest.approx(0.44931051, abs=1e-7)
    assert ks_1samp(X, exp_cdf, method="asymptotic")[1] == pytest.approx(0.52337859, abs=1e-7)
    assert ks_1samp(X, exp_cdf, "greater")[1] == pytest.approx(0.22668362, abs=1e-7)
    a = [1.2, 3.4, 2.2, 5.1, 4.4, 3.9]
    b = [0.3, 1.1, 2.0, 0.9, 1.7, 2.5, 0.5]
    assert ks_2samp_stat(a, b) == (29, 6, 7)
    assert ks_2samp(a, b)[1] == pytest.approx(116 / 1716, rel=1e-12)


def test_matrix_method_against_exact_integration() -> None:
    for n in range(1, 8):
        for d in (Fraction(1, 9), Fraction(1, 5), Fraction(2, 7), Fraction(3, 10), Fraction(1, 2),
                  Fraction(3, 5), Fraction(5, 7), Fraction(9, 10)):
            want = float(exact_two_sided(n, d))
            assert kolmogorov_cdf(n, float(d)) == pytest.approx(want, rel=1e-11, abs=1e-14)


def test_one_observation() -> None:
    # D_1 = max(u, 1 - u), so P(D_1 < d) = 2d - 1 for 1/2 <= d <= 1.
    for d in (0.55, 0.7, 0.95):
        assert kolmogorov_cdf(1, d) == pytest.approx(2 * d - 1, rel=1e-12)
    assert kolmogorov_cdf(1, 0.4) == 0.0


def test_one_sided_sum_against_exact_integration() -> None:
    for n in range(1, 8):
        for d in (Fraction(1, 9), Fraction(1, 4), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5)):
            assert smirnov_sf(n, float(d)) == pytest.approx(float(1 - exact_one_sided(n, d)), rel=1e-11)


def test_two_sided_is_twice_one_sided_above_half() -> None:
    # For d >= 1/2 the events D+ >= d and D- >= d cannot both happen.
    for n in range(1, 8):
        for d in (Fraction(1, 2), Fraction(3, 5), Fraction(4, 5)):
            assert 1 - exact_two_sided(n, d) == 2 * (1 - exact_one_sided(n, d))


def test_statistic_against_direct_supremum() -> None:
    rng = random.Random(1)
    for _ in range(200):
        x = [rng.random() for _ in range(rng.randint(1, 12))]
        n = len(x)
        best_plus = best_minus = 0.0
        for t in x:  # the supremum is attained at a data point or just before it
            at = sum(v <= t for v in x) / n
            before = sum(v < t for v in x) / n
            best_plus = max(best_plus, at - t)
            best_minus = max(best_minus, t - before)
        d, d_plus, d_minus = ks_statistic(x, lambda v: v)
        assert d_plus == pytest.approx(best_plus, abs=1e-15)
        assert d_minus == pytest.approx(best_minus, abs=1e-15)
        assert d == max(d_plus, d_minus)


def test_two_sample_against_all_labelings() -> None:
    rng = random.Random(2)
    for _ in range(40):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        pooled = rng.sample(range(100), m + n)  # distinct values
        x, y = pooled[:m], pooled[m:]

        def dist(a: list[int], b: list[int]) -> Fraction:
            return max(abs(Fraction(sum(v <= t for v in a), len(a)) - Fraction(sum(v <= t for v in b), len(b)))
                       for t in a + b)

        observed = dist(x, y)
        assert Fraction(ks_2samp(x, y)[0]).limit_denominator(1000) == observed
        hits = total = 0
        for idx in itertools.combinations(range(m + n), m):
            a = [pooled[i] for i in idx]
            b = [pooled[i] for i in range(m + n) if i not in idx]
            total += 1
            hits += dist(a, b) >= observed
        assert ks_2samp(x, y)[1] == pytest.approx(hits / total, rel=1e-12)


def test_limit_law() -> None:
    assert kolmogorov_sf(1.3580986393) == pytest.approx(0.05, abs=1e-9)
    # The two series used below and above x = 1 agree.
    left = 1.0 - math.sqrt(2 * math.pi) * sum(math.exp(-((2 * k - 1) ** 2) * math.pi**2 / 8) for k in range(1, 30))
    assert kolmogorov_sf(1.0) == pytest.approx(left, abs=1e-14)
    assert kolmogorov_cdf(400, 1.2 / 20) == pytest.approx(1 - kolmogorov_sf(1.2), abs=1e-2)


def test_size_monte_carlo() -> None:
    rng = random.Random(64)
    r, alpha = 1500, 0.05
    hits = sum(ks_1samp([rng.random() for _ in range(10)], lambda v: v)[1] <= alpha for _ in range(r))
    assert hits / r <= alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_edges() -> None:
    with pytest.raises(ValueError):
        ks_1samp([], exp_cdf)
    with pytest.raises(ValueError):
        ks_1samp([1.0], exp_cdf, "both")
    with pytest.raises(ValueError):
        ks_2samp([], [1.0])
    assert ks_2samp([1.0, 2.0], [1.0, 2.0])[0] == 0.0
