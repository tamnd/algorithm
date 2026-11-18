# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-mass-spring/. The authors are listed in prov/CQQNYH.jsonl.

"""Tests of fast mass-spring simulation against brute force, Newton's method and exact values."""

import math
import random

from anim import num_grad, solve
import fast_mass_spring as fms


def test_lemma_by_brute_force():
    """(|p| - r)^2 = min over |d| = r of |p - d|^2, by a scan of directions."""
    rng = random.Random(1)
    for _ in range(20):
        p = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        r = rng.uniform(0.0, 2.0)
        best = min((p[0] - r * math.cos(t)) ** 2 + (p[1] - r * math.sin(t)) ** 2
                   for t in (2 * math.pi * i / 20000 for i in range(20000)))
        assert abs(best - (math.hypot(*p) - r) ** 2) < 1e-6


def test_banded_cholesky_against_dense_solve():
    rng = random.Random(2)
    x, springs = fms.grid(5, 4, 0.1, 30.0, 10.0)
    s = fms.FastMassSpring(len(x), springs, [rng.uniform(0.5, 1.5) for _ in x], 0.05, fixed={0, 4})
    nf = len(s.free)
    a = [[0.0] * nf for _ in range(nf)]
    for i in range(nf):
        for j in range(nf):
            a[i][j] = sum(s.r[i][k] * s.r[j][k] for k in range(nf))
    b = [rng.uniform(-1, 1) for _ in range(nf)]
    got = fms.cholesky_solve(s.r, s.bw, b)
    want = solve(a, b)
    assert max(abs(p - q) for p, q in zip(got, want)) < 1e-12
    assert s.bw == 6  # a 5 wide grid with shear springs couples i and i + 6


def test_forces_against_num_grad_rest_and_rotation():
    rng = random.Random(3)
    x, springs = fms.grid(4, 4, 0.2, 50.0, 20.0)
    s = fms.FastMassSpring(len(x), springs, [1.0] * len(x), 0.05)
    y = [(p[0] + rng.uniform(-0.05, 0.05), p[1] + rng.uniform(-0.05, 0.05)) for p in x]
    f = s.spring_forces(y)

    def energy(flat):
        return s.spring_energy([(flat[2 * i], flat[2 * i + 1]) for i in range(len(y))])

    g = num_grad(energy, [c for p in y for c in p], 1e-6)
    scale = max(abs(c) for c in g)
    for i in range(len(y)):
        for c in range(2):
            assert abs(f[i][c] + g[2 * i + c]) <= 1e-6 * scale
    for th in (0.0, 1.1):
        cs, sn = math.cos(th), math.sin(th)
        z = [(cs * p[0] - sn * p[1] + 0.3, sn * p[0] + cs * p[1] - 0.7) for p in x]
        assert max(abs(c) for fi in s.spring_forces(z) for c in fi) < 1e-10


def hanging_scene(rng, nx=4, ny=4, h=0.05, k=200.0):
    x, springs = fms.grid(nx, ny, 0.1, k, k / 2)
    mass = [rng.uniform(0.02, 0.05) for _ in x]
    s = fms.FastMassSpring(len(x), springs, mass, h, fixed={0, nx - 1})
    v = [(0.0, 0.0) if i in s.fixed else (rng.uniform(-1, 1), rng.uniform(-1, 1)) for i in range(len(x))]
    x = [p if i in s.fixed else (p[0] + rng.uniform(-0.02, 0.02), p[1] + rng.uniform(-0.02, 0.02))
         for i, p in enumerate(x)]
    return s, x, v


def test_objective_never_increases():
    s, x, v = hanging_scene(random.Random(4))
    y = s.inertial_target(x, v)
    z = list(y)
    prev = s.objective(z, y)
    for _ in range(40):
        z = s.global_step(z, s.local_step(z), y)
        cur = s.objective(z, y)
        assert cur <= prev + 1e-12 * abs(prev)
        prev = cur


