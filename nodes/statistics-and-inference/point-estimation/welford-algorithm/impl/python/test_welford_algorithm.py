# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welford-algorithm/. The authors are listed in prov/3F3F57.jsonl.

import math
import random
from fractions import Fraction

from stdist import chi2_cdf, chi2_ppf
from welford_algorithm import RunningVariance, welford_algorithm

U = 2.0 ** -53


def two_pass(xs):
    """Oracle: the mean, then the sum of squared deviations, in exact arithmetic."""
    n = len(xs)
    m = sum(xs, Fraction(0)) / n
    s = sum(((x - m) ** 2 for x in xs), Fraction(0))
    return m, s / (n - 1), s


def test_running_example_trace():
    acc = RunningVariance()
    trace = []
    for x in (3, 7, 7, 9, 14):
        acc.push(Fraction(x))
        trace.append((acc.mean, acc.ss))
    assert trace == [
        (3, 0), (5, 8), (Fraction(17, 3), Fraction(32, 3)), (Fraction(13, 2), 19), (8, 64),
    ]
    assert welford_algorithm([Fraction(x) for x in (3, 7, 7, 9, 14)]) == (8, 16, 64)
    assert acc.variance() == 16 and acc.variance(ddof=0) == Fraction(64, 5)


def test_exact_against_two_pass_on_random_inputs():
    rng = random.Random(20261114)
    for _ in range(600):
        n = rng.randint(2, 12)
        xs = [Fraction(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(n)]
        assert welford_algorithm(xs) == two_pass(xs)
        acc = RunningVariance()
        acc.extend(xs)
        m, v, s = two_pass(xs)
        assert acc.count == n and acc.mean == m and acc.ss == s
        for k in range(1, n + 1):
            pre = RunningVariance()
            pre.extend(xs[:k])
            mk = sum(xs[:k], Fraction(0)) / k
            assert pre.mean == mk
            assert pre.ss == sum(((x - mk) ** 2 for x in xs[:k]), Fraction(0))


def test_float_error_is_small_on_shifted_data():
    rng = random.Random(7)
    for c in (0.0, 1e3, 1e6):
        for n in (2, 10, 300):
            xs = [c + rng.gauss(0.0, 1.0) for _ in range(n)]
            _, v_exact, s_exact = two_pass([Fraction(x) for x in xs])
            m, v, s = welford_algorithm(xs)
            kappa = math.sqrt(1 + n * float(sum(map(Fraction, xs)) / n) ** 2 / float(s_exact))
            rel = abs(Fraction(v) - v_exact) / v_exact
            assert rel <= 50 * n * kappa * U


def test_textbook_formula_cancels_but_welford_does_not():
    xs = [1e9 + t for t in (3, 7, 7, 9, 14)]
    n = len(xs)
    textbook = (sum(x * x for x in xs) - n * (sum(xs) / n) ** 2) / (n - 1)
    assert textbook == -256.0
    _, v, _ = welford_algorithm(xs)
    assert abs(v - 16) <= 1e-6 * 16


def test_short_inputs():
    acc = RunningVariance()
    acc.push(5.0)
    assert acc.mean == 5.0 and acc.ss == 0.0 and acc.variance(ddof=0) == 0.0
    for bad in ([], [1.0]):
        try:
            welford_algorithm(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_chi_square_law_monte_carlo():
    # (n - 1) S^2 / sigma^2 is chi-square with n - 1 degrees of freedom for normal data.
    rng = random.Random(12345)
    n, sigma, r = 5, 2.0, 2000
    stats = []
    for _ in range(r):
        xs = [1000.0 + sigma * rng.gauss(0.0, 1.0) for _ in range(n)]
        _, v, _ = welford_algorithm(xs)
        stats.append((n - 1) * v / sigma ** 2)
    for p in (0.1, 0.5, 0.9):
        q = chi2_ppf(p, n - 1)
        assert abs(chi2_cdf(q, n - 1) - p) < 1e-9
        emp = sum(1 for t in stats if t <= q) / r
        assert abs(emp - p) <= 4 * math.sqrt(p * (1 - p) / r)
