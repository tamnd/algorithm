# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-seidel-method/. The authors are listed in prov/2WJJ4E.jsonl.

import math
import random
from fractions import Fraction

import pytest

from gauss_seidel_method import CSR, gauss_seidel

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


def gs_matrix(a):
    """G = -(D + L)^{-1} U in exact arithmetic, column by column."""
    n = len(a)
    g = [[Fraction(0)] * n for _ in range(n)]
    for c in range(n):
        y = [Fraction(0)] * n
        for i in range(n):
            s = -(a[i][c] if c > i else 0) - sum(a[i][j] * y[j] for j in range(i))
            y[i] = Fraction(s) / a[i][i]
        for i in range(n):
            g[i][c] = y[i]
    return g


def a_norm2(a, v):
    n = len(v)
    return sum(v[i] * sum(Fraction(a[i][j]) * v[j] for j in range(n)) for i in range(n))


def laplacian(m):
    return [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(m)] for i in range(m)]


def test_page_example_exact():
    a = [[Fraction(v) for v in row] for row in [[4, -1, 0], [-1, 4, -1], [0, -1, 4]]]
    b = [Fraction(3), Fraction(2), Fraction(3)]
    want = [
        [Fraction(3, 4), Fraction(11, 16), Fraction(59, 64)],
        [Fraction(59, 64), Fraction(123, 128), Fraction(507, 512)],
        [Fraction(507, 512), Fraction(1019, 1024), Fraction(4091, 4096)],
    ]
    for k, w in enumerate(want, start=1):
        assert gauss_seidel(a, b, tol=0, maxit=k).x == w


def test_error_recursion_exact():
    rng = random.Random(4)
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
        g = gs_matrix(a)
        e = list(x)
        for k in range(1, 4):
            e = [sum(g[i][j] * e[j] for j in range(n)) for i in range(n)]
            assert [xi - yi for xi, yi in zip(x, gauss_seidel(a, b, tol=0, maxit=k).x)] == e


def test_edges():
    assert gauss_seidel([[4.0]], [2.0]).x == [0.5]
    res = gauss_seidel([[2.0, 0], [0, -4.0]], [1.0, 1.0])
    assert res.converged and res.iterations == 1 and res.x == [0.5, -0.25]
    # Lower triangular: one sweep is forward substitution.
    a = [[Fraction(v) for v in row] for row in [[2, 0, 0], [1, 3, 0], [-4, 2, 5]]]
    b = [Fraction(1), Fraction(2), Fraction(3)]
    res = gauss_seidel(a, b, tol=0, maxit=5)
    assert res.converged and res.iterations == 1 and res.x == exact_solve(a, b)
    with pytest.raises(ValueError):
        gauss_seidel([[0.0, 1.0], [1.0, 0.0]], [1.0, 1.0])


def test_singular_reports_failure():
    res = gauss_seidel([[1.0, 1.0], [1.0, 1.0]], [1.0, 2.0], maxit=30)
    assert not res.converged


def test_jacobi_wins_gs_diverges():
    a = [[1.0, 2.0, -2.0], [1.0, 1.0, 1.0], [2.0, 2.0, 1.0]]
    g = gs_matrix([[Fraction(v) for v in row] for row in a])
    assert g == [[0, -2, 2], [0, 2, -3], [0, 0, 2]]
    res = gauss_seidel(a, [1.0, 1.0, 1.0], maxit=40)
    assert not res.converged and res.residual_norms[-1] > 1e8


def test_spd_where_jacobi_diverges():
    a = [[1.0, 0.8, 0.8], [0.8, 1.0, 0.8], [0.8, 0.8, 1.0]]
    res = gauss_seidel(a, [1.0, 2.0, 3.0], tol=1e-12, maxit=500)
    assert res.converged