def newton_reference(s, x, v):
    """Backward Euler by Newton's method with a dense Hessian and a backtracking line search."""
    y = s.inertial_target(x, v)
    z = list(y)
    h2 = s.h * s.h
    nf = len(s.free)
    for _ in range(200):
        fs = s.spring_forces(z)
        grad = []
        for p in s.free:
            for c in range(2):
                grad.append(s.mass[p] * (z[p][c] - y[p][c]) - h2 * (fs[p][c] + s.f_ext[p][c]))
        if max(abs(g) for g in grad) < 1e-13:
            break
        hess = [[0.0] * (2 * nf) for _ in range(2 * nf)]
        for i, p in enumerate(s.free):
            hess[2 * i][2 * i] += s.mass[p]
            hess[2 * i + 1][2 * i + 1] += s.mass[p]
        for a, b, rest, k in s.springs:
            d = (z[a][0] - z[b][0], z[a][1] - z[b][1])
            length = math.hypot(*d)
            u = (d[0] / length, d[1] / length)
            # the transverse term is clamped at zero, which keeps the Hessian positive definite
            blk = [[h2 * k * (max(0.0, 1 - rest / length) * ((1.0 if r == c else 0.0) - u[r] * u[c]) + u[r] * u[c])
                    for c in range(2)] for r in range(2)]
            for p, q, sg in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
                if p in s.fixed or q in s.fixed:
                    continue
                for r in range(2):
                    for c in range(2):
                        hess[2 * s.slot[p] + r][2 * s.slot[q] + c] += sg * blk[r][c]
        step = solve(hess, [-g for g in grad])
        t = 1.0
        g0 = s.objective(z, y)
        while True:
            trial = list(z)
            for i, p in enumerate(s.free):
                trial[p] = (z[p][0] + t * step[2 * i], z[p][1] + t * step[2 * i + 1])
            if s.objective(trial, y) <= g0 or t < 1e-8:
                break
            t *= 0.5
        z = trial
    return z


def test_converges_to_the_backward_euler_solution():
    s, x, v = hanging_scene(random.Random(5))
    ref = newton_reference(s, x, v)
    z, _ = s.step(x, v, iterations=300)
    assert max(math.dist(p, q) for p, q in zip(z, ref)) < 1e-9
    # and z solves M (z - y) = h^2 (f(z) + f_ext) to rounding
    y = s.inertial_target(x, v)
    fs = s.spring_forces(z)
    for p in s.free:
        for c in range(2):
            res = s.mass[p] * (z[p][c] - y[p][c]) - s.h ** 2 * (fs[p][c] + s.f_ext[p][c])
            assert abs(res) < 1e-10


def test_momentum_after_any_number_of_iterations():
    rng = random.Random(6)
    x, springs = fms.grid(4, 3, 0.1, 100.0, 50.0)
    mass = [rng.uniform(0.5, 2.0) for _ in x]
    s = fms.FastMassSpring(len(x), springs, mass, 0.02)
    v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in x]
    total = sum(mass)
    for iters in (1, 3):
        xs, vs = list(x), list(v)
        p0 = [sum(m * vi[c] for m, vi in zip(mass, vs)) for c in range(2)]
        for n in range(1, 101):
            xs, vs = s.step(xs, vs, iterations=iters)
            for c in range(2):
                want = p0[c] + n * 0.02 * total * fms.GRAVITY[c]
                got = sum(m * vi[c] for m, vi in zip(mass, vs))
                assert abs(got - want) <= 1e-10 * max(1.0, abs(want))


def test_linear_oscillator_loses_energy_as_backward_euler():
    """One mass on a spring along a line: each step multiplies the energy by 1 / (1 + (omega h)^2)."""
    s = fms.FastMassSpring(2, [(0, 1, 1.0, 100.0)], [1.0, 1.0], 0.1, fixed={0}, gravity=(0.0, 0.0))
    x = [(0.0, 0.0), (1.5, 0.0)]
    v = [(0.0, 0.0), (0.0, 0.0)]

    def energy(x, v):
        return 0.5 * v[1][0] ** 2 + 0.5 * 100.0 * (x[1][0] - 1.0) ** 2

    e = energy(x, v)
    for _ in range(20):
        x, v = s.step(x, v, iterations=1)
        e1 = energy(x, v)
        assert abs(e1 / e - 0.5) < 1e-12  # omega h = 10 * 0.1 = 1
        e = e1


def test_large_step_stays_bounded_where_symplectic_euler_fails():
    nx = 6
    x0, springs = fms.grid(nx, nx, 0.1, 1e4, 5e3)
    mass = [0.01] * len(x0)
    h = 1.0 / 30.0
    s = fms.FastMassSpring(len(x0), springs, mass, h, fixed={0, nx - 1})
    x, v = list(x0), [(0.0, 0.0)] * len(x0)
    for _ in range(30):
        x, v = s.step(x, v, iterations=10)
        assert s.spring_energy(x) < 10.0 and max(math.hypot(*vi) for vi in v) < 10.0
    # symplectic Euler with the same step blows up: omega = 1000 rad/s, omega h = 33
    x, v = list(x0), [(0.0, 0.0)] * len(x0)
    x = [p if i in s.fixed else (p[0], p[1] - 0.001 * (i % 3)) for i, p in enumerate(x)]
    for _ in range(10):
        f = s.spring_forces(x)
        v = [(0.0, 0.0) if i in s.fixed else (v[i][0] + h * (f[i][0] / mass[i]),
                                              v[i][1] + h * (f[i][1] / mass[i] + fms.GRAVITY[1]))
             for i in range(len(x))]
        x = [(x[i][0] + h * v[i][0], x[i][1] + h * v[i][1]) for i in range(len(x))]
    assert s.spring_energy(x) > 1e6
