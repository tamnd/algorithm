# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-solid-fluid-coupling/. The authors are listed in prov/T5ZPKE.jsonl.

"""Tests of the variational pressure projection and the rigid body coupling."""

import math
import random

import pytest

import macgrid
from macgrid import AIR, SOLID
import variational_solid_fluid_coupling as VC

RHO, G, DT = 1000.0, 9.81, 0.01


def bowl_grid(n, level=0.75):
    """An n by n grid of the unit square; cells above the level are AIR."""
    g = macgrid.make_grid(n, n, 1.0 / n)
    for i in range(n):
        for j in range(n):
            if (j + 0.5) / n > level:
                g.label[i][j] = AIR
    return g


def bowl(x, y):
    """A round container: fluid inside the circle of radius 0.46 about (0.5, 0.5)."""
    return 0.46 - math.hypot(x - 0.5, y - 0.5)


def disk(r):
    return lambda x, y: math.hypot(x, y) - r


def test_inside_fraction():
    assert VC.inside_fraction(-1.0, -2.0) == 1.0
    assert VC.inside_fraction(1.0, 0.0) == 0.0
    assert VC.inside_fraction(-1.0, 3.0) == 0.25
    assert VC.inside_fraction(3.0, -1.0) == 0.25


def test_binary_weights_match_the_voxelized_solve():
    rng = random.Random(1)
    n = 12
    g = macgrid.make_grid(n, n, 1.0 / n)
    for i in range(n):
        for j in range(n):
            if j >= 9:
                g.label[i][j] = AIR
            elif rng.random() < 0.15:
                g.label[i][j] = SOLID
    g.u = [[rng.uniform(-1, 1) for j in range(n)] for i in range(n + 1)]
    g.v = [[rng.uniform(-1, 1) for j in range(n + 1)] for i in range(n)]
    h = macgrid.make_grid(n, n, 1.0 / n)
    h.label = [list(c) for c in g.label]
    h.u, h.v = macgrid.copy_field(g.u), macgrid.copy_field(g.v)
    macgrid.project(h, DT, RHO)
    VC.project(g, DT, RHO, VC.binary_weights(g))
    for a, b in ((g.u, h.u), (g.v, h.v)):
        assert max(abs(x - y) for c1, c2 in zip(a, b) for x, y in zip(c1, c2)) < 1e-10
    assert max(abs(x - y) for c1, c2 in zip(g.p, h.p) for x, y in zip(c1, c2)) < 1e-7


def channel(deg):
    """A straight channel of width 0.24 at deg degrees across a 24 by 16 grid, open at both ends."""
    nx, ny = 24, 16
    dx = 1.0 / nx
    th = math.radians(deg)
    t = (math.cos(th), math.sin(th))
    c = (0.5, 0.5 * ny * dx)

    def wall(x, y):
        return 0.12 - abs(-t[1] * (x - c[0]) + t[0] * (y - c[1]))

    def grid():
        g = macgrid.make_grid(nx, ny, dx)
        for j in range(ny):
            g.label[0][j] = AIR
            g.label[nx - 1][j] = AIR
        g.u = [[t[0]] * ny for _ in range(nx + 1)]
        g.v = [[t[1]] * (ny + 1) for _ in range(nx)]
        return g

    return wall, grid


@pytest.mark.parametrize("deg, vox_flux", [(10, 0.22388), (20, 0.21864)])
def test_uniform_flow_along_a_tilted_channel_is_kept(deg, vox_flux):
    wall, grid = channel(deg)
    g = grid()
    W = VC.Weights(g, wall)
    u0, v0 = macgrid.copy_field(g.u), macgrid.copy_field(g.v)
    VC.project(g, DT, RHO, W)
    assert max(abs(g.u[i][j] - u0[i][j]) for i in range(25) for j in range(16) if W.wu[i][j] > 0) < 1e-12
    assert max(abs(g.v[i][j] - v0[i][j]) for i in range(24) for j in range(17) if W.wv[i][j] > 0) < 1e-12
    flux = sum(W.wu[12][j] * g.u[12][j] for j in range(16)) / 24
    assert abs(flux - 0.24) < 1e-12  # speed 1 times the width 0.24
    h = grid()  # the voxelized solve: a cell is SOLID if its center is in the wall
    for i in range(1, 23):
        for j in range(16):
            if wall((i + 0.5) / 24, (j + 0.5) / 24) < 0.0:
                h.label[i][j] = SOLID
    macgrid.project(h, DT, RHO)
    vflux = sum(h.u[12][j] for j in range(16) if not macgrid.is_solid_u_face(h, 12, j)) / 24
    assert abs(vflux - vox_flux) < 1e-4


def test_hydrostatic_rest_in_a_round_bowl():
    n = 24
    g = bowl_grid(n)
    W = VC.Weights(g, bowl)
    VC.gravity(g, W, DT, G)
    S, _ = VC.project(g, DT, RHO, W)
    assert max(abs(t) for c in g.u + g.v for t in c) < 1e-10
    top = max(j for j in range(n) if g.label[0][j] != AIR)
    assert max(abs(g.p[i][j] - RHO * G * (top + 1 - j) / n) for (i, j) in S.cells) < 1e-8


