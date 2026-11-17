# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mac-grid/. The authors are listed in prov/NKCN2S.jsonl.

"""Tests of the MAC grid page and of the shared helper macgrid.py."""

import random
from fractions import Fraction

import macgrid
from macgrid import AIR, FLUID, SOLID
from mac_grid import (
    divergence,
    gradient_update,
    nullity,
    periodic_collocated_laplacian,
    periodic_mac_laplacian,
    poisson_system,
    sample,
)


def random_grid(nx, ny, dx, seed):
    rng = random.Random(seed)
    g = macgrid.make_grid(nx, ny, dx)
    for col in g.u:
        for j in range(ny):
            col[j] = rng.uniform(-1.0, 1.0)
    for col in g.v:
        for j in range(ny + 1):
            col[j] = rng.uniform(-1.0, 1.0)
    return g, rng


def dense_solve(a, b):
    """Gaussian elimination with partial pivoting (works on floats and Fractions)."""
    n = len(b)
    m = [list(row) + [b[k]] for k, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    x = [0] * n
    for c in range(n - 1, -1, -1):
        x[c] = (m[c][n] - sum(m[c][k] * x[k] for k in range(c + 1, n))) / m[c][c]
    return x


# ---- the page: layout, sampling, divergence and the Poisson rows ----

def test_array_sizes():
    g = macgrid.make_grid(5, 3, 0.25)
    assert len(g.p) == 5 and len(g.p[0]) == 3
    assert len(g.u) == 6 and len(g.u[0]) == 3
    assert len(g.v) == 5 and len(g.v[0]) == 4
    assert macgrid.cell_center(g, 0, 0) == (0.125, 0.125)
    assert macgrid.cell_label(g, -1, 0) == SOLID and macgrid.cell_label(g, 0, 3) == SOLID


def test_sample_reproduces_affine_fields_exactly():
    dx = Fraction(1, 4)
    for ox, oy in ((0, Fraction(1, 2)), (Fraction(1, 2), 0), (Fraction(1, 2), Fraction(1, 2))):
        q = [[3 * (a + ox) * dx - 2 * (b + oy) * dx + 1 for b in range(5)] for a in range(6)]
        for (x, y) in ((Fraction(1, 3), Fraction(2, 5)), (Fraction(7, 8), Fraction(1, 2)), (Fraction(5, 7), Fraction(3, 4))):
            assert sample(q, x, y, dx, ox, oy) == 3 * x - 2 * y + 1


def test_sample_agrees_with_helper():
    g, rng = random_grid(6, 5, 0.2, 1)
    for _ in range(200):
        x, y = rng.uniform(-0.3, 1.5), rng.uniform(-0.3, 1.3)
        assert abs(sample(g.u, x, y, g.dx, 0.0, 0.5) - macgrid.u_at(g, x, y)) < 1e-14
        assert abs(sample(g.v, x, y, g.dx, 0.5, 0.0) - macgrid.v_at(g, x, y)) < 1e-14


def test_divergence_matches_helper_and_example():
    g, _ = random_grid(4, 4, 0.5, 2)
    d1 = divergence(g.u, g.v, g.dx)
    d2 = macgrid.divergence(g)
    assert all(abs(d1[i][j] - d2[i][j]) < 1e-14 for i in range(4) for j in range(4))
    u = [[Fraction(0)], [Fraction(1)], [Fraction(3)]]
    v = [[Fraction(0), Fraction(2)], [Fraction(1), Fraction(1)]]
    assert divergence(u, v, Fraction(1, 2)) == [[Fraction(6)], [Fraction(4)]]


def test_divergence_of_gradient_is_minus_poisson_matrix_exactly():
    rng = random.Random(3)
    nx, ny = 5, 4
    label = [[FLUID] * ny for _ in range(nx)]
    label[2][1] = SOLID
    label[0][3] = AIR
    label[4][3] = AIR
    dt, rho, dx = Fraction(1, 10), Fraction(1000), Fraction(1, 8)
    u = [[Fraction(0)] * ny for _ in range(nx + 1)]
    v = [[Fraction(0)] * (ny + 1) for _ in range(nx)]
    p = [[Fraction(rng.randint(-50, 50), 7) if label[i][j] == FLUID else Fraction(0) for j in range(ny)] for i in range(nx)]
    cells, a_mat, _ = poisson_system(u, v, label, dt, rho, dx)
    gradient_update(u, v, p, label, dt, rho, dx)
    d = divergence(u, v, dx)
    for k, (i, j) in enumerate(cells):
        ap = sum(a_mat[k][m] * p[c[0]][c[1]] for m, c in enumerate(cells))
        assert d[i][j] == dt / (rho * dx * dx) * ap


def test_poisson_matrix_is_symmetric_with_the_right_diagonal():
    label = [[FLUID, FLUID, AIR], [FLUID, SOLID, FLUID], [FLUID, FLUID, FLUID]]
    u = [[0] * 3 for _ in range(4)]
    v = [[0] * 4 for _ in range(3)]
    cells, a_mat, _ = poisson_system(u, v, label, 1, 1, 1)
    n = len(cells)
    assert all(a_mat[r][c] == a_mat[c][r] for r in range(n) for c in range(n))
    k = cells.index((0, 1))
    assert a_mat[k][k] == 2  # the wall on the left and the SOLID cell (1, 1) close two faces
    assert sum(a_mat[k]) == 1  # one FLUID neighbor, and the AIR neighbor adds only to the diagonal


def test_checkerboard_null_space():
    for n in (4, 6):
        assert nullity(periodic_mac_laplacian(n)) == 1
        assert nullity(periodic_collocated_laplacian(n)) == 4
    n = 4
    a = periodic_collocated_laplacian(n)
    check = [Fraction((-1) ** (i + j)) for i in range(n) for j in range(n)]
    assert all(sum(a[r][c] * check[c] for c in range(n * n)) == 0 for r in range(n * n))
    a = periodic_mac_laplacian(n)
    assert all(sum(a[r][c] * check[c] for c in range(n * n)) == -8 * check[r] for r in range(n * n))


# ---- the shared helper macgrid.py ----

def test_helper_project_box():
    g, _ = random_grid(16, 16, 1.0 / 16.0, 4)
    macgrid.set_solid_boundaries(g)
    e0 = macgrid.kinetic_energy(g, 1000.0)
    it = macgrid.project(g, 0.01, 1000.0)
    assert it > 0
    assert macgrid.max_fluid_divergence(g) < 1e-8
    assert macgrid.kinetic_energy(g, 1000.0) <= e0 * (1 + 1e-12)
    mean = sum(g.p[i][j] for i in range(16) for j in range(16)) / 256
    assert abs(mean) < 1e-9 * max(abs(g.p[i][j]) for i in range(16) for j in range(16))


def test_helper_project_32_grid():
    g, _ = random_grid(32, 32, 1.0 / 32.0, 5)
    e0 = macgrid.kinetic_energy(g, 1000.0)
    macgrid.project(g, 1.0 / 60.0, 1000.0)
    assert macgrid.max_fluid_divergence(g) < 1e-8
    assert macgrid.kinetic_energy(g, 1000.0) <= e0


def test_helper_project_with_air_and_solid():
    g, _ = random_grid(10, 10, 0.1, 6)
    for i in range(10):
        for j in range(7, 10):
            g.label[i][j] = AIR
    g.label[4][2] = SOLID
    g.label[5][2] = SOLID
    macgrid.set_solid_boundaries(g)
    e0 = macgrid.kinetic_energy(g, 1.0)
    macgrid.project(g, 0.05, 1.0)
    assert macgrid.max_fluid_divergence(g) < 1e-8
    assert macgrid.kinetic_energy(g, 1.0) <= e0 * (1 + 1e-12)
    assert all(g.p[i][j] == 0.0 for i in range(10) for j in range(7, 10))
    assert g.u[5][2] == 0.0 and g.u[4][2] == 0.0 and g.v[4][2] == 0.0


def test_helper_pressure_matches_dense_solve():
    g, _ = random_grid(5, 4, 0.25, 7)
    for i in range(5):
        g.label[i][3] = AIR
    g.label[2][1] = SOLID
    macgrid.set_solid_boundaries(g)
    cells, a_mat, b = poisson_system(g.u, g.v, g.label, 0.1, 2.0, g.dx)
    x = dense_solve(a_mat, b)
    macgrid.pressure_solve(g, 0.1, 2.0)
    assert all(abs(g.p[i][j] - x[k]) < 1e-9 * (1 + abs(x[k])) for k, (i, j) in enumerate(cells))


def test_helper_two_closed_components():
    g, _ = random_grid(6, 4, 0.5, 8)
    for j in range(4):
        g.label[3][j] = SOLID
    macgrid.project(g, 0.1, 1.0)
    assert macgrid.max_fluid_divergence(g) < 1e-8
    for rng_i in (range(0, 3), range(4, 6)):
        cells = [(i, j) for i in rng_i for j in range(4)]
        assert abs(sum(g.p[i][j] for (i, j) in cells)) < 1e-9


def test_helper_moving_solid_velocity():
    g = macgrid.make_grid(6, 6, 0.5)
    g.label[2][2] = SOLID
    macgrid.set_solid_boundaries(g, lambda x, y: (1.0, -2.0))
    assert g.u[2][2] == 1.0 and g.u[3][2] == 1.0 and g.v[2][2] == -2.0 and g.v[2][3] == -2.0
    assert g.u[0][2] == 0.0 and g.v[2][0] == 0.0
    macgrid.project(g, 0.1, 1.0, solid_velocity=lambda x, y: (1.0, -2.0))
    assert macgrid.max_fluid_divergence(g) < 1e-8


def test_helper_advect_constant_and_maximum_principle():
    g, rng = random_grid(12, 12, 1.0 / 12.0, 9)
    macgrid.project(g, 0.1, 1.0)
    const = [[2.5] * 12 for _ in range(12)]
    out = macgrid.advect(g, const, 0.3)
    assert all(abs(t - 2.5) < 1e-14 for col in out for t in col)
    q = [[rng.uniform(0.0, 1.0) for _ in range(12)] for _ in range(12)]
    dt = 0.4
    out = macgrid.advect(g, q, dt)
    dx = g.dx
    for a in range(12):
        for b in range(12):
            xb, yb = macgrid.backtrace(g, (a + 0.5) * dx, (b + 0.5) * dx, dt)
            fx = min(max(xb / dx - 0.5, 0.0), 11.0)
            fy = min(max(yb / dx - 0.5, 0.0), 11.0)
            i0, j0 = min(int(fx), 10), min(int(fy), 10)
            st = [q[i0][j0], q[i0 + 1][j0], q[i0][j0 + 1], q[i0 + 1][j0 + 1]]
            assert min(st) - 1e-14 <= out[a][b] <= max(st) + 1e-14


def test_helper_advect_uniform_flow_shifts_linear_field():
    g = macgrid.make_grid(10, 10, 0.1)
    for col in g.u:
        for j in range(10):
            col[j] = 0.5
    q = [[(a + 0.5) * 0.1 for b in range(10)] for a in range(10)]
    out = macgrid.advect(g, q, 0.2)
    for a in range(2, 10):
        assert abs(out[a][4] - (q[a][4] - 0.1)) < 1e-12
    nu, nv = macgrid.advect_velocity(g, 0.2)
    assert all(abs(t - 0.5) < 1e-14 for col in nu for t in col)
    assert all(t == 0.0 for col in nv for t in col)
