# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-interior-penalty-galerkin/. The authors are listed in prov/Z6FE5T.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

import scimat
from symmetric_interior_penalty_galerkin import evaluate, sipg, sipg_system

# 5-point Gauss-Legendre rule on [-1, 1], independent of the code under test
GX = [-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640]
GW = [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891]


def errors(coef, m, u, du):
    h = 1.0 / m
    e0 = e1 = 0.0
    for j in range(m):
        c = coef[j]
        for xg, wg in zip(GX, GW):
            xi = (xg + 1) / 2
            x = j * h + xi * h
            v = sum(float(cr) * xi ** r for r, cr in enumerate(c))
            d = sum(float(cr) * r * xi ** (r - 1) for r, cr in enumerate(c) if r) / h
            e0 += wg * h / 2 * (v - u(x)) ** 2
            e1 += wg * h / 2 * (d - du(x)) ** 2
    return math.sqrt(e0), math.sqrt(e1)


def local_coefficients(p, x0, h):
    """Coefficients of p(x0 + xi h) in powers of xi, for p given by its coefficients in powers of x."""
    out = [F(0)] * len(p)
    for n, pn in enumerate(p):
        # (x0 + xi h)^n = sum_r C(n, r) x0^(n - r) h^r xi^r
        for r in range(n + 1):
            out[r] += pn * math.comb(n, r) * x0 ** (n - r) * h ** r
    return out


def test_page_example_two_cells() -> None:
    A, b = sipg_system(lambda x: F(2), 2, 1, F(3))
    assert A == [[12, 7, -6, -1], [7, 6, -5, -1], [-6, -5, 12, 5], [-1, -1, 5, 4]]
    assert b == [1, F(1, 2), 1, F(1, 2)]
    c = sipg(lambda x: F(2), 2, 1, F(3))
    assert c == [[F(1, 8), F(1, 8)], [F(1, 4), F(-1, 8)]]
    # the boundary value is only imposed weakly: u_h(0+) = 1 / (4 (sigma - 1))
    for s in (F(3), F(10), F(100)):
        c = sipg(lambda x: F(2), 2, 1, s)
        assert c[0][0] == 1 / (4 * (s - 1))
        assert sum(c[0]) == F(1, 4) == c[1][0]


def test_matrix_is_symmetric_exactly() -> None:
    for m, k in ((1, 1), (3, 2), (4, 3)):
        A, _ = sipg_system(lambda x: F(0), m, k, F(2 * k * k + 1))
        n = len(A)
        assert all(A[i][j] == A[j][i] for i in range(n) for j in range(n))


def test_spd_above_bound_and_not_spd_below() -> None:
    for m in (1, 2, 5):
        for k in (1, 2, 3):
            A, _ = sipg_system(lambda x: 0.0, m, k, 2.0 * k * k + 0.01)
            scimat.cholesky(A)  # raises if not positive definite
    # k = 1: the bounds 2 (one cell) and 3/2 (two or more cells) are sharp
    for m, s in ((1, 2.0), (2, 1.5)):
        with pytest.raises(ValueError):
            scimat.cholesky(sipg_system(lambda x: 0.0, m, 1, s - 0.01)[0])
        scimat.cholesky(sipg_system(lambda x: 0.0, m, 1, s + 0.01)[0])
    with pytest.raises(ValueError):
        scimat.cholesky(sipg_system(lambda x: 0.0, 6, 2, 1.0)[0])


def test_polynomials_of_degree_k_are_reproduced_exactly() -> None:
    # u = x^2 with k = 2, Fraction arithmetic: the discrete solution is u itself
    m, k = 3, 2
    c = sipg(lambda x: F(-2), m, k, F(9), F(0), F(1))
    h = F(1, m)
    assert c == [local_coefficients([0, 0, 1], j * h, h) for j in range(m)]


def test_random_polynomials_against_closed_form() -> None:
    # oracle: the exact solution, a random polynomial of degree <= k
    rng = random.Random(11)
    for _ in range(500):
        k = rng.randint(1, 3)
        m = rng.randint(1, 4)
        p = [rng.randint(-5, 5) for _ in range(k + 1)]
        # f = -p''
        f2 = [-(n + 2) * (n + 1) * p[n + 2] for n in range(k - 1)]

        def f(x, f2=f2):
            return sum(cn * x ** n for n, cn in enumerate(f2))

        def u(x, p=p):
            return sum(cn * x ** n for n, cn in enumerate(p))

        sigma = 2.0 * k * k + rng.uniform(0.5, 10.0)
        coef = sipg(f, m, k, sigma, u(0.0), u(1.0))
        h = F(1, m)
        for j in range(m):
            want = local_coefficients([F(v) for v in p], j * h, h)
            assert all(abs(float(a) - float(b)) < 1e-8 for a, b in zip(coef[j], want))


def test_convergence_rates() -> None:
    u = lambda x: math.sin(math.pi * x)
    du = lambda x: math.pi * math.cos(math.pi * x)
    f = lambda x: math.pi ** 2 * math.sin(math.pi * x)
    for k in (1, 2, 3):
        e = [errors(sipg(f, m, k), m, u, du) for m in (8, 16)]
        assert abs(math.log2(e[0][0] / e[1][0]) - (k + 1)) < 0.15
        assert abs(math.log2(e[0][1] / e[1][1]) - k) < 0.15


def test_evaluate_and_weak_boundary_values() -> None:
    f = lambda x: math.pi ** 2 * math.sin(math.pi * x)
    coef = sipg(f, 8, 2)
    v, d = evaluate(coef, 8, 0.5)
    assert abs(v - 1.0) < 1e-3 and abs(d) < 1e-2
    # the boundary value is close to 0 but not equal to it
    v0, _ = evaluate(coef, 8, 0.0)
    assert 0 < abs(v0) < 1e-3
