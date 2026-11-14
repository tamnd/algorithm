# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-least-squares/. The authors are listed in prov/3EE4N8.jsonl.

import math
import random
from fractions import Fraction

import pytest

from weighted_least_squares import confidence_intervals, weighted_least_squares

# The example of the page: x, y and weights 1/x^2.
EX_X = [1, 2, 3, 4, 5]
EX_Y = [2, 5, 5, 9, 9]
EX_W = [Fraction(1, v * v) for v in EX_X]


def solve_exact(a, b):
    """Gauss-Jordan elimination in exact rational arithmetic."""
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


def wls_exact(x, y, w):
    """(X^T W X)^(-1) X^T W y by the weighted normal equations, exactly."""
    p = len(x[0])
    a = [[sum(Fraction(wi) * r[i] * r[j] for r, wi in zip(x, w)) for j in range(p)] for i in range(p)]
    rhs = [sum(Fraction(wi) * r[i] * yi for r, yi, wi in zip(x, y, w)) for i in range(p)]
    return solve_exact(a, rhs)


def design(xs):
    return [[1, v] for v in xs]


def test_page_example_exact():
    b = wls_exact(design(EX_X), EX_Y, EX_W)
    assert b == [Fraction(281, 1894), Fraction(14967, 7576)]
    assert wls_exact(design(EX_X), EX_Y, [1] * 5) == [Fraction(3, 5), Fraction(9, 5)]  # OLS
    fit = weighted_least_squares(design(EX_X), EX_Y, [float(v) for v in EX_W])
    assert fit.b[0] == pytest.approx(float(b[0]), abs=1e-12)
    assert fit.b[1] == pytest.approx(float(b[1]), abs=1e-12)
    rss = sum(wi * (yi - b[0] - b[1] * xi) ** 2 for xi, yi, wi in zip(EX_X, EX_Y, EX_W))
    assert fit.rss == pytest.approx(float(rss), abs=1e-12)
    assert fit.df == 3


def test_equals_ols_on_rows_scaled_by_root_weight_exact():
    rng = random.Random(11)
    for _ in range(20):
        n, p = rng.randint(4, 8), rng.randint(1, 3)
        x = [[1] + [rng.randint(-5, 5) for _ in range(p - 1)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        roots = [Fraction(rng.randint(1, 4), rng.randint(1, 3)) for _ in range(n)]
        w = [r * r for r in roots]
        try:
            exact = wls_exact(x, y, w)
        except StopIteration:
            continue  # singular design, skipped
        scaled_x = [[r * v for v in row] for row, r in zip(x, roots)]
        scaled_y = [r * v for v, r in zip(y, roots)]
        assert wls_exact(scaled_x, scaled_y, [1] * n) == exact
        fit = weighted_least_squares(x, y, [float(v) for v in w])
        for u, v in zip(fit.b, exact):
            assert u == pytest.approx(float(v), abs=1e-9)


def test_covariance_matches_inverse_of_weighted_gram_exact():
    x, w = design(EX_X), EX_W
    fit = weighted_least_squares(x, EX_Y, [float(v) for v in w])
    g = [[sum(wi * r[i] * r[j] for r, wi in zip(x, w)) for j in range(2)] for i in range(2)]
    det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
    inv = [[g[1][1] / det, -g[0][1] / det], [-g[1][0] / det, g[0][0] / det]]
    for i in range(2):
        for j in range(2):
            assert fit.cov[i][j] == pytest.approx(fit.s2 * float(inv[i][j]), rel=1e-10)


def test_zero_weight_equals_deleting_the_row():
    x = design([1, 2, 3, 4, 5, 6])
    y = [1.0, 3.0, 2.0, 5.0, 4.0, 40.0]
    w = [1.0, 2.0, 1.0, 3.0, 1.0, 0.0]
    a = weighted_least_squares(x, y, w)
    b = weighted_least_squares(x[:5], y[:5], w[:5])
    assert a.b == pytest.approx(b.b, abs=1e-12)
    assert a.df == b.df == 3
    assert a.s2 == pytest.approx(b.s2, rel=1e-12)


def test_scaling_all_weights_changes_nothing():
    x = design(EX_X)
    w = [float(v) for v in EX_W]
    a = weighted_least_squares(x, EX_Y, w)
    b = weighted_least_squares(x, EX_Y, [7.5 * v for v in w])
    assert a.b == pytest.approx(b.b, abs=1e-12)
    assert b.s2 == pytest.approx(7.5 * a.s2, rel=1e-12)
    for i in range(2):
        assert a.cov[i] == pytest.approx(b.cov[i], rel=1e-10)


def test_bad_inputs():
    with pytest.raises(ValueError):
        weighted_least_squares(design([1, 2, 3]), [1, 2, 3], [1.0, -1.0, 1.0])
    with pytest.raises(ValueError):
        weighted_least_squares([[1, 2], [2, 4], [3, 6]], [1, 2, 3], [1.0, 1.0, 1.0])
    with pytest.raises(ValueError):
        weighted_least_squares(design([1, 2, 3]), [1, 2, 3], [1.0, 0.0, 0.0])


def test_coverage_and_efficiency_measured():
    """Normal errors with sd proportional to x. The t interval with weights 1/x^2 is exact,
    so its coverage must be 0.95 up to Monte Carlo error: r = 2000 gives 4 SE of 0.0195."""
    rng = random.Random(20261114)
    xs = [1 + 0.5 * i for i in range(20)]
    x = design(xs)
    w = [1.0 / (v * v) for v in xs]
    r, hit, slopes_w, slopes_o = 2000, 0, [], []
    for _ in range(r):
        y = [2.0 + 0.5 * v + rng.gauss(0.0, 0.3 * v) for v in xs]
        fit = weighted_least_squares(x, y, w)
        lo, hi = confidence_intervals(fit, 0.95)[1]
        hit += lo <= 0.5 <= hi
        slopes_w.append(fit.b[1])
        slopes_o.append(weighted_least_squares(x, y, [1.0] * len(xs)).b[1])
    assert abs(hit / r - 0.95) < 0.0195 + 0.002
    var_w = sum((s - 0.5) ** 2 for s in slopes_w) / r
    var_o = sum((s - 0.5) ** 2 for s in slopes_o) / r
    # Var(slope) = sigma^2 [(X^T W X)^(-1)]_22 with sigma = 0.3 and the 2 x 2 inverse by hand.
    sw = sum(w)
    swx = sum(wi * v for wi, v in zip(w, xs))
    swxx = sum(wi * v * v for wi, v in zip(w, xs))
    theory_w = 0.09 * sw / (sw * swxx - swx * swx)
    assert theory_w > 0.0 and math.isfinite(theory_w)
    assert abs(var_w / theory_w - 1.0) < 0.15  # chi-square spread of a variance with r = 2000 is about 0.032
    assert var_w < var_o  # Gauss-Markov on the scaled model: WLS beats OLS here
