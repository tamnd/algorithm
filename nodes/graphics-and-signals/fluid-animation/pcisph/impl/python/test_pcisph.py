# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcisph/. The authors are listed in prov/Y0N4QC.jsonl.

import math
import random

import pcisph
import sph

DX = 0.02
H = 1.3 * DX
RHO0 = 1000.0
M = RHO0 * DX * DX


def lattice(n_side):
    return [((i + 0.5) * DX, (j + 0.5) * DX) for i in range(n_side) for j in range(n_side)]


def test_prototype_delta_matches_its_formula() -> None:
    dt = 0.004
    d = pcisph.prototype_delta(DX, H, M, RHO0, dt)
    # Direct sum over a large lattice, written out again.
    ss = 0.0
    gx = gy = 0.0
    for a in range(-6, 7):
        for b in range(-6, 7):
            if (a, b) != (0, 0):
                r = math.hypot(a * DX, b * DX)
                dw = sph.dw_cubic(r, H)
                ss += dw * dw
                g = sph.grad_w((a * DX, b * DX), H)
                gx += g[0]
                gy += g[1]
    beta = 2.0 * dt * dt * M * M / (RHO0 * RHO0)
    assert abs(gx) < 1e-9 and abs(gy) < 1e-9  # the full lattice is symmetric
    assert abs(d - 1.0 / (beta * ss)) < 1e-9 * d
    # delta scales as 1 / dt^2.
    assert abs(pcisph.prototype_delta(DX, H, M, RHO0, 2 * dt) - d / 4.0) < 1e-9 * d


def test_delta_removes_a_small_density_error_to_first_order() -> None:
    # The derivation of delta: pressure p = delta e on the prototype particle c
    # moves each neighbor j by dt^2 m (2 p / rho0^2) grad W_cj, and this lowers
    # the density of c by e to first order.
    dt = 0.004
    d = pcisph.prototype_delta(DX, H, M, RHO0, dt)
    pos = [(a * DX, b * DX) for a in range(-5, 6) for b in range(-5, 6)]
    c = pos.index((0.0, 0.0))
    rho_c = sum(M * sph.w_cubic(math.hypot(*p), H) for p in pos)
    for e in (1e-3, 1e-2):
        p = d * e
        moved = []
        for k, x in enumerate(pos):
            if k == c:
                moved.append(x)
                continue
            g = sph.grad_w((0.0 - x[0], 0.0 - x[1]), H)  # grad W_cj with respect to x_c
            s = dt * dt * M * 2.0 * p / (RHO0 * RHO0)
            moved.append((x[0] + s * g[0], x[1] + s * g[1]))
        new_rho = sum(M * sph.w_cubic(math.hypot(*q), H) for q in moved)
        assert abs((rho_c - new_rho) - e) < 0.05 * e


def test_momentum_is_conserved_without_walls_and_gravity() -> None:
    rng = random.Random(3)
    pos = [(x + rng.uniform(-0.3, 0.3) * DX, y + rng.uniform(-0.3, 0.3) * DX) for x, y in lattice(7)]
    # Squeeze the blob so the pressure is not zero.
    pos = [(0.8 * x, 0.8 * y) for x, y in pos]
    vel = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in pos]
    dt = 0.002
    d = pcisph.prototype_delta(DX, H, M, RHO0, dt)
    p0 = pcisph.momentum(vel, M)
    l0 = pcisph.angular_momentum(pos, vel, M)
    for _ in range(10):
        pos, vel, (it, _) = pcisph.step(pos, vel, M, dt, H, RHO0, d, gravity=(0.0, 0.0))
        assert it >= 3
    p1 = pcisph.momentum(vel, M)
    l1 = pcisph.angular_momentum(pos, vel, M)
    scale = M * sum(math.hypot(*v) for v in vel)
    assert abs(p1[0] - p0[0]) < 1e-10 * scale and abs(p1[1] - p0[1]) < 1e-10 * scale
    assert abs(l1 - l0) < 1e-10 * scale


def test_small_dam_break_reaches_one_percent() -> None:
    n_side = 8
    pos = lattice(n_side)
    vel = [(0.0, 0.0)] * len(pos)
    dt = 0.004
    d = pcisph.prototype_delta(DX, H, M, RHO0, dt)
    box = (0.0, 0.0, 0.4, 0.4)
    worst = 0.0
    for _ in range(60):
        pos, vel, (it, err) = pcisph.step(pos, vel, M, dt, H, RHO0, d, eta=0.01, box=box)
        assert 3 <= it < 50
        assert err <= 0.01
        rho = sph.density(pos, [M] * len(pos), H)
        worst = max(worst, sum(max(r - RHO0, 0.0) for r in rho) / (RHO0 * len(rho)))
    assert worst < 0.01
    assert max(x for x, _ in pos) > n_side * DX + 0.05
    # The step is far above the WCSPH limit 0.4 h / (c + v) with c = 10 v.
    v = math.sqrt(2 * 9.81 * n_side * DX)
    assert dt > 5 * 0.4 * H / (11 * v)
