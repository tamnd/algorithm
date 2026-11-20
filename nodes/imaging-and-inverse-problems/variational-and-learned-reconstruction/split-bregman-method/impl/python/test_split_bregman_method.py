# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-bregman-method/. The authors are listed in prov/4TK5JZ.jsonl.

import itertools
import math
import random

from split_bregman_method import (
    chol_solve,
    cholesky,
    difference_matrix,
    gradient_matrix,
    mat_t_vec,
    mat_vec,
    objective,
    split_bregman,
)


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def rof_brute(f, lam):
    """Exact 1D TV denoising by trying every sign pattern of the differences."""
    n = len(f)
    I, D = eye(n), difference_matrix(n)
    best, best_val = None, math.inf
    for s in itertools.product((-1, 0, 1), repeat=n - 1):
        cuts = [0] + [b + 1 for b in range(n - 1) if s[b] != 0] + [n]
        u = []
        for a, b in zip(cuts, cuts[1:]):
            sl = s[a - 1] if a > 0 else 0
            sr = s[b - 1] if b < n else 0
            u.extend([sum(f[a:b]) / (b - a) - lam * (sl - sr) / (b - a)] * (b - a))
        val = objective(I, f, D, lam, u)
        if val < best_val:
            best, best_val = u, val
    return best


def lasso_brute(A, y, lam):
    n = len(A[0])
    best, best_val = [0.0] * n, objective(A, y, eye(n), lam, [0.0] * n)
    for s in itertools.product((-1, 0, 1), repeat=n):
        S = [j for j in range(n) if s[j] != 0]
        if not S:
            continue
        M = [[sum(A[i][p] * A[i][q] for i in range(len(y))) for q in S] for p in S]
        r = [sum(A[i][p] * y[i] for i in range(len(y))) - lam * s[p] for p in S]
        try:
            xs = chol_solve(cholesky(M), r)
        except ValueError:
            continue
        x = [0.0] * n
        for p, v in zip(S, xs):
            x[p] = v
        val = objective(A, y, eye(n), lam, x)
        if val < best_val:
            best, best_val = x, val
    return best


def test_cholesky() -> None:
    rng = random.Random(1)
    B = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(7)]
    M = [[sum(B[k][i] * B[k][j] for k in range(7)) for j in range(5)] for i in range(5)]
    r = [rng.uniform(-1, 1) for _ in range(5)]
    x = chol_solve(cholesky(M), r)
    assert max(abs(a - b) for a, b in zip(mat_vec(M, x), r)) < 1e-10


def test_example_first_step() -> None:
    f = [0.0, 0.0, 3.0, 3.0]
    x, d, b = split_bregman(eye(4), f, difference_matrix(4), 1.0, 1.0, 1)
    assert max(abs(a - c) for a, c in zip(x, (3 / 7, 6 / 7, 15 / 7, 18 / 7))) < 1e-12
    assert max(abs(a - c) for a, c in zip(d, (0, 2 / 7, 0))) < 1e-12
    assert max(abs(a - c) for a, c in zip(b, (3 / 7, 1, 3 / 7))) < 1e-12


def test_tv1d_brute_force() -> None:
    rng = random.Random(6)
    for _ in range(8):
        n = rng.randint(2, 6)
        f = [float(rng.randint(-3, 3)) for _ in range(n)]
        lam = rng.choice((0.3, 0.7, 1.5))
        mu = rng.choice((0.5, 1.0, 2.0))
        x, _, _ = split_bregman(eye(n), f, difference_matrix(n), lam, mu, 400)
        ref = rof_brute(f, lam)
        assert max(abs(a - c) for a, c in zip(x, ref)) < 1e-6


def test_isotropic_step_image() -> None:
    f = [0.0, 0.0, 4.0, 4.0] * 4
    x, _, _ = split_bregman(eye(16), f, gradient_matrix(4, 4), 1.0, 1.0, 300, group=16)
    for a, c in zip(x, [0.5, 0.5, 3.5, 3.5] * 4):
        assert abs(a - c) < 1e-6


def test_lasso_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(5):
        m, n = 5, rng.randint(2, 4)
        A = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        y = [rng.gauss(0, 1) for _ in range(m)]
        lam = rng.choice((0.2, 0.8, 2.0))
        x, _, _ = split_bregman(A, y, eye(n), lam, 1.0, 600)
        ref = lasso_brute(A, y, lam)
        assert max(abs(a - c) for a, c in zip(x, ref)) < 1e-6


def test_deblur_dual_certificate() -> None:
    # TV deblurring with a 3-tap blur: check the optimality conditions with v = mu b.
    rng = random.Random(10)
    n, lam, mu = 8, 0.3, 1.0
    A = [[{0: 0.5, 1: 0.25, -1: 0.25}.get(j - i, 0.0) for j in range(n)] for i in range(n)]
    x0 = [0.0, 0.0, 2.0, 2.0, 2.0, -1.0, -1.0, -1.0]
    y = [a + rng.gauss(0, 0.05) for a in mat_vec(A, x0)]
    D = difference_matrix(n)
    x, d, b = split_bregman(A, y, D, lam, mu, 3000)
    v = [mu * bi for bi in b]
    grad = [a + c for a, c in zip(mat_t_vec(A, [p - q for p, q in zip(mat_vec(A, x), y)]), mat_t_vec(D, v))]
    assert max(abs(g) for g in grad) < 1e-6
    dx = mat_vec(D, x)
    for vi, di in zip(v, dx):
        assert abs(vi) <= lam + 1e-6
        if abs(di) > 1e-4:
            assert abs(vi - lam * math.copysign(1.0, di)) < 1e-6
    # The certificate implies optimality: no random point does better.
    best = objective(A, y, D, lam, x)
    for _ in range(50):
        z = [a + rng.uniform(-0.05, 0.05) for a in x]
        assert objective(A, y, D, lam, z) >= best - 1e-9
