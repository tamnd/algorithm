# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projective-dynamics/. The authors are listed in prov/NBWGAF.jsonl.

"""Tests of projective dynamics: the solver parts, monotone descent, convergence and momentum."""

import math
import random

from anim import num_grad, rot2, solve
import projective_dynamics as pd


def test_example_one_triangle():
    mesh = pd.Mesh([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], [(0, 1, 2)], 200.0, density=6.0, pinned=[0, 1])
    assert abs(mesh.mass[2] - 1.0) < 1e-15 and abs(mesh.weights[0] - 100.0) < 1e-12
    solver = pd.Solver(mesh, 0.1)
    x = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.5)]
    x1, v1 = pd.pd_step(solver, x, [(0.0, 0.0)] * 3, 1, gravity=(0.0, 0.0))
    assert math.dist(x1[2], (0.0, 1.25)) < 1e-14 and math.dist(v1[2], (0.0, -2.5)) < 1e-12
    x2, _ = pd.pd_step(solver, x, [(0.0, 0.0)] * 3, 5, gravity=(0.0, 0.0))
    assert math.dist(x2[2], (0.0, 1.25)) < 1e-14


def test_cholesky_against_lu():
    rng = random.Random(31)
    for n in (1, 3, 8):
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        a = [[sum(b[i][k] * b[j][k] for k in range(n)) + (n if i == j else 0.0) for j in range(n)] for i in range(n)]
        rhs = [rng.uniform(-1, 1) for _ in range(n)]
        c = pd.cholesky(a)
        assert max(abs(sum(c[i][k] * c[j][k] for k in range(n)) - a[i][j]) for i in range(n) for j in range(n)) < 1e-12
        x1 = pd.cholesky_solve(c, rhs)
        x2 = solve(a, rhs)
        assert max(abs(p - q) for p, q in zip(x1, x2)) < 1e-12


def test_energy_is_zero_exactly_on_rigid_motions():
    rng = random.Random(32)
    mesh = pd.grid(4, 3, 0.1, 50.0, pin_left=False)
    assert energy_close(mesh, mesh.rest, 0.0)
    for _ in range(10):
        r = rot2(rng.uniform(-math.pi, math.pi))
        t = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        x = [(r[0][0] * p[0] + r[0][1] * p[1] + t[0], r[1][0] * p[0] + r[1][1] * p[1] + t[1]) for p in mesh.rest]
        assert energy_close(mesh, x, 0.0)
    stretched = [(1.1 * p[0], p[1]) for p in mesh.rest]
    total_area = 0.3 * 0.2
    assert energy_close(mesh, stretched, 0.5 * 50.0 * total_area * 0.01)


def energy_close(mesh, x, want):
    return abs(pd.energy(mesh, x) - want) < 1e-12


def test_gradient_against_num_grad():
    rng = random.Random(33)
    mesh = pd.grid(3, 3, 0.2, 80.0, density=2.0)
    x = [(p[0] + rng.uniform(-0.03, 0.03), p[1] + rng.uniform(-0.03, 0.03)) if i in mesh.free else p
         for i, p in enumerate(mesh.rest)]
    y = [(p[0] + 0.01, p[1] - 0.02) for p in x]
    dt = 0.05
    grad = pd.gradient(mesh, x, y, dt)
    flat = [c for p in x for c in p]

    def f(z):
        return pd.objective(mesh, [(z[2 * i], z[2 * i + 1]) for i in range(len(x))], y, dt)

    ng = num_grad(f, flat)
    for i in mesh.free:
        for d in range(2):
            assert abs(ng[2 * i + d] - grad[i][d]) < 1e-6 * max(1.0, abs(grad[i][d]))


def test_objective_never_increases():
    for k in (10.0, 1000.0):
        mesh = pd.grid(5, 3, 0.1, k)
        solver = pd.Solver(mesh, 1.0 / 30.0)
        x, v = list(mesh.rest), [(0.0, 0.0)] * len(mesh.rest)
        for _ in range(4):
            hist = []
            y = pd.predict(mesh, x, v, solver.dt)
            start = pd.objective(mesh, y, y, solver.dt)
            x, v = pd.pd_step(solver, x, v, 30, history=hist)
            seq = [start] + hist
            assert all(b <= a + 1e-12 * abs(a) for a, b in zip(seq, seq[1:]))


def test_converges_to_a_backward_euler_step():
    mesh = pd.grid(5, 3, 0.1, 100.0)
    solver = pd.Solver(mesh, 1.0 / 30.0)
    x, v = list(mesh.rest), [(0.0, 0.0)] * len(mesh.rest)
    x, v = pd.pd_step(solver, x, v, 20)
    y = pd.predict(mesh, x, v, solver.dt)
    z, _ = pd.pd_step(solver, x, v, 300)
    grad = pd.gradient(mesh, z, y, solver.dt)
    assert max(abs(c) for g in grad for c in g) < 1e-10
    z5, _ = pd.pd_step(solver, x, v, 5)
    grad5 = pd.gradient(mesh, z5, y, solver.dt)
    assert max(abs(c) for g in grad5 for c in g) > 1e-6


def test_linear_momentum_is_kept_at_every_iteration_count():
    rng = random.Random(34)
    mesh = pd.grid(4, 3, 0.1, 200.0, pin_left=False)
    solver = pd.Solver(mesh, 0.02)
    x = list(mesh.rest)
    v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in x]
    p0 = [sum(m * u[d] for m, u in zip(mesh.mass, v)) for d in range(2)]
    for it in (1, 2, 7):
        for _ in range(10):
            x, v = pd.pd_step(solver, x, v, it, gravity=(0.0, 0.0))
        p1 = [sum(m * u[d] for m, u in zip(mesh.mass, v)) for d in range(2)]
        assert max(abs(a - b) for a, b in zip(p0, p1)) < 1e-12


def test_free_fall_of_an_unstressed_body():
    mesh = pd.grid(3, 2, 0.1, 100.0, pin_left=False)
    solver = pd.Solver(mesh, 0.1)
    x, v = list(mesh.rest), [(0.0, 0.0)] * len(mesh.rest)
    for _ in range(10):
        x, v = pd.pd_step(solver, x, v, 3)
    for p, q in zip(x, mesh.rest):
        assert abs(p[1] - q[1] + 5.3955) < 1e-10 and abs(p[0] - q[0]) < 1e-10
