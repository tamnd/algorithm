# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divergence-free-sph/. The authors are listed in prov/9VJ2XT.jsonl.

import random

import divergence_free_sph as df

DX = 0.02
H = 1.3 * DX
RHO0 = 1000.0
M = RHO0 * DX * DX


def lattice(n_side, spacing):
    return [((i + 0.5) * spacing, (j + 0.5) * spacing) for i in range(n_side) for j in range(n_side)]


def jittered(rng, n_side, spacing):
    return [(x + rng.uniform(-0.1, 0.1) * DX, y + rng.uniform(-0.1, 0.1) * DX) for x, y in lattice(n_side, spacing)]


def test_alpha_matches_a_direct_sum() -> None:
    rng = random.Random(1)
    pos = jittered(rng, 5, 0.9 * DX)
    ms = [M * rng.uniform(0.9, 1.1) for _ in pos]
    nb = df.Neighborhood(pos, ms, H)
    for i in range(nb.n):
        gx = gy = sq = 0.0
        for j in range(nb.n):
            if j != i:
                g = df.grad_w((pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]), H)
                gx += ms[j] * g[0]
                gy += ms[j] * g[1]
                sq += (ms[j] * g[0]) ** 2 + (ms[j] * g[1]) ** 2
        assert abs(nb.alpha[i] - nb.rho[i] / (gx * gx + gy * gy + sq)) < 1e-12 * nb.alpha[i]


def test_one_kappa_removes_its_own_density_error() -> None:
    # With equal masses, kappa on particle i alone moves the predicted density
    # rho_i + dt D rho_i / Dt exactly to rho0, because the prediction is linear in v.
    rng = random.Random(2)
    pos = jittered(rng, 5, 0.9 * DX)
    ms = [M] * len(pos)
    nb = df.Neighborhood(pos, ms, H)
    dt = 0.003
    vel = [(rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2)) for _ in pos]
    rate = df.density_rate(nb, vel)
    for i in (0, 7, 12):
        e = nb.rho[i] + dt * rate[i] - RHO0
        kappa = [0.0] * nb.n
        kappa[i] = e * nb.alpha[i] / (dt * dt)
        new_rate = df.density_rate(nb, df.apply_kappa(nb, vel, kappa, dt))
        assert abs(nb.rho[i] + dt * new_rate[i] - RHO0) < 1e-9 * RHO0
        # The same for the divergence form: D rho_i / Dt goes to 0.
        kappa[i] = rate[i] * nb.alpha[i] / dt
        new_rate = df.density_rate(nb, df.apply_kappa(nb, vel, kappa, dt))
        assert abs(new_rate[i]) < 1e-9 * abs(rate[i])


def test_momentum_is_conserved_without_walls_and_gravity() -> None:
    rng = random.Random(3)
    pos = jittered(rng, 6, 0.85 * DX)
    ms = [M * rng.uniform(0.9, 1.1) for _ in pos]
    vel = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in pos]
    p0 = df.momentum(vel, ms)
    l0 = df.angular_momentum(pos, vel, ms)
    for _ in range(6):
        pos, vel, _ = df.step(pos, vel, ms, 0.002, H, RHO0, gravity=(0.0, 0.0))
    p1 = df.momentum(vel, ms)
    l1 = df.angular_momentum(pos, vel, ms)
    scale = sum(m * (abs(v[0]) + abs(v[1])) for m, v in zip(ms, vel))
    assert abs(p1[0] - p0[0]) < 1e-10 * scale and abs(p1[1] - p0[1]) < 1e-10 * scale
    assert abs(l1 - l0) < 1e-10 * scale


def test_small_dam_break_reaches_both_tolerances() -> None:
    n_side = 8
    pos = lattice(n_side, DX)
    ms = [M] * len(pos)
    vel = [(0.0, 0.0)] * len(pos)
    box = (0.0, 0.0, 0.4, 0.4)
    worst = 0.0
    t = 0.0
    while t < 0.2:
        dt = df.cfl_step(DX, df.max_speed(vel), 0.4, 0.004)
        pos, vel, (it_d, err_d, it_v, err_v) = df.step(pos, vel, ms, dt, H, RHO0, eta=0.001, eta_v=0.001, box=box)
        t += dt
        assert 2 <= it_d < 100 and err_d <= 0.001
        assert 1 <= it_v < 100 and err_v <= 0.001
        worst = max(worst, df.mean_compression(pos, ms, H, RHO0))
    assert worst < 0.01
    assert max(x for x, _ in pos) > n_side * DX + 0.1


def test_cfl_step() -> None:
    assert df.cfl_step(0.02, 0.0) == 0.005
    assert abs(df.cfl_step(0.02, 4.0) - 0.002) < 1e-15
    assert df.cfl_step(0.02, 0.1) == 0.005
