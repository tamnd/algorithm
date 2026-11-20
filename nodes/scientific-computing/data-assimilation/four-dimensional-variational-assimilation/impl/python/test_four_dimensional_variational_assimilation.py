# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-dimensional-variational-assimilation/. The authors are listed in prov/XB7N6C.jsonl.

import random

import scimat
from four_dimensional_variational_assimilation import (
    cost_and_gradient,
    linear_model,
    lorenz63,
    trajectory,
    var4d,
)


def random_spd(rng, n):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += 0.5
    return S


def kalman_and_rts(xb, B, M, obs, K):
    """Oracle: Kalman filter means and Rauch-Tung-Striebel smoother means, with Q = 0.

    Gains by Gaussian elimination. Return (filter means, smoother means).
    """
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


def test_scalar_check_value():
    step, adj = linear_model([[1.0]])
    xa, _ = var4d([0.0], [[1.0]], {0: ([[1.0]], [1.0], [[1.0]])}, step, adj, 0)
    assert abs(xa[0] - 0.5) < 1e-12


def test_page_example():
    # x_1 = 2 x_0, x^b = 0, B = 1, y_1 = 2, R = 1: x_0^a = 0.8 and x_1 = 1.6.
    step, adj = linear_model([[2.0]])
    obs = {1: ([[1.0]], [2.0], [[1.0]])}
    J, g = cost_and_gradient([0.0], [0.0], [[1.0]], {1: ([[1.0]], [2.0], [[1.0]])}, step, adj, 1)
    assert abs(J - 2.0) < 1e-15 and abs(g[0] + 4.0) < 1e-15
    xa, _ = var4d([0.0], [[1.0]], obs, step, adj, 1)
    assert abs(xa[0] - 0.8) < 1e-12
    assert abs(trajectory(xa, step, 1)[1][0] - 1.6) < 1e-12


def test_linear_model_equals_kalman_smoother():
    rng = random.Random(41)
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
        step, adj = linear_model(M)
        x0, _ = var4d(xb, B, obs, step, adj, K)
        xa, xs = kalman_and_rts(xb, B, M, obs, K)
        traj = trajectory(x0, step, K)
        assert close(x0, xs[0], 1e-8)
        assert close(traj[K], xa[K], 1e-8)
        for k in range(K + 1):
            assert close(traj[k], xs[k], 1e-8)


def test_gradient_matches_finite_differences_lorenz63():
    rng = random.Random(42)
    step, _, adj = lorenz63()
    K = 30
    LB = scimat.cholesky([[1.0, 0.2, 0.0], [0.2, 2.0, 0.1], [0.0, 0.1, 1.5]])
    xb = [1.0, 2.0, 20.0]
    obs = {}
    for k in (0, 10, 20, 30):
        H = [[1.0, 0.0, 0.0], [0.0, 0.5, 0.5]]
        obs[k] = (H, [rng.uniform(-5, 5), rng.uniform(-5, 5)], scimat.cholesky([[0.5, 0.0], [0.0, 1.0]]))
    for _ in range(4):
        x0 = [xi + rng.uniform(-1, 1) for xi in xb]
        J, g = cost_and_gradient(x0, xb, LB, obs, step, adj, K)
        eps = 1e-6
        for j in range(3):
            xp, xm = list(x0), list(x0)
            xp[j] += eps
            xm[j] -= eps
            fd = (cost_and_gradient(xp, xb, LB, obs, step, adj, K)[0] - cost_and_gradient(xm, xb, LB, obs, step, adj, K)[0]) / (2 * eps)
            assert abs(fd - g[j]) <= 1e-6 * (1 + abs(g[j]))


def test_dot_product_test_of_the_adjoint():
    rng = random.Random(43)
    step, tl, adj = lorenz63()
    x = [1.0, 2.0, 20.0]
    xs = trajectory(x, step, 40)
    for _ in range(10):
        dx = [rng.uniform(-1, 1) for _ in range(3)]
        lam = [rng.uniform(-1, 1) for _ in range(3)]
        # the whole window: M' = M_40' ... M_1'
        v = dx
        for k in range(1, 41):
            v = tl(k, xs[k - 1], v)
        w = lam
        for k in range(40, 0, -1):
            w = adj(k, xs[k - 1], w)
        lhs, rhs = scimat.dot(v, lam), scimat.dot(dx, w)
        assert abs(lhs - rhs) <= 1e-10 * (abs(lhs) + abs(rhs))


def test_lorenz63_twin_reduces_the_error():
    # A measurement over 8 twin experiments: the mean error of x_0 falls by more than half.
    step, _, adj = lorenz63()
    truth0 = trajectory([1.0, 1.0, 1.0], step, 500)[-1]
    K = 40
    truth = trajectory(truth0, step, K)
    H = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R = [[0.25, 0.0, 0.0], [0.0, 0.25, 0.0], [0.0, 0.0, 0.25]]
    B = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    eb = ea = 0.0
    for seed in range(44, 52):
        rng = random.Random(seed)
        obs = {k: (H, [v + rng.gauss(0, 0.5) for v in truth[k]], R) for k in range(0, K + 1, 8)}
        xb = [v + rng.gauss(0, 1.0) for v in truth0]
        x0, _ = var4d(xb, B, obs, step, adj, K)
        ob = {k: (h, y, scimat.cholesky(r)) for k, (h, y, r) in obs.items()}
        _, g = cost_and_gradient(x0, xb, scimat.cholesky(B), ob, step, adj, K)
        assert scimat.norm2(g) < 1e-8
        eb += scimat.norm2(scimat.sub(xb, truth0))
        ea += scimat.norm2(scimat.sub(x0, truth0))
    assert ea < 0.5 * eb
