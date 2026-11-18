# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-position-based-dynamics/. The authors are listed in prov/553NT7.jsonl.

"""Tests of XPBD against closed forms, a Newton solve of backward Euler and conservation laws."""

import math
import random

from anim import num_grad, solve
import extended_position_based_dynamics as xpbd


def predict(x, v, w, dt, g):
    return [(p[0] + dt * u[0] + dt * dt * g[0], p[1] + dt * u[1] + dt * dt * g[1]) if wi > 0.0 else tuple(p)
            for p, u, wi in zip(x, v, w)]


def newton_backward_euler(xt, w, cons, dt, tol=1e-13):
    """Minimize 1/2 |x - x~|_M^2 + dt^2 sum C^2 / (2 alpha) by Newton's method with backtracking."""
    free = [i for i in range(len(xt)) if w[i] > 0.0]
    col = {i: k for k, i in enumerate(free)}
    x = [tuple(p) for p in xt]
    for _ in range(100):
        nf = 2 * len(free)
        grad = [0.0] * nf
        hess = [[0.0] * nf for _ in range(nf)]
        for i in free:
            for d in range(2):
                r = 2 * col[i] + d
                grad[r] += (x[i][d] - xt[i][d]) / w[i]
                hess[r][r] += 1.0 / w[i]
        for i, j, rest, alpha in cons:
            c, n = xpbd.distance_value_and_gradient(x, i, j, rest)
            ln = c + rest
            s = dt * dt / alpha
            blk = [[s * (n[a] * n[b] + c * ((1.0 if a == b else 0.0) - n[a] * n[b]) / ln) for b in range(2)]
                   for a in range(2)]
            for p, sp in ((i, 1.0), (j, -1.0)):
                if p not in col:
                    continue
                for a in range(2):
                    grad[2 * col[p] + a] += s * c * sp * n[a]
                for q, sq in ((i, 1.0), (j, -1.0)):
                    if q not in col:
                        continue
                    for a in range(2):
                        for b in range(2):
                            hess[2 * col[p] + a][2 * col[q] + b] += sp * sq * blk[a][b]
        if max(abs(gv) for gv in grad) < tol:
            break
        step = solve(hess, [-gv for gv in grad])
        f0 = xpbd.energy_objective(x, xt, w, cons, dt)
        t = 1.0
        while True:
            y = list(x)
            for i in free:
                y[i] = (x[i][0] + t * step[2 * col[i]], x[i][1] + t * step[2 * col[i] + 1])
            if xpbd.energy_objective(y, xt, w, cons, dt) <= f0 or t < 1e-12:
                break
            t *= 0.5
        x = y
    return x


def test_example_one_spring_is_backward_euler():
    x = [(0.0, 0.0), (1.5, 0.0)]
    v = [(0.0, 0.0), (0.0, 0.0)]
    w = [0.0, 1.0]
    x1, v1, lam = xpbd.xpbd_step(x, v, w, [(0, 1, 1.0, 0.01)], 0.1, 1, gravity=(0.0, 0.0))
    assert abs(lam[0] + 0.25) < 1e-15
    assert abs(x1[1][0] - 1.25) < 1e-15 and abs(v1[1][0] + 2.5) < 1e-13


def test_one_linear_spring_matches_backward_euler_for_any_step():
    """x = (m y + dt^2 k r) / (m + dt^2 k) with k = 1 / alpha, in one sweep."""
    rng = random.Random(11)
    for _ in range(200):
        dt = rng.choice([1e-3, 1e-2, 0.1, 1.0])
        alpha = 10 ** rng.uniform(-6, 0)
        m = rng.uniform(0.1, 3.0)
        r = rng.uniform(0.5, 2.0)
        x0 = rng.uniform(0.6, 3.0)
        v0 = rng.uniform(-1.0, 1.0)
        y = x0 + dt * v0
        x1, _, _ = xpbd.xpbd_step([(0.0, 0.0), (x0, 0.0)], [(0.0, 0.0), (v0, 0.0)], [0.0, 1.0 / m],
                                  [(0, 1, r, alpha)], dt, 1, gravity=(0.0, 0.0))
        k = 1.0 / alpha
        want = (m * y + dt * dt * k * r) / (m + dt * dt * k)
        assert abs(x1[1][0] - want) < 1e-9 * max(1.0, abs(want))


def test_zero_compliance_is_the_pbd_projection():
    rng = random.Random(12)
    for _ in range(200):
        x = [(rng.uniform(-1, 1), rng.uniform(-1, 1)), (rng.uniform(-1, 1), rng.uniform(-1, 1))]
        w = [rng.uniform(0.1, 2.0), rng.uniform(0.1, 2.0)]
        d = rng.uniform(0.1, 1.0)
        c, n = xpbd.distance_value_and_gradient(x, 0, 1, d)
        want0 = (x[0][0] - w[0] / (w[0] + w[1]) * c * n[0], x[0][1] - w[0] / (w[0] + w[1]) * c * n[1])
        want1 = (x[1][0] + w[1] / (w[0] + w[1]) * c * n[0], x[1][1] + w[1] / (w[0] + w[1]) * c * n[1])
        x1, _, _ = xpbd.xpbd_step(x, [(0.0, 0.0)] * 2, w, [(0, 1, d, 0.0)], 1.0, 1, gravity=(0.0, 0.0))
        assert max(abs(x1[0][k] - want0[k]) for k in range(2)) < 1e-14
        assert max(abs(x1[1][k] - want1[k]) for k in range(2)) < 1e-14


