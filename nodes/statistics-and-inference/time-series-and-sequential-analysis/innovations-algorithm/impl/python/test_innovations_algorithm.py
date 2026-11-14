# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/innovations-algorithm/. The authors are listed in prov/1XEA6P.jsonl.

import math
import random
from fractions import Fraction

import pytest

from innovations_algorithm import (
    gaussian_neg2_loglik,
    innovations,
    ma_autocovariance,
    ma_preliminary_estimate,
    one_step_predictors,
    stationary_kappa,
)


def ldl(a: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[Fraction]]:
    """The LDL^T factorization of a symmetric positive definite matrix in exact arithmetic."""
    n = len(a)
    low = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    d = [Fraction(0)] * n
    for j in range(n):
        d[j] = a[j][j] - sum(low[j][k] ** 2 * d[k] for k in range(j))
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] * d[k] for k in range(j))) / d[j]
    return low, d


def solve_and_det(a: list[list[Fraction]], b: list[Fraction]) -> tuple[list[Fraction], Fraction]:
    """Gaussian elimination in Fractions: the solution of a y = b and det(a)."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    det = Fraction(1)
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            det = -det
        det *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    y = [Fraction(0)] * n
    for i in reversed(range(n)):
        y[i] = (m[i][n] - sum(m[i][j] * y[j] for j in range(i + 1, n))) / m[i][i]
    return y, det


def random_spd(n: int, rng: random.Random) -> list[list[Fraction]]:
    b = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    return [[sum(b[i][k] * b[j][k] for k in range(n)) + (1 if i == j else 0) for j in range(n)]
            for i in range(n)]


def test_matches_ldl_of_the_covariance_matrix():
    rng = random.Random(1)
    for n in range(1, 8):
        for _ in range(5):
            a = random_spd(n, rng)
            theta, v = innovations(lambda i, j: a[i - 1][j - 1], n)
            low, d = ldl(a)
            assert v == d
            for m in range(1, n):
                for k in range(m):
                    assert theta[m][m - k] == low[m][k]


def test_ma1_closed_form():
    th, s2 = Fraction(1, 2), Fraction(3)
    g = ma_autocovariance([th], s2, 1)
    theta, v = innovations(stationary_kappa(g), 12)

    def big_s(k: int) -> Fraction:
        return sum(th ** (2 * i) for i in range(k + 1))

    for m in range(12):
        assert v[m] == s2 * big_s(m + 1) / big_s(m)
        if m >= 1:
            assert theta[m][1] == th * s2 / v[m - 1]
            assert all(t == 0 for t in theta[m][2:])


def test_banded_version_equals_full_version_for_ma_q():
    rng = random.Random(2)
    for q in (1, 2, 3):
        for _ in range(4):
            th = [Fraction(rng.randint(-5, 5), 4) for _ in range(q)]
            g = ma_autocovariance(th, Fraction(1), q)
            full = innovations(stationary_kappa(g), 15)
            band = innovations(stationary_kappa(g), 15, q=q)
            assert full == band
            assert all(t == 0 for m in range(q + 1, 15) for t in full[0][m][q + 1:])


def test_ma_autocovariance_against_expansion():
    rng = random.Random(3)
    for q in range(5):
        th = [Fraction(rng.randint(-6, 6), 3) for _ in range(q)]
        c = [Fraction(1)] + th
        s2 = Fraction(rng.randint(1, 5))
        got = ma_autocovariance(th, s2, q + 3)
        for h in range(q + 4):
            # X_(t+h) = sum_i c_i e_(t+h-i) and X_t = sum_j c_j e_(t-j); only equal noise indices
            # contribute, each with variance s2.
            brute = sum(c[i] * c[j] * s2 for i in range(q + 1) for j in range(q + 1) if h - i == -j)
            assert got[h] == brute


def test_ar1_predictor_is_phi_times_last_value():
    phi = Fraction(3, 5)
    g = [phi ** h / (1 - phi ** 2) for h in range(10)]
    theta, v = innovations(stationary_kappa(g), 10)
    x = [Fraction(v_) for v_ in (2, -1, 3, 0, 5, -4, 1, 1, 2, -2)]
    xhat = one_step_predictors(x, theta)
    assert xhat[0] == 0
    assert all(xhat[m] == phi * x[m - 1] for m in range(1, 10))
    assert v[0] == 1 / (1 - phi ** 2) and all(vm == 1 for vm in v[1:])


def test_likelihood_matches_direct_determinant_and_quadratic_form():
    rng = random.Random(4)
    for n in (1, 3, 6, 9):
        a = random_spd(n, rng)
        x = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        y, det = solve_and_det(a, x)
        quad = sum(xi * yi for xi, yi in zip(x, y))
        direct = n * math.log(2 * math.pi) + math.log(det) + float(quad)
        got = gaussian_neg2_loglik([float(t) for t in x], lambda i, j: float(a[i - 1][j - 1]))
        assert got == pytest.approx(direct, rel=1e-12, abs=1e-9)


def test_preliminary_ma1_estimate_is_near_truth():
    # Measured, not proved: mean over r = 20 series of n = 2000 with theta = 0.5, seed 5.
    rng = random.Random(5)
    r, total = 20, 0.0
    for _ in range(r):
        e = [rng.gauss(0, 1) for _ in range(2001)]
        x = [e[t] + 0.5 * e[t - 1] for t in range(1, 2001)]
        est, v = ma_preliminary_estimate(x, 1, 20)
        total += est[0]
    # The innovations estimate has asymptotic variance 1/n here (Brockwell and Davis 1991,
    # section 8.3), so the standard error of the mean is about 0.005; the bias for m = 20 is small.
    assert abs(total / r - 0.5) < 0.04


def test_errors():
    with pytest.raises(ValueError):
        innovations(lambda i, j: 1.0, 2)  # a singular all-ones matrix
    with pytest.raises(ValueError):
        innovations(lambda i, j: 0.0, 1)
