# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimization-time-integration/. The authors are listed in prov/VE7FP8.jsonl.

"""Tests of optimization time integration: derivatives, a linear reference, monotone Newton and energy behaviour."""

import random

import optimization_time_integration as ot


def central_grad(f, x, h=1e-6):
    out = []
    for i in range(len(x)):
        a, b = list(x), list(x)
        a[i] += h
        b[i] -= h
        out.append((f(a) - f(b)) / (2 * h))
    return out


def flat(ch, x):
    return [c for i in ch.free for c in x[i]]


def unflat(ch, z, x):
    y = list(x)
    for k, i in enumerate(ch.free):
        y[i] = (z[2 * k], z[2 * k + 1])
    return y


def crumpled(seed):
    rng = random.Random(seed)
    ch = ot.hanging_chain(8, 0.1, 1e4, 0.1)
    x0 = [(0.0, 0.0)] + [(0.02 * i + rng.uniform(-0.03, 0.03), rng.uniform(-0.03, 0.03)) for i in range(1, 8)]
    return ch, x0


def test_example_one_spring_is_backward_euler():
    m, k, r, dt = 1.0, 100.0, 1.0, 0.1
    ch = ot.Chain([(0.0, 0.0), (1.5, 0.0)], [(0, 1, r, k)], [m, m], pinned=[0], gravity=(0.0, 0.0))
    x1, v1, _ = ot.oti_step(ch, [(0.0, 0.0), (1.5, 0.0)], [(0.0, 0.0)] * 2, dt, tau=1e-12)
    assert abs(x1[1][0] - 1.25) < 1e-12 and abs(x1[1][1]) < 1e-14 and abs(v1[1][0] + 2.5) < 1e-10


def test_gradient_and_hessian_against_central_differences():
    ch, x = crumpled(9)
    dt = 1.0 / 24.0
    xh = [(p[0] + 0.01, p[1] - 0.02) for p in x]
    g, h = ot.objective_grad_hess(ch, x, xh, dt)
    z0 = flat(ch, x)
    ng = central_grad(lambda z: ot.objective(ch, unflat(ch, z, x), xh, dt), z0)
    assert max(abs(a - b) for a, b in zip(g, ng)) < 1e-5 * max(abs(c) for c in g)
    for r in range(len(z0)):
        col = central_grad(lambda z, r=r: ot.objective_grad_hess(ch, unflat(ch, z, x), xh, dt)[0][r], z0)
        assert max(abs(col[c] - h[r][c]) for c in range(len(z0))) < 1e-4 * max(1.0, max(map(abs, h[r])))


def test_linear_springs_match_a_direct_linear_solve():
    """With zero rest lengths the step solves (M / dt^2 + K) x = M / dt^2 xh + f; the reference builds K by hand."""
    n, k, m, dt = 6, 50.0, 0.2, 0.05
    ch = ot.hanging_chain(n, 0.1, k, m, rest_zero=True)
    rng = random.Random(3)
    x0 = [(0.0, 0.0)] + [(0.1 * i + rng.uniform(-0.02, 0.02), rng.uniform(-0.02, 0.02)) for i in range(1, n)]
    v0 = [(0.0, 0.0)] + [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(1, n)]
    x1, _, _ = ot.oti_step(ch, x0, v0, dt, tau=1e-12)
    f = n - 1
    lap = [[0.0] * f for _ in range(f)]
    for i in range(1, n):
        lap[i - 1][i - 1] += k * (1 if i == n - 1 else 2)
        if i + 1 < n:
            lap[i - 1][i] -= k
            lap[i][i - 1] -= k
    for d, gd in ((0, 0.0), (1, -9.81)):
        a = [[lap[r][c] + (m / dt ** 2 if r == c else 0.0) for c in range(f)] for r in range(f)]
        rhs = [m / dt ** 2 * (x0[i][d] + dt * v0[i][d]) + m * gd for i in range(1, n)]
        rhs[0] += k * x0[0][d]
        sol = ot.gauss_solve(a, rhs)
        assert max(abs(sol[i - 1] - x1[i][d]) for i in range(1, n)) < 1e-12


def test_safeguarded_newton_never_increases_the_objective():
    for seed in range(4):
        for dt in (1.0 / 24.0, 1.0):
            ch, x0 = crumpled(seed)
            hist = []
            ot.oti_step(ch, x0, [(0.0, 0.0)] * 8, dt, history=hist)
            assert all(b <= a for a, b in zip(hist, hist[1:]))


def test_plain_newton_can_increase_the_objective_and_stop_higher():
    """Measured: from a crumpled start, unguarded Newton raises E and ends at a higher stationary value."""
    ch, x0 = crumpled(0)
    h1, h2 = [], []
    ot.oti_step(ch, x0, [(0.0, 0.0)] * 8, 1.0, history=h1)
    ot.oti_step(ch, x0, [(0.0, 0.0)] * 8, 1.0, safeguards=False, history=h2)
    assert any(b > a for a, b in zip(h2, h2[1:]))
    assert h1[-1] < h2[-1] - 1.0


def test_convex_potential_energy_inequality():
    """For a convex potential, the exact step satisfies E_n - E_(n+1) >= 1/2 |v_(n+1) - v_n|_M^2."""
    ch = ot.hanging_chain(8, 0.1, 100.0, 0.1, rest_zero=True)
    x, v = list(ch.rest), [(0.0, 0.0)] * 8
    for _ in range(48):
        e0 = ot.total_energy(ch, x, v)
        x1, v1, _ = ot.oti_step(ch, x, v, 1.0 / 24.0, tau=1e-10)
        dv = 0.5 * sum(ch.mass[i] * ((v1[i][0] - v[i][0]) ** 2 + (v1[i][1] - v[i][1]) ** 2) for i in ch.free)
        assert e0 - ot.total_energy(ch, x1, v1) >= dv - 1e-9
        x, v = x1, v1


def test_nonconvex_chain_energy_does_not_rise_here():
    """Measured: a falling chain with rest lengths loses energy at every step at dt = 1/24 s."""
    ch = ot.hanging_chain(8, 0.1, 1e4, 0.1)
    x, v = list(ch.rest), [(0.0, 0.0)] * 8
    prev = ot.total_energy(ch, x, v)
    for _ in range(48):
        x, v, _ = ot.oti_step(ch, x, v, 1.0 / 24.0)
        e = ot.total_energy(ch, x, v)
        assert e <= prev + 1e-9
        prev = e


def test_free_fall_is_symplectic_euler():
    ch = ot.Chain([(0.0, 0.0)], [], [1.0])
    x, v = [(0.0, 0.0)], [(0.0, 0.0)]
    for _ in range(10):
        x, v, _ = ot.oti_step(ch, x, v, 0.1)
    assert abs(x[0][1] + 5.3955) < 1e-12
