# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gmres/. The authors are listed in prov/JYTTHH.jsonl.

import math
import random
from fractions import Fraction

from gmres import CSR, gmres

U = 2.0**-53


def exact_min_residual(a, r0, k):
    """min ||r0 - A K c||_2 over the Krylov space K_k(A, r0), in Fractions.

    Returns the squared minimum, from the normal equations of the
    (exact) power basis; fine for the small sizes used here.
    """
    n = len(r0)
    af = [[Fraction(t) for t in row] for row in a]
    r = [Fraction(t) for t in r0]
    basis = [r]
    for _ in range(k - 1):
        basis.append([sum(p * q for p, q in zip(row, basis[-1])) for row in af])
    w = [[sum(p * q for p, q in zip(row, col)) for row in af] for col in basis]
    # Gaussian elimination on G c = h with G = W^T W, h = W^T r, dropping
    # dependent columns.
    cols = []
    for col in w:
        cols.append(col)
    g = [[sum(p * q for p, q in zip(ci, cj)) for cj in cols] for ci in cols]
    h = [sum(p * q for p, q in zip(ci, r)) for ci in cols]
    m = len(cols)
    keep = []
    aug = [row[:] + [h[i]] for i, row in enumerate(g)]
    rank_rows = []
    piv_col = []
    rowi = 0
    for c in range(m):
        p = next((i for i in range(rowi, m) if aug[i][c] != 0), None)
        if p is None:
            continue
        aug[rowi], aug[p] = aug[p], aug[rowi]
        for i in range(m):
            if i != rowi and aug[i][c] != 0:
                f = aug[i][c] / aug[rowi][c]
                aug[i] = [s - f * t for s, t in zip(aug[i], aug[rowi])]
        piv_col.append(c)
        rowi += 1
    coef = [Fraction(0)] * m
    for i, c in enumerate(piv_col):
        coef[c] = aug[i][m] / aug[i][c]
    res = [ri - sum(coef[j] * cols[j][i] for j in range(m)) for i, ri in enumerate(r)]
    return sum(t * t for t in res)


def residual(a, b, x):
    return [bi - sum(p * q for p, q in zip(row, x)) for row, bi in zip(a, b)]


def norm(v):
    return math.sqrt(sum(t * t for t in v))


def test_one_by_one():
    res = gmres([[4.0]], [2.0])
    assert res.converged and res.iterations == 1
    assert res.x == [0.5]


def test_page_example():
    a = [[2.0, 1.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 2.0]]
    b = [0.0, 0.0, 1.0]
    res = gmres(a, b, tol=1e-14)
    # history equals the exact minimum residuals over K_k
    for k in range(1, 4):
        exact = math.sqrt(float(exact_min_residual(a, b, k)))
        assert abs(res.history[k] - exact) <= 1e-13
    assert abs(res.history[1] - math.sqrt(1 / 5)) < 1e-15
    assert res.iterations == 3
    assert max(abs(s - t) for s, t in zip(res.x, [0.125, -0.25, 0.5])) < 1e-15


