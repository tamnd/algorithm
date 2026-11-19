# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chorin-projection-method/. The authors are listed in prov/MYD986.jsonl.

import math
import random
from fractions import Fraction as Fr

import scisparse as sp
from chorin_projection_method import Grid, chorin, divergence, max_err, project, taylor_green


# ---------------------------------------------------------------- the projection method


def test_projection_hand_example():
    # 4 by 1 periodic cells, dx = dy = 1, dt = 1, u* = (1, 0, 0, 0): the projection keeps the mean 1/4
    g = Grid(4, 1, 4.0, 1.0)
    u, v, p, _ = project(g, [1.0, 0.0, 0.0, 0.0], [0.0] * 4, 1.0)
    assert max(abs(x - 0.25) for x in u) < 1e-12
    assert max(abs(p[k] - q) for k, q in enumerate([0.375, 0.125, -0.125, -0.375])) < 1e-12


def test_projection_is_an_orthogonal_projector():
    rng = random.Random(3)
    g = Grid(6, 5, 1.0, 1.0)
    us = [rng.uniform(-1, 1) for _ in range(30)]
    vs = [rng.uniform(-1, 1) for _ in range(30)]
    u, v, _, _ = project(g, us, vs, 0.5)
    assert max(abs(x) for x in divergence(g, u, v)) < 1e-10
    u2, v2, _, _ = project(g, u, v, 0.5)
    assert max_err(u, u2) < 1e-10 and max_err(v, v2) < 1e-10
    inner = sum((us[k] - u[k]) * u[k] + (vs[k] - v[k]) * v[k] for k in range(30))
    assert abs(inner) < 1e-10


def test_taylor_green_space_order_and_divergence():
    nu, T = 0.1, 0.5
    errs = []
    for n in (8, 16, 32):
        g = Grid(n, n)
        u, v, _ = taylor_green(g, nu, 0.0)
        steps = max(1, round(T / (0.4 * g.dx**2)))  # dt proportional to dx^2
        u, v, p, _ = chorin(g, u, v, T / steps, nu, steps)
        assert max(abs(x) for x in divergence(g, u, v)) < 1e-10
        ue, ve, _ = taylor_green(g, nu, T)
        errs.append(max(max_err(u, ue), max_err(v, ve)))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(2)]
    assert all(abs(q - 2) < 0.2 for q in orders), orders
    assert abs(errs[0] - 2.266e-3) < 1e-5  # N = 8: 2 steps of dt = 0.25


def test_taylor_green_time_order():
    nu, T = 0.1, 1.0
    g = Grid(16, 16)
    runs = []
    for steps in (10, 20, 40):
        u, v, _ = taylor_green(g, nu, 0.0)
        u, v, _, _ = chorin(g, u, v, T / steps, nu, steps)
        runs.append((u, v))
    d1 = max(max_err(runs[0][0], runs[1][0]), max_err(runs[0][1], runs[1][1]))
    d2 = max(max_err(runs[1][0], runs[2][0]), max_err(runs[1][1], runs[2][1]))
    assert abs(math.log2(d1 / d2) - 1) < 0.2


# ---------------------------------------------------------------- the shared helper scisparse


def test_thomas_hand_system():
    # tridiag(-1, 2, -1) x = (1, 0, 0, 1) has the solution x = (1, 1, 1, 1)
    a = [Fr(0), Fr(-1), Fr(-1), Fr(-1)]
    b = [Fr(2)] * 4
    c = [Fr(-1), Fr(-1), Fr(-1), Fr(0)]
    assert sp.thomas(a, b, c, [Fr(1), Fr(0), Fr(0), Fr(1)]) == [1, 1, 1, 1]


def test_thomas_periodic_hand_system():
    # cyclic tridiag(-1, 3, -1); for x = (1, 2, 3, 4) the right side is (-3, 2, 3, 8)
    a = [Fr(-1)] * 4
    b = [Fr(3)] * 4
    c = [Fr(-1)] * 4
    assert sp.thomas_periodic(a, b, c, [Fr(-3), Fr(2), Fr(3), Fr(8)]) == [1, 2, 3, 4]


