# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boussinesq-buoyancy/. The authors are listed in prov/QV9FZM.jsonl.

"""Tests of the buoyancy force on a small MAC grid."""

import math

import pytest

import macgrid
import boussinesq_buoyancy as B

NX, NY = 16, 24
DX = 1.0 / 16
TA = 300.0
BETA = B.ideal_gas_beta(9.81, TA)
DT = 0.05


def fields(Tf, sf=lambda x, y: 0.0):
    T = [[Tf((i + 0.5) * DX, (j + 0.5) * DX) for j in range(NY)] for i in range(NX)]
    s = [[sf((i + 0.5) * DX, (j + 0.5) * DX) for j in range(NY)] for i in range(NX)]
    return s, T


def blob(amp, cy=0.4):
    return lambda x, y: amp * math.exp(-((x - 0.5) ** 2 + (y - cy) ** 2) / (2 * 0.1 ** 2))


def kick(Tf, sf=lambda x, y: 0.0, alpha=0.0):
    """One buoyancy kick and one projection from rest."""
    g = macgrid.make_grid(NX, NY, DX)
    s, T = fields(Tf, sf)
    B.add_buoyancy(g, s, T, DT, alpha, BETA, TA)
    macgrid.project(g, DT, 1.0)
    return g


def test_force_is_zero_at_ambient_and_linear():
    assert B.buoyancy(0.0, TA, 0.7, BETA, TA) == 0.0
    assert B.buoyancy(0.0, 400.0, 0.7, BETA, TA) == pytest.approx(100.0 * BETA)
    assert B.buoyancy(2.0, TA, 0.7, BETA, TA) == pytest.approx(-1.4)
    a, b = (0.3, 350.0), (1.1, 420.0)
    f = lambda s, T: B.buoyancy(s, T, 0.7, BETA, TA)
    assert f(a[0] + b[0], a[1] + b[1] - TA) == pytest.approx(f(*a) + f(*b))


def test_ideal_gas_slope():
    assert BETA == pytest.approx(0.0327)
    # the linear force against g (rho_amb - rho) / rho_amb = g (T - T_amb) / T
    for T, ratio in ((303.0, 1.01), (330.0, 1.1), (600.0, 2.0), (2000.0, 20.0 / 3.0)):
        assert BETA * (T - TA) / B.ideal_gas_force(9.81, T, TA) == pytest.approx(ratio)


def test_uniform_heat_in_a_closed_box_does_not_move():
    g = kick(lambda x, y: 400.0)
    assert max(abs(t) for c in g.u + g.v for t in c) < 1e-12


def test_layers_in_a_closed_box_do_not_move():
    g = kick(lambda x, y: 300.0 + 100.0 * y)  # the force depends on the height only: a gradient
    assert max(abs(t) for c in g.u + g.v for t in c) < 1e-12
    g = kick(lambda x, y: 400.0 - 100.0 * y)  # hot below: unstable, but still at rest
    assert max(abs(t) for c in g.u + g.v for t in c) < 1e-12


def test_a_hot_blob_rises_and_the_rest_comes_down():
    g = kick(lambda x, y: TA + blob(300.0)(x, y))
    assert g.v[8][7] == pytest.approx(0.19822, abs=1e-5) and g.v[7][7] == g.v[8][7]
    assert g.v[0][7] < 0.0  # the return flow at the side walls
    assert max(abs(g.u[i][j] + g.u[NX - i][j]) for i in range(NX + 1) for j in range(NY)) < 1e-12  # mirror image
    for j in range(NY + 1):  # a closed box: no net flow through any horizontal line
        assert abs(sum(g.v[i][j] for i in range(NX))) < 1e-10
    assert macgrid.max_fluid_divergence(g) < 1e-10


def test_dense_smoke_sinks():
    g = kick(lambda x, y: TA, blob(1.0, 0.6), alpha=0.5)
    assert g.v[8][10] < 0.0 and g.v[0][10] > 0.0


def test_the_blob_rises_over_time():
    g = macgrid.make_grid(NX, NY, DX)
    s, T = fields(lambda x, y: TA + blob(300.0)(x, y))
    h0 = B.centroid_height(T, TA, DX)
    for _ in range(12):
        s, T = B.step(g, s, T, DT, 1.0, 0.0, BETA, TA)
    assert abs(h0 - 0.40001) < 1e-4
    assert abs(B.centroid_height(T, TA, DX) - 0.66560) < 1e-4
    assert abs(max(max(c) for c in T) - 440.712) < 1e-2  # the peak falls by numerical diffusion, not by the model
    assert macgrid.max_fluid_divergence(g) < 1e-9


def test_bad_input():
    g = macgrid.make_grid(2, 2, 0.5)
    z = macgrid.zeros(2, 2)
    with pytest.raises(ValueError):
        B.add_buoyancy(g, z, z, DT, -1.0, BETA, TA)
    with pytest.raises(ValueError):
        B.ideal_gas_beta(9.81, 0.0)
