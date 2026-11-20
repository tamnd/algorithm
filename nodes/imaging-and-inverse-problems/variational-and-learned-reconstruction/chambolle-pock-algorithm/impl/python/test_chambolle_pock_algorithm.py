# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chambolle-pock-algorithm/. The authors are listed in prov/JY6DNX.jsonl.

import itertools
import math
import random

from chambolle_pock_algorithm import (
    chambolle_pock,
    chambolle_pock_accelerated,
    grad_adjoint,
    grad_op,
    lasso,
    project_balls,
    rof_denoise,
    rof_energy,
)


def solve(M: list[list[float]], r: list[float]) -> list[float] | None:
    """Gaussian elimination with partial pivoting; None if singular."""
    n = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = max(range(c, n), key=lambda i: abs(a[i][c]))
        if abs(a[piv][c]) < 1e-12:
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


def lasso_obj(A, b, lam, x) -> float:
    r = [sum(A[i][j] * x[j] for j in range(len(x))) - b[i] for i in range(len(b))]
    return 0.5 * sum(t * t for t in r) + lam * sum(abs(t) for t in x)


def lasso_brute(A, b, lam) -> list[float]:
    """Try every sign pattern; on the support S solve A_S^T A_S x = A_S^T b - lam s_S."""
    n = len(A[0])
    best, best_val = [0.0] * n, lasso_obj(A, b, lam, [0.0] * n)
    for s in itertools.product((-1, 0, 1), repeat=n):
        S = [j for j in range(n) if s[j] != 0]
        if not S:
            continue
        M = [[sum(A[i][p] * A[i][q] for i in range(len(b))) for q in S] for p in S]
        r = [sum(A[i][p] * b[i] for i in range(len(b))) - lam * s[p] for p in S]
        xs = solve(M, r)
        if xs is None:
            continue
        x = [0.0] * n
        for p, v in zip(S, xs):
            x[p] = v
        val = lasso_obj(A, b, lam, x)
        if val < best_val:
            best, best_val = x, val
    return best


def rof_brute_1d(f: list[float], lam: float) -> list[float]:
    n = len(f)
    best, best_val = None, math.inf
    for s in itertools.product((-1, 0, 1), repeat=n - 1):
        cuts = [0] + [b + 1 for b in range(n - 1) if s[b] != 0] + [n]
        u = []
        for a, b in zip(cuts, cuts[1:]):
            sl = s[a - 1] if a > 0 else 0
            sr = s[b - 1] if b < n else 0
            u.extend([sum(f[a:b]) / (b - a) - lam * (sl - sr) / (b - a)] * (b - a))
        val = rof_energy(u, f, lam, 1, n)
        if val < best_val:
            best, best_val = u, val
    return best


def test_adjoint_and_norm() -> None:
    rng = random.Random(2)
    n1, n2 = 4, 5
    K, KT = grad_op(n1, n2), grad_adjoint(n1, n2)
    u = [rng.uniform(-1, 1) for _ in range(n1 * n2)]
    q = [rng.uniform(-1, 1) for _ in range(2 * n1 * n2)]
    assert abs(sum(a * b for a, b in zip(K(u), q)) - sum(a * b for a, b in zip(u, KT(q)))) < 1e-12
    # Power iteration on K^T K: the estimate of ||K||^2 stays below 8.
    v = u
    est = 0.0
    for _ in range(200):
        w = KT(K(v))
        est = math.sqrt(sum(a * a for a in w))
        v = [a / est for a in w]
    assert 7.0 < est < 8.0


def test_step_image() -> None:
    f = [[0.0, 0.0, 4.0, 4.0] for _ in range(4)]
    u = rof_denoise(f, 1.0, 0.35, 0.35, iters=600)
    for row in u:
        for a, b in zip(row, (0.5, 0.5, 3.5, 3.5)):
            assert abs(a - b) < 1e-5


def test_rof_brute_force_1d() -> None:
    rng = random.Random(11)
    for _ in range(8):
        n = rng.randint(2, 6)
        f = [float(rng.randint(-3, 3)) for _ in range(n)]
        lam = rng.choice((0.3, 0.7, 1.5))
        u = rof_denoise([f], lam, 0.45, 0.45, iters=3000)[0]
        ref = rof_brute_1d(f, lam)
        assert max(abs(a - b) for a, b in zip(u, ref)) < 1e-5


def test_lasso_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(5):
        m, n = 5, rng.randint(2, 4)
        A = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        b = [rng.gauss(0, 1) for _ in range(m)]
        lam = rng.choice((0.2, 0.8, 2.0))
        x = lasso(A, b, lam, iters=4000)
        ref = lasso_brute(A, b, lam)
        assert max(abs(a - c) for a, c in zip(x, ref)) < 1e-5


def test_ergodic_gap_bound() -> None:
    rng = random.Random(9)
    n1, n2, lam = 3, 4, 0.6
    N = n1 * n2
    f = [rng.uniform(0, 3) for _ in range(N)]
    K, KT = grad_op(n1, n2), grad_adjoint(n1, n2)
    tau = sigma = 0.35
    x0, y0 = f[:], [0.0] * (2 * N)

    def L(x, y):
        return sum(a * b for a, b in zip(K(x), y)) + 0.5 * sum((a - c) ** 2 for a, c in zip(x, f))

    for iters in (1, 5, 20, 80):
        _, _, X, Y = chambolle_pock(K, KT, lambda v, t: [(a + t * c) / (1 + t) for a, c in zip(v, f)],
                                    project_balls(lam, N), x0, y0, tau, sigma, iters)
        for _ in range(30):
            x = [rng.uniform(-2, 5) for _ in range(N)]
            y = project_balls(lam, N)([rng.uniform(-1, 1) for _ in range(2 * N)], 1.0)
            bound = (sum((a - c) ** 2 for a, c in zip(x, x0)) / (2 * tau)
                     + sum((a - c) ** 2 for a, c in zip(y, y0)) / (2 * sigma)) / iters
            assert L(X, y) - L(x, Y) <= bound + 1e-9


def test_accelerated_rof() -> None:
    f = [[0.0, 0.0, 4.0, 4.0] for _ in range(4)]
    fl = [a for row in f for a in row]
    K, KT = grad_op(4, 4), grad_adjoint(4, 4)
    ref = [0.5, 0.5, 3.5, 3.5] * 4
    prev = math.inf
    # G is 1-strongly convex; tau sigma ||K||^2 <= 1 with tau = 1, sigma = 1/8.
    for n in (25, 50, 100, 200):
        x, _ = chambolle_pock_accelerated(K, KT, lambda v, t: [(a + t * c) / (1 + t) for a, c in zip(v, fl)],
                                          project_balls(1.0, 16), fl, [0.0] * 32, 1.0, 0.125, 1.0, n)
        err = math.sqrt(sum((a - b) ** 2 for a, b in zip(x, ref)))
        assert n * err < 2.5  # the O(1/N) rate of the error
        assert err < prev
        prev = err
