# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeometric-quadrature/. The authors are listed in prov/61XER4.jsonl.

import math
import random
from fractions import Fraction as F

from isogeometric_quadrature import (
    assemble,
    basis_and_derivative,
    cardinal_bspline,
    gauss_legendre,
    half_point_rule,
    newton_cotes,
    periodic_bspline,
    spans,
    weighted_quadrature_weights,
)


def knots(p, n_el):
    return [F(0)] * (p + 1) + [F(i, n_el) for i in range(1, n_el)] + [F(1)] * (p + 1)


def exact_matrices(t, p, c):
    """Mass and stiffness for B-splines and the affine map x = c xi, exactly.

    The integrands are polynomials of degree at most 2p on each span, so the
    closed Newton-Cotes rule with 2p + 1 points is exact.
    """
    n = len(t) - p - 1
    M = [[F(0)] * n for _ in range(n)]
    K = [[F(0)] * n for _ in range(n)]
    m = 2 * p
    for k in spans(t):
        a, b = t[k], t[k + 1]
        tab = [basis_and_derivative(t, p, k, a + (b - a) * F(j, m)) for j in range(m + 1)]
        for ra in range(p + 1):
            for rb in range(p + 1):
                vm = [N[ra] * N[rb] for N, _ in tab]
                vk = [d[ra] * d[rb] for _, d in tab]
                M[k - p + ra][k - p + rb] += (b - a) * newton_cotes(m, vm) * c
                K[k - p + ra][k - p + rb] += (b - a) * newton_cotes(m, vk) / c
    return M, K


def maxdiff(A, B):
    return max(abs(float(x) - float(y)) for ra, rb in zip(A, B) for x, y in zip(ra, rb))


def greville(t, p):
    return [sum(t[i + 1 : i + p + 1]) / p for i in range(len(t) - p - 1)]


def test_gauss_degree_of_exactness():
    for n in range(1, 8):
        xs, ws = gauss_legendre(n)
        for d in range(2 * n):
            assert abs(sum(w * x**d for x, w in zip(xs, ws)) - 1 / (d + 1)) < 1e-13
        assert abs(sum(w * x ** (2 * n) for x, w in zip(xs, ws)) - 1 / (2 * n + 1)) > 1e-9


def test_p_plus_1_gauss_is_exact_for_bsplines_on_an_affine_map():
    for p in (1, 2, 3, 4):
        t = knots(p, 5)
        c = F(3)
        X = [c * g for g in greville(t, p)]  # linear precision: x = 3 xi
        M, K = assemble(t, p, X)
        Me, Ke = exact_matrices(t, p, c)
        assert maxdiff(M, Me) < 1e-12 and maxdiff(K, Ke) < 1e-11
        Mp, _ = assemble(t, p, X, n_gauss=p)  # one point fewer is not exact
        assert maxdiff(Mp, Me) > 1e-6


def test_nonaffine_polynomial_map_needs_more_points():
    p = 3
    t = knots(p, 4)
    rng = random.Random(11)
    X = sorted(g + F(rng.randint(-3, 3), 100) for g in greville(t, p))
    X[0], X[-1] = F(0), F(1)
    ref_M, ref_K = assemble(t, p, X, n_gauss=40)
    M4, K4 = assemble(t, p, X, n_gauss=p + 1)
    M5, K5 = assemble(t, p, X, n_gauss=math.ceil(3 * p / 2))  # degree 3p - 1
    assert maxdiff(M4, ref_M) > 1e-9  # mass integrand has degree 3p - 1 = 8
    assert maxdiff(M5, ref_M) < 1e-12
    assert maxdiff(K5, ref_K) > 1e-9  # stiffness integrand is rational
    K12, _ = assemble(t, p, X, n_gauss=12)[1], None
    assert maxdiff(K12, ref_K) < maxdiff(K5, ref_K)


def test_rational_weights_break_exactness():
    p = 2
    t = knots(p, 3)
    w = [F(1), F(1, 2), F(2), F(1, 2), F(1)]
    X = greville(t, p)
    ref_M, _ = assemble(t, p, X, w=w, n_gauss=40)
    M3, _ = assemble(t, p, X, w=w, n_gauss=p + 1)
    assert maxdiff(M3, ref_M) > 1e-6
    M10, _ = assemble(t, p, X, w=w, n_gauss=10)
    assert maxdiff(M10, ref_M) < maxdiff(M3, ref_M)


def test_half_point_rule_exact_on_uniform_smooth_splines():
    rng = random.Random(12)
    for p in range(1, 7):
        for h in (F(1), F(1, 3)):
            coef = {i: F(rng.randint(-9, 9)) for i in range(-4, 6)}
            f = lambda x: sum(c * cardinal_bspline(p, x / h - i) for i, c in coef.items())
            lo, hi = -6 * h, (p + 8) * h
            pts, wts = half_point_rule(p, h, lo, hi)
            q = sum(w * f(x) for x, w in zip(pts, wts))
            # exact integral by Newton-Cotes with p + 1 points on each element
            exact = sum(h * newton_cotes(p, [f(lo + (e + F(j, p)) * h) for j in range(p + 1)]) for e in range(int((hi - lo) / h)))
            assert q == exact == h * sum(coef.values())
            assert len(pts) <= (hi - lo) / h / 2 + 1  # about one point per two elements


def test_half_point_rule_fails_outside_its_space():
    # the even rule (points at even integers) on a cubic B-spline: 2 * 2/3 != 1
    pts, wts = half_point_rule(2, F(1), F(-2), F(8))
    assert sum(w * cardinal_bspline(3, x) for x, w in zip(pts, wts)) == F(4, 3)
    # and on a mass matrix integrand of degree 2p with C^(p-1) smoothness
    pts, wts = half_point_rule(2, F(1), F(-2), F(8))
    q = sum(w * cardinal_bspline(2, x) ** 2 for x, w in zip(pts, wts))
    assert q != F(11, 20)


def test_weighted_quadrature_reproduces_the_mass_matrix():
    n = 10
    for p in (1, 2, 3):
        for i in (0, 4):
            pts, wts = weighted_quadrature_weights(p, n, i)
            assert len(pts) == 2 * p + 1
            for j in range(n):
                q = sum(w * periodic_bspline(p, n, j, x) for x, w in zip(pts, wts))
                d = (j - i + n // 2) % n - n // 2
                exact = F(0)
                for a in range(-1, p + 2):
                    nodes = [a + F(k, 2 * p) for k in range(2 * p + 1)]
                    exact += newton_cotes(2 * p, [cardinal_bspline(p, x) * cardinal_bspline(p, x - d) for x in nodes])
                assert q == exact
    pts, wts = weighted_quadrature_weights(1, n, 3)
    assert wts == [F(1, 3)] * 3  # composite Cavalieri-Simpson


def test_weighted_quadrature_with_a_coefficient_is_not_symmetric():
    n, p = 10, 3
    c = lambda x: x * x
    m = {}
    for i in (3, 4):
        pts, wts = weighted_quadrature_weights(p, n, i)
        for j in (3, 4):
            m[i, j] = sum(w * c(x) * periodic_bspline(p, n, j, x) for x, w in zip(pts, wts))
    assert m[3, 4] == F(144959, 20160) and m[4, 3] == F(16087, 2240)
    assert m[3, 4] != m[4, 3]
