# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mm-estimator/. The authors are listed in prov/MBJNZK.jsonl.

import math
import random

import pytest

from mm_estimator import (
    B, C0, C1, m_objective, m_scale, mm_estimate, ols, psi, residuals, rho, s_estimate,
)

XS = list(range(1, 11))
YS = [3.1, 4.8, 7.2, 9.1, 10.8, 13.2, 15.0, 16.9, 2.0, 1.0]
X = [[1.0, float(v)] for v in XS]


def test_m_scale_by_hand() -> None:
    # Four residuals of size 1: rho(1/s) = 1/2, so s = 1 / (c0 sqrt(1 - 2^(-1/3))).
    s = m_scale([1, -1, 1, -1])
    assert s == pytest.approx(1 / (C0 * math.sqrt(1 - 2 ** (-1 / 3))), rel=1e-12)
    # At most n b nonzero residuals: an exact fit of half the points gives scale 0.
    assert m_scale([0, 0, 5, -7]) == 0.0


def test_m_scale_is_consistent_at_the_normal() -> None:
    rng = random.Random(1)
    r = [rng.gauss(0.0, 2.0) for _ in range(20000)]
    assert m_scale(r) == pytest.approx(2.0, rel=0.03)


def test_page_example() -> None:
    assert ols(X, YS) == pytest.approx([7.306667, 0.182424], abs=1e-6)
    beta_s, s = s_estimate(X, YS, subsets=None)
    assert beta_s == pytest.approx([37 / 30, 59 / 30], abs=1e-9)  # the line through (4, 9.1) and (7, 15.0)
    assert sum(rho(v / s, C0) for v in residuals(X, YS, beta_s)) / len(YS) == pytest.approx(B, abs=1e-12)
    beta, s2 = mm_estimate(X, YS, subsets=None)
    assert s2 == s
    assert beta == pytest.approx([1.058707, 1.990247], abs=1e-6)


def test_m_step_descent_and_stationarity() -> None:
    rng = random.Random(2)
    for _ in range(15):
        n, p = rng.randint(20, 40), rng.choice([2, 3])
        x = [[1.0] + [rng.gauss(0.0, 1.0) for _ in range(p - 1)] for _ in range(n)]
        y = [1.0 + sum(row[1:]) + rng.gauss(0.0, 0.5) for row in x]
        for i in rng.sample(range(n), n // 5):
            y[i] += rng.uniform(10.0, 30.0)
        trace = []
        beta, s = mm_estimate(x, y, subsets=60, seed=rng.randint(0, 10**6), trace=trace)
        q = [m_objective(x, y, b, s) for b in trace]
        assert all(b <= a + 1e-12 for a, b in zip(q, q[1:]))
        assert q[-1] <= q[0]
        r = residuals(x, y, beta)
        for j in range(p):
            assert abs(sum(psi(v / s, C1) * row[j] for v, row in zip(r, x))) <= 1e-6 * n
        # The scale solves the M-scale equation at the S residuals.
        b0 = trace[0]
        assert sum(rho(v / s, C0) for v in residuals(x, y, b0)) / n == pytest.approx(B, abs=1e-9)


def test_s_step_takes_the_least_scale() -> None:
    rng = random.Random(3)
    n = 9
    x = [[1.0, float(i)] for i in range(n)]
    y = [2.0 * i + rng.gauss(0.0, 1.0) for i in range(n)]
    beta, s = s_estimate(x, y, subsets=None)
    from mm_estimator import solve
    for i in range(n):
        for j in range(i + 1, n):
            b = solve([x[i], x[j]], [y[i], y[j]])
            assert m_scale(residuals(x, y, b)) >= s


def test_exact_fit_of_a_majority() -> None:
    x = [[1.0, float(i)] for i in range(10)]
    y = [3.0 - 0.5 * i for i in range(10)]
    y[1], y[4], y[7] = 50.0, -40.0, 99.0
    beta, s = mm_estimate(x, y, subsets=None)
    assert s == 0.0
    assert beta == pytest.approx([3.0, -0.5], abs=1e-12)


def test_contaminated_regression_error_is_measured() -> None:
    # 30% bad leverage points: OLS slope is far off, MM stays near the true slope 2.
    rng = random.Random(4)
    n = 60
    xs = [rng.uniform(0.0, 10.0) for _ in range(n)]
    ys = [1.0 + 2.0 * v + rng.gauss(0.0, 1.0) for v in xs]
    for i in range(int(0.3 * n)):
        xs[i], ys[i] = rng.uniform(25.0, 30.0), rng.uniform(-5.0, 0.0)
    x = [[1.0, v] for v in xs]
    b_ols = ols(x, ys)
    b_mm, _ = mm_estimate(x, ys, subsets=200, seed=5)
    assert abs(b_ols[1] - 2.0) > 1.0
    assert abs(b_mm[1] - 2.0) < 0.15


def test_efficiency_on_clean_data_is_measured() -> None:
    # On clean normal errors the MM and OLS slopes are close; the variance ratio over
    # replications is measured, and must be near the 95% of the theory.
    rng = random.Random(6)
    d_ols, d_mm = [], []
    for _ in range(40):
        xs = [rng.uniform(0.0, 1.0) for _ in range(40)]
        x = [[1.0, v] for v in xs]
        y = [rng.gauss(0.0, 1.0) for _ in xs]
        d_ols.append(ols(x, y)[1])
        d_mm.append(mm_estimate(x, y, subsets=30, seed=rng.randint(0, 10**6))[0][1])
    v_ols = sum(v * v for v in d_ols) / len(d_ols)
    v_mm = sum(v * v for v in d_mm) / len(d_mm)
    assert 0.75 < v_ols / v_mm <= 1.1
