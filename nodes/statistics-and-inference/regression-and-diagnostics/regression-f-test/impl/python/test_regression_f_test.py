# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-f-test/. The authors are listed in prov/KE7D2K.jsonl.

import math
import random
from fractions import Fraction

import pytest

from regression_f_test import (
    coefficient_t_tests, householder_qr, linear_hypothesis_f_test, nested_f_test, ols_fit,
    overall_f_test,
)
from stdist import f_sf

X1 = [1, 2, 3, 4, 5, 6, 7, 8]
X2 = [3, 1, 4, 1, 5, 9, 2, 6]
Y = [3, 5, 6, 6, 9, 13, 10, 14]
DESIGN = [[1, a, b] for a, b in zip(X1, X2)]


def exact_rss(X, y):
    """Residual sum of squares by the normal equations in exact rational arithmetic, or None if singular."""
    p = len(X[0])
    M = [[Fraction(sum(Fraction(r[i]) * r[j] for r in X)) for j in range(p)]
         + [Fraction(sum(Fraction(r[i]) * v for r, v in zip(X, y)))] for i in range(p)]
    for col in range(p):
        piv = next((r for r in range(col, p) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(p):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    b = [M[i][p] for i in range(p)]
    return sum((Fraction(v) - sum(Fraction(a) * c for a, c in zip(r, b))) ** 2 for r, v in zip(X, y))


def exact_f(X, y, p0):
    n, p = len(X), len(X[0])
    rss1 = exact_rss(X, y)
    if p0 == 0:
        rss0 = sum(Fraction(v) ** 2 for v in y)
    else:
        rss0 = exact_rss([r[:p0] for r in X], y)
    return ((rss0 - rss1) / (p - p0)) / (rss1 / (n - p)), rss0, rss1


def close(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(1.0, abs(b))


def test_worked_example() -> None:
    f, q, nu, pv, rss0, rss1 = overall_f_test(DESIGN, Y)
    assert (q, nu) == (2, 5)
    assert close(rss1, 3092 / 1143) and close(rss0, 107.5)
    assert abs(f - 96.847) < 1e-3 and abs(pv - 1.0045e-4) < 1e-7
    f, q, nu, pv, rss0, rss1 = nested_f_test(DESIGN, Y, 2)
    assert (q, nu) == (1, 5) and close(rss0, 13.0)
    assert abs(f - 19.0281) < 1e-4 and abs(pv - 0.0072757) < 1e-7
    fe, _, _ = exact_f(DESIGN, Y, 2)
    assert close(f, float(fe), 1e-12)


def test_against_exact_normal_equations() -> None:
    rng = random.Random(20261114)
    checked = 0
    while checked < 500:
        p = rng.randint(1, 4)
        n = rng.randint(p + 1, p + 5)
        X = [[1] + [rng.randint(-5, 5) for _ in range(p - 1)] for _ in range(n)]
        if rng.random() < 0.3:
            X = [[rng.randint(-5, 5) for _ in range(p)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        if exact_rss(X, y) in (None, 0):
            continue
        p0 = rng.randint(0, p - 1)
        fe, rss0e, rss1e = exact_f(X, y, p0)
        f, q, nu, pv, rss0, rss1 = nested_f_test(X, y, p0)
        assert (q, nu) == (p - p0, n - p)
        assert close(rss1, float(rss1e)) and close(rss0, float(rss0e))
        assert close(f, float(fe), 1e-8)
        assert close(pv, f_sf(float(fe), q, nu), 1e-7)
        checked += 1


def test_one_restriction_is_t_squared() -> None:
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(5, 12)
        X = [[1.0, rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]
        f, _, _, pv, _, _ = nested_f_test(X, y, 2)
        _, _, t, tp = coefficient_t_tests(X, y)[2]
        assert close(f, t * t, 1e-9) and close(pv, tp, 1e-8)
    t = coefficient_t_tests(DESIGN, Y)
    assert abs(t[2][2] - 4.3621) < 1e-4 and abs(t[1][2] - 9.5297) < 1e-4


def test_wald_form_equals_nested_form() -> None:
    # Dropping the last q columns.
    rng = random.Random(11)
    for _ in range(40):
        n, p = rng.randint(6, 12), rng.randint(2, 5)
        X = [[1.0] + [rng.uniform(-2, 2) for _ in range(p - 1)] for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]
        p0 = rng.randint(0, p - 1)
        Rm = [[1.0 if j == i else 0.0 for j in range(p)] for i in range(p0, p)]
        f1 = nested_f_test(X, y, p0)[0]
        f2 = linear_hypothesis_f_test(X, y, Rm, [0.0] * (p - p0))[0]
        assert close(f1, f2, 1e-8)
    # H_0: b_1 = b_2 is the nested test after the change of basis [1, x1 + x2, x2].
    Xr = [[1, a + b, b] for a, b in zip(X1, X2)]
    assert close(linear_hypothesis_f_test(DESIGN, Y, [[0, 1, -1]], [0])[0], nested_f_test(Xr, Y, 2)[0])
    # H_0: b_1 = 1 is the nested test on y - x1.
    y_off = [v - a for v, a in zip(Y, X1)]
    Xo = [[1, b, a] for a, b in zip(X1, X2)]
    assert close(linear_hypothesis_f_test(DESIGN, Y, [[0, 1, 0]], [1])[0], nested_f_test(Xo, y_off, 2)[0])


def test_overall_f_from_r_squared() -> None:
    f, q, nu, _, rss0, rss1 = overall_f_test(DESIGN, Y)
    r2 = 1.0 - rss1 / rss0
    assert close(f, (r2 / q) / ((1.0 - r2) / nu))
    assert abs(r2 - 0.97484) < 1e-5


def test_one_way_anova() -> None:
    groups = [[4.2, 5.1, 3.9, 4.8], [5.9, 6.3, 5.5], [4.0, 3.6, 4.4, 3.1, 4.9]]
    k, N = len(groups), sum(len(g) for g in groups)
    grand = math.fsum(v for g in groups for v in g) / N
    means = [math.fsum(g) / len(g) for g in groups]
    ssb = math.fsum(len(g) * (m - grand) ** 2 for g, m in zip(groups, means))
    ssw = math.fsum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
    f_anova = (ssb / (k - 1)) / (ssw / (N - k))
    X = [[1.0] + [1.0 if j == gi else 0.0 for j in range(1, k)] for gi, g in enumerate(groups) for _ in g]
    y = [v for g in groups for v in g]
    f, q, nu, _, _, _ = overall_f_test(X, y)
    assert (q, nu) == (k - 1, N - k) and close(f, f_anova)


def test_invariance() -> None:
    f0 = nested_f_test(DESIGN, Y, 2)[0]
    # y + X0 a leaves F unchanged; so do column scaling and a row permutation.
    y2 = [v + 3.0 - 2.0 * a for v, a in zip(Y, X1)]
    assert close(nested_f_test(DESIGN, y2, 2)[0], f0)
    X3 = [[2.0 * r[0] + r[1], -r[1], 10.0 * r[2]] for r in DESIGN]
    assert close(nested_f_test(X3, Y, 2)[0], f0)
    order = [3, 0, 7, 5, 1, 6, 2, 4]
    assert close(nested_f_test([DESIGN[i] for i in order], [Y[i] for i in order], 2)[0], f0)


def test_qr_factor() -> None:
    R, c = householder_qr(DESIGN, Y)
    # R^T R = X^T X and |c|^2 = |y|^2.
    for i in range(3):
        for j in range(3):
            rtr = sum(R[k][i] * R[k][j] for k in range(3))
            xtx = sum(r[i] * r[j] for r in DESIGN)
            assert close(rtr, xtx, 1e-12)
    assert close(math.fsum(v * v for v in c), sum(v * v for v in Y), 1e-12)
    b, rss, _ = ols_fit(DESIGN, Y)
    assert abs(b[1] - 1.2310) < 1e-4 and abs(b[2] - 0.5022) < 1e-4 and close(rss, 3092 / 1143)


def test_edge_cases() -> None:
    with pytest.raises(ValueError):
        nested_f_test(DESIGN, Y, 3)  # q = 0
    with pytest.raises(ValueError):
        nested_f_test(DESIGN[:3], Y[:3], 1)  # n = p
    with pytest.raises(ValueError):
        nested_f_test([[1, a, 2 * a] for a in X1], Y, 1)  # rank deficient
    with pytest.raises(ValueError):
        linear_hypothesis_f_test(DESIGN, Y, [[0, 1, 0], [0, 2, 0]], [0, 0])  # dependent rows
    # An exact fit of the full model: F is infinite or huge, p is 0 or tiny.
    y_exact = [1.0 + 2.0 * a - b for a, b in zip(X1, X2)]
    f, _, _, pv, _, _ = nested_f_test(DESIGN, y_exact, 1)
    assert f > 1e15 and pv < 1e-12
    # p0 = 0: the null model is b = 0.
    f, q, nu, _, rss0, _ = nested_f_test(DESIGN, Y, 0)
    assert q == 3 and close(rss0, float(sum(v * v for v in Y)))


def test_size_by_simulation() -> None:
    rng = random.Random(1)
    n, reps, alpha = 12, 2000, 0.05
    X = [[1.0, rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)] for _ in range(n)]
    rejections = 0
    for _ in range(reps):
        y = [2.0 + 0.5 * r[1] + rng.gauss(0, 1) for r in X]  # H_0 true: b_2 = b_3 = 0
        rejections += nested_f_test(X, y, 2)[3] <= alpha
    assert abs(rejections / reps - alpha) < 0.02
