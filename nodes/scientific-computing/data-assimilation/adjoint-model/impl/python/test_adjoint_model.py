# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjoint-model/. The authors are listed in prov/D36VQ5.jsonl.

import random

from adjoint_model import (
    adj_step,
    adj_tendency,
    cost,
    forward,
    gradient,
    step,
    tendency,
    tlm_step,
    tlm_tendency,
)

F, H = 8.0, 0.05


def dot(a, b):
    return sum(u * v for u, v in zip(a, b))


def attractor_state(n, seed):
    rng = random.Random(seed)
    x = [F + rng.uniform(-1, 1) for _ in range(n)]
    for _ in range(200):
        x = step(x, F, H)
    return x


def test_dot_product_test_tendency():
    rng = random.Random(31)
    for _ in range(200):
        n = rng.randint(4, 20)
        x = [rng.uniform(-10, 10) for _ in range(n)]
        dx = [rng.uniform(-1, 1) for _ in range(n)]
        lam = [rng.uniform(-1, 1) for _ in range(n)]
        a, b = dot(tlm_tendency(x, dx), lam), dot(dx, adj_tendency(x, lam))
        assert abs(a - b) <= 1e-12 * (1 + abs(a))


def test_dot_product_test_step_and_trajectory():
    rng = random.Random(32)
    n, K = 40, 20
    x0 = attractor_state(n, 1)
    path = forward(x0, F, H, K)
    for _ in range(5):
        dx = [rng.gauss(0, 1) for _ in range(n)]
        lam = [rng.gauss(0, 1) for _ in range(n)]
        # one step
        a, b = dot(tlm_step(x0, dx, F, H), lam), dot(dx, adj_step(x0, lam, F, H))
        assert abs(a - b) <= 1e-12 * (1 + abs(a))
        # K steps: <M_K ... M_1 dx, lam> = <dx, M_1^T ... M_K^T lam>
        u = list(dx)
        for k in range(K):
            u = tlm_step(path[k], u, F, H)
        v = list(lam)
        for k in range(K - 1, -1, -1):
            v = adj_step(path[k], v, F, H)
        a, b = dot(u, lam), dot(dx, v)
        assert abs(a - b) <= 1e-10 * (1 + abs(a))


def test_tangent_linear_against_finite_differences():
    rng = random.Random(33)
    n = 40
    x = attractor_state(n, 2)
    dx = [rng.gauss(0, 1) for _ in range(n)]
    tl = tlm_step(x, dx, F, H)
    errs = []
    for eps in (1e-2, 1e-3):
        xp = step([a + eps * b for a, b in zip(x, dx)], F, H)
        xm = step([a - eps * b for a, b in zip(x, dx)], F, H)
        fd = [(p - m) / (2 * eps) for p, m in zip(xp, xm)]
        errs.append(max(abs(a - b) for a, b in zip(fd, tl)))
    # central differences: the error falls like eps^2
    assert errs[1] < 2e-4
    assert 50 < errs[0] / errs[1] < 200


def make_problem(n, K, seed):
    rng = random.Random(seed)
    xt = attractor_state(n, seed)
    truth = forward(xt, F, H, K)
    idx = list(range(0, n, 2))
    obs = {k: [truth[k][i] + rng.gauss(0, 1) for i in idx] for k in range(0, K + 1, 2)}
    x0 = [v + rng.gauss(0, 0.5) for v in xt]
    return x0, obs, idx


def test_gradient_against_forward_mode_columns():
    # Reference: the gradient from n tangent linear runs, one per unit vector.
    n, K, r = 12, 10, 1.0
    x0, obs, idx = make_problem(n, K, 3)
    g = gradient(x0, F, H, K, obs, idx, r)
    path = forward(x0, F, H, K)
    for j in range(n):
        u = [1.0 if i == j else 0.0 for i in range(n)]
        gj = 0.0
        for k in range(K + 1):
            if k in obs:
                gj += sum(u[i] * (path[k][i] - yi) / r for i, yi in zip(idx, obs[k]))
            if k < K:
                u = tlm_step(path[k], u, F, H)
        assert abs(gj - g[j]) <= 1e-10 * (1 + abs(gj))


def test_gradient_against_finite_differences():
    n, K, r = 40, 20, 1.0
    x0, obs, idx = make_problem(n, K, 4)
    g = gradient(x0, F, H, K, obs, idx, r)
    eps = 1e-5
    for j in (0, 7, 13, 39):
        xp, xm = list(x0), list(x0)
        xp[j] += eps
        xm[j] -= eps
        fd = (cost(xp, F, H, K, obs, idx, r) - cost(xm, F, H, K, obs, idx, r)) / (2 * eps)
        assert abs(fd - g[j]) < 1e-5 * (1 + abs(g[j]))


def test_tendency_is_lorenz96():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    f = tendency(x, 8.0)
    # j = 0: (x1 - x3) x4 - x0 + F = (2 - 4) 5 - 1 + 8
    assert f[0] == -3.0
    assert tendency([8.0] * 6, 8.0) == [0.0] * 6
