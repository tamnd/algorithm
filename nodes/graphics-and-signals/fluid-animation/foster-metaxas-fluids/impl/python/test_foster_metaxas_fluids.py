# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/foster-metaxas-fluids/. The authors are listed in prov/NBGCFG.jsonl.

"""Tests of the Foster-Metaxas liquid solver in 2D."""

import random

import macgrid
import foster_metaxas_fluids as fm
from foster_metaxas_fluids import EMPTY, FULL, SURFACE


def box(n, rows, seed=None, dx=None):
    """A liquid with one marker in each cell of the lowest rows rows; random inner velocities if seed is given."""
    dx = dx or 1.0 / n
    liq = fm.Liquid(n, n, dx, [((i + 0.5) * dx, (j + 0.5) * dx) for i in range(n) for j in range(rows)])
    if seed is not None:
        rng = random.Random(seed)
        g = liq.g
        for i in range(1, n):
            for j in range(n):
                g.u[i][j] = rng.uniform(-1.0, 1.0)
        for i in range(n):
            for j in range(1, n):
                g.v[i][j] = rng.uniform(-1.0, 1.0)
    return liq


def face_diff(a, b):
    return max(abs(x - y) for c1, c2 in zip(a, b) for x, y in zip(c1, c2))


def test_labels():
    liq = box(5, 3)
    assert [liq.cells[2][j] for j in range(5)] == [FULL, FULL, SURFACE, EMPTY, EMPTY]
    liq = fm.Liquid(4, 4, 0.25, [(0.6, 0.6)])
    assert liq.cells[2][2] == SURFACE and sum(c.count(EMPTY) for c in liq.cells) == 15


def test_one_cell_update_with_beta0_one_zeroes_its_divergence():
    liq = box(3, 3, seed=1)
    fm.relax_cell(liq, 1, 1, 0.02, 1.0)
    assert abs(fm.cell_divergence(liq, 1, 1)) < 1e-12
    liq = box(3, 3, seed=2)
    d0 = fm.cell_divergence(liq, 0, 1)  # 3 open faces: omega = 3/4
    fm.relax_cell(liq, 0, 1, 0.02, 1.0)
    assert abs(fm.cell_divergence(liq, 0, 1) - 0.25 * d0) < 1e-12


def test_each_cell_update_lowers_kinetic_energy_by_the_formula():
    liq = box(6, 6, seed=3)
    g = liq.g
    for (i, j) in [(i, j) for i in range(6) for j in range(6)] * 2:
        n = sum((i > 0, i < 5, j > 0, j < 5))
        f = g.dx * fm.cell_divergence(liq, i, j)
        w = 1.7 * n / 4.0
        e0 = fm.kinetic_energy(liq)
        fm.relax_cell(liq, i, j, 0.05, 1.7)
        de = fm.kinetic_energy(liq) - e0
        assert de <= 1e-15
        assert abs(de + f * f / (2.0 * n) * w * (2.0 - w)) < 1e-12


def test_pressure_iteration_gives_the_helper_projection_closed_box():
    liq = box(16, 16, seed=4)
    h = macgrid.make_grid(16, 16, 1.0 / 16.0)
    h.u, h.v = macgrid.copy_field(liq.g.u), macgrid.copy_field(liq.g.v)
    e0 = fm.kinetic_energy(liq)
    sweeps = fm.pressure_iteration(liq, 0.01, 1.7, 1e-10)
    macgrid.project(h, 0.01, 1.0)
    assert sweeps > 0 and fm.max_full_divergence(liq) < 1e-10
    assert face_diff(liq.g.u, h.u) < 1e-9 and face_diff(liq.g.v, h.v) < 1e-9
    assert fm.kinetic_energy(liq) <= e0


def test_pressure_iteration_with_a_free_surface_matches_helper():
    liq = box(10, 7, seed=5)
    h = macgrid.make_grid(10, 10, 0.1)
    h.u, h.v = macgrid.copy_field(liq.g.u), macgrid.copy_field(liq.g.v)
    for i in range(10):
        for j in range(10):
            h.label[i][j] = macgrid.FLUID if liq.cells[i][j] == FULL else macgrid.AIR
    fm.pressure_iteration(liq, 0.01, 1.7, 1e-10)
    macgrid.project(h, 0.01, 1.0)
    assert face_diff(liq.g.u, h.u) < 1e-9 and face_diff(liq.g.v, h.v) < 1e-9
    assert max(abs(liq.g.p[i][j] - h.p[i][j]) for i in range(10) for j in range(10)
               if liq.cells[i][j] == FULL) < 1e-8


def test_over_relaxation_needs_fewer_sweeps():
    counts = {}
    for b0 in (1.0, 1.5, 1.7, 1.9):
        counts[b0] = fm.pressure_iteration(box(16, 16, seed=1), 0.01, b0, 1e-4)
    assert counts == {1.0: 402, 1.5: 155, 1.7: 83, 1.9: 102}


