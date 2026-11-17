# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fire-simulation/. The authors are listed in prov/QHWFYD.jsonl.

"""Tests of the thin flame fire model on the MAC grid of macgrid.py."""

import math
import random
from fractions import Fraction as Fr

import pytest

import macgrid
from macgrid import AIR, SOLID
import fire_simulation as F

DX = 0.05


def planar(orientation, init="steady"):
    """A planar flame in a channel: fuel enters at 0.5 m/s through an injector and the products leave through AIR cells.

    orientation is "right" (fuel moves in +x), "left" (in -x) or "up" (in +y).
    The front is at 6.75 cells from the injector side. With init "steady" the
    velocity is the steady solution; with "uniform" it is 0.5 m/s everywhere.
    """
    long_, short = 16, 3
    up = orientation == "up"
    nx, ny = (short, long_) if up else (long_, short)
    g = macgrid.make_grid(nx, ny, DX)
    sgn = -1.0 if orientation == "left" else 1.0
    pos = (lambda i, j: (j + 0.5) * DX) if up else (
        (lambda i, j: (i + 0.5) * DX) if sgn > 0 else (lambda i, j: (nx - i - 0.5) * DX))
    for i in range(nx):
        for j in range(ny):
            k = j if up else (i if sgn > 0 else nx - 1 - i)
            if k == 0:
                g.label[i][j] = SOLID
            elif k == long_ - 1:
                g.label[i][j] = AIR
    x0 = 6.75 * DX
    phi = [[x0 - pos(i, j) for j in range(ny)] for i in range(nx)]
    st = F.Fire(g, phi, alpha=0.0)
    S, J = st.S, st.J()
    if up:
        for i in range(nx):
            for j in range(ny + 1):
                g.v[i][j] = S if init == "uniform" or j * DX < x0 else S + J
        inj = (lambda x, y: (0.0, S))
    else:
        for i in range(nx + 1):
            for j in range(ny):
                d = i * DX if sgn > 0 else (nx - i) * DX
                g.u[i][j] = sgn * (S if init == "uniform" or d < x0 else S + J)
        inj = (lambda x, y: (sgn * S, 0.0))
    return st, inj


def line(st, orientation, field):
    """The values of a face field (u, v) or a cell field along the channel, from the injector side."""
    g = st.g
    if field == "p":
        q = g.p
        if orientation == "up":
            return [q[1][j] for j in range(g.ny)]
        r = [q[i][1] for i in range(g.nx)]
        return r if orientation == "right" else r[::-1]
    if orientation == "up":
        return [g.v[1][j] for j in range(g.ny + 1)]
    r = [g.u[i][1] for i in range(g.nx + 1)]
    return r if orientation == "right" else [-t for t in r[::-1]]


def test_jump_conditions_are_exact():
    rho_f, rho_h, S, V_f, p_f = Fr(1), Fr(1, 5), Fr(1, 2), Fr(3, 2), Fr(7)
    D, V_h, p_h = F.jump_conditions(rho_f, rho_h, S, V_f, p_f)
    assert rho_h * (V_h - D) == rho_f * (V_f - D)  # mass, equation 2
    assert rho_h * (V_h - D) ** 2 + p_h == rho_f * (V_f - D) ** 2 + p_f  # momentum, equation 3
    assert (D, V_h, p_h) == (Fr(1), Fr(7, 2), Fr(6))
    assert F.jump_conditions(rho_f, rho_f, S, V_f, p_f) == (Fr(1), V_f, p_f)
    rho_s, V_s = Fr(500), Fr(0)
    V_g = F.solid_fuel_velocity(V_s, rho_s, rho_f, S)
    D_s = V_s - S
    assert rho_f * (V_g - D_s) == rho_s * (V_s - D_s)  # equation 4
    assert V_g == Fr(499, 2)


def test_ghost_velocity_round_trip():
    rng = random.Random(3)
    for _ in range(20):
        a = rng.uniform(0.0, 2.0 * math.pi)
        m = (math.cos(a), math.sin(a))
        u = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        h = F.ghost_velocity(u, m, 2.0, True)
        back = F.ghost_velocity(h, m, 2.0, False)
        assert max(abs(x - y) for x, y in zip(back, u)) < 1e-14
        dn = (h[0] - u[0]) * m[0] + (h[1] - u[1]) * m[1]
        dt_ = (h[0] - u[0]) * -m[1] + (h[1] - u[1]) * m[0]
        assert abs(dn - 2.0) < 1e-14 and abs(dt_) < 1e-14


def test_planar_front_in_still_fuel_moves_at_flame_speed():
    g = macgrid.make_grid(12, 3, DX)
    phi = [[0.4 - (i + 0.5) * DX for j in range(3)] for i in range(12)]
    st = F.Fire(g, phi, rho_h=1.0, S=0.5)
    for _ in range(10):
        F.level_set_step(st, 0.01)
    assert max(abs(st.phi[i][j] - (0.35 - (i + 0.5) * DX)) for i in range(12) for j in range(3)) < 1e-12


