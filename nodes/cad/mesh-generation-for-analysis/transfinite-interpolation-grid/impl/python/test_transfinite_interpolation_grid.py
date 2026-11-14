# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transfinite-interpolation-grid/. The authors are listed in prov/FNVCY2.jsonl.

import random
from fractions import Fraction as F

import pytest

from mg1geom import orient2d, twice_area
from transfinite_interpolation_grid import cell_corner_values, is_unfolded, sample_polyline, tfi_grid


def annulus_sides():
    """The block of the page example: a quarter annulus with radii 1 and 2."""
    bottom = [(F(1), F(0)), (F(3, 2), F(0)), (F(2), F(0))]
    top = [(F(0), F(1)), (F(0), F(3, 2)), (F(0), F(2))]
    left = [(F(1), F(0)), (F(3, 5), F(4, 5)), (F(0), F(1))]
    right = [(F(2), F(0)), (F(6, 5), F(8, 5)), (F(0), F(2))]
    return bottom, top, left, right


def random_sides(rng, m, n, dim=2):
    """Random rational sides with matching corners."""
    def pt():
        return tuple(F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(dim))

    p00, p10, p01, p11 = pt(), pt(), pt(), pt()
    bottom = [p00] + [pt() for _ in range(m - 1)] + [p10]
    top = [p01] + [pt() for _ in range(m - 1)] + [p11]
    left = [p00] + [pt() for _ in range(n - 1)] + [p01]
    right = [p10] + [pt() for _ in range(n - 1)] + [p11]
    return bottom, top, left, right


def random_params(rng, k):
    """0 = t_0 < t_1 < ... < t_k = 1, random rationals."""
    inner = sorted(set(F(rng.randint(1, 999), 1000) for _ in range(3 * k)))
    while len(inner) < k - 1:
        inner = sorted(set(inner) | {F(rng.randint(1, 999), 1000)})
    return [F(0)] + sorted(rng.sample(inner, k - 1)) + [F(1)]


def test_example_of_the_page() -> None:
    g = tfi_grid(*annulus_sides())
    assert g[1][0] == (F(3, 2), F(0))
    assert g[1][1] == (F(9, 10), F(6, 5))
    assert g[1][1][0] ** 2 + g[1][1][1] ** 2 == F(9, 4)
    vals = cell_corner_values(g)
    assert vals[(0, 0)] == [F(2, 5), F(3, 5), F(3, 5), F(2, 5)]
    assert vals[(1, 1)] == [F(9, 20), F(3, 5), F(3, 5), F(9, 20)]
    assert is_unfolded(g)


def test_boundary_reproduction_is_exact() -> None:
    rng = random.Random(20261114)
    for trial in range(200):
        m, n = rng.randint(1, 7), rng.randint(1, 7)
        dim = 2 if trial % 2 else 3
        bottom, top, left, right = random_sides(rng, m, n, dim)
        u = random_params(rng, m) if trial % 3 == 0 else None
        v = random_params(rng, n) if trial % 3 == 0 else None
        g = tfi_grid(bottom, top, left, right, u, v)
        assert [g[i][0] for i in range(m + 1)] == list(bottom)
        assert [g[i][n] for i in range(m + 1)] == list(top)
        assert g[0] == list(left)
        assert g[m] == list(right)


def coons(c0, c1, d0, d1, s, t):
    """The bilinearly blended Coons patch of four curves, written out term by term (an independent oracle)."""
    p00, p10, p01, p11 = c0(0), c0(1), c1(0), c1(1)
    return tuple(
        (1 - t) * c0(s)[k] + t * c1(s)[k] + (1 - s) * d0(t)[k] + s * d1(t)[k]
        - ((1 - s) * (1 - t) * p00[k] + s * (1 - t) * p10[k] + (1 - s) * t * p01[k] + s * t * p11[k])
        for k in range(2)
    )


