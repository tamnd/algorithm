# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ljung-box-test/. The authors are listed in prov/NPBB3C.jsonl.

import math
import random
from fractions import Fraction

import pytest

from ljung_box_test import ljung_box, residual_autocorrelations
from stdist import chi2_ppf, chi2_sf


def exact_q(x: list[int], h: int) -> tuple[Fraction, Fraction]:
    """Ljung-Box and Box-Pierce statistics in exact rational arithmetic (the reference)."""
    n = len(x)
    m = Fraction(sum(x), n)
    d = [Fraction(v) - m for v in x]
    c0 = sum(v * v for v in d)
    r = [sum(d[t] * d[t - k] for t in range(k, n)) / c0 for k in range(1, h + 1)]
    lb = n * (n + 2) * sum(r[k - 1] ** 2 / (n - k) for k in range(1, h + 1))
    bp = n * sum(v * v for v in r)
    return lb, bp


def simulate_ar1(phi: float, n: int, rng: random.Random, burn: int = 200) -> list[float]:
    x, prev = [], 0.0
    for t in range(n + burn):
        prev = phi * prev + rng.gauss(0.0, 1.0)
        if t >= burn:
            x.append(prev)
    return x


def test_statistic_matches_exact_rational_value():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(4, 30)
        x = [rng.randint(-9, 9) for _ in range(n)]
        if len(set(x)) == 1:
            continue
        h = rng.randint(1, n - 1)
        lb, bp = exact_q(x, h)
        assert ljung_box([float(v) for v in x], h)[0] == pytest.approx(float(lb), rel=1e-12)
        assert ljung_box([float(v) for v in x], h, statistic="box-pierce")[0] == pytest.approx(float(bp), rel=1e-12)
        assert lb >= bp


def test_worked_example():
    x = [3.0, 5.0, 6.0, 4.0, 2.0, 1.0, 3.0, 6.0, 7.0, 5.0]
    r = residual_autocorrelations(x, 3)
    assert r == pytest.approx([69 / 140, -89 / 280, -523 / 840], rel=1e-12)
    q, df, p = ljung_box(x, 3)
    assert df == 3
    assert q == pytest.approx(11.399778304178811, rel=1e-12)
    assert p == pytest.approx(chi2_sf(q, 3), rel=1e-15)
    assert p == pytest.approx(0.00974936528681176, rel=1e-9)


def test_helper_closed_forms():
    for x in (0.1, 1.0, 3.0, 12.5):
        assert chi2_sf(x, 2) == pytest.approx(math.exp(-x / 2), rel=1e-12)
        assert chi2_sf(x, 1) == pytest.approx(math.erfc(math.sqrt(x / 2)), rel=1e-10)
    assert chi2_ppf(0.95, 1) == pytest.approx(3.841458821, abs=1e-8)


def test_monte_carlo_size_iid_normal():
    # Measured, not proved: r = 2000 series of n = 100 iid N(0, 1), h = 10, seed 2.
    rng = random.Random(2)
    r, rej = 2000, 0
    for _ in range(r):
        x = [rng.gauss(0.0, 1.0) for _ in range(100)]
        rej += ljung_box(x, 10)[2] <= 0.05
    # 4 standard errors are 4 sqrt(0.05 * 0.95 / 2000) = 0.0195.
    assert abs(rej / r - 0.05) < 0.025


def test_monte_carlo_size_ar1_residuals_with_df_h_minus_1():
    # Measured: AR(1) with phi = 0.5, n = 100, Yule-Walker fit, h = 10, df = 9, seed 3.
    rng = random.Random(3)
    r, rej = 1500, 0
    for _ in range(r):
        x = simulate_ar1(0.5, 100, rng)
        m = math.fsum(x) / 100
        d = [v - m for v in x]
        c0 = math.fsum(v * v for v in d)
        a = math.fsum(d[t] * d[t - 1] for t in range(1, 100)) / c0
        res = [d[t] - a * d[t - 1] for t in range(1, 100)]
        rej += ljung_box(res, 10, fitted=1)[2] <= 0.05
    assert abs(rej / r - 0.05) < 0.025


def test_power_against_ar1():
    rng = random.Random(4)
    rej = sum(ljung_box(simulate_ar1(0.5, 100, rng), 5)[2] <= 0.05 for _ in range(300))
    assert rej / 300 > 0.9


def test_errors():
    with pytest.raises(ValueError):
        ljung_box([1.0, 1.0, 1.0, 1.0], 2)
    with pytest.raises(ValueError):
        ljung_box([1.0, 2.0, 3.0], 3)
    with pytest.raises(ValueError):
        ljung_box([1.0, 2.0, 0.0, 5.0], 2, fitted=2)
    with pytest.raises(ValueError):
        ljung_box([1.0, 2.0, 0.0, 5.0], 2, statistic="other")
