# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-incompressible-sph/. The authors are listed in prov/V1STXV.jsonl.

import random

import implicit_incompressible_sph as ii

DX = 0.02
H = 1.3 * DX
RHO0 = 1000.0
M = RHO0 * DX * DX


def lattice(n_side, spacing):
    return [((i + 0.5) * spacing, (j + 0.5) * spacing) for i in range(n_side) for j in range(n_side)]


def solve_dense(a, b):
    n = len(b)
    a = [row[:] + [b[k]] for k, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[piv] = a[piv], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n + 1):
                a[r][k] -= f * a[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (a[r][n] - sum(a[r][k] * x[k] for k in range(r + 1, n))) / a[r][r]
    return x


def squeezed_cluster(rng, n_side=5):
    pos = [(x + rng.uniform(-0.1, 0.1) * DX, y + rng.uniform(-0.1, 0.1) * DX) for x, y in lattice(n_side, 0.8 * DX)]
    ms = [M * rng.uniform(0.9, 1.1) for _ in pos]
    return pos, ms


def test_diagonal_equals_the_operator_on_unit_vectors() -> None:
    rng = random.Random(1)
    pos, ms = squeezed_cluster(rng)
    nb = ii.Neighborhood(pos, ms, H)
    dt = 0.003
    diag = ii.diagonal(nb, dt)
    for i in range(nb.n):
        e = [0.0] * nb.n
        e[i] = 1.0
        col = ii.apply_a(nb, e, dt)
        assert abs(col[i] - diag[i]) < 1e-10 * abs(diag[i])
        assert diag[i] < 0.0


def test_operator_is_the_predicted_density_change() -> None:
    # (A p)_i is the first order change of rho_i when the pressure acceleration
    # acts for one step dt: x_j moves by dt^2 a^p_j.
    rng = random.Random(2)
    pos, ms = squeezed_cluster(rng)
    nb = ii.Neighborhood(pos, ms, H)
    dt = 1e-4
    p = [rng.uniform(0.0, 50.0) for _ in pos]
    ax, ay = ii.pressure_acc(nb, p)
    ap = ii.apply_a(nb, p, dt)
    moved = [(x + dt * dt * ax[k], y + dt * dt * ay[k]) for k, (x, y) in enumerate(pos)]
    rho_new = ii.density(moved, ms, H)
    for i in range(nb.n):
        assert abs((rho_new[i] - nb.rho[i]) - ap[i]) < 1e-3 * max(abs(ap[i]), 1e-12) + 1e-12


def test_relaxed_jacobi_equals_gaussian_elimination() -> None:
    # Without the clamp, relaxed Jacobi converges to the exact solution of A p = s.
    rng = random.Random(3)
    pos, ms = squeezed_cluster(rng, 4)
    nb = ii.Neighborhood(pos, ms, H)
    dt = 0.003
    vel_adv = [(0.0, 0.0)] * nb.n
    s = ii.source(nb, vel_adv, dt, RHO0)
    diag = ii.diagonal(nb, dt)
    cols = [ii.apply_a(nb, [1.0 if k == c else 0.0 for k in range(nb.n)], dt) for c in range(nb.n)]
    a = [[cols[c][r] for c in range(nb.n)] for r in range(nb.n)]
    ref = solve_dense(a, s)
    p, it, err = ii.relaxed_jacobi(nb, s, diag, dt, RHO0, [0.0] * nb.n, eta=0.0, min_iter=500,
                                   max_iter=500, clamp=False)
    assert it == 500
    scale = max(abs(t) for t in ref)
    for x, y in zip(p, ref):
        assert abs(x - y) < 1e-9 * scale


def test_momentum_is_conserved_without_walls_and_gravity() -> None:
    rng = random.Random(4)
    pos, ms = squeezed_cluster(rng, 6)
    vel = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in pos]
    p0 = ii.momentum(vel, ms)
    l0 = ii.angular_momentum(pos, vel, ms)
    p = None
    for _ in range(8):
        pos, vel, p, _ = ii.step(pos, vel, ms, 0.002, H, RHO0, p, gravity=(0.0, 0.0))
    p1 = ii.momentum(vel, ms)
    l1 = ii.angular_momentum(pos, vel, ms)
    scale = sum(m * ii.speed(v) for m, v in zip(ms, vel))
    assert abs(p1[0] - p0[0]) < 1e-10 * scale and abs(p1[1] - p0[1]) < 1e-10 * scale
    assert abs(l1 - l0) < 1e-10 * scale


def test_small_dam_break_reaches_its_tolerance() -> None:
    n_side = 8
    pos = lattice(n_side, DX)
    ms = [M] * len(pos)
    vel = [(0.0, 0.0)] * len(pos)
    box = (0.0, 0.0, 0.4, 0.4)
    p = None
    worst = 0.0
    for _ in range(100):
        pos, vel, p, (it, err) = ii.step(pos, vel, ms, 0.002, H, RHO0, p, eta=0.001, box=box)
        assert 2 <= it < 100
        assert err <= 0.001
        worst = max(worst, ii.mean_compression(pos, ms, H, RHO0))
    # The solver bounds the predicted error; the measured compression after the
    # step is larger (first order prediction, wall clamp) but stays below 1%.
    assert worst < 0.01
    assert max(x for x, _ in pos) > n_side * DX + 0.1
    assert all(q >= 0.0 for q in p)
