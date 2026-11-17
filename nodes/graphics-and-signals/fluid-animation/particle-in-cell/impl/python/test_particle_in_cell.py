# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-in-cell/. The authors are listed in prov/N6Z3N3.jsonl.

import random

import macgrid as mg
import particle_in_cell as pic

N = 8
DX = 1.0 / N


def inner_particles(rng, count):
    """Random particles at least half a cell from the walls, so no weight is clamped."""
    xs = [rng.uniform(0.5 * DX, 1.0 - 0.5 * DX) for _ in range(count)]
    ys = [rng.uniform(0.5 * DX, 1.0 - 0.5 * DX) for _ in range(count)]
    return xs, ys


def random_state(seed, count=200):
    rng = random.Random(seed)
    xs, ys = inner_particles(rng, count)
    us = [rng.uniform(-1.0, 1.0) for _ in xs]
    vs = [rng.uniform(-1.0, 1.0) for _ in xs]
    ms = [rng.uniform(0.5, 1.5) for _ in xs]
    return xs, ys, us, vs, ms


def test_weights_match_macgrid_sample() -> None:
    rng = random.Random(1)
    g = mg.make_grid(N, N, DX)
    g.u = [[rng.uniform(-1.0, 1.0) for _ in range(N)] for _ in range(N + 1)]
    g.v = [[rng.uniform(-1.0, 1.0) for _ in range(N + 1)] for _ in range(N)]
    xs = [rng.uniform(-0.2, 1.2) for _ in range(100)]
    ys = [rng.uniform(-0.2, 1.2) for _ in range(100)]
    us, vs = pic.g2p(g, xs, ys)
    for x, y, u, v in zip(xs, ys, us, vs):
        assert abs(u - mg.u_at(g, x, y)) < 1e-12
        assert abs(v - mg.v_at(g, x, y)) < 1e-12
        for wts in (pic.u_weights(g, x, y), pic.v_weights(g, x, y)):
            assert min(w for _, _, w, _, _ in wts) >= 0.0
            assert abs(sum(w for _, _, w, _, _ in wts) - 1.0) < 1e-12


def test_transfers_do_not_add_kinetic_energy() -> None:
    for seed in (2, 3, 4):
        xs, ys, us, vs, ms = random_state(seed)
        g = mg.make_grid(N, N, DX)
        e_particles = pic.particle_kinetic_energy(us, vs, ms)
        mu, mv = pic.p2g(g, xs, ys, us, vs, ms)
        e_grid = pic.grid_kinetic_energy(g, mu, mv)
        us2, vs2 = pic.g2p(g, xs, ys)
        e_back = pic.particle_kinetic_energy(us2, vs2, ms)
        assert e_grid <= e_particles * (1.0 + 1e-12)
        assert e_back <= e_grid * (1.0 + 1e-12)
        assert e_back < 0.9 * e_particles


def test_transfers_keep_linear_momentum() -> None:
    xs, ys, us, vs, ms = random_state(5)
    # Particles near the walls too: the weights are clamped, and the momentum is still kept.
    rng = random.Random(6)
    xs[:20] = [rng.uniform(0.0, 1.0) for _ in range(20)]
    ys[:20] = [rng.uniform(0.0, 1.0) for _ in range(20)]
    g = mg.make_grid(N, N, DX)
    p0 = pic.particle_momentum(us, vs, ms)
    mu, mv = pic.p2g(g, xs, ys, us, vs, ms)
    p1 = pic.grid_momentum(g, mu, mv)
    us2, vs2 = pic.g2p(g, xs, ys)
    p2 = pic.particle_momentum(us2, vs2, ms)
    for a in range(2):
        assert abs(p1[a] - p0[a]) < 1e-12 * len(xs)
        assert abs(p2[a] - p1[a]) < 1e-12 * len(xs)


def test_p2g_keeps_angular_momentum_and_g2p_loses_it() -> None:
    xs, ys, _, _, ms = random_state(7)
    us = [-(y - 0.5) for y in ys]
    vs = [x - 0.5 for x in xs]
    g = mg.make_grid(N, N, DX)
    l0 = sum(m * (x * v - y * u) for x, y, u, v, m in zip(xs, ys, us, vs, ms))
    mu, mv = pic.p2g(g, xs, ys, us, vs, ms)
    l1 = sum(mu[a][b] * -((b + 0.5) * DX) * g.u[a][b] for a in range(N + 1) for b in range(N))
    l1 += sum(mv[a][b] * (a + 0.5) * DX * g.v[a][b] for a in range(N) for b in range(N + 1))
    assert abs(l1 - l0) < 1e-12 * abs(l0) * len(xs)
    us2, vs2 = pic.g2p(g, xs, ys)
    l2 = sum(m * (x * v - y * u) for x, y, u, v, m in zip(xs, ys, us2, vs2, ms))
    assert l2 < 0.99 * l0


def test_constant_velocity_survives_a_round_trip() -> None:
    xs, ys, _, _, ms = random_state(8)
    us = [0.3] * len(xs)
    vs = [-0.7] * len(xs)
    g = mg.make_grid(N, N, DX)
    pic.p2g(g, xs, ys, us, vs, ms)
    us2, vs2 = pic.g2p(g, xs, ys)
    assert max(abs(u - 0.3) for u in us2) < 1e-12
    assert max(abs(v + 0.7) for v in vs2) < 1e-12


def test_small_dam_break() -> None:
    rng = random.Random(9)
    n, dx, dt = 12, 0.05, 0.005
    g = mg.make_grid(n, n, dx)
    xs, ys = pic.seed_block(rng, 4, 6, dx)
    ms = [1000.0 * dx * dx / 4] * len(xs)
    us = [0.0] * len(xs)
    vs = [0.0] * len(xs)
    for _ in range(60):
        xs, ys, us, vs = pic.step(g, xs, ys, us, vs, ms, dt)
        assert mg.max_fluid_divergence(g) < 1e-9
        assert min(xs) >= 0.5 * dx and max(xs) <= n * dx - 0.5 * dx
        assert min(ys) >= 0.5 * dx and max(ys) <= n * dx - 0.5 * dx
    assert max(xs) > 8 * dx
