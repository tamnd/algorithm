# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-4d-var/. The authors are listed in prov/FTZTDM.jsonl.

import math
import random

import scimat
from incremental_4d_var import (
    adjoint_sweep,
    conjugate_gradient,
    cost,
    incremental_4dvar,
    linear_model,
    lorenz63,
    tangent_sweep,
    trajectory,
)


def random_spd(rng, n):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += 0.5
    return S


def kalman_and_rts(xb, B, M, obs, K):
    """Oracle: Kalman filter and Rauch-Tung-Striebel smoother means with Q = 0."""
    Mt = scimat.transpose(M)
    xf, Pf, xa, Pa = [], [], [], []
    x, P = list(xb), B
    for k in range(K + 1):
        if k > 0:
            x = scimat.matvec(M, xa[-1])
            P = scimat.matmul(scimat.matmul(M, Pa[-1]), Mt)
        xf.append(x)
        Pf.append(P)
        if k in obs:
            H, y, R = obs[k]
            S = scimat.add(scimat.matmul(scimat.matmul(H, P), scimat.transpose(H)), R)
            G = scimat.transpose(scimat.solve(S, scimat.matmul(H, P)))
            x = scimat.add(x, scimat.matvec(G, scimat.sub(y, scimat.matvec(H, x))))
            P = scimat.sub(P, scimat.matmul(G, scimat.matmul(H, P)))
        xa.append(x)
        Pa.append(P)
    xs = [None] * (K + 1)
    xs[K] = xa[K]
    for k in range(K - 1, -1, -1):
        C = scimat.transpose(scimat.solve(Pf[k + 1], scimat.matmul(M, Pa[k])))
        xs[k] = scimat.add(xa[k], scimat.matvec(C, scimat.sub(xs[k + 1], xf[k + 1])))
    return xa, xs


def close(a, b, tol):
    return all(abs(u - v) <= tol * (1 + abs(v)) for u, v in zip(a, b))


def fd_gradient(x0, xb, B, obs, step, K, eps=1e-6):
    g = []
    for j in range(len(x0)):
        xp, xm = list(x0), list(x0)
        xp[j] += eps
        xm[j] -= eps
        g.append((cost(xp, xb, B, obs, step, K) - cost(xm, xb, B, obs, step, K)) / (2 * eps))
    return g


def gauss_newton_step_by_finite_differences(x0, xb, B, obs, step, K, eps=1e-6):
    """Reference: one Gauss-Newton step for the stacked residuals, Jacobian by finite differences."""

    def residuals(x):
        xs = trajectory(x, step, K)
        out = [scimat.sub(x, xb)]
        for k in sorted(obs):
            H, y, R = obs[k]
            out.append(scimat.sub(y, scimat.matvec(H, xs[k])))
        return out

    n = len(x0)
    base = residuals(x0)
    cols = []
    for j in range(n):
        xp, xm = list(x0), list(x0)
        xp[j] += eps
        xm[j] -= eps
        rp, rm = residuals(xp), residuals(xm)
        cols.append([[(a - b) / (2 * eps) for a, b in zip(u, v)] for u, v in zip(rp, rm)])
    weights = [B] + [obs[k][2] for k in sorted(obs)]
    A = [[0.0] * n for _ in range(n)]
    g = [0.0] * n
    for blk, W in enumerate(weights):
        Wr = scimat.solve(W, base[blk])
        WJ = [scimat.solve(W, cols[j][blk]) for j in range(n)]
        for i in range(n):
            g[i] += scimat.dot(cols[i][blk], Wr)
            for j in range(n):
                A[i][j] += scimat.dot(cols[i][blk], WJ[j])
    return scimat.add(x0, scimat.solve(A, [-v for v in g]))


def test_scalar_check_value():
    step, tl, adj = linear_model([[1.0]])
    xa, its = incremental_4dvar([0.0], [[1.0]], {0: ([[1.0]], [1.0], [[1.0]])}, step, tl, adj, 0)
    assert abs(xa[0] - 0.5) < 1e-14 and abs(its[1][0] - 0.5) < 1e-14


def test_page_example_square_model():
    # x_1 = x_0^2, x^b = 1, B = 1, y_1 = 2, R = 1. The minimizer is (1 + sqrt 3) / 2.
    step = lambda k, x: [x[0] * x[0]]
    tl = lambda k, x, dx: [2 * x[0] * dx[0]]
    adj = lambda k, x, lam: [2 * x[0] * lam[0]]
    xa, its = incremental_4dvar([1.0], [[1.0]], {1: ([[1.0]], [2.0], [[1.0]])}, step, tl, adj, 1)
    assert abs(its[1][0] - 1.4) < 1e-14
    assert abs(its[2][0] - 1.367420814479638) < 1e-12
    star = (1 + math.sqrt(3)) / 2
    assert abs(xa[0] - star) < 1e-12
    errs = [abs(x[0] - star) for x in its[1:6]]
    for k in range(len(errs) - 1):
        assert 0.02 < errs[k + 1] / errs[k] < 0.05  # linear convergence