def test_surface_rules_give_zero_divergence():
    rng = random.Random(6)
    for marks, cell in (
            ([(1.5, 0.5), (0.5, 0.5), (2.5, 0.5), (1.5, 1.5)], (1, 1)),  # top cell: three open faces
            ([(0.5, 0.5), (1.5, 0.5), (2.5, 0.5), (0.5, 1.5), (1.5, 1.5), (2.5, 1.5)], (1, 1)),  # one open face
            ([(0.5, 0.5), (1.5, 0.5), (0.5, 1.5), (1.5, 1.5)], (1, 1)),  # a corner: two open faces
            ([(0.5, 0.5), (0.5, 1.5), (0.5, 2.5), (1.5, 1.5), (2.5, 0.5), (2.5, 1.5), (2.5, 2.5)], (1, 1))):
        liq = fm.Liquid(4, 4, 1.0, marks)
        g = liq.g
        for i in range(1, 4):
            for j in range(4):
                g.u[i][j] = rng.uniform(-1.0, 1.0)
        for i in range(4):
            for j in range(1, 4):
                g.v[i][j] = rng.uniform(-1.0, 1.0)
        i, j = cell
        assert liq.cells[i][j] == SURFACE
        fm.surface_velocities(liq)
        n_open = sum(liq.cells[a][b] == EMPTY for (a, b) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)))
        if n_open != 3:
            assert abs(fm.cell_divergence(liq, i, j)) < 1e-12


def test_gravity_and_hydrostatic_rest():
    liq = box(6, 4)
    u, v = fm.tentative_velocity(liq, 0.01, 0.0, -9.81, 0.0)
    assert all(abs(v[i][j] + 0.0981) < 1e-15 for i in range(6) for j in range(1, 5))
    assert all(v[i][0] == 0.0 and v[i][6] == 0.0 and v[i][5] == 0.0 for i in range(6))
    for i in range(6):
        for j in range(3):
            liq.g.p[i][j] = 9.81 * (3 - j) * liq.g.dx
    u, v = fm.tentative_velocity(liq, 0.01, 0.0, -9.81, 0.0)
    assert max(abs(t) for col in u for t in col) < 1e-15
    assert max(abs(v[i][j]) for i in range(6) for j in range(4)) < 1e-15  # faces below the SURFACE row
    assert all(abs(v[i][4] + 0.0981) < 1e-15 for i in range(6))  # SURFACE to EMPTY: only gravity


def test_still_pool_stays_still():
    n, dx = 12, 1.0 / 12.0
    marks = [((i + 0.25 + 0.5 * a) * dx, (j + 0.25 + 0.5 * b) * dx)
             for i in range(n) for j in range(6) for a in range(2) for b in range(2)]
    liq = fm.Liquid(n, n, dx, marks)
    for _ in range(40):
        fm.step(liq, 0.005, eps=1e-8)
    assert max(abs(t) for col in liq.g.u + liq.g.v for t in col) < 1e-8
    assert max(abs(m[1] - o[1]) for m, o in zip(liq.markers, marks)) < 1e-9


def test_explicit_viscosity_has_a_step_limit():
    def grow(r):
        liq = box(10, 10)
        g = liq.g
        for i in range(1, 10):
            for j in range(10):
                g.u[i][j] = 1e-3 * (-1) ** (i + j)
        a0 = max(abs(t) for col in g.u for t in col)
        dt = 0.01
        nu = r * g.dx * g.dx / dt
        for _ in range(30):
            g.u, g.v = fm.tentative_velocity(liq, dt, 0.0, 0.0, nu)
        return max(abs(t) for col in g.u for t in col) / a0
    assert grow(0.2) < 0.01
    assert grow(0.25) < 1.0
    assert grow(0.3) > 100.0


def test_dam_break():
    n, dx, dt = 16, 0.05, 0.004
    marks = [((i + 0.25 + 0.5 * a) * dx, (j + 0.25 + 0.5 * b) * dx)
             for i in range(5) for j in range(10) for a in range(2) for b in range(2)]
    liq = fm.Liquid(n, n, dx, marks)
    front = []
    for k in range(60):
        fm.step(liq, dt)
        assert fm.max_full_divergence(liq) < 1e-4
        assert fm.cfl_number(liq, dt) < 1.0
        front.append(max(m[0] for m in liq.markers))
    assert len(liq.markers) == 200 and fm.isfinite_state(liq)
    assert all(0.0 < m[0] < 0.8 and 0.0 < m[1] < 0.8 for m in liq.markers)
    assert front[0] < front[29] < front[59]
    assert abs(front[59] - 0.661) < 0.001
