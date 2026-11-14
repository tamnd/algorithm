# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elliptic-grid-generation/. The authors are listed in prov/EEEWVA.jsonl.

import math
import random

import pytest

from elliptic_grid_generation import cell_corner_values_exact, elliptic_grid, is_unfolded, residual, side, tfi_start

RESIDUAL_TOL = 1e-10


def discrete_equation(x, i, j):
    """alpha x_xixi - 2 beta x_xieta + gamma x_etaeta at (i, j), written out on its own (an independent oracle)."""
    def d(a, b):
        return (a[0] - b[0], a[1] - b[1])

    xi = [c / 2 for c in d(x[i + 1][j], x[i - 1][j])]
    eta = [c / 2 for c in d(x[i][j + 1], x[i][j - 1])]
    alpha = eta[0] ** 2 + eta[1] ** 2
    beta = xi[0] * eta[0] + xi[1] * eta[1]
    gamma = xi[0] ** 2 + xi[1] ** 2
    out = []
    for k in range(2):
        xx = x[i + 1][j][k] - 2 * x[i][j][k] + x[i - 1][j][k]
        yy = x[i][j + 1][k] - 2 * x[i][j][k] + x[i][j - 1][k]
        xy = (x[i + 1][j + 1][k] - x[i + 1][j - 1][k] - x[i - 1][j + 1][k] + x[i - 1][j - 1][k]) / 4
        out.append((alpha * xx - 2 * beta * xy + gamma * yy) / (2 * (alpha + gamma)))
    return out


def test_example_of_the_page() -> None:
    b = [(0, 0), (2, 0), (4, 0)]
    t = [(0, 2), (1, 2), (2, 2)]
    l = [(0, 0), (0, 1), (0, 2)]
    r = [(4, 0), (3, 1), (2, 2)]
    assert tfi_start(b, t, l, r)[1][1] == (1.5, 1.0)
    x, sweeps, res, ok = elliptic_grid(b, t, l, r, omega=1.0)
    assert ok and sweeps == 1 and res == 0.0
    assert abs(x[1][1][0] - 39 / 28) < 1e-15 and abs(x[1][1][1] - 1) < 1e-15
    assert is_unfolded(x)


def test_parallelogram_is_a_fixed_point() -> None:
    m, n = 5, 3
    b = side((0, 0), (4, 1), [i / m for i in range(m + 1)])
    t = side((1, 3), (5, 4), [i / m for i in range(m + 1)])
    l = side((0, 0), (1, 3), [j / n for j in range(n + 1)])
    r = side((4, 1), (5, 4), [j / n for j in range(n + 1)])
    x0 = tfi_start(b, t, l, r)
    assert residual(x0) < 1e-14
    x, sweeps, res, ok = elliptic_grid(b, t, l, r)
    assert ok and sweeps <= 2
    assert max(math.dist(x[i][j], x0[i][j]) for i in range(m + 1) for j in range(n + 1)) < 1e-13


def random_convex_quad(rng):
    return [(rng.uniform(-1, 0), rng.uniform(-1, 0)), (rng.uniform(1, 2), rng.uniform(-1, 0)),
            (rng.uniform(1, 2), rng.uniform(1, 2)), (rng.uniform(-1, 0), rng.uniform(1, 2))]


def random_params(rng, k):
    inner = sorted(rng.uniform(0.02, 0.98) for _ in range(k - 1))
    return [0.0] + inner + [1.0]


