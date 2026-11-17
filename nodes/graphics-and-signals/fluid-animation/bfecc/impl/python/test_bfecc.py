# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bfecc/. The authors are listed in prov/Z26PRS.jsonl.

"""Tests of BFECC advection on the MAC grid of macgrid.py."""

import cmath
import math
import random

import pytest

import macgrid
import bfecc as B


def bump(x, y, cx, cy, r):
    """A smooth bump (1 - |x - c|^2 / r^2)^4 with compact support of radius r."""
    t = ((x - cx) ** 2 + (y - cy) ** 2) / (r * r)
    return (1.0 - t) ** 4 if t < 1.0 else 0.0


def move_bump(n, steps, limiter, plain=False):
    """Move the bump of radius 0.3 by the constant velocity (1, 0.5) m/s for 0.25 s; return the max error."""
    g = macgrid.make_grid(n, n, 1.0 / n)
    B.constant_velocity(g, 1.0, 0.5)
    dt = 0.25 / steps
    q = B.cell_field(g, lambda x, y: bump(x, y, 0.35, 0.4, 0.3))
    for _ in range(steps):
        q = B.semi_lagrangian(g, q, dt) if plain else B.bfecc(g, q, dt, limiter=limiter)
    return B.max_error(q, B.cell_field(g, lambda x, y: bump(x, y, 0.6, 0.525, 0.3)))


def test_constant_field_is_exact():
    rng = random.Random(1)
    g = macgrid.make_grid(8, 8, 0.125)
    for col in g.u + g.v:
        for k in range(len(col)):
            col[k] = rng.uniform(-3.0, 3.0)
    q = [[0.7] * 8 for _ in range(8)]
    for lim in (None, "clamp", "revert"):
        out = B.bfecc(g, q, 0.2, limiter=lim)
        assert B.max_error(out, q) < 1e-14


def test_interior_matches_the_fourier_symbol():
    n = 40
    g = macgrid.make_grid(n, 1, 1.0)
    for c in (0.3, 1.5, 2.7):
        B.constant_velocity(g, c, 0.0)
        m, phi = int(c), c - int(c)
        for th in (0.4, 1.3, 2.9):
            q = [[math.cos(th * a)] for a in range(n)]
            out = B.bfecc(g, q, 1.0)
            amp = cmath.exp(-1j * m * th) * ((1.0 - phi) + phi * cmath.exp(-1j * th))
            sym = amp * (3.0 - abs(amp) ** 2) / 2.0
            r = 3 * (m + 1) + 1
            assert max(abs(out[a][0] - (sym * cmath.exp(1j * th * a)).real) for a in range(r, n - r)) < 1e-13
            assert abs(amp) <= abs(sym) <= 1.0


def test_second_order_on_a_smooth_bump():
    sl16, sl32 = move_bump(16, 3, None, True), move_bump(32, 6, None, True)
    bf16, bf32 = move_bump(16, 3, None), move_bump(32, 6, None)
    cl16, cl32 = move_bump(16, 3, "clamp"), move_bump(32, 6, "clamp")
    rv32 = move_bump(32, 6, "revert")
    assert abs(sl32 - 0.1062) < 1e-4 and abs(bf32 - 0.00684) < 1e-5
    assert 0.8 < math.log2(sl16 / sl32) < 1.0
    assert math.log2(bf16 / bf32) > 2.3
    assert math.log2(cl16 / cl32) > 2.0
    assert bf32 < cl32 < rv32 < sl32


def test_rotation_quarter_turn():
    n = 32
    g = macgrid.make_grid(n, n, 1.0 / n)
    B.rotation_velocity(g, 2.0 * math.pi, 0.5, 0.5)
    assert macgrid.max_fluid_divergence(g) < 1e-12
    q0 = B.cell_field(g, lambda x, y: bump(x, y, 0.5, 0.75, 0.2))
    exact = B.cell_field(g, lambda x, y: bump(x, y, 0.25, 0.5, 0.2))
    err = {}
    for name, lim in (("sl", None), ("bfecc", None), ("clamp", "clamp")):
        q = q0
        for _ in range(16):
            q = B.semi_lagrangian(g, q, 1.0 / 64.0) if name == "sl" else B.bfecc(g, q, 1.0 / 64.0, limiter=lim)
        err[name] = B.max_error(q, exact)
        if name == "clamp":
            assert min(map(min, q)) >= 0.0
    assert err["bfecc"] < err["clamp"] < err["sl"] / 4.0
    assert abs(err["sl"] - 0.3754) < 1e-3 and abs(err["bfecc"] - 0.0594) < 1e-3


def test_limiters_keep_the_range_of_a_step():
    g = macgrid.make_grid(24, 24, 1.0 / 24.0)
    B.constant_velocity(g, 1.0, 0.4)
    q0 = B.cell_field(g, lambda x, y: 1.0 if 0.2 < x < 0.5 and 0.3 < y < 0.6 else 0.0)
    q = q0
    for _ in range(5):
        q = B.bfecc(g, q, 0.03)
    assert max(map(max, q)) > 1.2 and min(map(min, q)) < -0.1
    for lim in ("clamp", "revert"):
        q = q0
        for _ in range(5):
            lo, hi = B.stencil_bounds(g, q, 0.03)
            q = B.bfecc(g, q, 0.03, limiter=lim)
            assert all(lo[a][b] <= q[a][b] <= hi[a][b] for a in range(24) for b in range(24))
        assert 0.0 <= min(map(min, q)) and max(map(max, q)) <= 1.0


def test_semi_lagrangian_stays_in_its_stencil():
    rng = random.Random(2)
    g = macgrid.make_grid(10, 10, 0.1)
    for col in g.u + g.v:
        for k in range(len(col)):
            col[k] = rng.uniform(-2.0, 2.0)
    q = [[rng.random() for _ in range(10)] for _ in range(10)]
    lo, hi = B.stencil_bounds(g, q, 0.13)
    out = B.semi_lagrangian(g, q, 0.13)
    assert all(lo[a][b] - 1e-15 <= out[a][b] <= hi[a][b] + 1e-15 for a in range(10) for b in range(10))


def test_velocity_and_errors():
    g = macgrid.make_grid(6, 6, 1.0 / 6.0)
    B.constant_velocity(g, 0.8, -0.3)
    u, v = B.bfecc_velocity(g, 0.5, "revert")
    assert B.max_error(u, g.u) < 1e-14 and B.max_error(v, g.v) < 1e-14
    with pytest.raises(ValueError):
        B.bfecc(g, [[0.0] * 6 for _ in range(6)], 0.1, limiter="minmod")
