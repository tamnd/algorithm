# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-method-of-moments/. The authors are listed in prov/A39F7K.jsonl.

import math
import random
from fractions import Fraction

from generalized_method_of_moments import (
    efficient_cov,
    gmm,
    inverse,
    mean_jacobian,
    objective,
    sandwich_cov,
    solve,
)


def poisson(rng: random.Random, m: float) -> int:
    u, k, pk = rng.random(), 0, math.exp(-m)
    cum = pk
    while u > cum:
        k += 1
        pk *= m / k
        cum += pk
    return k


def pois_g(x, t):
    lam = t[0]
    return [x - lam, x * x - lam - lam * lam]


def pois_dg(x, t):
    return [[-1], [-1 - 2 * t[0]]]


def ols(x, y):
    p = len(x[0])
    xtx = [[sum(r[i] * r[j] for r in x) for j in range(p)] for i in range(p)]
    xty = [sum(r[i] * yi for r, yi in zip(x, y)) for i in range(p)]
    return solve(xtx, xty)


def test_exactly_identified_is_method_of_moments():
    rng = random.Random(1)
    xs = [rng.gauss(5, 2) for _ in range(60)]

    def g(x, t):
        return [x - t[0], x * x - t[1] - t[0] * t[0]]

    def dg(x, t):
        return [[-1.0, 0.0], [-2.0 * t[0], -1.0]]

    res = gmm(g, xs, [0.0, 1.0], dg)
    n = len(xs)
    mean = sum(xs) / n
    var_n = sum((x - mean) ** 2 for x in xs) / n  # divisor n
    assert abs(res.theta[0] - mean) < 1e-10 and abs(res.theta[1] - var_n) < 1e-9
    assert res.df == 0 and res.p_value == 1.0 and res.j_stat < 1e-15
    assert res.converged


def iv_data():
    # y = 1 + 2 x + u, x endogenous, two instruments plus the constant
    rows = [
        (3, 1, 0, 1), (6, 2, 1, 1), (4, 1, 1, 0), (9, 4, 2, 1),
        (2, 0, 0, 0), (8, 3, 2, 0), (5, 2, 0, 2), (11, 5, 3, 2), (7, 3, 1, 1),
    ]
    y = [Fraction(r[0]) for r in rows]
    x = [[Fraction(1), Fraction(r[1])] for r in rows]
    z = [[Fraction(1), Fraction(r[2]), Fraction(r[3])] for r in rows]
    return y, x, z


def test_linear_iv_first_step_is_two_stage_least_squares_exact():
    y, x, z = iv_data()
    n = len(y)
    data = list(zip(y, x, z))

    def g(d, b):
        yi, xi, zi = d
        e = yi - xi[0] * b[0] - xi[1] * b[1]
        return [zj * e for zj in zi]

    def dg(d, b):
        _, xi, zi = d
        return [[-zj * xk for xk in xi] for zj in zi]

    zz = [[sum(r[i] * r[j] for r in z) / n for j in range(3)] for i in range(3)]
    res = gmm(g, data, [Fraction(0), Fraction(0)], dg, w1=inverse(zz), tol=0)
    # reference: the two literal stages
    xhat_cols = []
    for col in range(2):
        c = ols(z, [xi[col] for xi in x])
        xhat_cols.append([sum(zi[j] * c[j] for j in range(3)) for zi in z])
    xhat = [list(r) for r in zip(*xhat_cols)]
    assert res.first_step == ols(xhat, y)
    # second step: closed form (X'Z S^-1 Z'X)^-1 X'Z S^-1 Z'y with S from the first step
    b1 = res.first_step
    rows = [[zj * (yi - xi[0] * b1[0] - xi[1] * b1[1]) for zj in zi] for yi, xi, zi in data]
    gb = [sum(r[j] for r in rows) / n for j in range(3)]
    s = [[sum((r[i] - gb[i]) * (r[j] - gb[j]) for r in rows) / n for j in range(3)] for i in range(3)]
    si = inverse(s)
    xz = [[sum(xi[a] * zi[j] for xi, zi in zip(x, z)) for j in range(3)] for a in range(2)]
    zy = [sum(zi[j] * yi for zi, yi in zip(z, y)) for j in range(3)]
    m = [[sum(xz[a][i] * si[i][j] * xz[b][j] for i in range(3) for j in range(3)) for b in range(2)] for a in range(2)]
    r = [sum(xz[a][i] * si[i][j] * zy[j] for i in range(3) for j in range(3)) for a in range(2)]
    assert res.theta == solve(m, r)
    assert res.df == 1 and res.j_stat >= 0


