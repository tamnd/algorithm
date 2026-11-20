# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bregman-iteration/. The authors are listed in prov/3BKXGP.jsonl.

import itertools
import math
import random

from bregman_iteration import bregman_iteration, lasso_fista, matvec, norm, soft_threshold, tv1d

IDENT = lambda x: x[:]


def tv(x):
    return sum(abs(x[i + 1] - x[i]) for i in range(len(x) - 1))


def rof_brute(f, lam):
    """Exact 1D TV denoising by trying every sign pattern of the differences."""
    n = len(f)
    best, best_val = None, math.inf
    for s in itertools.product((-1, 0, 1), repeat=n - 1):
        cuts = [0] + [b + 1 for b in range(n - 1) if s[b] != 0] + [n]
        u = []
        for a, b in zip(cuts, cuts[1:]):
            sl = s[a - 1] if a > 0 else 0
            sr = s[b - 1] if b < n else 0
            u.extend([sum(f[a:b]) / (b - a) - lam * (sl - sr) / (b - a)] * (b - a))
        val = 0.5 * sum((a - b) ** 2 for a, b in zip(u, f)) + lam * tv(u)
        if val < best_val:
            best, best_val = u, val
    return best


def solve_square(M, r):
    n = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = max(range(c, n), key=lambda i: abs(a[i][c]))
        if abs(a[piv][c]) < 1e-10:
            return None
        a[c], a[piv] = a[piv], a[c]
        for i in range(c + 1, n):
            t = a[i][c] / a[c][c]
            for j in range(c, n + 1):
                a[i][j] -= t * a[c][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def basis_pursuit_brute(A, y):
    """min ||x||_1 subject to A x = y, by trying every basic solution (an LP optimum is a vertex)."""
    m, n = len(A), len(A[0])
    best = math.inf
    for S in itertools.combinations(range(n), m):
        xs = solve_square([[A[i][j] for j in S] for i in range(m)], y)
        if xs is not None:
            best = min(best, sum(abs(v) for v in xs))
    return best


def test_l1_example() -> None:
    _, xs, ys = bregman_iteration(soft_threshold(1.0), IDENT, [3.0, 0.5, -2.0], 3)
    assert xs[0] == [2.0, 0.0, -1.0]
    assert ys[1] == [4.0, 1.0, -3.0]
    assert xs[1] == [3.0, 0.0, -2.0]
    assert xs[2] == [3.0, 0.5, -2.0]


def test_tv_inner_solver_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(10):
        n = rng.randint(2, 7)
        f = [float(rng.randint(-3, 3)) for _ in range(n)]
        lam = rng.choice((0.4, 1.0, 2.5))
        x = tv1d(lam)(f)
        ref = rof_brute(f, lam)
        assert max(abs(a - b) for a, b in zip(x, ref)) < 1e-6


def test_tv_step_contrast_restored() -> None:
    f = [0.0] * 4 + [2.0] * 4
    _, xs, ys = bregman_iteration(tv1d(1.0), IDENT, f, 2)
    assert max(abs(a - b) for a, b in zip(xs[0], [0.25] * 4 + [1.75] * 4)) < 1e-6
    assert max(abs(a - b) for a, b in zip(ys[1], [-0.25] * 4 + [2.25] * 4)) < 1e-6
    assert max(abs(a - b) for a, b in zip(xs[1], f)) < 1e-6


def test_monotone_residual_and_rate() -> None:
    rng = random.Random(8)
    for _ in range(4):
        n = 7
        y = [rng.uniform(-2, 2) for _ in range(n)]
        lam = 1.5
        K = 8
        _, xs, _ = bregman_iteration(tv1d(lam), IDENT, y, K)
        res = [norm([a - b for a, b in zip(x, y)]) for x in xs]
        for a, b in zip(res, res[1:]):
            assert b <= a + 1e-6
        # 1/2 ||x^k - y||^2 <= 1/2 ||xt - y||^2 + lam TV(xt) / k for every xt.
        for _ in range(10):
            xt = [rng.uniform(-2, 2) for _ in range(n)]
            for k, r in enumerate(res, start=1):
                bound = 0.5 * sum((a - b) ** 2 for a, b in zip(xt, y)) + lam * tv(xt) / k
                assert 0.5 * r * r <= bound + 1e-6


def test_basis_pursuit_limit() -> None:
    rng = random.Random(21)
    for _ in range(3):
        m, n = 3, 5
        A = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        xs_true = [0.0] * n
        xs_true[rng.randrange(n)] = rng.choice((-2.0, 2.0))
        y = matvec(A)(xs_true)
        x, _, _ = bregman_iteration(lasso_fista(A, 0.5, iters=500), matvec(A), y, 4)
        assert norm([a - b for a, b in zip(matvec(A)(x), y)]) < 1e-4
        assert abs(sum(abs(v) for v in x) - basis_pursuit_brute(A, y)) < 1e-3


def test_discrepancy_stop_and_bregman_distance() -> None:
    rng = random.Random(13)
    lam = 1.0
    xd = [rng.choice((0.0, 0.0, 4.0, -3.0)) for _ in range(12)]
    e = [rng.gauss(0, 0.3) for _ in range(12)]
    yd = [a + b for a, b in zip(xd, e)]
    delta = norm(e)
    x, xs, ys = bregman_iteration(soft_threshold(lam), IDENT, yd, 100, delta=delta, tau=1.0)
    k = len(xs)
    assert norm([a - b for a, b in zip(x, yd)]) <= delta
    assert all(norm([a - b for a, b in zip(xi, yd)]) > delta for xi in xs[:-1])
    # p^k = (y^k - y) / lam lies in the subdifferential of ||.||_1 at x^k (A = I).
    dist = []
    for j in range(1, k + 1):
        p = [(a - b) / lam for a, b in zip(ys[j], yd)] if j < len(ys) else None
        if p is None:
            break
        assert all(abs(pi) <= 1 + 1e-12 for pi in p)
        dist.append(sum(abs(a) for a in xd) - sum(a * b for a, b in zip(p, xd)))
    for a, b in zip(dist, dist[1:]):
        assert b < a + 1e-12
