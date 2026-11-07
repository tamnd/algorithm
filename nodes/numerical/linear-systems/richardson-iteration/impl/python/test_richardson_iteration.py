# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/richardson-iteration/. The authors are listed in prov/5FXKP1.jsonl.

import math
import random
from fractions import Fraction

from richardson_iteration import (
    chebyshev_omegas, from_dense, norm2, optimal_omega, residual, richardson,
)

U = 2.0 ** -53


def model(n):
    return [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]


def model_eigs(n):
    return [2 - 2 * math.cos(math.pi * j / (n + 1)) for j in range(1, n + 1)]


def reflected(lams, v):
    """Q diag(lams) Q with Q = I - 2 v v^T / v^T v, exact in Fractions: eigenvalues lams."""
    n = len(lams)
    vv = sum(t * t for t in v)
    q = [[(1 if i == j else 0) - 2 * v[i] * v[j] / vv for j in range(n)] for i in range(n)]
    return [[sum(q[i][k] * lams[k] * q[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def test_one_by_one_exact_in_one_step():
    x, k, ok = richardson(from_dense([[4.0]]), [8.0], 0.25)
    assert ok and k == 1 and x == [2.0]


def test_zero_rhs_needs_no_step():
    x, k, ok = richardson(from_dense(model(5)), [0.0] * 5, 0.5)
    assert ok and k == 0 and x == [0.0] * 5


def test_diagonal_residual_contracts_by_exact_factor():
    d = [Fraction(1), Fraction(2), Fraction(4)]
    rows = from_dense([[d[i] if i == j else Fraction(0) for j in range(3)] for i in range(3)])
    b = [Fraction(1)] * 3
    w = Fraction(2, 5)  # optimal 2 / (1 + 4)
    x = [Fraction(0)] * 3
    for k in range(1, 6):
        x, _, _ = richardson(rows, b, w, x0=x, tol=0, maxiter=1)
        r = residual(rows, b, x)
        assert r == [(1 - w * di) ** k for di in d]
    assert max(abs(1 - w * di) for di in d) == Fraction(3, 5)  # (kappa - 1)/(kappa + 1)


def test_exact_roots_annihilate_the_residual():
    rng = random.Random(1)
    for _ in range(25):
        n = rng.randint(1, 5)
        lams = [Fraction(rng.randint(1, 6)) for _ in range(n)]
        v = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        if all(t == 0 for t in v):
            v[0] = Fraction(1)
        a = reflected(lams, v)
        b = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        if all(t == 0 for t in b):
            b[0] = Fraction(1)
        distinct = sorted(set(lams))
        x, k, ok = richardson(from_dense(a), b, [1 / lam for lam in distinct], tol=0, maxiter=len(distinct))
        assert residual(from_dense(a), b, x) == [0] * n  # finite termination in exact arithmetic


def test_random_spd_iteration_count_within_theory():
    rng = random.Random(2)
    for _ in range(30):
        n = rng.randint(2, 6)
        lams = [Fraction(rng.randint(1, 30)) for _ in range(n)]
        v = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        if all(t == 0 for t in v):
            v[0] = Fraction(1)
        a = [[float(t) for t in row] for row in reflected(lams, v)]
        lmin, lmax = float(min(lams)), float(max(lams))
        b = [rng.uniform(-1, 1) for _ in range(n)]
        w = optimal_omega(lmin, lmax) if rng.random() < 0.5 else 1.0 / lmax
        rho = max(abs(1 - w * float(lam)) for lam in lams)
        tol = 1e-9
        x, k, ok = richardson(from_dense(a), b, w, tol=tol, maxiter=50000)
        assert ok
        if rho > 0:
            # ||r_k||_2 <= rho^k ||r_0||_2 (G symmetric), r_0 = b: proved, plus slack for rounding
            assert k <= math.ceil(math.log(tol) / math.log(rho)) + 2


def test_model_problem_count_matches_kappa():
    n, tol = 20, 1e-8
    rows, b = from_dense(model(n)), [1.0] * n
    lam = model_eigs(n)
    lmin, lmax = lam[0], lam[-1]
    rho = (lmax / lmin - 1) / (lmax / lmin + 1)
    _, k, ok = richardson(rows, b, optimal_omega(lmin, lmax), tol=tol, maxiter=5000)
    pred = math.log(tol) / math.log(rho)
    assert ok and 0.9 * pred <= k <= pred + 1


def test_chebyshev_parameters_meet_the_chebyshev_bound():
    n, m, tol = 20, 16, 1e-8
    rows, b = from_dense(model(n)), [1.0] * n
    lam = model_eigs(n)
    lmin, lmax = lam[0], lam[-1]
    om = chebyshev_omegas(lmin, lmax, m)
    x, k, ok = richardson(rows, b, om, tol=tol, maxiter=2000)
    assert ok
    t = (lmax + lmin) / (lmax - lmin)
    per_cycle = 1.0 / math.cosh(m * math.acosh(t))
    x = [0.0] * n
    for c in range(1, 6):
        x, _, _ = richardson(rows, b, om, x0=x, tol=0, maxiter=m)
        assert norm2(residual(rows, b, x)) <= per_cycle ** c * norm2(b) * (1 + 1e-6)
    _, kst, _ = richardson(rows, b, optimal_omega(lmin, lmax), tol=tol, maxiter=5000)
    assert k < kst / 5  # sqrt(kappa) against kappa


def test_omega_too_large_diverges():
    n = 20
    rows, b = from_dense(model(n)), [1.0] * n
    x, k, ok = richardson(rows, b, 0.6, maxiter=100)  # 0.6 > 2 / lambda_max = 0.503
    assert not ok and norm2(residual(rows, b, x)) > 1e6


def test_omega_at_the_limit_stagnates():
    n = 20
    rows = from_dense(model(n))
    lmax = model_eigs(n)[-1]
    b = [1.0] + [0.0] * (n - 1)  # has a component along the top eigenvector
    x, k, ok = richardson(rows, b, 2.0 / lmax, maxiter=3000)
    assert not ok
    r = norm2(residual(rows, b, x))
    assert 1e-3 < r < 1.0  # the factor -1 neither grows nor decays


def test_symmetric_indefinite_fails_for_every_omega():
    rows = from_dense([[1.0, 2.0], [2.0, 1.0]])  # eigenvalues 3 and -1
    for w in (0.1, 0.5, -0.1, -0.5):
        x, k, ok = richardson(rows, [1.0, 0.5], w, maxiter=300)
        assert not ok


def test_stagnation_at_rounding_level():
    n = 20
    rows, b = from_dense(model(n)), [1.0] * n
    lam = model_eigs(n)
    x, k, ok = richardson(rows, b, optimal_omega(lam[0], lam[-1]), tol=1e-18, maxiter=4000)
    assert not ok
    r = max(abs(t) for t in residual(rows, b, x))
    xn = max(abs(t) for t in x)
    assert r <= n * U * 4.0 * xn  # observed, not a proved bound
    exact = [(i + 1) * (n - i) / 2 for i in range(n)]
    assert max(abs(p - q) for p, q in zip(x, exact)) <= 1e-11