def test_poisson_two_moments_against_grid_search():
    rng = random.Random(3)
    xs = [poisson(rng, 3.0) for _ in range(150)]
    res = gmm(pois_g, xs, [1.0], pois_dg)
    w = res.weight
    c = sum(xs) / len(xs)
    best = min((objective(pois_g, xs, [c - 1 + i / 10000], w), c - 1 + i / 10000) for i in range(20001))
    h = 1e-4
    best = min((objective(pois_g, xs, [best[1] - h + i * h / 5000], w), best[1] - h + i * h / 5000) for i in range(10001))
    assert abs(res.theta[0] - best[1]) < 1e-7
    assert objective(pois_g, xs, res.theta, w) <= best[0] + 1e-15
    assert abs(res.j_stat - len(xs) * objective(pois_g, xs, res.theta, w)) < 1e-9


def test_numeric_jacobian_matches_analytic():
    rng = random.Random(4)
    xs = [poisson(rng, 2.0) for _ in range(50)]
    a = mean_jacobian(pois_dg, pois_g, xs, [2.3])
    b = mean_jacobian(None, pois_g, xs, [2.3])
    assert all(abs(u[0] - v[0]) < 1e-7 for u, v in zip(a, b))
    r1 = gmm(pois_g, xs, [1.0], pois_dg)
    r2 = gmm(pois_g, xs, [1.0])
    assert abs(r1.theta[0] - r2.theta[0]) < 1e-8


def test_poisson_efficient_variance_is_cramer_rao_exact():
    # Population G and S for the two Poisson moments; efficient GMM reaches lambda / n.
    lam, n = Fraction(5, 2), 40
    big_g = [[Fraction(-1)], [-1 - 2 * lam]]
    s = [[lam, 2 * lam * lam + lam], [2 * lam * lam + lam, 4 * lam ** 3 + 6 * lam * lam + lam]]
    assert efficient_cov(big_g, s, n) == [[lam / n]]
    ident = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    assert sandwich_cov(big_g, ident, s, n)[0][0] > lam / n
    assert sandwich_cov(big_g, inverse(s), s, n) == [[lam / n]]


def test_sandwich_minus_efficient_is_positive_semidefinite_exact():
    rng = random.Random(5)
    for _ in range(30):
        big_g = [[Fraction(rng.randint(-4, 4)) for _ in range(2)] for _ in range(4)]
        a = [[Fraction(rng.randint(-3, 3)) for _ in range(4)] for _ in range(4)]
        b = [[Fraction(rng.randint(-3, 3)) for _ in range(4)] for _ in range(4)]
        s = [[sum(a[i][t] * a[j][t] for t in range(4)) + (i == j) for j in range(4)] for i in range(4)]
        w = [[sum(b[i][t] * b[j][t] for t in range(4)) + (i == j) for j in range(4)] for i in range(4)]
        gtg = [[sum(big_g[t][i] * big_g[t][j] for t in range(4)) for j in range(2)] for i in range(2)]
        if gtg[0][0] * gtg[1][1] - gtg[0][1] ** 2 == 0:
            continue
        d = sandwich_cov(big_g, w, s, 1)
        e = efficient_cov(big_g, s, 1)
        m = [[d[i][j] - e[i][j] for j in range(2)] for i in range(2)]
        assert m[0][0] >= 0 and m[1][1] >= 0 and m[0][0] * m[1][1] - m[0][1] * m[1][0] >= 0


def test_j_test_size_and_power_measured():
    # Measured, not proved: rejection rate of the J test at level 0.05.
    # At n = 200 the test over-rejects a little (about 0.07 in 1000 runs),
    # so the bound is wide: it checks the chi-squared scale, not exact size.
    r, n = 300, 200
    rng = random.Random(6)
    rej = 0
    for _ in range(r):
        xs = [poisson(rng, 3.0) for _ in range(n)]
        rej += gmm(pois_g, xs, [sum(xs) / n], pois_dg).p_value < 0.05
    size = rej / r
    assert 0.02 < size < 0.05 + 4 * math.sqrt(0.05 * 0.95 / r)
    # negative binomial with mean 3 and variance 6: the second condition fails
    rej = 0
    for _ in range(100):
        xs = [poisson(rng, rng.gammavariate(3.0, 1.0)) for _ in range(n)]
        rej += gmm(pois_g, xs, [sum(xs) / n], pois_dg).p_value < 0.05
    assert rej / 100 > 0.8
