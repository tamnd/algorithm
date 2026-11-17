# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vorticity-confinement/. The authors are listed in prov/8A418J.jsonl.

"""Tests of vorticity confinement on a small MAC grid."""

import math

import pytest

import macgrid
import vorticity_confinement as V

N = 20
DX = 1.0 / N


def grid_with(vel, project=False):
    g = macgrid.make_grid(N, N, DX)
    V.set_velocity(g, vel)
    if project:
        macgrid.project(g, 0.01, 1.0)
    return g


def rotation(x, y):
    return (-(y - 0.5), x - 0.5)  # solid body rotation, vorticity 2


VORTEX = V.gaussian_vortex(0.5, 0.5, 0.12, 0.06)


def test_vorticity_of_a_solid_rotation_is_two():
    w = V.vorticity(grid_with(rotation))
    assert max(abs(t - 2.0) for c in w for t in c) < 1e-12


def test_no_force_for_uniform_flow_or_solid_rotation():
    fx, fy = V.confinement_force(grid_with(lambda x, y: (0.3, -0.2)), 0.5)
    assert max(abs(t) for c in fx + fy for t in c) == 0.0
    fx, fy = V.confinement_force(grid_with(rotation), 0.5)
    assert max(abs(t) for c in fx + fy for t in c) < 1e-9


def test_without_delta_rounding_noise_gives_a_full_force():
    fx, fy = V.confinement_force(grid_with(rotation), 0.3, delta=0.0)
    big = max(math.hypot(fx[i][j], fy[i][j]) for i in range(N) for j in range(N))
    assert big == pytest.approx(0.3 * DX * 2.0, rel=1e-9)  # eps dx |w| from a direction that is only noise


def test_force_is_perpendicular_to_n_and_has_size_eps_dx_w():
    g = grid_with(VORTEX)
    w = V.vorticity(g)
    fx, fy = V.confinement_force(g, 0.5)
    a = [[abs(t) for t in c] for c in w]
    checked = 0
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            ex = (a[i + 1][j] - a[i - 1][j]) / (2 * DX)
            ey = (a[i][j + 1] - a[i][j - 1]) / (2 * DX)
            if math.hypot(ex, ey) < 0.05 * max(map(max, a)) / DX:  # far from the peak, where delta does not matter
                continue
            checked += 1
            assert abs(fx[i][j] * ex + fy[i][j] * ey) < 1e-12 * math.hypot(ex, ey)
            assert math.hypot(fx[i][j], fy[i][j]) == pytest.approx(0.5 * DX * abs(w[i][j]), rel=1e-4)
    assert checked > 50


def test_force_pushes_along_the_flow_of_a_vortex():
    g = grid_with(VORTEX, project=True)
    fx, fy = V.confinement_force(g, 0.5)
    uc, vc = V.center_velocity(g)
    for i in (11, 12):  # right of the center (0.5, 0.5), inside the core: w > 0 and the flow goes up
        j = 10
        assert vc[i][j] > 0.0 and fy[i][j] > 0.0 and fx[i][j] * uc[i][j] + fy[i][j] * vc[i][j] > 0.0
    w = V.vorticity(g)
    assert w[13][10] < 0.0 and fy[13][10] < 0.0  # the ring of opposite vorticity around a Gaussian vortex
    assert sum(fx[i][j] * uc[i][j] + fy[i][j] * vc[i][j] for i in range(N) for j in range(N)) > 0.0
    e0 = macgrid.kinetic_energy(g, 1.0)
    V.add_confinement(g, 0.5, 0.05)
    assert macgrid.kinetic_energy(g, 1.0) > e0  # the force adds energy


def test_force_is_linear_in_eps_and_zero_for_eps_zero():
    g = grid_with(VORTEX)
    f1 = V.confinement_force(g, 0.25)
    f2 = V.confinement_force(g, 0.5)
    for a, b in zip(f1, f2):
        assert max(abs(2.0 * s - t) for c1, c2 in zip(a, b) for s, t in zip(c1, c2)) < 1e-15
    u0, v0 = macgrid.copy_field(g.u), macgrid.copy_field(g.v)
    V.add_confinement(g, 0.0, 0.05)
    assert g.u == u0 and g.v == v0


def test_walls_get_no_force():
    g = grid_with(VORTEX)
    g.label[10][10] = macgrid.SOLID
    V.add_confinement(g, 1.0, 0.05)
    assert all(g.u[0][j] == VORTEX(0.0, (j + 0.5) * DX)[0] for j in range(N))
    assert g.u[10][10] == VORTEX(10 * DX, 10.5 * DX)[0] and g.v[10][11] == VORTEX(10.5 * DX, 11 * DX)[1]


def decay(eps, steps=10):
    g = grid_with(VORTEX, project=True)
    e0 = macgrid.kinetic_energy(g, 1.0)
    for _ in range(steps):
        V.step(g, 0.05, 1.0, eps)
    assert macgrid.max_fluid_divergence(g) < 1e-9
    return macgrid.kinetic_energy(g, 1.0) / e0


def test_confinement_slows_the_numerical_decay_and_too_much_adds_energy():
    r0, r1, r3 = decay(0.0), decay(1.0), decay(3.0)
    assert abs(r0 - 0.64968) < 1e-4  # semi-Lagrangian advection loses a third of the energy in 10 steps
    assert abs(r1 - 0.79221) < 1e-4
    assert r3 > 1.1  # eps = 3 ends with more energy than the start


def test_bad_input():
    with pytest.raises(ValueError):
        V.confinement_force(grid_with(VORTEX), -1.0)
