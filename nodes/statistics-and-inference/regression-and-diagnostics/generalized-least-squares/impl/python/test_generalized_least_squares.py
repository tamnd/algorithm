# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-least-squares/. The authors are listed in prov/A3NRM4.jsonl.

import math
import random
from fractions import Fraction

import pytest

from generalized_least_squares import (
    ar1_covariance, cholesky, confidence_intervals, feasible_gls_ar1,
    forward_substitute, generalized_least_squares, prais_winsten,
)


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


def inverse_exact(a):
    n = len(a)
    cols = [solve_exact(a, [int(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def ols_exact(x, y):
    p = len(x[0])
    g = [[sum(Fraction(r[i]) * r[j] for r in x) for j in range(p)] for i in range(p)]
    return solve_exact(g, [sum(Fraction(r[i]) * v for r, v in zip(x, y)) for i in range(p)])


def gls_formula_exact(x, y, v):
    """(X^T V^(-1) X)^(-1) X^T V^(-1) y with V^(-1) formed explicitly, in Fractions."""
    vi = inverse_exact(v)
    xt = transpose(x)
    a = matmul(matmul(xt, vi), x)
    rhs = [row[0] for row in matmul(matmul(xt, vi), [[v] for v in y])]
    return solve_exact(a, rhs)


def ar1_whitener_exact(n, rho, root):
    """The Prais-Winsten matrix P with sqrt(1 - rho^2) = root given exactly."""
    p = [[Fraction(0)] * n for _ in range(n)]
    p[0][0] = root
    for i in range(1, n):
        p[i][i] = Fraction(1)
        p[i][i - 1] = -rho
    return p


def test_page_example_exact():
    t, y = [1, 2, 3, 4, 5], [2, 3, 5, 4, 6]
    x = [[1, v] for v in t]
    p = ar1_whitener_exact(5, Fraction(3, 5), Fraction(4, 5))
    xw, yw = matmul(p, x), [r[0] for r in matmul(p, [[v] for v in y])]
    assert [r[1] for r in xw] == [Fraction(4, 5), Fraction(7, 5), Fraction(9, 5), Fraction(11, 5), Fraction(13, 5)]
    assert yw == [Fraction(8, 5), Fraction(9, 5), Fraction(16, 5), Fraction(1), Fraction(18, 5)]
    b = ols_exact(xw, yw)
    assert b == [Fraction(40, 37), Fraction(36, 37)]
    assert ols_exact(x, y) == [Fraction(13, 10), Fraction(9, 10)]
    rss = sum((v - r[0] * b[0] - r[1] * b[1]) ** 2 for r, v in zip(xw, yw))
    assert rss == Fraction(3622, 925)
    v = [[Fraction(3, 5) ** abs(i - j) / Fraction(16, 25) for j in range(5)] for i in range(5)]
    assert gls_formula_exact(x, y, v) == b
    fit = generalized_least_squares(x, y, ar1_covariance(5, 0.6))
    assert fit.b == pytest.approx([40 / 37, 36 / 37], abs=1e-12)
    assert fit.rss == pytest.approx(3622 / 925, rel=1e-12)
    assert fit.df == 3


def test_whitening_equals_the_formula_exact():
    """V = L L^T with a random rational L: OLS on L^(-1) X, L^(-1) y equals the GLS formula exactly."""
    rng = random.Random(7)
    done = 0
    while done < 12:
        n, p = rng.randint(4, 7), rng.randint(1, 3)
        x = [[1] + [rng.randint(-4, 4) for _ in range(p - 1)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        l = [[Fraction(rng.randint(-3, 3), rng.randint(1, 3)) if j < i else
              (Fraction(rng.randint(1, 4), rng.randint(1, 2)) if j == i else Fraction(0))
              for j in range(n)] for i in range(n)]
        v = matmul(l, transpose(l))
        li = inverse_exact(l)
        xw, yw = matmul(li, x), [r[0] for r in matmul(li, [[t] for t in y])]
        try:
            exact = ols_exact(xw, yw)
        except StopIteration:
            continue  # singular design
        assert exact == gls_formula_exact(x, y, v)
        fit = generalized_least_squares(x, y, [[float(t) for t in r] for r in v])
        assert fit.b == pytest.approx([float(t) for t in exact], rel=1e-8, abs=1e-8)
        done += 1


def test_prais_winsten_is_the_inverse_cholesky_factor():
    """P V P^T = I exactly for rho = 3/5, and numerically P = L^(-1) for L = cholesky(V)."""
    n, rho = 6, Fraction(3, 5)
    v = [[rho ** abs(i - j) / (1 - rho * rho) for j in range(n)] for i in range(n)]
    p = ar1_whitener_exact(n, rho, Fraction(4, 5))
    assert matmul(matmul(p, v), transpose(p)) == [[int(i == j) for j in range(n)] for i in range(n)]
    l = cholesky(ar1_covariance(n, 0.6))
    for j in range(n):
        col = forward_substitute(l, [float(i == j) for i in range(n)])  # column j of L^(-1)
        assert col == pytest.approx([float(p[i][j]) for i in range(n)], abs=1e-12)
    rows = [[1.0, float(t)] for t in range(n)]
    got = prais_winsten(rows, 0.6)
    for i in range(n):
        want = [float(sum(p[i][k] * Fraction(rows[k][j]) for k in range(n))) for j in range(2)]
        assert got[i] == pytest.approx(want, abs=1e-12)


def test_diagonal_v_gives_weighted_least_squares():
    x = [[1, t] for t in [1, 2, 3, 4, 5]]
    y = [2, 5, 5, 9, 9]
    v = [[Fraction(t * t) if i == j else Fraction(0) for j, _ in enumerate(x)] for i, t in enumerate([1, 2, 3, 4, 5])]
    b = gls_formula_exact(x, y, v)
    assert b == [Fraction(281, 1894), Fraction(14967, 7576)]  # the example of the WLS page
    fit = generalized_least_squares(x, y, [[float(t) for t in r] for r in v])
    assert fit.b == pytest.approx([float(t) for t in b], abs=1e-12)


def test_equicorrelation_with_intercept_gives_ols_exact():
    """Kruskal's condition: V = I + c 1 1^T maps col(X) into itself when X has an intercept."""
    rng = random.Random(3)
    for c in [Fraction(1, 2), Fraction(3), Fraction(-1, 10)]:
        n = 6
        x = [[1, rng.randint(-5, 5), rng.randint(-5, 5)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        v = [[int(i == j) + c for j in range(n)] for i in range(n)]
        assert gls_formula_exact(x, y, v) == ols_exact(x, y)


def test_bad_inputs():
    with pytest.raises(ValueError):
        cholesky([[1.0, 2.0], [2.0, 1.0]])
    with pytest.raises(ValueError):
        generalized_least_squares([[1, 1], [1, 2]], [1, 2, 3], [[1.0, 0.0], [0.0, 1.0]])
    with pytest.raises(ValueError):
        ar1_covariance(4, 1.0)


def test_coverage_under_ar1_measured():
    """AR(1) errors with rho = 0.6, n = 30. The GLS t interval with the true V is exact, so its
    coverage is 0.95 up to Monte Carlo error: r = 800 gives 4 SE of 0.031. The OLS interval with
    the usual standard error is far below 0.95 (about 0.68 measured)."""
    rng = random.Random(20261114)
    n, rho, r = 30, 0.6, 800
    x = [[1.0, float(i + 1)] for i in range(n)]
    v = ar1_covariance(n, rho)
    eye = [[float(i == j) for j in range(n)] for i in range(n)]
    hit_g = hit_o = 0
    for _ in range(r):
        u = [rng.gauss(0.0, 1.0) / math.sqrt(1.0 - rho * rho)]
        for _ in range(n - 1):
            u.append(rho * u[-1] + rng.gauss(0.0, 1.0))
        y = [1.0 + 0.2 * row[1] + ui for row, ui in zip(x, u)]
        lo, hi = confidence_intervals(generalized_least_squares(x, y, v))[1]
        hit_g += lo <= 0.2 <= hi
        lo, hi = confidence_intervals(generalized_least_squares(x, y, eye))[1]
        hit_o += lo <= 0.2 <= hi
    assert abs(hit_g / r - 0.95) < 0.031
    assert hit_o / r < 0.85


def test_feasible_gls_estimates_rho():
    """A long series: rho-hat has standard error about sqrt((1 - rho^2)/n) = 0.04; the tolerance is 4 SE."""
    rng = random.Random(5)
    n, rho = 400, 0.6
    x = [[1.0, t / n] for t in range(n)]
    u = [rng.gauss(0.0, 1.0) / math.sqrt(1.0 - rho * rho)]
    for _ in range(n - 1):
        u.append(rho * u[-1] + rng.gauss(0.0, 1.0))
    y = [2.0 - row[1] + ui for row, ui in zip(x, u)]
    fit, rho_hat = feasible_gls_ar1(x, y)
    assert abs(rho_hat - rho) < 0.16
    exact = prais_winsten(x, rho_hat)
    assert len(exact) == n and fit.df == n - 2
