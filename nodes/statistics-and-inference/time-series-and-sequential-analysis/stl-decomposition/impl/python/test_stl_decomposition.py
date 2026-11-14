# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stl-decomposition/. The authors are listed in prov/GHRJ1G.jsonl.

import math
import random
from fractions import Fraction

import pytest

from stl_decomposition import default_spans, loess, loess_at, moving_average, robustness_weights, stl

QUARTERLY = [12, 8, 14, 10, 16, 11, 17, 14, 19, 14, 21, 17]


def brute_loess(y, x, q, degree):
    """Direct definition in rationals: the q nearest positions, tricube weights, weighted least squares."""
    n = len(y)
    pos = sorted(range(1, n + 1), key=lambda i: (abs(i - x), i))[:min(q, n)]
    lam = Fraction(max(abs(i - x) for i in pos))
    if q > n:
        lam = lam * q / n
    w = {i: (1 - (Fraction(abs(i - x)) / lam) ** 3) ** 3 if abs(i - x) < lam else Fraction(0) for i in pos}
    sw = sum(w.values())
    xb = sum(w[i] * i for i in pos) / sw
    yb = sum(w[i] * y[i - 1] for i in pos) / sw
    if degree == 0:
        return yb
    sxx = sum(w[i] * (i - xb) ** 2 for i in pos)
    if sxx == 0:  # only one point has positive weight (q = 3 at an interior x): a local constant
        return yb
    sxy = sum(w[i] * (i - xb) * y[i - 1] for i in pos)
    return yb + sxy / sxx * (x - xb)


@pytest.mark.parametrize("q", [3, 5, 7, 15])
@pytest.mark.parametrize("degree", [0, 1])
def test_loess_matches_definition(q, degree) -> None:
    rng = random.Random(q * 10 + degree)
    y = [Fraction(rng.randint(-10, 10)) for _ in range(11)]
    for x in range(0, 13):  # includes the extrapolated positions 0 and n + 1
        assert loess_at(y, x, q, degree) == brute_loess(y, x, q, degree)


def test_loess_reproduces_lines() -> None:
    y = [Fraction(3) - Fraction(2, 7) * i for i in range(1, 10)]
    for q in (3, 5, 9, 13):
        out = loess(y, q, 1, extend=True)
        assert out == [Fraction(3) - Fraction(2, 7) * x for x in range(0, 11)]
    assert loess([Fraction(4)] * 6, 3, 0) == [4] * 6


def test_low_pass_of_line_plus_season() -> None:
    # Moving averages of lengths m, m and 3, then LOESS, map a line plus a zero-sum
    # season on times 1-m..N+m to the line on times 1..N exactly.
    m, big_n = 4, 12
    s = [Fraction(3), Fraction(-1), Fraction(-4), Fraction(2)]
    c = [Fraction(5) + Fraction(1, 2) * t + s[t % m] for t in range(1 - m, big_n + m + 1)]
    low = moving_average(moving_average(moving_average(c, m), m), 3)
    assert len(low) == big_n
    assert loess(low, 5, 1) == [Fraction(5) + Fraction(1, 2) * t for t in range(1, big_n + 1)]


@pytest.mark.parametrize("outer", [0, 2])
@pytest.mark.parametrize("n_s", [7, 11])
def test_exact_recovery_of_line_plus_season(outer, n_s) -> None:
    s = [Fraction(3), Fraction(-1), Fraction(-4), Fraction(2)]
    y = [Fraction(5) + Fraction(1, 2) * t + s[(t - 1) % 4] for t in range(1, 21)]
    r = stl(y, 4, n_s, outer=outer)
    assert r["seasonal"] == [s[i % 4] for i in range(20)]
    assert r["trend"] == [Fraction(5) + Fraction(1, 2) * t for t in range(1, 21)]
    assert all(v == 0 for v in r["remainder"])


def test_components_add_up_and_worked_example() -> None:
    y = [Fraction(v) for v in QUARTERLY]
    r = stl(y, 4, 7)
    assert r["spans"] == {"seasonal": 7, "trend": 9, "low_pass": 5}
    assert all(a + b + c == v for a, b, c, v in zip(r["seasonal"], r["trend"], r["remainder"], y))
    want_s = [2.437, -2.591, 2.389, -2.156, 2.565, -2.979, 2.482, -1.966, 2.631, -3.356, 2.660, -1.852]
    want_t = [9.683, 10.564, 11.438, 12.308, 13.164, 14.003, 14.836, 15.658, 16.504, 17.336, 18.166, 18.996]
    assert all(abs(float(a) - b) < 5e-4 for a, b in zip(r["seasonal"], want_s))
    assert all(abs(float(a) - b) < 5e-4 for a, b in zip(r["trend"], want_t))


def test_default_spans() -> None:
    assert default_spans(12, 13) == (13, 21)  # 1.5 * 12 / (1 - 1.5 / 13) = 20.35
    assert default_spans(4, 7) == (5, 9)  # 7.64
    assert default_spans(7, 7) == (7, 15)  # 13.36


def test_robustness_weights() -> None:
    w = robustness_weights([Fraction(v) for v in (1, -1, 2, -2, 0, 30)])
    # median |R| = 1.5, h = 9: B(1/9) = (1 - 1/81)^2, B(30/9) = 0
    assert w[0] == (1 - Fraction(1, 81)) ** 2 and w[5] == 0 and w[4] == 1


def test_robust_iterations_isolate_outliers() -> None:
    rng = random.Random(2026)
    m, n = 12, 120
    season = [8 * math.sin(2 * math.pi * i / m) + 3 * math.cos(4 * math.pi * i / m) for i in range(m)]
    trend = [50 + 0.2 * t + 5 * math.sin(2 * math.pi * t / 60) for t in range(n)]
    y = [trend[t] + season[t % m] + rng.gauss(0, 1) for t in range(n)]
    for t in (30, 31, 75):
        y[t] += 25

    def rmse_s(r):
        return math.sqrt(sum((r["seasonal"][t] - season[t % m]) ** 2 for t in range(n)) / n)

    plain, robust = stl(y, m, 13), stl(y, m, 13, outer=15)
    assert all(robust["weights"][t] == 0 for t in (30, 31, 75))
    assert all(robust["remainder"][t] > 20 for t in (30, 31, 75))
    assert rmse_s(robust) < 0.7 < 1.2 < rmse_s(plain)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        stl([1.0] * 10, 12, 7)
    with pytest.raises(ValueError):
        stl([1.0] * 30, 4, 8)