def test_linear_model_one_outer_loop_is_exact():
    rng = random.Random(51)
    for _ in range(40):
        n = rng.randint(1, 4)
        K = rng.randint(1, 6)
        M = [[(1.0 if i == j else 0.0) + 0.3 * rng.uniform(-1, 1) for j in range(n)] for i in range(n)]
        B = random_spd(rng, n)
        xb = [rng.uniform(-2, 2) for _ in range(n)]
        obs = {}
        for k in range(K + 1):
            if rng.random() < 0.6:
                p = rng.randint(1, 3)
                H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
                obs[k] = (H, [rng.uniform(-2, 2) for _ in range(p)], random_spd(rng, p))
        if not obs:
            obs[K] = ([[1.0] + [0.0] * (n - 1)], [1.0], [[1.0]])
        step, tl, adj = linear_model(M)
        x0, its = incremental_4dvar(xb, B, obs, step, tl, adj, K)
        xa, xs = kalman_and_rts(xb, B, M, obs, K)
        assert close(its[1], xs[0], 1e-8)
        assert close(trajectory(its[1], step, K)[K], xa[K], 1e-8)
        assert len(its) <= 4


def test_outer_loop_is_gauss_newton_lorenz63():
    rng = random.Random(52)
    step, tl, adj = lorenz63()
    K = 30
    B = [[1.0, 0.2, 0.0], [0.2, 2.0, 0.1], [0.0, 0.1, 1.5]]
    truth = trajectory([-5.8, -5.0, 24.0], step, K)
    H = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    R = [[0.5, 0.0], [0.0, 0.5]]
    obs = {k: (H, [v + rng.gauss(0, 0.7) for v in scimat.matvec(H, truth[k])], R) for k in (0, 10, 20, 30)}
    xb = [v + rng.gauss(0, 1.0) for v in truth[0]]
    x0, its = incremental_4dvar(xb, B, obs, step, tl, adj, K)
    ref = gauss_newton_step_by_finite_differences(xb, xb, B, obs, step, K)
    assert close(its[1], ref, 1e-6)
    ref2 = gauss_newton_step_by_finite_differences(its[1], xb, B, obs, step, K)
    assert close(its[2], ref2, 1e-6)
    # the limit is a stationary point of the full cost
    g = fd_gradient(x0, xb, B, obs, step, K)
    assert max(abs(v) for v in g) < 1e-6
    costs = [cost(x, xb, B, obs, step, K) for x in its]
    assert costs[-1] < costs[0]


def test_inner_operators_are_transposes():
    rng = random.Random(53)
    step, tl, adj = lorenz63()
    K = 40
    xs = trajectory([1.0, 2.0, 20.0], step, K)
    for _ in range(10):
        dx = [rng.uniform(-1, 1) for _ in range(3)]
        lam = [rng.uniform(-1, 1) for _ in range(3)]
        vK = tangent_sweep(xs, dx, tl, K)[K]
        w = adjoint_sweep(xs, {K: lam}, adj, K, 3)
        lhs, rhs = scimat.dot(vK, lam), scimat.dot(dx, w)
        assert abs(lhs - rhs) <= 1e-10 * (abs(lhs) + abs(rhs))


def test_non_tangent_linear_inner_model_moves_the_fixed_point():
    # A simplified inner model (the tangent linear model times 0.9, with its own transpose)
    # still converges, but to a point where the gradient of the full cost is not zero.
    rng = random.Random(54)
    step, tl, adj = lorenz63()
    K = 20
    B = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    truth = trajectory([-5.8, -5.0, 24.0], step, K)
    H = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R = [[0.5, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.0, 0.5]]
    obs = {k: (H, [v + rng.gauss(0, 0.7) for v in truth[k]], R) for k in (0, 10, 20)}
    xb = [v + rng.gauss(0, 1.0) for v in truth[0]]
    tl9 = lambda k, x, dx: [0.9 * v for v in tl(k, x, dx)]
    adj9 = lambda k, x, lam: [0.9 * v for v in adj(k, x, lam)]
    x_exact, _ = incremental_4dvar(xb, B, obs, step, tl, adj, K)
    x_simple, its = incremental_4dvar(xb, B, obs, step, tl9, adj9, K, max_outer=200)
    assert scimat.norm2(scimat.sub(its[-1], its[-2])) < 1e-10
    assert max(abs(v) for v in fd_gradient(x_exact, xb, B, obs, step, K)) < 1e-6
    assert max(abs(v) for v in fd_gradient(x_simple, xb, B, obs, step, K)) > 1e-3


def test_conjugate_gradient_against_elimination():
    rng = random.Random(55)
    for _ in range(50):
        n = rng.randint(1, 8)
        A = random_spd(rng, n)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        z = conjugate_gradient(lambda v: scimat.matvec(A, v), b)
        assert close(z, scimat.solve(A, b), 1e-9)