def test_energy_norm_monotone_exact():
    """Theorem 3: ||e_k||_A strictly decreases for SPD A (exact arithmetic)."""
    rng = random.Random(6)
    for _ in range(30):
        n = rng.randint(2, 5)
        g = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        a = [[sum(g[k][i] * g[k][j] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
        b = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        x = exact_solve(a, b)
        prev = a_norm2(a, x)
        for k in range(1, 5):
            xk = gauss_seidel(a, b, tol=0, maxit=k).x
            cur = a_norm2(a, [p - q for p, q in zip(x, xk)])
            assert cur < prev or cur == 0
            prev = cur


def test_random_dominant_rate_and_one_sweep_backward_error():
    """Theorem 4 on 500 random matrices, and Theorem 5 for the computed first sweep."""
    rng = random.Random(2026)
    for _ in range(500):
        n = rng.randint(1, 7)
        a = []
        for i in range(n):
            row = [rng.uniform(-1, 1) for _ in range(n)]
            row[i] = 0.0
            off = sum(abs(v) for v in row)
            row[i] = rng.choice([-1, 1]) * (off / rng.uniform(0.2, 0.95) + 1e-3)
            a.append(row)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        af = [[Fraction(v) for v in row] for row in a]
        x = exact_solve(af, [Fraction(v) for v in b])
        alpha = [sum(abs(af[i][j]) for j in range(i)) / abs(af[i][i]) for i in range(n)]
        beta = [sum(abs(af[i][j]) for j in range(i + 1, n)) / abs(af[i][i]) for i in range(n)]
        eta = max(bb / (1 - aa) for aa, bb in zip(alpha, beta))
        x1 = gauss_seidel(a, b, tol=0.0, maxit=1).x
        # Theorem 5: (D + L + dL) x1 + U x0 = b + db with x0 = 0.
        for i in range(n):
            lhs = sum(af[i][j] * Fraction(x1[j]) for j in range(i + 1))
            slack = gamma(n + 1) * (abs(Fraction(b[i])) + sum(abs(af[i][j] * Fraction(x1[j])) for j in range(i)))
            assert abs(lhs - Fraction(b[i])) <= slack
        # Theorem 4 (exact contraction) checked on the float iterate with a rounding allowance.
        e0 = max(abs(v) for v in x)
        e1 = max(abs(xi - Fraction(yi)) for xi, yi in zip(x, x1))
        assert e1 <= eta * e0 + 4 * n * U * (e0 + max(abs(v) for v in x1)) / (1 - eta)


def test_model_problem_rate_is_jacobi_squared():
    m = 30
    a = laplacian(m)
    rho_j = math.cos(math.pi / (m + 1))
    rng = random.Random(1)
    x0 = [rng.uniform(-1, 1) for _ in range(m)]
    x = gauss_seidel(a, [0.0] * m, x0=x0, tol=0.0, maxit=200).x
    y = gauss_seidel(a, [0.0] * m, x0=x, tol=0.0, maxit=10).x
    norm = lambda w: math.sqrt(sum(t * t for t in w))
    rate = (norm(y) / norm(x)) ** (1 / 10)
    assert abs(rate - rho_j**2) < 1e-4


def test_stagnation_on_hilbert():
    n = 6
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    b = [sum(row) for row in h]
    res = gauss_seidel(h, b, tol=1e-12, maxit=1000)
    assert not res.converged
    err = max(abs(v - 1) for v in res.x)
    assert err > 1e-2 and res.residual_norms[-1] < 1e-4
    assert all(r2 <= r1 * 10 for r1, r2 in zip(res.residual_norms[1:], res.residual_norms[2:]))


def test_symmetric_sweep_and_csr():
    rng = random.Random(10)
    n = 50
    a = laplacian(n)
    for i in range(n):
        a[i][i] += rng.uniform(0, 0.5)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    csr = CSR.from_dense(a)
    fwd = gauss_seidel(csr, b, tol=1e-10, maxit=20000)
    sym = gauss_seidel(csr, b, tol=1e-10, maxit=20000, symmetric=True)
    assert fwd.converged and sym.converged
    xe = exact_solve(a, b)
    assert max(abs(Fraction(v) - w) for v, w in zip(sym.x, xe)) < 1e-7 * max(abs(w) for w in xe) * 1e3
