# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/engle-granger-test/. The authors are listed in prov/33J9EX.jsonl.

import math
import random
from fractions import Fraction

import pytest

from engle_granger_test import (engle_granger, error_correction, mackinnon_critical_value, ols,
                                residual_adf, simulate_null)


def walk(rng, n, start=0.0):
    s, out = start, []
    for _ in range(n):
        s += rng.gauss(0.0, 1.0)
        out.append(s)
    return out


def cointegrated_pair(seed, n=200, beta=2.0, phi=0.5):
    rng = random.Random(seed)
    x = walk(rng, n)
    u, a = [], 0.0
    for _ in range(n):
        a = phi * a + rng.gauss(0.0, 1.0)
        u.append(a)
    return [1.0 + beta * xi + ui for xi, ui in zip(x, u)], x


def exact_ols(columns, y):
    """Brute force: the normal equations in exact rationals by Gauss-Jordan."""
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
    return [a[i][k] / a[i][i] for i in range(k)]


def test_worked_example() -> None:
    # The page example.
    y = [2, 2, 7, 6, 8, 12, 15, 12, 18, 18]
    x = [0, 1, 3, 2, 4, 5, 7, 6, 8, 9]
    r = engle_granger(y, [x], "c", 0)
    b = exact_ols([[1] * 10, x], y)
    assert b == [Fraction(14, 11), Fraction(64, 33)]
    assert abs(r["beta"][0] - 14 / 11) < 1e-12 and abs(r["beta"][1] - 64 / 33) < 1e-12
    u = [Fraction(v) - b[0] - b[1] * xv for v, xv in zip(y, x)]
    assert all(abs(float(p) - q) < 1e-12 for p, q in zip(u, r["resid"]))
    num = sum(u[t - 1] * (u[t] - u[t - 1]) for t in range(1, 10))
    den = sum(u[t - 1] ** 2 for t in range(1, 10))
    rho = num / den
    assert rho == Fraction(-2163, 1301)
    rss = sum((u[t] - u[t - 1] - rho * u[t - 1]) ** 2 for t in range(1, 10))
    tau = float(rho) / math.sqrt(float(rss / 8 / den))
    assert abs(r["tau"] - tau) < 1e-10
    assert abs(r["tau"] - (-6.27828)) < 1e-5
    assert r["nobs"] == 9 and abs(r["critical"][0.05] - (-4.09926)) < 1e-5
    assert r["reject"]


@pytest.mark.parametrize("case", ["c", "ct"])
def test_step_one_matches_exact_normal_equations(case) -> None:
    rng = random.Random(3)
    n = 15
    x1 = [rng.randint(-9, 9) for _ in range(n)]
    x2 = [rng.randint(-9, 9) for _ in range(n)]
    y = [rng.randint(-20, 20) for _ in range(n)]
    det = [[1] * n] + ([[t + 1 for t in range(n)]] if case == "ct" else [])
    b = exact_ols(det + [x1, x2], y)
    r = engle_granger(y, [x1, x2], case, 0)
    assert all(abs(p - float(q)) < 1e-9 for p, q in zip(r["beta"], b))


def test_residual_adf_closed_form() -> None:
    rng = random.Random(4)
    u = [rng.gauss(0, 1) for _ in range(30)]
    tau, nobs, rss, k = residual_adf(u, 0)
    num = sum(u[t - 1] * (u[t] - u[t - 1]) for t in range(1, 30))
    den = sum(u[t - 1] ** 2 for t in range(1, 30))
    rho = num / den
    s2 = sum((u[t] - u[t - 1] - rho * u[t - 1]) ** 2 for t in range(1, 30)) / (29 - 1)
    assert nobs == 29 and k == 1
    assert abs(tau - rho / math.sqrt(s2 / den)) < 1e-10


def test_invariance() -> None:
    # tau depends only on the step-1 residuals, which do not change when y is
    # moved by a + d x or scaled, or when x is moved by an affine map.
    y, x = cointegrated_pair(1, 80)
    base = engle_granger(y, [x], "c", 2)["tau"]
    for yy, xx in (([3.0 - 0.7 * v for v in y], x), ([v + 5.0 * w for v, w in zip(y, x)], x),
                   (y, [4.0 + 0.1 * w for w in x])):
        assert abs(engle_granger(yy, [xx], "c", 2)["tau"] - base) < 1e-8


def test_size_against_mackinnon_surface() -> None:
    # Two independent random walks, n = 100 (nobs 99), 1500 samples: the share
    # of tau below the 5% value for N = 2 must be within 4 binomial SE (0.0225).
    reps = 1500
    sims = simulate_null(100, 2, "c", reps, random.Random(17))
    crit = mackinnon_critical_value("c", 2, 0.05, 99)
    rate = sum(1 for s in sims if s < crit) / reps
    assert abs(rate - 0.05) < 4 * math.sqrt(0.05 * 0.95 / reps)


def test_critical_values_shift_with_more_variables() -> None:
    for case in ("c", "ct"):
        vals = [mackinnon_critical_value(case, nv, 0.05, 200) for nv in range(1, 6)]
        assert all(a > b for a, b in zip(vals, vals[1:]))
    assert abs(mackinnon_critical_value("c", 2, 0.05) - (-3.33613)) < 1e-12


def test_superconsistency() -> None:
    # The spread of beta-hat shrinks like 1/n, not 1/sqrt(n): multiplying n by 4
    # divides the interquartile range by about 4 (between 2.8 and 6 here).
    def iqr(n, seed):
        rng = random.Random(seed)
        bs = []
        for _ in range(200):
            x = walk(rng, n)
            y = [2.0 * xi + rng.gauss(0.0, 1.0) for xi in x]
            bs.append(engle_granger(y, [x], "c", 0)["beta"][1])
        bs.sort()
        return bs[150] - bs[50]
    ratio = iqr(50, 1) / iqr(200, 2)
    assert 2.8 < ratio < 6.0


def test_detects_cointegration_and_spurious_regression() -> None:
    y, x = cointegrated_pair(2026, 200)
    r = engle_granger(y, [x], "c", None)
    assert r["reject"] and abs(r["beta"][1] - 2.0) < 0.1
    rng = random.Random(99)
    rejections = 0
    for _ in range(20):
        a, b = walk(rng, 200), walk(rng, 200)
        rejections += engle_granger(a, [b], "c", None)["reject"]
    assert rejections <= 4


def test_error_correction_speed() -> None:
    # With u_t = 0.5 u_(t-1) + e_t, dy_t = 2 dx_t - 0.5 u_(t-1) + e_t, so alpha = -0.5.
    y, x = cointegrated_pair(7, 400)
    r = engle_granger(y, [x], "c", 0)
    coef, se = error_correction(y, x, r["resid"], 0)
    assert abs(coef[1] + 0.5) < 4 * se[1]
    assert abs(coef[2] - 2.0) < 4 * se[2]


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        engle_granger([1, 2, 3, 4], [[1, 2, 3, 4]], "x", 0)
    with pytest.raises(ValueError):
        ols([[1, 2, 3], [2, 4, 6]], [1, 2, 3])
