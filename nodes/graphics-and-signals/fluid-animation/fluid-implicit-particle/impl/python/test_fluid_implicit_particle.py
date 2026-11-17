# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fluid-implicit-particle/. The authors are listed in prov/QNPJRR.jsonl.

import math
import random

import macgrid as mg
import fluid_implicit_particle as fl

N = 8
DX = 1.0 / N


def random_state(seed, count=200):
    rng = random.Random(seed)
    xs = [rng.uniform(0.0, 1.0) for _ in range(count)]
    ys = [rng.uniform(0.0, 1.0) for _ in range(count)]
    us = [rng.uniform(-1.0, 1.0) for _ in xs]
    vs = [rng.uniform(-1.0, 1.0) for _ in xs]
    ms = [rng.uniform(0.5, 1.5) for _ in xs]
    return rng, xs, ys, us, vs, ms


def test_no_grid_change_keeps_the_particle_velocities() -> None:
    _, xs, ys, us, vs, ms = random_state(1)
    g = mg.make_grid(N, N, DX)
    fl.p2g(g, xs, ys, us, vs, ms)
    u_old, v_old = mg.copy_field(g.u), mg.copy_field(g.v)
    us2, vs2 = fl.g2p_flip(g, u_old, v_old, xs, ys, us, vs, 1.0)
    assert us2 == us and vs2 == vs


def test_alpha_zero_is_pic() -> None:
    rng, xs, ys, us, vs, ms = random_state(2)
    g = mg.make_grid(N, N, DX)
    fl.p2g(g, xs, ys, us, vs, ms)
    u_old, v_old = mg.copy_field(g.u), mg.copy_field(g.v)
    g.u = [[c + rng.uniform(-0.5, 0.5) for c in col] for col in g.u]
    g.v = [[c + rng.uniform(-0.5, 0.5) for c in col] for col in g.v]
    us2, vs2 = fl.g2p_flip(g, u_old, v_old, xs, ys, us, vs, 0.0)
    for x, y, u, v in zip(xs, ys, us2, vs2):
        assert abs(u - mg.u_at(g, x, y)) < 1e-12
        assert abs(v - mg.v_at(g, x, y)) < 1e-12


def test_transfers_keep_linear_momentum_for_every_alpha() -> None:
    rng, xs, ys, us, vs, ms = random_state(3)
    g = mg.make_grid(N, N, DX)
    p0 = fl.particle_momentum(us, vs, ms)
    mu, mv = fl.p2g(g, xs, ys, us, vs, ms)
    p1 = fl.grid_momentum(g, mu, mv)
    u_old, v_old = mg.copy_field(g.u), mg.copy_field(g.v)
    g.u = [[c + rng.uniform(-0.5, 0.5) for c in col] for col in g.u]
    g.v = [[c + rng.uniform(-0.5, 0.5) for c in col] for col in g.v]
    p2 = fl.grid_momentum(g, mu, mv)
    for alpha in (0.0, 0.95, 1.0):
        us2, vs2 = fl.g2p_flip(g, u_old, v_old, xs, ys, us, vs, alpha)
        p3 = fl.particle_momentum(us2, vs2, ms)
        for a in range(2):
            assert abs(p1[a] - p0[a]) < 1e-12 * len(xs)
            assert abs(p3[a] - p2[a]) < 1e-12 * len(xs)


def swirl_energy(alpha, steps):
    rng = random.Random(4)
    g = mg.make_grid(N, N, DX)
    xs, ys = fl.seed_block(rng, N, N, DX)
    ms = [1.0] * len(xs)
    us = [math.sin(math.pi * x) * math.cos(math.pi * y) for x, y in zip(xs, ys)]
    vs = [-math.cos(math.pi * x) * math.sin(math.pi * y) for x, y in zip(xs, ys)]
    e0 = fl.particle_kinetic_energy(us, vs, ms)
    for _ in range(steps):
        xs, ys, us, vs = fl.step(g, xs, ys, us, vs, ms, 0.02, alpha=alpha, gravity=0.0)
        assert mg.max_fluid_divergence(g) < 1e-9
    return fl.particle_kinetic_energy(us, vs, ms) / e0


def test_flip_keeps_more_energy_than_pic() -> None:
    # A measurement on a closed box full of liquid, without gravity.
    e_pic = swirl_energy(0.0, 10)
    e_flip = swirl_energy(0.95, 10)
    assert e_pic < 0.5
    assert e_flip > 0.8


def test_small_dam_break() -> None:
    rng = random.Random(5)
    n, dx, dt = 12, 0.05, 0.005
    g = mg.make_grid(n, n, dx)
    xs, ys = fl.seed_block(rng, 4, 6, dx)
    ms = [1000.0 * dx * dx / 4] * len(xs)
    us = [0.0] * len(xs)
    vs = [0.0] * len(xs)
    for _ in range(60):
        xs, ys, us, vs = fl.step(g, xs, ys, us, vs, ms, dt)
        assert mg.max_fluid_divergence(g) < 1e-9
        assert min(xs) >= 0.5 * dx and max(xs) <= n * dx - 0.5 * dx
        assert min(ys) >= 0.5 * dx and max(ys) <= n * dx - 0.5 * dx
    assert max(xs) > 8 * dx
