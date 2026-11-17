# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stable-fluids/. The authors are listed in prov/4DDRB0.jsonl.

"""Tests of the stable fluids step and of its parts against the shared helper."""

import math
import random

import macgrid
from macgrid import AIR, SOLID
import stable_fluids as sf


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


def copy_grid(g):
    h = macgrid.make_grid(g.nx, g.ny, g.dx)
    h.u = macgrid.copy_field(g.u)
    h.v = macgrid.copy_field(g.v)
    h.label = [list(col) for col in g.label]
    return h


def dense_solve(a, b):
    n = len(b)
    m = [list(row) + [b[k]] for k, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    x = [0.0] * n
    for c in range(n - 1, -1, -1):
        x[c] = (m[c][n] - sum(m[c][k] * x[k] for k in range(c + 1, n))) / m[c][c]
    return x


def max_abs(*fields):
    return max(abs(t) for q in fields for col in q for t in col)


# ---- the parts against the helper ----

def test_interp_and_advect_match_helper():
    g, rng = random_grid(10, 8, 0.125, 1)
    macgrid.project(g, 0.1, 1.0)
    for _ in range(200):
        x, y = rng.uniform(-0.2, 1.4), rng.uniform(-0.2, 1.2)
        assert abs(sf.velocity(g, x, y)[0] - macgrid.u_at(g, x, y)) < 1e-14
        assert abs(sf.velocity(g, x, y)[1] - macgrid.v_at(g, x, y)) < 1e-14
        assert sf.trace_back(g, x, y, 0.3) == macgrid.backtrace(g, x, y, 0.3)
    q = [[rng.uniform(0.0, 2.0) for _ in range(8)] for _ in range(10)]
    a1, a2 = sf.advect(g, q, 0.4), macgrid.advect(g, q, 0.4)
    assert max(abs(a1[i][j] - a2[i][j]) for i in range(10) for j in range(8)) < 1e-14
    u1, v1 = sf.advect_velocity(g, 0.4)
    u2, v2 = macgrid.advect_velocity(g, 0.4)
    assert u1 == u2 and v1 == v2


def test_project_matches_helper_with_air_and_solid():
    g, _ = random_grid(12, 10, 0.1, 2)
    for i in range(12):
        for j in range(7, 10):
            g.label[i][j] = AIR
    g.label[5][3] = SOLID
    g.label[6][3] = SOLID
    h = copy_grid(g)
    sf.project(g, 0.05, 1000.0)
    macgrid.project(h, 0.05, 1000.0)
    pmax = max_abs(h.p)
    assert max(abs(g.p[i][j] - h.p[i][j]) for i in range(12) for j in range(10)) < 1e-9 * pmax
    assert max(abs(g.u[i][j] - h.u[i][j]) for i in range(13) for j in range(10)) < 1e-9
    assert max(abs(g.v[i][j] - h.v[i][j]) for i in range(12) for j in range(11)) < 1e-9
    assert macgrid.max_fluid_divergence(g) < 1e-8


def test_project_closed_box_32():
    g, _ = random_grid(32, 32, 1.0 / 32.0, 3)
    sf.set_walls(g)
    e0 = macgrid.kinetic_energy(g, 1000.0)
    it = sf.project(g, 1.0 / 60.0, 1000.0)
    assert it > 0
    assert macgrid.max_fluid_divergence(g) < 1e-8
    assert macgrid.kinetic_energy(g, 1000.0) <= e0
    assert abs(sum(map(sum, g.p))) < 1e-9 * 1024 * max_abs(g.p)


# ---- diffusion ----

def test_diffuse_matches_dense_solve_and_keeps_sum_and_bounds():
    rng = random.Random(4)
    na, nb, alpha = 5, 4, 2.5
    q = [[rng.uniform(-1.0, 3.0) for _ in range(nb)] for _ in range(na)]
    w, it = sf.diffuse(q, alpha)
    assert it > 0
    n = na * nb
    a = [[0.0] * n for _ in range(n)]
    for i in range(na):
        for j in range(nb):
            k = i * nb + j
            a[k][k] = 1.0
            for (i2, j2) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if 0 <= i2 < na and 0 <= j2 < nb:
                    a[k][k] += alpha
                    a[k][i2 * nb + j2] -= alpha
    x = dense_solve(a, [q[i][j] for i in range(na) for j in range(nb)])
    assert max(abs(w[i][j] - x[i * nb + j]) for i in range(na) for j in range(nb)) < 1e-10
    assert abs(sum(map(sum, w)) - sum(map(sum, q))) < 1e-10
    lo, hi = min(map(min, q)), max(map(max, q))
    assert all(lo - 1e-12 <= t <= hi + 1e-12 for col in w for t in col)
    assert sum(t * t for col in w for t in col) <= sum(t * t for col in q for t in col)


def test_diffuse_large_step_is_bounded_and_flattens():
    q = [[1.0 if (i + j) % 2 == 0 else 0.0 for j in range(8)] for i in range(8)]
    w, _ = sf.diffuse(q, 1000.0)
    assert all(abs(t - 0.5) < 1e-3 for col in w for t in col)
    w0, it = sf.diffuse(q, 0.0)
    assert w0 == q and it == 0


# ---- advection order and stability ----

def bump_error(nx, cfl=2.5, x0=0.34375, dist=0.3125, sigma=0.1):
    """Max error after moving a Gaussian bump by dist with u = 1, at the CFL number cfl."""
    g = macgrid.make_grid(nx, 2, 1.0 / nx)
    for col in g.u:
        col[0] = col[1] = 1.0

    def f(x):
        return math.exp(-(x - x0) ** 2 / (2.0 * sigma * sigma))

    s = [[f((a + 0.5) * g.dx)] * 2 for a in range(nx)]
    steps = round(dist / (cfl * g.dx))
    for _ in range(steps):
        s = sf.advect(g, s, dist / steps)
    return max(abs(s[a][0] - f((a + 0.5) * g.dx - dist)) for a in range(nx))


def test_advection_is_first_order_at_fixed_cfl():
    e8, e16, e32 = bump_error(8), bump_error(16), bump_error(32)
    assert e8 > e16 > e32
    order = math.log2(e16 / e32)
    assert 0.8 < order < 1.2
    assert 0.04 < e32 < 0.05


def test_constant_field_and_maximum_principle():
    g, rng = random_grid(12, 12, 1.0 / 12.0, 5)
    sf.project(g, 0.1, 1.0)
    const = [[2.5] * 12 for _ in range(12)]
    assert all(abs(t - 2.5) < 1e-14 for col in sf.advect(g, const, 0.7) for t in col)
    q = [[rng.uniform(0.0, 1.0) for _ in range(12)] for _ in range(12)]
    out = sf.advect(g, q, 0.7)
    assert 0.0 <= min(map(min, out)) and max(map(max, out)) <= 1.0


def test_large_step_stays_bounded():
    g, _ = random_grid(16, 16, 1.0 / 16.0, 11)
    sf.project(g, 0.01, 1.0)
    umax = max_abs(g.u, g.v)
    dt = 5.0 * g.dx / umax
    s = [[1.0 if 4 <= a < 8 and 4 <= b < 8 else 0.0 for b in range(16)] for a in range(16)]
    e = [macgrid.kinetic_energy(g, 1.0)]
    for _ in range(10):
        s = sf.step(g, dt, 1.0, scalars=[s])[0]
        e.append(macgrid.kinetic_energy(g, 1.0))
        assert macgrid.max_fluid_divergence(g) < 1e-8
    assert all(math.isfinite(t) for t in e)
    assert all(e[k + 1] <= e[k] for k in range(10))
    assert e[10] < 0.02 * e[0]
    assert 0.0 <= min(map(min, s)) and max(map(max, s)) <= 1.0


# ---- the full step ----

def test_step_with_force_viscosity_and_decay():
    g = macgrid.make_grid(12, 12, 1.0 / 12.0)
    s = [[1.0 if 5 <= a < 7 and 1 <= b < 3 else 0.0 for b in range(12)] for a in range(12)]

    def lift(x, y):
        return (0.0, 4.0 if 0.4 < x < 0.6 and y < 0.4 else 0.0)

    for _ in range(5):
        s = sf.step(g, 0.02, 1.0, nu=1e-3, force=lift, scalars=[s], kappa=1e-4, decay=0.5)[0]
        assert macgrid.max_fluid_divergence(g) < 1e-8
    assert max_abs(g.v) > 0.0
    assert all(t == 0.0 for t in g.v[3][:1] + g.v[3][12:])
    assert 0.0 <= min(map(min, s)) and max(map(max, s)) <= 1.0
    s1 = sf.step(macgrid.make_grid(4, 4, 0.25), 0.1, 1.0, scalars=[[[1.0] * 4 for _ in range(4)]], decay=2.0)[0]
    assert all(abs(t - 1.0 / 1.2) < 1e-15 for col in s1 for t in col)
