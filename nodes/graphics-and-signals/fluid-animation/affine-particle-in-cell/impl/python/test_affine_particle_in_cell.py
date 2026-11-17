# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-particle-in-cell/. The authors are listed in prov/AJQ8H2.jsonl.

import math
import random

import macgrid as mg
import affine_particle_in_cell as ap

N = 8
DX = 1.0 / N


def random_state(seed, count=200):
    """Random particles at least half a cell from the walls, so no weight is clamped."""
    rng = random.Random(seed)
    xs = [rng.uniform(0.5 * DX, 1.0 - 0.5 * DX) for _ in range(count)]
    ys = [rng.uniform(0.5 * DX, 1.0 - 0.5 * DX) for _ in range(count)]
    us = [rng.uniform(-1.0, 1.0) for _ in xs]
    vs = [rng.uniform(-1.0, 1.0) for _ in xs]
    cus = [(rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)) for _ in xs]
    cvs = [(rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)) for _ in xs]
    ms = [rng.uniform(0.5, 1.5) for _ in xs]
    return rng, xs, ys, us, vs, cus, cvs, ms


def test_transfers_keep_angular_momentum() -> None:
    for seed in (1, 2):
        _, xs, ys, us, vs, cus, cvs, ms = random_state(seed)
        g = mg.make_grid(N, N, DX)
        l0 = ap.particle_angular_momentum(g, xs, ys, us, vs, cus, cvs, ms)
        mu, mv = ap.p2g(g, xs, ys, us, vs, cus, cvs, ms)
        l1 = ap.grid_angular_momentum(g, mu, mv)
        us2, vs2, cus2, cvs2 = ap.g2p(g, xs, ys)
        l2 = ap.particle_angular_momentum(g, xs, ys, us2, vs2, cus2, cvs2, ms)
        scale = sum(m * (abs(u) + abs(v)) for u, v, m in zip(us, vs, ms))
        assert abs(l1 - l0) < 1e-12 * scale
        assert abs(l2 - l1) < 1e-12 * scale


def test_transfers_keep_linear_momentum() -> None:
    _, xs, ys, us, vs, cus, cvs, ms = random_state(3)
    g = mg.make_grid(N, N, DX)
    p0 = ap.particle_momentum(us, vs, ms)
    mu, mv = ap.p2g(g, xs, ys, us, vs, cus, cvs, ms)
    p1 = ap.grid_momentum(g, mu, mv)
    us2, vs2, _, _ = ap.g2p(g, xs, ys)
    p2 = ap.particle_momentum(us2, vs2, ms)
    for a in range(2):
        assert abs(p1[a] - p0[a]) < 1e-12 * len(xs)
        assert abs(p2[a] - p1[a]) < 1e-12 * len(xs)


def test_affine_field_survives_a_round_trip() -> None:
    rng, xs, ys, _, _, _, _, ms = random_state(4)
    a, b, c, d, e, f = (rng.uniform(-1.0, 1.0) for _ in range(6))
    us = [a + b * x + c * y for x, y in zip(xs, ys)]
    vs = [d + e * x + f * y for x, y in zip(xs, ys)]
    g = mg.make_grid(N, N, DX)
    ap.p2g(g, xs, ys, us, vs, [(b, c)] * len(xs), [(e, f)] * len(xs), ms)
    us2, vs2, cus2, cvs2 = ap.g2p(g, xs, ys)
    for i in range(len(xs)):
        assert abs(us2[i] - us[i]) < 1e-12 and abs(vs2[i] - vs[i]) < 1e-12
        assert abs(cus2[i][0] - b) < 1e-11 and abs(cus2[i][1] - c) < 1e-11
        assert abs(cvs2[i][0] - e) < 1e-11 and abs(cvs2[i][1] - f) < 1e-11
    # Without the gradients (the PIC transfer), the same field loses energy.
    zero = [(0.0, 0.0)] * len(xs)
    ap.p2g(g, xs, ys, us, vs, zero, zero, ms)
    us3, vs3, _, _ = ap.g2p(g, xs, ys)
    assert ap.particle_kinetic_energy(us3, vs3, ms) < ap.particle_kinetic_energy(us, vs, ms)


def test_gradient_equals_b_times_d_inverse() -> None:
    rng, xs, ys, _, _, _, _, _ = random_state(5)
    g = mg.make_grid(N, N, DX)
    g.u = [[rng.uniform(-1.0, 1.0) for _ in range(N)] for _ in range(N + 1)]
    g.v = [[rng.uniform(-1.0, 1.0) for _ in range(N + 1)] for _ in range(N)]
    _, _, cus, cvs = ap.g2p(g, xs, ys)
    for p, (x, y) in enumerate(zip(xs, ys)):
        for wts, face, field, grad in ((ap.u_weights(g, x, y), ap.u_face, g.u, cus[p]),
                                       (ap.v_weights(g, x, y), ap.v_face, g.v, cvs[p])):
            bx = by = dxx = dyy = dxy = 0.0
            for a, b, w, _, _ in wts:
                fx, fy = face(g, a, b)
                bx += w * field[a][b] * (fx - x)
                by += w * field[a][b] * (fy - y)
                dxx += w * (fx - x) ** 2
                dyy += w * (fy - y) ** 2
                dxy += w * (fx - x) * (fy - y)
            assert abs(dxy) < 1e-15
            if dxx > 1e-6 * DX * DX and dyy > 1e-6 * DX * DX:
                assert abs(grad[0] - bx / dxx) < 1e-8
                assert abs(grad[1] - by / dyy) < 1e-8


def test_swirl_keeps_most_energy() -> None:
    # A measurement on a closed box full of liquid, without gravity.
    rng = random.Random(4)
    g = mg.make_grid(N, N, DX)
    xs, ys = ap.seed_block(rng, N, N, DX)
    ms = [1.0] * len(xs)
    us = [math.sin(math.pi * x) * math.cos(math.pi * y) for x, y in zip(xs, ys)]
    vs = [-math.cos(math.pi * x) * math.sin(math.pi * y) for x, y in zip(xs, ys)]
    cus = [(0.0, 0.0)] * len(xs)
    cvs = [(0.0, 0.0)] * len(xs)
    e0 = ap.particle_kinetic_energy(us, vs, ms)
    for _ in range(10):
        xs, ys, us, vs, cus, cvs = ap.step(g, xs, ys, us, vs, cus, cvs, ms, 0.02, gravity=0.0)
        assert mg.max_fluid_divergence(g) < 1e-9
    assert ap.particle_kinetic_energy(us, vs, ms) > 0.8 * e0


def test_small_dam_break() -> None:
    rng = random.Random(6)
    n, dx, dt = 12, 0.05, 0.005
    g = mg.make_grid(n, n, dx)
    xs, ys = ap.seed_block(rng, 4, 6, dx)
    ms = [1000.0 * dx * dx / 4] * len(xs)
    us = [0.0] * len(xs)
    vs = [0.0] * len(xs)
    cus = [(0.0, 0.0)] * len(xs)
    cvs = [(0.0, 0.0)] * len(xs)
    for _ in range(60):
        xs, ys, us, vs, cus, cvs = ap.step(g, xs, ys, us, vs, cus, cvs, ms, dt)
        assert mg.max_fluid_divergence(g) < 1e-9
        assert min(xs) >= 0.5 * dx and max(xs) <= n * dx - 0.5 * dx
        assert min(ys) >= 0.5 * dx and max(ys) <= n * dx - 0.5 * dx
    assert max(xs) > 8 * dx