def disk_error(n):
    dx = 1.0 / n
    g = macgrid.make_grid(n, n, dx)
    phi = [[0.35 - math.hypot((i + 0.5) * dx - 0.5, (j + 0.5) * dx - 0.5) for j in range(n)] for i in range(n)]
    st = F.Fire(g, phi, rho_h=1.0, S=0.5)
    for _ in range(6):
        F.level_set_step(st, 0.05)
    j = n // 2
    row = [st.phi[i][j] for i in range(n)]
    i = max(k for k in range(n - 1) if row[k] > 0.0 >= row[k + 1])
    xc = (i + 0.5 + row[i] / (row[i] - row[i + 1])) * dx
    return math.hypot(xc - 0.5, (j + 0.5) * dx - 0.5) - 0.2


def test_burning_disk_shrinks_at_flame_speed():
    e16, e32 = disk_error(16), disk_error(32)
    assert abs(e16 + 0.00346) < 1e-4 and abs(e32 + 0.00080) < 1e-4
    assert abs(e32) < abs(e16) / 2.0


@pytest.mark.parametrize("orientation", ["right", "left", "up"])
def test_steady_planar_flame_is_kept_exactly(orientation):
    st, inj = planar(orientation)
    phi0 = macgrid.copy_field(st.phi)
    for _ in range(3):
        F.step(st, 0.02, inj)
    vel = line(st, orientation, "u")
    assert all(abs(t - 0.5) < 1e-10 for t in vel[1:7])  # fuel
    assert all(abs(t - 2.5) < 1e-10 for t in vel[7:-1])  # products, 0.5 + (1 / 0.2 - 1) 0.5
    p = line(st, orientation, "p")
    assert all(abs(t - 1.0) < 1e-9 for t in p[1:7])  # p_f - p_h = (1 / 0.2 - 1) 1 0.5^2
    assert all(abs(t) < 1e-9 for t in p[7:])
    assert max(abs(a - b) for c1, c2 in zip(st.phi, phi0) for a, b in zip(c1, c2)) < 1e-12
    assert F.max_jump_divergence(st) < 1e-10


def test_expansion_accelerates_the_products():
    st, inj = planar("right", "uniform")
    F.step(st, 0.02, inj)
    vel = line(st, "right", "u")
    assert all(abs(t - 0.5) < 1e-10 for t in vel[1:7])
    assert all(abs(t - 2.5) < 1e-10 for t in vel[7:-1])
    assert abs(line(st, "right", "p")[1] - 9.72) < 1e-9  # includes the impulse that accelerates the products


def test_cooling_is_integrated_exactly():
    g = macgrid.make_grid(2, 2, DX)
    st = F.Fire(g, [[-1.0, -1.0], [-1.0, -1.0]])
    T = 1900.0
    one = F.cool(st, T, 0.02)
    two = F.cool(st, F.cool(st, T, 0.01), 0.01)
    assert abs(one - two) < 1e-9
    th0 = (T - 300.0) / 1700.0
    th = (th0 ** -3 + 3.0 * 3000.0 * 0.02 / 1700.0) ** (-1.0 / 3.0)
    assert abs(one - (300.0 + 1700.0 * th)) < 1e-9
    y, n = T, 20000
    for _ in range(n):
        y -= 0.02 / n * 3000.0 * ((y - 300.0) / 1700.0) ** 4
    assert abs(one - y) < 1e-3
    assert F.cool(st, 300.0, 1.0) == 300.0 and F.cool(st, 250.0, 1.0) == 250.0


def test_buoyancy_force():
    g = macgrid.make_grid(3, 4, DX)
    st = F.Fire(g, [[-1.0] * 4 for _ in range(3)], alpha=0.15)
    st.T = [[300.0 + 100.0 * (i + j) for j in range(4)] for i in range(3)]
    F.add_buoyancy(st, 0.1)
    for i in range(3):
        assert g.v[i][0] == 0.0 and g.v[i][4] == 0.0
        for j in range(1, 4):
            assert abs(g.v[i][j] - 0.1 * 0.15 * 100.0 * (i + j - 0.5)) < 1e-12


def plume(S, steps=25):
    nx, ny = 12, 16
    c = nx * DX / 2.0
    g = macgrid.make_grid(nx, ny, DX)
    for i in range(nx):
        g.label[i][0] = SOLID
        g.label[i][ny - 1] = AIR
    phi = [[min(0.1 - abs((i + 0.5) * DX - c), 0.1 - (j + 0.5) * DX) for j in range(ny)] for i in range(nx)]
    st = F.Fire(g, phi, S=S, alpha=0.0)
    inj = (lambda x, y: (0.0, 1.5 if abs(x - c) < 0.1 else 0.0))
    for _ in range(steps):
        F.step(st, 0.02, inj)
    col = [st.phi[nx // 2][j] for j in range(ny)]
    top = max(j for j in range(ny) if col[j] > 0.0)
    return st, (top + 0.5 + col[top] / (col[top] - col[top + 1])) * DX - DX


def test_nozzle_flame():
    st, h = plume(0.5)
    assert abs(h - 0.1761) < 1e-3  # height of the blue core above the nozzle, in m
    assert F.max_jump_divergence(st) < 1e-8
    Ts = [st.T[i][j] for i in range(st.g.nx) for j in range(1, st.g.ny)]
    assert st.T_air <= min(Ts) and max(Ts) <= st.T_max
    _, h_fast = plume(0.75)
    assert h_fast < h / 4.0  # a faster flame speed gives a smaller core


def test_bad_constants():
    g = macgrid.make_grid(2, 2, DX)
    with pytest.raises(ValueError):
        F.Fire(g, [[1.0, 1.0], [1.0, 1.0]], rho_f=0.1, rho_h=0.2)