def test_equals_the_coons_patch_at_the_grid_parameters() -> None:
    rng = random.Random(7)
    for _ in range(30):
        cb = [F(rng.randint(-9, 9), 7) for _ in range(6)]
        c0 = lambda s: (s, cb[0] * s * (1 - s))
        c1 = lambda s: (s + cb[1] * s * (1 - s), 1 + cb[2] * s * s * (1 - s))
        d0 = lambda t: (cb[3] * t * (1 - t), t)
        d1 = lambda t: (1 + cb[4] * t * (1 - t) * (1 - 2 * t), t + cb[5] * t * (1 - t))
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        u, v = random_params(rng, m), random_params(rng, n)
        g = tfi_grid([c0(s) for s in u], [c1(s) for s in u], [d0(t) for t in v], [d1(t) for t in v], u, v)
        for i in range(m + 1):
            for j in range(n + 1):
                assert g[i][j] == coons(c0, c1, d0, d1, u[i], v[j])


def test_bilinear_data_are_reproduced() -> None:
    rng = random.Random(11)
    for _ in range(50):
        a, b, c, d = [(F(rng.randint(-20, 20), 3), F(rng.randint(-20, 20), 5)) for _ in range(4)]

        def f(s, t):
            return tuple(a[k] + b[k] * s + c[k] * t + d[k] * s * t for k in range(2))

        m, n = rng.randint(1, 5), rng.randint(1, 5)
        u, v = random_params(rng, m), random_params(rng, n)
        g = tfi_grid([f(s, 0) for s in u], [f(s, 1) for s in u], [f(0, t) for t in v], [f(1, t) for t in v], u, v)
        assert all(g[i][j] == f(u[i], v[j]) for i in range(m + 1) for j in range(n + 1))


def test_convex_quadrilateral_gives_cells_that_tile_it() -> None:
    q = [(F(0), F(0)), (F(7), F(1)), (F(6), F(5)), (F(1), F(4))]
    m, n = 5, 4
    us, vs = [F(i, m) for i in range(m + 1)], [F(j, n) for j in range(n + 1)]
    g = tfi_grid(sample_polyline([q[0], q[1]], us), sample_polyline([q[3], q[2]], us),
                 sample_polyline([q[0], q[3]], vs), sample_polyline([q[1], q[2]], vs))
    assert is_unfolded(g)
    total = sum(twice_area([g[i][j], g[i + 1][j], g[i + 1][j + 1], g[i][j + 1]]) for i in range(m) for j in range(n))
    assert total == twice_area(q)


def test_hook_boundary_folds() -> None:
    m, n = 6, 4
    us, vs = [F(i, m) for i in range(m + 1)], [F(j, n) for j in range(n + 1)]
    hook = [(F(0), F(0)), (F(3, 5), F(1, 5)), (F(2, 5), F(2, 5)), (F(1), F(0))]
    bottom = sample_polyline(hook, us)
    # the hook is a simple polyline: its first and last pieces do not meet
    assert orient2d(hook[2], hook[3], hook[1]) < 0 and orient2d(hook[2], hook[3], hook[0]) < 0
    g = tfi_grid(bottom, [(s, F(1)) for s in us], [(F(0), t) for t in vs], [(F(1), t) for t in vs])
    vals = cell_corner_values(g)
    assert not is_unfolded(g)
    assert all(x < 0 for x in vals[(2, 0)]) and all(x < 0 for x in vals[(3, 0)])
    bad = {key for key, vs4 in vals.items() if min(vs4) <= 0}
    assert bad == {(2, 0), (3, 0), (2, 1), (3, 1)}


def test_float_input_is_accepted() -> None:
    g = tfi_grid([(0.0, 0.0), (1.0, 0.0)], [(0.0, 1.0), (1.0, 1.0)], [(0.0, 0.0), (0.0, 1.0)], [(1.0, 0.0), (1.0, 1.0)])
    assert g == [[(0.0, 0.0), (0.0, 1.0)], [(1.0, 0.0), (1.0, 1.0)]]


def test_bad_input() -> None:
    b, t, l, r = annulus_sides()
    with pytest.raises(ValueError):
        tfi_grid(b, t, l, [(F(5), F(5))] + r[1:])
    with pytest.raises(ValueError):
        tfi_grid(b, t[:2], l, r)
    with pytest.raises(ValueError):
        tfi_grid(b, t, l, r, u=[F(0), F(1, 2), F(2)])