def test_random_against_exact_minimum():
    rng = random.Random(20261107)
    for trial in range(500):
        n = rng.randint(1, 6)
        a = [[float(rng.randint(-5, 5)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] += 12.0  # keep A well conditioned
        b = [float(rng.randint(-9, 9)) for _ in range(n)]
        if all(t == 0 for t in b):
            b[0] = 1.0
        res = gmres(a, b, tol=1e-13)
        assert res.converged
        k = min(len(res.history) - 1, n)
        for j in range(1, k + 1):
            exact = math.sqrt(float(exact_min_residual(a, b, j)))
            assert abs(res.history[j] - exact) <= 1e-9 * norm(b)
        # monotone residuals, at most n steps
        assert all(s <= t * (1 + 1e-12) for s, t in zip(res.history[1:], res.history))
        assert res.iterations <= n
        r = residual(a, b, res.x)
        anorm = max(sum(abs(t) for t in row) for row in a)
        eta = max(map(abs, r)) / (anorm * max(map(abs, res.x)) + max(map(abs, b)))
        assert eta <= 1e-12


def test_few_distinct_eigenvalues():
    # A = V D V^{-1} with three distinct eigenvalues: three steps.
    n = 9
    rng = random.Random(3)
    d = [1.0, 2.0, 5.0] * 3
    a = [[(d[i] if i == j else 0.0) for j in range(n)] for i in range(n)]
    # similarity with a unit upper bidiagonal T: T D T^{-1} keeps eigenvalues
    # but is nonnormal; diagonalizable since D is.
    t = [[1.0 if i == j else (0.5 if j == i + 1 else 0.0) for j in range(n)] for i in range(n)]
    tinv = [[(-0.5) ** (j - i) if j >= i else 0.0 for j in range(n)] for i in range(n)]
    td = [[t[i][j] * d[j] for j in range(n)] for i in range(n)]
    a = [[sum(td[i][k] * tinv[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = gmres(a, b, tol=1e-12)
    assert res.converged and res.iterations == 3


def test_cyclic_shift_stagnates_until_step_n():
    n = 8
    a = [[1.0 if i == (j + 1) % n else 0.0 for j in range(n)] for i in range(n)]
    b = [1.0] + [0.0] * (n - 1)
    res = gmres(a, b, tol=1e-12)
    assert res.converged and res.iterations == n
    assert all(abs(h - 1.0) < 1e-14 for h in res.history[: n])
    assert res.x == [0.0] * (n - 1) + [1.0]


def test_restarted_stagnation():
    # GMRES(1) on a rotation: A r is orthogonal to r, no progress ever.
    a = [[0.0, 1.0], [-1.0, 0.0]]
    res = gmres(a, [1.0, 0.0], restart=1, maxit=50)
    assert not res.converged and res.status == "maxit"
    assert all(abs(h - 1.0) < 1e-15 for h in res.history)
    full = gmres(a, [1.0, 0.0])
    assert full.converged and full.iterations == 2


def test_chebyshev_bound_spd():
    # For SPD A, ||r_k|| <= 2 ((sqrt k - 1)/(sqrt k + 1))^k ||r_0||.
    n, kappa = 200, 100.0
    d = [1.0 + (kappa - 1.0) * i / (n - 1) for i in range(n)]
    a = CSR(n, list(range(n + 1)), list(range(n)), d)
    rng = random.Random(11)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = gmres(a, b, tol=1e-8, restart=60)
    q = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    for k, h in enumerate(res.history[:61]):
        assert h <= 2 * q**k * res.history[0] * (1 + 1e-8) + 1e-14
    bound_k = math.ceil(math.log(2 / 1e-8) / math.log(1 / q))
    assert res.converged and res.iterations <= bound_k


def test_singular_reports_failure():
    a = [[1.0, 0.0], [0.0, 0.0]]
    res = gmres(a, [0.0, 1.0])
    assert not res.converged and res.status == "breakdown"
    res = gmres(a, [1.0, 1.0], maxit=20)
    assert not res.converged
    # consistent singular system is solved
    res = gmres(a, [3.0, 0.0])
    assert res.converged and res.x == [3.0, 0.0]


def test_hilbert_backward_stable():
    n = 8
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    xt = [1.0] * n
    b = [sum(row) for row in h]
    res = gmres(h, b, tol=1e-15, maxit=n)
    r = residual(h, b, res.x)
    hn = max(sum(abs(t) for t in row) for row in h)
    eta = max(map(abs, r)) / (hn * max(map(abs, res.x)) + max(map(abs, b)))
    assert eta < 100 * n * U
    ferr = max(abs(s - t) for s, t in zip(res.x, xt))
    assert ferr > 1e-8  # forward error is about kappa u, kappa(H_8) ~ 1.5e10


def test_restart_converges_convection_diffusion():
    n = 120
    rows = []
    for i in range(n):
        row = [0.0] * n
        row[i] = 2.0
        if i > 0:
            row[i - 1] = -1.3
        if i < n - 1:
            row[i + 1] = -0.7
        rows.append(row)
    a = CSR.from_dense(rows)
    b = [1.0] * n
    res = gmres(a, b, tol=1e-10, restart=20, maxit=2000)
    assert res.converged and res.restarts >= 1
    r = residual(rows, b, res.x)
    assert norm(r) <= 1e-9 * norm(b)
