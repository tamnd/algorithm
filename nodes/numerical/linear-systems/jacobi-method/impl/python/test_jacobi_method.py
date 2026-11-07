# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobi-method/. The authors are listed in prov/R75FV5.jsonl.

import math
import random
from fractions import Fraction

import pytest

from jacobi_method import CSR, jacobi

U = Fraction(1, 2**53)


def gamma(m):
    return m * U / (1 - m * U)


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


def random_dominant(rng, n, q):
    """Random matrix with off-diagonal row sums exactly q times |a_ii| (up to rounding)."""
    a = []
    for i in range(n):
        row = [rng.uniform(-1, 1) if j != i else 0.0 for j in range(n)]
        off = sum(abs(v) for v in row)
        d = rng.choice([-1, 1]) * 10 ** rng.uniform(-2, 2)
        scale = q * abs(d) / off if off else 0.0
        row = [v * scale for v in row]
        row[i] = d
        a.append(row)
    return a


def test_page_example_exact():
    a = [[4, -1, 0], [-1, 4, -1], [0, -1, 4]]
    a = [[Fraction(v) for v in row] for row in a]
    b = [Fraction(3), Fraction(2), Fraction(3)]
    want = [
        [Fraction(3, 4), Fraction(1, 2), Fraction(3, 4)],
        [Fraction(7, 8)] * 3,
        [Fraction(31, 32), Fraction(15, 16), Fraction(31, 32)],
        [Fraction(63, 64)] * 3,
    ]
    for k, w in enumerate(want, start=1):
        res = jacobi(a, b, tol=0, maxit=k)
        assert res.x == w and not res.converged


def test_error_is_power_of_iteration_matrix_exact():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(1, 5)
        a = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] = Fraction(rng.choice([-1, 1]) * rng.randint(1, 9))
        try:
            x = exact_solve(a, [Fraction(1)] * n)
        except StopIteration:
            continue
        b = [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)]
        g = [[Fraction(0) if i == j else -a[i][j] / a[i][i] for j in range(n)] for i in range(n)]
        e = list(x)  # e_0 = x - 0
        for k in range(1, 5):
            e = [sum(g[i][j] * e[j] for j in range(n)) for i in range(n)]
            res = jacobi(a, b, tol=0, maxit=k)
            assert [xi - yi for xi, yi in zip(x, res.x)] == e


def test_one_by_one_and_diagonal():
    res = jacobi([[4.0]], [2.0])
    assert res.converged and res.iterations == 1 and res.x == [0.5]
    res = jacobi([[2.0, 0, 0], [0, -5.0, 0], [0, 0, 0.25]], [1.0, 1.0, 1.0])
    assert res.converged and res.iterations == 1 and res.x == [0.5, -0.2, 4.0]


def test_triangular_terminates_in_n_sweeps_exact():
    # G_J is strictly triangular, hence nilpotent: e_n = 0.
    a = [[Fraction(v) for v in row] for row in [[2, 0, 0, 0], [1, 3, 0, 0], [-4, 2, 1, 0], [5, 1, -1, 7]]]
    b = [Fraction(1), Fraction(2), Fraction(3), Fraction(4)]
    res = jacobi(a, b, tol=0, maxit=10)
    assert res.converged and res.iterations <= 4 and res.x == exact_solve(a, b)


def test_zero_diagonal_raises():
    with pytest.raises(ValueError):
        jacobi([[0.0, 1.0], [1.0, 0.0]], [1.0, 1.0])  # needs a row swap first


def test_singular_reports_failure():
    res = jacobi([[1.0, 1.0], [1.0, 1.0]], [1.0, 2.0], maxit=50)
    assert not res.converged and res.iterations == 50


def test_spd_but_divergent():
    a = [[1.0, 0.8, 0.8], [0.8, 1.0, 0.8], [0.8, 0.8, 1.0]]
    res = jacobi(a, [1.0, 2.0, 3.0], maxit=40)
    assert not res.converged
    assert res.residual_norms[-1] > 1e5 * res.residual_norms[0]  # rho = 1.6


def test_random_dominant_rounding_bound():
    """Theorem 4 of the correctness proof, checked exactly on 500 random matrices."""
    rng = random.Random(2025)
    for t in range(500):
        n = rng.randint(1, 8)
        q = rng.choice([0.1, 0.5, 0.9])
        a = random_dominant(rng, n, q)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        if not any(b):
            b[0] = 1.0
        x = exact_solve(a, b)
        qq = max(sum(abs(Fraction(a[i][j])) for j in range(n) if j != i) / abs(Fraction(a[i][i])) for i in range(n))
        p = qq * (1 + gamma(n + 1))
        k = rng.randint(0, 60)
        res = jacobi(a, b, tol=0.0, maxit=k)
        xn = max(abs(v) for v in x)
        err = max(abs(xi - Fraction(yi)) for xi, yi in zip(x, res.x))
        bound = p**k * xn + gamma(n + 1) * (1 + 2 * qq) / (1 - p) * xn
        assert err <= bound
        if k >= 60 and q <= 0.5:
            assert err <= 8 * n * U / (1 - qq) * xn


def test_model_problem_rate():
    """1D Laplacian: rho(G_J) = cos(pi h); e_k = rho^k e_0 for the smoothest eigenvector."""
    m = 30
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(m)] for i in range(m)]
    h = 1.0 / (m + 1)
    rho = math.cos(math.pi * h)
    v = [math.sin(math.pi * (i + 1) * h) for i in range(m)]
    b = [0.0] * m  # x = 0, so x_k = -e_k
    for k in (1, 10, 100):
        res = jacobi(a, b, x0=v, tol=0.0, maxit=k)
        ratio = [xi / vi for xi, vi in zip(res.x, v)]
        assert all(abs(t - rho**k) < 1e-12 for t in ratio)
    # Iteration count for a random start against ln(1/eps)/ln(1/rho) in the 2-norm (G_J is symmetric).
    rng = random.Random(1)
    x0 = [rng.uniform(-1, 1) for _ in range(m)]
    eps = 1e-3
    kpred = math.ceil(math.log(1 / eps) / math.log(1 / rho))
    res = jacobi(a, b, x0=x0, tol=0.0, maxit=kpred)
    norm = lambda w: math.sqrt(sum(t * t for t in w))
    assert norm(res.x) <= eps * norm(x0) * (1 + 1e-9)


def test_stagnation_when_rho_near_one():
    m = 60
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(m)] for i in range(m)]
    res = jacobi(a, [1.0] * m, tol=1e-8, maxit=200)
    assert not res.converged
    assert res.residual_norms[-1] > 1e-3 * res.residual_norms[0]


def test_csr_input_and_tolerance():
    rng = random.Random(9)
    n = 40
    a = random_dominant(rng, n, 0.5)
    for i in range(n):
        for j in range(n):
            if i != j and abs(i - j) > 2:
                a[i][j] = 0.0
    b = [rng.uniform(-1, 1) for _ in range(n)]
    csr = CSR.from_dense(a)
    res = jacobi(csr, b, tol=1e-12, maxit=200)
    assert res.converged
    r = [bi - ai for bi, ai in zip(b, csr.matvec(res.x))]
    assert max(abs(v) for v in r) <= 1e-12 * max(abs(v) for v in b) * (1 + 1e-6)
    q = 0.5
    assert res.iterations <= math.ceil(math.log(1e12 * 1e4 * 1e4 * n) / math.log(1 / q))