def test_collinear_chain_converges_to_backward_euler():
    """Linear constraints: the dropped terms are zero, and the sweeps converge to the Newton solution."""
    dt = 1.0 / 30.0
    x, v, w, cons = xpbd.chain(8, 0.1, 1e-3, vertical=True)
    xt = predict(x, v, w, dt, xpbd.GRAVITY)
    ref = newton_backward_euler(xt, w, cons, dt)
    errs = []
    for it in (1, 2, 5, 10, 200):
        x1, _, lam = xpbd.xpbd_step(x, v, w, cons, dt, it)
        errs.append(max(abs(a[1] - b[1]) for a, b in zip(x1, ref)))
    assert errs[0] > errs[1] > errs[2] > errs[3] > 0.0
    assert errs[0] > 1e-4 and errs[4] < 1e-12
    for k, (i, j, rest, alpha) in enumerate(cons):
        assert abs(math.dist(x1[i], x1[j]) - rest + alpha / dt ** 2 * lam[k]) < 1e-12


def test_nonlinear_chain_is_close_to_backward_euler():
    """A swinging chain: the converged XPBD step differs from backward Euler by the residual g (measured)."""
    x, v, w, cons = xpbd.chain(6, 0.1, 1e-4)
    for _ in range(6):
        x, v, _ = xpbd.xpbd_step(x, v, w, cons, 1.0 / 60.0, 50)
    errs = []
    for dt in (1.0 / 60.0, 1.0 / 120.0):
        xt = predict(x, v, w, dt, xpbd.GRAVITY)
        ref = newton_backward_euler(xt, w, cons, dt)
        x1, _, _ = xpbd.xpbd_step(x, v, w, cons, dt, 500)
        err = max(math.dist(a, b) for a, b in zip(x1, ref))
        move = max(math.dist(a, b) for a, b in zip(ref, x))
        assert 0.0 < err < 1e-2 * move
        errs.append(err)
    assert errs[1] < errs[0] / 4.0


def test_linear_momentum_is_conserved():
    rng = random.Random(13)
    x = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(10)]
    v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(10)]
    w = [rng.uniform(0.5, 2.0) for _ in range(10)]
    cons = [(i, j, 0.9 * math.dist(x[i], x[j]), rng.choice([0.0, 1e-4, 1e-2]))
            for i in range(10) for j in range(i + 1, 10) if (i * j) % 4 == 1]
    p0 = [sum(u[k] / wi for u, wi in zip(v, w)) for k in range(2)]
    for _ in range(40):
        x, v, _ = xpbd.xpbd_step(x, v, w, cons, 0.01, 3, gravity=(0.0, 0.0))
    p1 = [sum(u[k] / wi for u, wi in zip(v, w)) for k in range(2)]
    scale = sum(math.hypot(*u) / wi for u, wi in zip(v, w))
    assert max(abs(p1[k] - p0[k]) for k in range(2)) < 1e-10 * scale


def test_objective_gradient_against_num_grad():
    """The gradient of the backward Euler objective, and the constraint forces sum to zero."""
    rng = random.Random(14)
    x = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(4)]
    xt = [(p[0] + 0.01, p[1] - 0.02) for p in x]
    w = [0.5, 1.0, 2.0, 1.0]
    cons = [(0, 1, 0.3, 1e-2), (1, 2, 0.4, 1e-3), (2, 3, 0.2, 1e-1)]
    dt = 0.05
    lam = [rng.uniform(-1e-3, 1e-3) for _ in cons]
    flat = [u for p in x for u in p]

    def f(z):
        return xpbd.energy_objective([(z[2 * i], z[2 * i + 1]) for i in range(4)], xt, w, cons, dt)

    ng = num_grad(f, flat)
    for i in range(4):
        for k in range(2):
            want = (x[i][k] - xt[i][k]) / w[i]
            for j, (a, b, rest, alpha) in enumerate(cons):
                c, n = xpbd.distance_value_and_gradient(x, a, b, rest)
                if i == a:
                    want += dt * dt / alpha * c * n[k]
                if i == b:
                    want -= dt * dt / alpha * c * n[k]
            assert abs(ng[2 * i + k] - want) <= 1e-6 * max(1.0, abs(want))
    f_lam = xpbd.constraint_force(x, cons, lam, dt)
    assert abs(sum(u[0] for u in f_lam)) < 1e-12 and abs(sum(u[1] for u in f_lam)) < 1e-12


def test_free_fall_is_symplectic_euler():
    x, v, w = [(0.0, 0.0)], [(0.0, 0.0)], [1.0]
    for _ in range(10):
        x, v, _ = xpbd.xpbd_step(x, v, w, [], 0.1, 1)
    assert abs(x[0][1] + 5.3955) < 1e-12
