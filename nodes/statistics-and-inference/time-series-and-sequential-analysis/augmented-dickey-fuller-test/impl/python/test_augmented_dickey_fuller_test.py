# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/augmented-dickey-fuller-test/. The authors are listed in prov/61BK07.jsonl.

import math
import random
from fractions import Fraction

import pytest

from augmented_dickey_fuller_test import (adf_regression, augmented_dickey_fuller_test,
                                          mackinnon_critical_value, monte_carlo_p_value, ols,
                                          schwert_max_lag, select_lags, simulate_null)


def exact_ols(columns, y):
    """Brute force: solve the normal equations X^T X b = X^T y in exact rationals."""
    k = len(columns)
    cols = [[Fraction(v) for v in c] for c in columns]
    yy = [Fraction(v) for v in y]
    a = [[sum(p * q for p, q in zip(cols[i], cols[j])) for j in range(k)]
         + [sum(p * q for p, q in zip(cols[i], yy))] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        for r in range(k):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [u - f * v for u, v in zip(a[r], a[c])]
    b = [a[i][k] / a[i][i] for i in range(k)]
    resid = [v - sum(b[j] * cols[j][t] for j in range(k)) for t, v in enumerate(yy)]
    return b, resid


def exact_inverse_diag(columns):
    k = len(columns)
    cols = [[Fraction(v) for v in c] for c in columns]
    a = [[sum(p * q for p, q in zip(cols[i], cols[j])) for j in range(k)]
         + [Fraction(int(i == j)) for j in range(k)] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        a[c] = [u / a[c][c] for u in a[c]]
        for r in range(k):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [u - f * v for u, v in zip(a[r], a[c])]
    return [a[i][k + i] for i in range(k)]


def test_worked_example() -> None:
    # The page example: y = 3 5 4 6 8 7 9 8, constant, no lags.
    y = [3, 5, 4, 6, 8, 7, 9, 8]
    r = adf_regression(y, 0, "c")
    assert r["nobs"] == 7
    assert abs(r["rho"] - (-3 / 7)) < 1e-13
    assert abs(r["rss"] - 72 / 7) < 1e-12
    assert abs(r["tau"] - (-math.sqrt(5 / 2))) < 1e-12
    assert abs(mackinnon_critical_value("c", 0.05, 7) - (-3.4775828571)) < 1e-9


@pytest.mark.parametrize("trend", ["n", "c", "ct"])
@pytest.mark.parametrize("lags", [0, 1, 3])
def test_regression_matches_exact_normal_equations(trend, lags) -> None:
    rng = random.Random(100 + lags)
    y = [rng.randint(-20, 20) for _ in range(25)]
    first = lags + 1
    rows = range(first, len(y))
    resp = [y[t] - y[t - 1] for t in rows]
    cols = [[y[t - 1] for t in rows]]
    if trend != "n":
        cols.append([1] * len(resp))
    if trend == "ct":
        cols.append(list(rows))
    for i in range(1, lags + 1):
        cols.append([y[t - i] - y[t - i - 1] for t in rows])
    b, resid = exact_ols(cols, resp)
    rss = sum(e * e for e in resid)
    s2 = rss / (len(resp) - len(cols))
    tau = float(b[0]) / math.sqrt(float(s2 * exact_inverse_diag(cols)[0]))
    r = adf_regression(y, lags, trend)
    assert abs(r["rho"] - float(b[0])) < 1e-10
    assert abs(r["rss"] - float(rss)) < 1e-8 * float(rss)
    assert abs(r["tau"] - tau) < 1e-9
    coef, res2, _, _ = ols(cols, resp)
    assert all(abs(u - float(v)) < 1e-9 for u, v in zip(coef, b))


def test_dependent_regressors_rejected() -> None:
    with pytest.raises(ValueError):
        ols([[1, 2, 3, 4], [2, 4, 6, 8]], [1, 0, 1, 0])


@pytest.mark.parametrize("trend,shift", [("c", lambda t: 7.5), ("ct", lambda t: -3.0 + 0.4 * t)])
def test_invariance_to_level_drift_and_scale(trend, shift) -> None:
    # With trend "c" tau ignores y -> a + c y; with "ct" also an added linear trend.
    rng = random.Random(7)
    y, s = [], 0.0
    for _ in range(60):
        s += rng.gauss(0, 1)
        y.append(s)
    for lags in (0, 2):
        base = adf_regression(y, lags, trend)["tau"]
        moved = adf_regression([shift(t) + 3.0 * v for t, v in enumerate(y)], lags, trend)["tau"]
        assert abs(base - moved) < 1e-9


@pytest.mark.parametrize("trend", ["n", "c", "ct"])
def test_size_against_mackinnon_surface(trend) -> None:
    # Random walks of length 100 give nobs = 99. The share of tau below the 5%
    # MacKinnon value must be 0.05 within 4 binomial standard errors (0.016).
    reps = 3000
    sims = simulate_null(100, trend, 0, reps, random.Random({"n": 11, "c": 12, "ct": 13}[trend]))
    crit = mackinnon_critical_value(trend, 0.05, 99)
    rate = sum(1 for s in sims if s < crit) / reps
    assert abs(rate - 0.05) < 4 * math.sqrt(0.05 * 0.95 / reps)


def test_asymptotic_values() -> None:
    assert mackinnon_critical_value("n", 0.05) == -1.94100
    assert mackinnon_critical_value("c", 0.05) == -2.86154
    assert mackinnon_critical_value("ct", 0.05) == -3.41049
    for tr in ("n", "c", "ct"):
        c = [mackinnon_critical_value(tr, a, 100) for a in (0.01, 0.05, 0.10)]
        assert c[0] < c[1] < c[2]


def test_power_against_stationary_ar1() -> None:
    rng = random.Random(21)
    rejections = 0
    for _ in range(40):
        y, s = [], 0.0
        for _ in range(200):
            s = 0.5 * s + rng.gauss(0, 1)
            y.append(s)
        r = augmented_dickey_fuller_test(y, "c")
        rejections += r["tau"] < r["critical"][0.05]
    assert rejections >= 38


def test_lag_selection_finds_ar_in_differences() -> None:
    # dy_t = 0.6 dy_(t-1) + e_t: one lagged difference is needed.
    rng = random.Random(5)
    y, d, s = [], 0.0, 0.0
    for _ in range(300):
        d = 0.6 * d + rng.gauss(0, 1)
        s += d
        y.append(s)
    assert select_lags(y, 8, "c", "bic") == 1
    assert select_lags(y, 8, "c", "aic") >= 1
    assert select_lags(y, 8, "c", "t-stat") >= 1
    r = augmented_dickey_fuller_test(y, "c", criterion="bic")
    assert r["lags"] == 1 and r["nobs"] == 298


def test_schwert_rule() -> None:
    assert [schwert_max_lag(n) for n in (50, 100, 200, 1000)] == [10, 12, 14, 21]


def test_monte_carlo_p_value() -> None:
    y = [3, 5, 4, 6, 8, 7, 9, 8]
    tau = adf_regression(y, 0, "c")["tau"]
    p = monte_carlo_p_value(tau, 8, "c", 0, 1999, random.Random(5))
    assert 0.38 < p < 0.51
    assert monte_carlo_p_value(-50.0, 8, "c", 0, 99, random.Random(1)) == 0.01