def test_thomas_random_exact_residual():
    rng = random.Random(7)
    for n in (1, 2, 5, 9):
        a = [Fr(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(n)]
        c = [Fr(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(n)]
        b = [abs(a[i]) + abs(c[i]) + Fr(1, rng.randint(1, 5)) for i in range(n)]
        d = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        x = sp.thomas(a, b, c, d)
        for i in range(n):
            s = b[i] * x[i]
            if i > 0:
                s += a[i] * x[i - 1]
            if i < n - 1:
                s += c[i] * x[i + 1]
            assert s == d[i]


def test_thomas_periodic_random_exact_residual():
    rng = random.Random(11)
    for n in (3, 4, 7):
        a = [Fr(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(n)]
        c = [Fr(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(n)]
        b = [abs(a[i]) + abs(c[i]) + 1 for i in range(n)]
        d = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        x = sp.thomas_periodic(a, b, c, d)
        for i in range(n):
            assert a[i] * x[(i - 1) % n] + b[i] * x[i] + c[i] * x[(i + 1) % n] == d[i]


def test_cg_hand_system():
    A = sp.from_dense([[4, 1, 0, 0], [1, 4, 1, 0], [0, 1, 4, 1], [0, 0, 1, 4]])
    x, it = sp.cg(A, [5, 6, 6, 5], tol=1e-14)
    assert it <= 4
    assert max(abs(v - 1) for v in x) < 1e-12
    assert sp.to_dense(A)[1] == [1, 4, 1, 0]


def test_gauss_seidel_hand_system():
    A = sp.from_dense([[4, 1, 0, 0], [1, 4, 1, 0], [0, 1, 4, 1], [0, 0, 1, 4]])
    x = sp.gauss_seidel(A, [5.0, 6.0, 6.0, 5.0], 40)
    assert max(abs(v - 1) for v in x) < 1e-12


def _sym(A):
    return all(A[j].get(i, 0) == v for i, row in enumerate(A) for j, v in row.items())


def test_poisson_dirichlet_eigenfunction():
    nx, ny, p, q = 7, 5, 2, 3
    dx, dy = 1 / (nx + 1), 1 / (ny + 1)
    A = sp.poisson2d(nx, ny, dx, dy)
    assert _sym(A)
    v = [math.sin(p * math.pi * (i + 1) * dx) * math.sin(q * math.pi * (j + 1) * dy) for j in range(ny) for i in range(nx)]
    lam = 4 / dx**2 * math.sin(p * math.pi * dx / 2) ** 2 + 4 / dy**2 * math.sin(q * math.pi * dy / 2) ** 2
    av = sp.spmatvec(A, v)
    assert max(abs(av[k] - lam * v[k]) for k in range(nx * ny)) < 1e-9
    x, _ = sp.cg(A, [lam * t for t in v], tol=1e-13)
    assert max(abs(x[k] - v[k]) for k in range(nx * ny)) < 1e-10


def test_poisson_periodic_eigenfunction():
    nx, ny = 8, 6
    dx, dy = 1 / nx, 1 / ny
    A = sp.poisson2d(nx, ny, dx, dy, bc="periodic")
    assert _sym(A)
    assert max(abs(s) for s in sp.spmatvec(A, [1.0] * (nx * ny))) == 0
    v = [math.cos(2 * math.pi * i * dx) * math.sin(4 * math.pi * j * dy) for j in range(ny) for i in range(nx)]
    lam = 4 / dx**2 * math.sin(math.pi * dx) ** 2 + 4 / dy**2 * math.sin(2 * math.pi * dy) ** 2
    x, _ = sp.cg(A, [lam * t for t in v], tol=1e-13)
    assert max(abs(x[k] - v[k]) for k in range(nx * ny)) < 1e-10


def test_poisson_neumann_eigenfunction():
    nx, ny = 6, 5
    dx, dy = 1 / nx, 1 / ny
    A = sp.poisson2d(nx, ny, dx, dy, bc="neumann")
    assert _sym(A)
    assert max(abs(s) for s in sp.spmatvec(A, [1.0] * (nx * ny))) < 1e-12
    assert sum(sp.spmatvec(sp.poisson2d(4, 3, Fr(1, 4), Fr(1, 3), bc="neumann"), [Fr(1)] * 12), Fr(0)) == 0
    v = [math.cos(math.pi * (i + 0.5) * dx) * math.cos(2 * math.pi * (j + 0.5) * dy) for j in range(ny) for i in range(nx)]
    lam = 4 / dx**2 * math.sin(math.pi * dx / 2) ** 2 + 4 / dy**2 * math.sin(math.pi * dy) ** 2
    x, _ = sp.cg(A, [lam * t for t in v], tol=1e-13)
    assert max(abs(x[k] - v[k]) for k in range(nx * ny)) < 1e-10


def test_poisson_exact_fraction_stencil():
    A = sp.poisson2d(3, 3, Fr(1, 2), Fr(1, 3))
    # center unknown k = 4: 2/dx^2 + 2/dy^2 = 8 + 18, and -4, -9 to the neighbors
    assert A[4] == {4: 26, 3: -4, 5: -4, 1: -9, 7: -9}
