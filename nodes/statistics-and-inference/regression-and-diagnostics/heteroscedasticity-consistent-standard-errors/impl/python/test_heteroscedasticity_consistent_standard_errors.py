# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heteroscedasticity-consistent-standard-errors/. The authors are listed in prov/PTWW7S.jsonl.

import math
import random
from fractions import Fraction

import pytest

from heteroscedasticity_consistent_standard_errors import KINDS, confidence_intervals, hc_covariance

EX_X = [[1, v] for v in [1, 2, 3, 4, 10]]
EX_Y = [1, 3, 2, 5, 14]


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


def inverse(a):
    n = len(a)
    cols = [solve(a, [int(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def gram(x):
    p = len(x[0])
    return [[sum(Fraction(r[i]) * r[j] for r in x) for j in range(p)] for i in range(p)]


def direct(x, y, kind):
    """(X^T X)^(-1) X^T diag(omega) X (X^T X)^(-1) with explicit matrices in exact arithmetic."""
    n, p = len(x), len(x[0])
    gi = inverse(gram(x))
    b = solve(gram(x), [sum(Fraction(r[i]) * v for r, v in zip(x, y)) for i in range(p)])
    e = [v - sum(Fraction(a) * c for a, c in zip(r, b)) for r, v in zip(x, y)]
    h = [sum(Fraction(r[i]) * gi[i][j] * r[j] for i in range(p) for j in range(p)) for r in x]
    factor = {"HC0": lambda hi: 1, "HC1": lambda hi: Fraction(n, n - p),
              "HC2": lambda hi: 1 / (1 - hi), "HC3": lambda hi: 1 / (1 - hi) ** 2}[kind]
    omega = [ei * ei * factor(hi) for ei, hi in zip(e, h)]
    meat = [[sum(o * r[i] * r[j] for o, r in zip(omega, x)) for j in range(p)] for i in range(p)]
    v = [[sum(gi[i][k] * meat[k][l] * gi[l][j] for k in range(p) for l in range(p)) for j in range(p)]
         for i in range(p)]
    return b, e, h, v


def test_page_example_exact():
    b, e, h, _ = direct(EX_X, EX_Y, "HC0")
    assert b == [Fraction(-21, 25), Fraction(73, 50)]
    assert e == [Fraction(19, 50), Fraction(23, 25), Fraction(-77, 50), 0, Fraction(6, 25)]
    assert h == [Fraction(19, 50), Fraction(7, 25), Fraction(11, 50), Fraction(1, 5), Fraction(23, 25)]
    want_se = {"HC0": 0.060433, "HC1": 0.078019, "HC2": 0.119597, "HC3": 0.367592}
    for kind in KINDS:
        v = direct(EX_X, EX_Y, kind)[3]
        fit = hc_covariance(EX_X, EX_Y, kind)
        for i in range(2):
            assert fit.cov[i] == pytest.approx([float(t) for t in v[i]], rel=1e-10, abs=1e-14)
        assert fit.se[1] == pytest.approx(want_se[kind], abs=1e-6)


def test_matches_direct_matrices_on_random_designs_exact():
    rng = random.Random(8)
    done = 0
    while done < 10:
        n, p = rng.randint(6, 10), 3
        x = [[1, rng.randint(-4, 4), rng.randint(0, 6)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        try:
            ref = {k: direct(x, y, k) for k in KINDS}
        except (StopIteration, ZeroDivisionError):
            continue  # singular design or a leverage of 1
        for kind in KINDS:
            fit = hc_covariance(x, y, kind)
            assert fit.leverage == pytest.approx([float(t) for t in ref[kind][2]], abs=1e-12)
            for i in range(p):
                assert fit.cov[i] == pytest.approx([float(t) for t in ref[kind][3][i]], rel=1e-9, abs=1e-12)
        done += 1


def test_hc3_is_the_sum_of_squared_leave_one_out_changes_exact():
    """b_(i) - b = -(X^T X)^(-1) x_i e_i / (1 - h_ii), so HC3 = sum_i (b_(i) - b)(b_(i) - b)^T."""
    rng = random.Random(9)
    for _ in range(5):
        n = 8
        x = [[1, rng.randint(-5, 5), rng.randint(-5, 5)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        try:
            b, _, _, hc3 = direct(x, y, "HC3")
            drops = [solve(gram(x[:i] + x[i + 1:]),
                           [sum(Fraction(r[j]) * v for r, v in zip(x[:i] + x[i + 1:], y[:i] + y[i + 1:])) for j in range(3)])
                     for i in range(n)]
        except (StopIteration, ZeroDivisionError):
            continue
        d = [[bi - bb for bi, bb in zip(di, b)] for di in drops]
        s = [[sum(t[i] * t[j] for t in d) for j in range(3)] for i in range(3)]
        assert s == hc3
        # The jackknife variance centers at the mean of the b_(i): ((n - 1)/n)(HC3 - n dbar dbar^T).
        dbar = [sum(t[i] for t in d) / n for i in range(3)]
        jack = [[Fraction(n - 1, n) * sum((t[i] - dbar[i]) * (t[j] - dbar[j]) for t in d) for j in range(3)]
                for i in range(3)]
        assert jack == [[Fraction(n - 1, n) * (hc3[i][j] - n * dbar[i] * dbar[j]) for j in range(3)] for i in range(3)]


def test_expected_values_under_equal_variances_exact():
    """With Cov(e) = I: E e_i^2 = 1 - h_ii, so E[HC2] = (X^T X)^(-1) exactly and E[HC0] is smaller."""
    x = EX_X
    n, p = len(x), 2
    gi = inverse(gram(x))
    hat = [[sum(Fraction(x[a][i]) * gi[i][j] * x[c][j] for i in range(p) for j in range(p)) for c in range(n)]
           for a in range(n)]
    m = [[int(a == c) - hat[a][c] for c in range(n)] for a in range(n)]
    ee = [sum(m[a][c] ** 2 for c in range(n)) for a in range(n)]  # diag of (I - H) I (I - H)^T
    assert ee == [1 - hat[a][a] for a in range(n)]

    def expected(factor):
        meat = [[sum(ee[a] * factor(hat[a][a]) * x[a][i] * x[a][j] for a in range(n)) for j in range(p)] for i in range(p)]
        return [[sum(gi[i][k] * meat[k][l] * gi[l][j] for k in range(p) for l in range(p)) for j in range(p)] for i in range(p)]

    assert expected(lambda h: 1 / (1 - h)) == gi
    hc0 = expected(lambda h: 1)
    assert all(hc0[j][j] < gi[j][j] for j in range(p))


def test_bad_inputs():
    with pytest.raises(ValueError):
        hc_covariance(EX_X, EX_Y, "HC9")
    x = [[1, 0], [1, 0], [1, 0], [1, 1]]  # the last point has leverage 1
    with pytest.raises(ValueError):
        hc_covariance(x, [1, 2, 3, 4], "HC3")
    # HC0 still works, but the point with leverage 1 has residual 0 and adds nothing:
    # slope = y_4 - mean(y_1..y_3), and only the first three residuals (-1, 0, 1) enter, each with weight 1/9.
    assert hc_covariance(x, [1, 2, 3, 4], "HC0").cov[1][1] == pytest.approx(2.0 / 9.0)


def test_coverage_measured():
    """Errors with sd 0.5 x and lognormal x, n = 25. Measured coverage with r = 2000 was
    HC0 0.858, HC1 0.867, HC2 0.889, HC3 0.912 and 0.767 for the usual standard error.
    Here r = 800 (4 SE about 0.04): HC3 must be at least 0.87 and the usual one at most 0.81."""
    rng = random.Random(20261114)
    n, r = 25, 800
    xs = [math.exp(rng.gauss(0.0, 1.0)) for _ in range(n)]
    x = [[1.0, v] for v in xs]
    xb = sum(xs) / n
    sxx = sum((v - xb) ** 2 for v in xs)
    hit3 = hit0 = hit_naive = 0
    for _ in range(r):
        y = [1.0 + v + rng.gauss(0.0, 0.5 * v) for v in xs]
        f3 = hc_covariance(x, y, "HC3")
        lo, hi = confidence_intervals(f3)[1]
        hit3 += lo <= 1.0 <= hi
        f0 = hc_covariance(x, y, "HC0")
        lo, hi = confidence_intervals(f0)[1]
        hit0 += lo <= 1.0 <= hi
        se = math.sqrt(sum(t * t for t in f3.residuals) / (n - 2) / sxx)
        q = (hi - f0.b[1]) / f0.se[1]  # the same t quantile
        hit_naive += abs(f3.b[1] - 1.0) <= q * se
    assert hit3 >= hit0  # HC3 dominates HC0 entrywise in its weights, so its intervals contain those of HC0
    assert hit3 / r >= 0.87
    assert hit_naive / r <= 0.81