def test_convex_quadrilaterals_give_positive_jacobians() -> None:
    rng = random.Random(5)
    tfi_failures = 0
    for _ in range(25):
        q = random_convex_quad(rng)
        m, n = rng.randint(6, 12), rng.randint(6, 12)
        b = side(q[0], q[1], random_params(rng, m))
        t = side(q[3], q[2], random_params(rng, m))
        l = side(q[0], q[3], random_params(rng, n))
        r = side(q[1], q[2], random_params(rng, n))
        tfi_failures += not is_unfolded(tfi_start(b, t, l, r))
        x, sweeps, res, ok = elliptic_grid(b, t, l, r, omega=1.5, tol=1e-12)
        assert ok
        assert residual(x) < RESIDUAL_TOL
        assert max(abs(c) for i in range(1, m) for j in range(1, n) for c in discrete_equation(x, i, j)) < RESIDUAL_TOL
        assert [x[i][0] for i in range(m + 1)] == b and [x[i][n] for i in range(m + 1)] == t
        assert x[0] == l and x[m] == r
        vals = cell_corner_values_exact(x)
        assert all(s > 0 for v in vals.values() for s in v)
    assert tfi_failures > 0  # random spacing on the sides makes some TFI starts fail CHECK


def test_converges_to_the_conformal_map_of_an_annular_sector() -> None:
    errors = []
    for n in (4, 8, 16):
        k = (math.pi / 2) / n

        def f(i, j):
            return (math.exp(k * i) * math.cos(k * j), math.exp(k * i) * math.sin(k * j))

        b = [f(i, 0) for i in range(n + 1)]
        t = [f(i, n) for i in range(n + 1)]
        l = [f(0, j) for j in range(n + 1)]
        r = [f(n, j) for j in range(n + 1)]
        x, sweeps, res, ok = elliptic_grid(b, t, l, r, omega=1.8, tol=1e-13)
        assert ok and is_unfolded(x)
        errors.append(max(math.dist(x[i][j], f(i, j)) for i in range(n + 1) for j in range(n + 1)))
    assert errors[0] < 0.04
    assert 3.5 < errors[0] / errors[1] < 4.5 and 3.5 < errors[1] / errors[2] < 4.5


def hook_sides(m, n):
    hook = [(0.0, 0.0), (0.6, 0.2), (0.4, 0.4), (1.0, 0.0)]
    b = []
    for i in range(m + 1):
        s = 3 * i / m
        seg = min(int(s), 2)
        f = s - seg
        a, c = hook[seg], hook[seg + 1]
        b.append((a[0] + f * (c[0] - a[0]), a[1] + f * (c[1] - a[1])))
    t = [(i / m, 1.0) for i in range(m + 1)]
    l = [(0.0, j / n) for j in range(n + 1)]
    r = [(1.0, j / n) for j in range(n + 1)]
    return b, t, l, r


def test_hook_domain_converges_but_the_grid_is_not_valid() -> None:
    b, t, l, r = hook_sides(6, 4)
    start = cell_corner_values_exact(tfi_start(b, t, l, r))
    assert all(s < 0 for s in start[(2, 0)])
    x, sweeps, res, ok = elliptic_grid(b, t, l, r, omega=1.5)
    assert ok and residual(x) < RESIDUAL_TOL
    vals = cell_corner_values_exact(x)
    bad = {key for key, v in vals.items() if min(v) <= 0}
    assert bad == {(2, 0), (3, 0)}
    # no cell is turned over, but two cells are not convex
    assert sum(s > 0 for s in vals[(2, 0)]) == 3 and sum(s > 0 for s in vals[(3, 0)]) == 2


def test_control_functions_and_bad_input() -> None:
    q = [(0.0, 0.0), (2.0, 0.0), (2.0, 1.0), (0.0, 1.0)]
    m, n = 8, 6
    b = side(q[0], q[1], [i / m for i in range(m + 1)])
    t = side(q[3], q[2], [i / m for i in range(m + 1)])
    l = side(q[0], q[3], [j / n for j in range(n + 1)])
    r = side(q[1], q[2], [j / n for j in range(n + 1)])
    P = lambda i, j: 0.0
    Q = lambda i, j: -0.5
    x, sweeps, res, ok = elliptic_grid(b, t, l, r, P=P, Q=Q)
    assert ok and residual(x, P, Q) < RESIDUAL_TOL and is_unfolded(x)
    assert x[0] == l and x[m] == r
    with pytest.raises(ValueError):
        elliptic_grid(b, t, l, [(5.0, 5.0)] + r[1:])
