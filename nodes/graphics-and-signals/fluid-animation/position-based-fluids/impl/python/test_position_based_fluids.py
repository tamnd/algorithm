# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-fluids/. The authors are listed in prov/XH6YNA.jsonl.

import math
import random

import position_based_fluids as pb

DX = 0.02
H = 1.8 * DX
RHO0 = 1000.0
M = RHO0 * DX * DX
D0 = pb.full_lattice_denominator(DX, H, M, RHO0)


def lattice(n_side, spacing):
    return [((i + 0.5) * spacing, (j + 0.5) * spacing) for i in range(n_side) for j in range(n_side)]


def radial_integral(f, h, n=2000):
    # Simpson rule for the integral of f(r) 2 pi r dr over [0, h].
    s = 0.0
    for k in range(n + 1):
        r = h * k / n
        w = 1 if k in (0, n) else (4 if k % 2 else 2)
        s += w * f(r) * 2.0 * math.pi * r
    return s * h / (3 * n)


def test_kernels_integrate_to_one() -> None:
    assert abs(pb.POLY6_2D - 1.273240) < 1e-6
    assert abs(pb.SPIKY_2D - 3.183099) < 1e-6
    for h in (0.5, H):
        assert abs(radial_integral(lambda r: pb.w_poly6(r * r, h), h) - 1.0) < 1e-9
        assert abs(radial_integral(lambda r: pb.w_spiky(r, h), h) - 1.0) < 1e-9


def test_spiky_gradient_matches_finite_differences() -> None:
    rng = random.Random(1)
    e = 1e-7
    for _ in range(20):
        x, y = rng.uniform(-H, H), rng.uniform(-H, H)
        if not 0.05 * H < math.hypot(x, y) < 0.95 * H:
            continue
        g = pb.grad_spiky(x, y, H)
        fx = (pb.w_spiky(math.hypot(x + e, y), H) - pb.w_spiky(math.hypot(x - e, y), H)) / (2 * e)
        fy = (pb.w_spiky(math.hypot(x, y + e), H) - pb.w_spiky(math.hypot(x, y - e), H)) / (2 * e)
        scale = abs(g[0]) + abs(g[1])
        assert abs(g[0] - fx) < 1e-6 * scale and abs(g[1] - fy) < 1e-6 * scale


def test_lambda_matches_a_direct_sum() -> None:
    rng = random.Random(2)
    pos = [(x + rng.uniform(-0.2, 0.2) * DX, y + rng.uniform(-0.2, 0.2) * DX) for x, y in lattice(5, 0.9 * DX)]
    pairs = pb.neighbor_pairs(pos, H)
    eps = 0.01 * D0
    lam, c = pb.lambdas(pos, pairs, M, H, RHO0, eps)
    f = M / RHO0
    for i in range(len(pos)):
        rho = sum(M * pb.w_poly6((pos[i][0] - q[0]) ** 2 + (pos[i][1] - q[1]) ** 2, H) for q in pos)
        gi = [0.0, 0.0]
        sq = 0.0
        for j, q in enumerate(pos):
            if j != i:
                g = pb.grad_spiky(pos[i][0] - q[0], pos[i][1] - q[1], H)
                gi[0] += f * g[0]
                gi[1] += f * g[1]
                sq += f * f * (g[0] ** 2 + g[1] ** 2)
        ci = rho / RHO0 - 1.0
        assert abs(c[i] - ci) < 1e-12
        assert abs(lam[i] - (-ci / (gi[0] ** 2 + gi[1] ** 2 + sq + eps))) < 1e-9 * abs(lam[i]) + 1e-18


def test_passes_lower_the_constraint_error_of_a_squeezed_block() -> None:
    rng = random.Random(3)
    pos = [(x + rng.uniform(-0.05, 0.05) * DX, y + rng.uniform(-0.05, 0.05) * DX) for x, y in lattice(10, 0.93 * DX)]
    vel = [(0.0, 0.0)] * len(pos)
    _, _, hist = pb.step(pos, vel, M, 0.004, H, RHO0, 0.01 * D0, iterations=6, gravity=(0.0, 0.0), c_xsph=0.0,
                         one_sided=True)
    errs = [pb.mean_positive(c) for c in hist]
    assert errs[0] > 0.02
    for a, b in zip(errs, errs[1:]):
        assert b < a
    assert errs[-1] < 0.2 * errs[0]


def test_linear_momentum_is_conserved_without_walls_and_gravity() -> None:
    rng = random.Random(4)
    pos = [(x + rng.uniform(-0.2, 0.2) * DX, y + rng.uniform(-0.2, 0.2) * DX) for x, y in lattice(7, 0.85 * DX)]
    vel = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in pos]
    p0 = pb.momentum(vel, M)
    for one_sided in (False, True):
        for _ in range(5):
            pos, vel, _ = pb.step(pos, vel, M, 0.003, H, RHO0, 0.01 * D0, iterations=4, k=0.1 / D0,
                                  gravity=(0.0, 0.0), one_sided=one_sided)
    p1 = pb.momentum(vel, M)
    scale = M * sum(abs(v[0]) + abs(v[1]) for v in vel)
    assert abs(p1[0] - p0[0]) < 1e-10 * scale and abs(p1[1] - p0[1]) < 1e-10 * scale


def test_small_dam_break_keeps_a_low_density_error() -> None:
    n_side = 8
    pos = lattice(n_side, DX)
    vel = [(0.0, 0.0)] * len(pos)
    box = (0.0, 0.0, 0.4, 0.4)
    worst = 0.0
    for _ in range(60):
        pos, vel, _ = pb.step(pos, vel, M, 0.004, H, RHO0, 0.01 * D0, iterations=4, k=0.1 / D0, box=box,
                              one_sided=True)
        rho = pb.densities(pos, pb.neighbor_pairs(pos, H), M, H)
        worst = max(worst, sum(max(r / RHO0 - 1.0, 0.0) for r in rho) / len(rho))
        assert all(0.0 <= x <= 0.4 and 0.0 <= y <= 0.4 for x, y in pos)
    assert worst < 0.01
    assert max(x for x, _ in pos) > n_side * DX + 0.1
