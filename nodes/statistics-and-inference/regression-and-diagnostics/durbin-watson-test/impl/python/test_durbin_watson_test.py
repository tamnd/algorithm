# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durbin-watson-test/. The authors are listed in prov/TBDQN3.jsonl.

import math
import random
from fractions import Fraction

import pytest

from durbin_watson_test import (bound_eigenvalues, bounds_p_values, durbin_watson, dw_statistic,
                                householder_q1, project_out)

EX_T = list(range(1, 13))
EX_X = [[1, t] for t in EX_T]
EX_Y = [Fraction(v) for v in ["1.0", "1.9", "3.1", "3.2", "3.0", "3.6", "4.4", "5.6", "6.2", "6.1", "6.0", "6.8"]]


def solve(a, b):
    k = len(a)
    m = [[Fraction(v) for v in row] + [Fraction(b[i])] for i, row in enumerate(a)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def exact_residuals(x, y):
    p = len(x[0])
    gram = [[sum(Fraction(r[i]) * r[j] for r in x) for j in range(p)] for i in range(p)]
    b = solve(gram, [sum(Fraction(r[i]) * v for r, v in zip(x, y)) for i in range(p)])
    return [Fraction(v) - sum(Fraction(a) * c for a, c in zip(r, b)) for r, v in zip(x, y)]


def exact_d(e):
    s = sum(t * t for t in e)
    return sum((e[t] - e[t - 1]) ** 2 for t in range(1, len(e))) / s, sum(e[t] * e[t - 1] for t in range(1, len(e))) / s


def jacobi_eigenvalues(a, sweeps=60):
    """Eigenvalues of a symmetric matrix by cyclic Jacobi rotations."""
    a = [row[:] for row in a]
    n = len(a)
    for _ in range(sweeps):
        off = math.fsum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-26:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def dw_matrix(n):
    return [[(2.0 if 0 < i < n - 1 else 1.0) if i == j else (-1.0 if abs(i - j) == 1 else 0.0)
             for j in range(n)] for i in range(n)]


def test_page_example_exact():
    e = exact_residuals(EX_X, EX_Y)
    d, r1 = exact_d(e)
    s = sum(t * t for t in e)
    assert d == 2 * (1 - r1) - (e[0] ** 2 + e[-1] ** 2) / s
    res = durbin_watson(EX_X, [float(v) for v in EX_Y], reps=1999, seed=7)
    assert res.d == pytest.approx(float(d), rel=1e-12)
    assert res.r1 == pytest.approx(float(r1), rel=1e-12)
    assert res.d == pytest.approx(1.2189, abs=1e-4) and res.r1 == pytest.approx(0.3329, abs=1e-4)
    # With B = 9999 the Monte Carlo p-value was 0.0278; here B = 1999 (4 SE about 0.015).
    assert abs(res.p_value - 0.0278) <= 0.015


def test_identity_range_and_invariance_exact():
    rng = random.Random(31)
    for _ in range(10):
        n = rng.randint(6, 12)
        x = [[1, t, rng.randint(-3, 3)] for t in range(n)]
        y = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        try:
            e = exact_residuals(x, y)
        except StopIteration:
            continue
        if all(t == 0 for t in e):
            continue
        d, r1 = exact_d(e)
        s = sum(t * t for t in e)
        assert d == 2 * (1 - r1) - (e[0] ** 2 + e[-1] ** 2) / s
        assert 0 < d < 4  # with an intercept the residuals add to 0, so they are not all equal
        # Residuals of a y + X c are a e, so d does not depend on b or sigma.
        a, c = Fraction(rng.choice([-3, -1, 2, 5]), rng.randint(1, 4)), [rng.randint(-5, 5) for _ in range(3)]
        y2 = [a * yi + sum(ci * xi for ci, xi in zip(c, row)) for yi, row in zip(y, x)]
        assert exact_d(exact_residuals(x, y2))[0] == d
        assert durbin_watson(x, [float(v) for v in y], reps=1).d == pytest.approx(float(d), rel=1e-10)


def test_projection_is_least_squares():
    q = householder_q1(EX_X)
    e = project_out(q, [float(v) for v in EX_Y])
    assert e == pytest.approx([float(t) for t in exact_residuals(EX_X, EX_Y)], abs=1e-12)
    for j in range(2):
        for k in range(2):
            assert math.fsum(row[j] * row[k] for row in q) == pytest.approx(float(j == k), abs=1e-12)


def test_eigenvalues_and_interlacing():
    """A has eigenvalues 2 - 2 cos(pi j / n). The nonzero eigenvalues nu_i of M A M satisfy
    lam_i <= nu_i <= lam_(i+p-1), which gives d_L <= d <= d_U for the same normal draws."""
    n = 12
    lam = bound_eigenvalues(n)
    assert jacobi_eigenvalues(dw_matrix(n)) == pytest.approx(lam, abs=1e-10)
    rng = random.Random(32)
    for x in (EX_X, [[1.0, rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(n)]):
        p = len(x[0])
        q = householder_q1(x)
        m = [[(1.0 if i == j else 0.0) - math.fsum(q[i][k] * q[j][k] for k in range(p)) for j in range(n)]
             for i in range(n)]
        a = dw_matrix(n)
        ma = [[math.fsum(m[i][k] * a[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        mam = [[math.fsum(ma[i][k] * m[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        nu = jacobi_eigenvalues(mam)[p:]  # drop the p zero eigenvalues of the column space of X
        for i in range(n - p):
            assert lam[i + 1] - 1e-9 <= nu[i] <= lam[i + p] + 1e-9


def test_bounds_bracket_the_monte_carlo_p_value_measured():
    """For the example, P(d_L <= d) = 0.131 and P(d_U <= d) = 0.030 with 20000 draws: the bounds
    test is inconclusive at 5%, while the Monte Carlo p-value 0.028 rejects. The trend regressor is
    close to an eigenvector of A, so the law of d is close to that of d_U."""
    d = durbin_watson(EX_X, [float(v) for v in EX_Y], reps=1).d
    lo, hi = bounds_p_values(d, 12, 2, reps=4000, seed=3)
    assert hi == pytest.approx(0.0296, abs=0.012)
    assert lo == pytest.approx(0.131, abs=0.022)
    assert hi < 0.05 < lo


def test_size_and_power_measured():
    """n = 20, X = [1, t], 5% level, B = 99. Under H0 the Monte Carlo test has exact size 0.05:
    with r = 600 (4 SE about 0.036) the rate must be within 0.036 of 0.05. With AR(1) errors,
    rho = 0.7, n = 30 the measured power was 0.936 with r = 1000; here r = 150 and it must be at least 0.8."""
    rng = random.Random(5)
    n, r = 20, 600
    x = [[1, t] for t in range(n)]
    rej = sum(durbin_watson(x, [rng.gauss(0.0, 1.0) for _ in range(n)], reps=99, seed=k + 1).p_value <= 0.05
              for k in range(r))
    assert abs(rej / r - 0.05) <= 0.036
    n, r, rho = 30, 150, 0.7
    x = [[1, t] for t in range(n)]
    rej = 0
    for k in range(r):
        u = rng.gauss(0.0, 1.0) / math.sqrt(1.0 - rho * rho)
        y = []
        for t in range(n):
            y.append(1.0 + 0.1 * t + u)
            u = rho * u + rng.gauss(0.0, 1.0)
        rej += durbin_watson(x, y, reps=99, seed=1000 + k).p_value <= 0.05
    assert rej / r >= 0.8


def test_bad_inputs():
    with pytest.raises(ValueError):
        durbin_watson(EX_X, [1.0] * 11)
    with pytest.raises(ValueError):
        durbin_watson(EX_X, [float(t) for t in EX_T], reps=1)  # a perfect fit
    with pytest.raises(ValueError):
        durbin_watson(EX_X, [float(v) for v in EX_Y], alternative="up")
    assert dw_statistic([1.0, -1.0, 1.0, -1.0])[0] == pytest.approx(3.0)
