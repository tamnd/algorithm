# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjugate-gradient-method/. The authors are listed in prov/QAMAC5.jsonl.

import math
import random
from fractions import Fraction

import pytest

from conjugate_gradient_method import CSR, NotPositiveDefinite, conjugate_gradient, dense_matvec, dot


def exact_solve(a, b):
    """Gaussian elimination in rational arithmetic: an independent oracle."""
    n = len(b)
    m = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k] != 0)
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def laplacian_1d(n, one=1):
    return [[2 * one if i == j else (-one if abs(i - j) == 1 else 0 * one) for j in range(n)] for i in range(n)]


def random_spd(rng, n, shift=0.1):
    g = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    a = [[sum(g[k][i] * g[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    for i in range(n):
        a[i][i] += shift
    return a


def test_page_example_exact():
    a = laplacian_1d(5, Fraction(1))
    b = [Fraction(1)] * 5
    res = conjugate_gradient(dense_matvec(a), b, tol=0)
    assert res.converged and res.iterations == 3
    assert res.x == [Fraction(5, 2), Fraction(4), Fraction(9, 2), Fraction(4), Fraction(5, 2)]
    assert res.rho_history == [5, Fraction(15, 2), Fraction(3, 2), 0]


def test_one_by_one():
    res = conjugate_gradient(dense_matvec([[4.0]]), [2.0])
    assert res.converged and res.iterations == 1 and res.x == [0.5]


def test_finite_termination_exact_arithmetic():
    rng = random.Random(31)
    for _ in range(60):
        n = rng.randint(1, 6)
        a = [[Fraction(v).limit_denominator(64) for v in row] for row in random_spd(rng, n)]
        a = [[a[min(i, j)][max(i, j)] for j in range(n)] for i in range(n)]
        b = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        if not any(b):
            b[0] = Fraction(1)
        res = conjugate_gradient(dense_matvec(a), b, tol=0, maxit=n + 1)
        assert res.converged and res.iterations <= n
        assert res.x == exact_solve(a, b)


def test_random_float_against_exact():
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(1, 8)
        a = random_spd(rng, n, shift=0.5)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        res = conjugate_gradient(dense_matvec(a), b, tol=1e-12, maxit=20 * n)
        assert res.converged
        xe = exact_solve(a, b)
        e = [Fraction(v) - w for v, w in zip(res.x, xe)]
        ae = [sum(Fraction(a[i][j]) * e[j] for j in range(n)) for i in range(n)]
        err_a = math.sqrt(float(sum(u * v for u, v in zip(e, ae))))
        xa = [sum(Fraction(a[i][j]) * xe[j] for j in range(n)) for i in range(n)]
        x_a = math.sqrt(float(sum(u * v for u, v in zip(xe, xa))))
        assert err_a <= 1e-8 * x_a


def test_iteration_count_within_chebyshev_bound():
    rng = random.Random(5)
    n, kappa, eps = 300, 100.0, 1e-8
    lam = [1.0 + (kappa - 1.0) * i / (n - 1) for i in range(n)]
    b = [rng.uniform(-1, 1) for _ in range(n)]
    x = [bi / li for bi, li in zip(b, lam)]
    mv = lambda v: [li * vi for li, vi in zip(lam, v)]
    k_bound = math.ceil(0.5 * math.sqrt(kappa) * math.log(2 / eps))
    a_norm = lambda e: math.sqrt(sum(li * ei * ei for li, ei in zip(lam, e)))
    e0 = a_norm(x)
    for k in (10, 30, 60, k_bound):
        res = conjugate_gradient(mv, b, tol=0.0, maxit=k)
        ek = a_norm([xi - yi for xi, yi in zip(x, res.x)])
        rate = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
        assert ek <= 2 * rate**k * e0 * (1 + 1e-6) + 1e-14 * e0
    assert ek <= eps * e0


def test_clustered_spectrum_converges_fast():
    rng = random.Random(8)
    n = 120
    lam = [float(1 + i % 3) for i in range(n)]  # three distinct eigenvalues
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = conjugate_gradient(lambda v: [li * vi for li, vi in zip(lam, v)], b, tol=1e-12)
    assert res.converged and res.iterations <= 4


def test_residual_not_monotone_but_converges():
    a = laplacian_1d(5, 1.0)
    res = conjugate_gradient(dense_matvec(a), [1.0] * 5, tol=1e-14)
    assert res.rho_history[1] > res.rho_history[0]
    assert res.converged and res.iterations == 3


def test_indefinite_detected():
    with pytest.raises(NotPositiveDefinite):
        conjugate_gradient(dense_matvec([[1.0, 0.0], [0.0, -1.0]]), [1.0, 1.0])


def test_stagnation_below_attainable_accuracy():
    # The updated residual keeps falling, the true residual b - A x_k levels off near u.
    n = 10
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    b = [sum(row) for row in h]
    nb = math.sqrt(dot(b, b))
    true_rel = []
    for maxit in (100, 300):
        res = conjugate_gradient(dense_matvec(h), b, tol=1e-30, maxit=maxit)
        r = [bi - ai for bi, ai in zip(b, dense_matvec(h)(res.x))]
        true_rel.append(math.sqrt(dot(r, r)) / nb)
    updated_rel = math.sqrt(res.rho_history[-1]) / nb
    assert updated_rel < 1e-25
    assert true_rel[1] > 1e-18 and true_rel[1] > 1e6 * updated_rel
    assert true_rel[1] > true_rel[0] / 10
    assert not conjugate_gradient(dense_matvec(h), b, tol=1e-30, maxit=3).converged


def test_jacobi_preconditioner_helps_bad_scaling():
    rng = random.Random(12)
    n = 60
    base = laplacian_1d(n, 1.0)
    d = [10.0 ** rng.uniform(-3, 3) for _ in range(n)]
    a = [[d[i] ** 0.5 * base[i][j] * d[j] ** 0.5 for j in range(n)] for i in range(n)]
    b = [rng.uniform(-1, 1) for _ in range(n)]
    csr = CSR.from_dense(a)
    assert csr.matvec(b) == dense_matvec(a)(b)
    plain = conjugate_gradient(csr.matvec, b, tol=1e-10, maxit=2000)
    pre = conjugate_gradient(csr.matvec, b, tol=1e-10, maxit=2000, precond=lambda r: [ri / a[i][i] for i, ri in enumerate(r)])
    assert pre.converged and pre.iterations < plain.iterations