def test_neutrally_buoyant_body_stays_at_rest():
    g = bowl_grid(24)
    body = VC.Body(disk(0.1), (0.5, 0.45), RHO, angle=0.3)
    W = VC.Weights(g, bowl, body)
    VC.gravity(g, W, DT, G, body)
    VC.project(g, DT, RHO, W, body)
    assert max(abs(t) for t in body.V) < 1e-12
    assert max(abs(t) for c in g.u + g.v for t in c) < 1e-10


@pytest.mark.parametrize("ratio, a_over_g", [(2.0, -0.33159), (0.5, 0.32986), (0.1, 0.80659)])
def test_heavy_and_light_bodies_feel_the_added_mass(ratio, a_over_g):
    g = bowl_grid(24)
    body = VC.Body(disk(0.1), (0.5, 0.45), ratio * RHO)
    W = VC.Weights(g, bowl, body)
    VC.gravity(g, W, DT, G, body)
    S, _ = VC.project(g, DT, RHO, W, body)
    a = body.V[1] / DT / G
    assert abs(a - a_over_g) < 1e-4
    # a cylinder in unbounded still fluid: a = g (rho_s - rho) / (rho_s + rho)
    assert abs(a + (ratio - 1.0) / (ratio + 1.0)) < 0.02
    assert abs(body.V[0]) < 1e-12 and abs(body.V[2]) < 1e-12
    assert VC.mixed_divergence(S, g.u, g.v) < 1e-9


def small_system(with_air):
    n = 8
    g = macgrid.make_grid(n, n, 1.0 / n)
    if with_air:
        for i in range(n):
            g.label[i][n - 1] = AIR
    body = VC.Body(disk(0.2), (0.45, 0.5), 700.0, angle=0.0)
    W = VC.Weights(g, bowl, body)
    return VC.System(g, W, DT, RHO, body)


def cholesky_pivots(A):
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    piv = []
    for k in range(n):
        d = A[k][k] - sum(L[k][m] ** 2 for m in range(k))
        piv.append(d)
        if d <= 0.0:
            return piv
        L[k][k] = math.sqrt(d)
        for r in range(k + 1, n):
            L[r][k] = (A[r][k] - sum(L[r][m] * L[k][m] for m in range(k))) / L[k][k]
    return piv


def test_matrix_is_semidefinite_and_definite_with_air():
    S = small_system(False)
    A = VC.matrix(S)
    n = len(A)
    scale = max(abs(A[r][c]) for r in range(n) for c in range(n))
    assert max(abs(A[r][c] - A[c][r]) for r in range(n) for c in range(n)) < 1e-12 * scale
    assert max(abs(sum(row)) for row in A) < 1e-12 * scale  # constants are in the null space
    rng = random.Random(5)
    for _ in range(20):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        assert sum(x[r] * A[r][c] * x[c] for r in range(n) for c in range(n)) >= -1e-12 * scale
    S = small_system(True)
    assert min(cholesky_pivots(VC.matrix(S))) > 0.0


def test_pressure_minimizes_the_kinetic_energy():
    rng = random.Random(7)
    n = 12
    g = bowl_grid(n)
    body = VC.Body(disk(0.15), (0.45, 0.4), 500.0, V=(0.3, -0.2, 1.0))
    W = VC.Weights(g, bowl, body)
    g.u = [[rng.uniform(-1, 1) for j in range(n)] for i in range(n + 1)]
    g.v = [[rng.uniform(-1, 1) for j in range(n + 1)] for i in range(n)]
    u0, v0, V0 = macgrid.copy_field(g.u), macgrid.copy_field(g.v), list(body.V)
    S, _ = VC.project(g, DT, RHO, W, body)
    best = VC.energy_of_pressure(S, u0, v0, V0, S.p)
    assert abs(best - VC.kinetic_energy(S, g.u, g.v, body.V)) < 1e-9 * best
    assert best < VC.energy_of_pressure(S, u0, v0, V0, [0.0] * len(S.p))  # the projection never adds energy
    for _ in range(10):
        q = [p + rng.uniform(-50, 50) for p in S.p]
        assert VC.energy_of_pressure(S, u0, v0, V0, q) > best
    assert VC.mixed_divergence(S, g.u, g.v) < 1e-9


def test_scripted_body_pushes_the_fluid():
    g = bowl_grid(16)
    body = VC.Body(disk(0.12), (0.45, 0.4), 0.0, V=(0.5, 0.2, 2.0), scripted=True)
    W = VC.Weights(g, bowl, body)
    S, _ = VC.project(g, DT, RHO, W, body)
    assert body.V == [0.5, 0.2, 2.0]
    assert VC.mixed_divergence(S, g.u, g.v) < 1e-9
    assert max(abs(t) for c in g.u for t in c) > 0.1  # the fluid moves out of the way


def test_bad_input():
    with pytest.raises(ValueError):
        VC.Body(disk(0.1), (0.5, 0.5), 0.0)
    g = macgrid.make_grid(2, 2, 0.5)
    with pytest.raises(ValueError):
        VC.System(g, VC.binary_weights(g), 0.0, RHO)
