# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unconditionally-stable-maccormack/. The authors are listed in prov/5R0MXZ.jsonl.

"""Tests of the unconditionally stable MacCormack method on the MAC grid of macgrid.py."""

import cmath
import math
import random

import pytest

import macgrid
import unconditionally_stable_maccormack as U


def bump(x, y, cx, cy, r):
    """A smooth bump (1 - |x - c|^2 / r^2)^4 with compact support of radius r."""
    t = ((x - cx) ** 2 + (y - cy) ** 2) / (r * r)
    return (1.0 - t) ** 4 if t < 1.0 else 0.0


def move_bump(n, steps, limiter, plain=False):
    """Move the bump of radius 0.3 by the constant velocity (1, 0.5) m/s for 0.25 s; return the max error."""
    g = macgrid.make_grid(n, n, 1.0 / n)
    U.constant_velocity(g, 1.0, 0.5)
    dt = 0.25 / steps
    q = U.cell_field(g, lambda x, y: bump(x, y, 0.35, 0.4, 0.3))
    for _ in range(steps):
        q = U.semi_lagrangian(g, q, dt) if plain else U.maccormack(g, q, dt, limiter=limiter)
    return U.max_error(q, U.cell_field(g, lambda x, y: bump(x, y, 0.6, 0.525, 0.3)))


def test_constant_field_is_exact():
    rng = random.Random(1)
    g = macgrid.make_grid(8, 8, 0.125)
    for col in g.u + g.v:
        for k in range(len(col)):
            col[k] = rng.uniform(-3.0, 3.0)
    q = [[0.7] * 8 for _ in range(8)]
    for lim in (None, "clamp", "revert"):
        assert U.max_error(U.maccormack(g, q, 0.2, limiter=lim), q) < 1e-14


def test_interior_matches_the_fourier_symbol():
    n = 40
    g = macgrid.make_grid(n, 1, 1.0)
    damped_more = False
    for c in (0.3, 1.5, 2.7):
        U.constant_velocity(g, c, 0.0)
        m, phi = int(c), c - int(c)
        for th in (0.4, 1.3, 2.9):
            q = [[math.cos(th * a)] for a in range(n)]
            out = U.maccormack(g, q, 1.0, limiter=None)
            amp = cmath.exp(-1j * m * th) * ((1.0 - phi) + phi * cmath.exp(-1j * th))
            sym = amp + (1.0 - abs(amp) ** 2) / 2.0
            r = 2 * (m + 1) + 1
            assert max(abs(out[a][0] - (sym * cmath.exp(1j * th * a)).real) for a in range(r, n - r)) < 1e-13
            assert abs(sym) <= 1.0
            damped_more = damped_more or abs(sym) < abs(amp)
    assert damped_more  # some modes are damped more than by the plain step


def test_second_order_on_a_smooth_bump():
    sl16, sl32 = move_bump(16, 3, None, True), move_bump(32, 6, None, True)
    mc16, mc32 = move_bump(16, 3, None), move_bump(32, 6, None)
    rv32 = move_bump(32, 6, "revert")
    assert abs(sl32 - 0.1062) < 1e-4 and abs(mc32 - 0.04924) < 1e-5
    assert 0.8 < math.log2(sl16 / sl32) < 1.0
    assert math.log2(mc16 / mc32) > 1.6
    assert mc32 < rv32 < sl32 / 2.0


def test_error_does_not_shrink_with_a_larger_step():
    e12, e6 = move_bump(32, 12, None), move_bump(32, 6, None)
    assert abs(e12 - 0.0486) < 1e-4 and abs(e6 - 0.0492) < 1e-4
    assert move_bump(32, 2, None) < 1e-14  # CFL number 4: whole cells, exact


def test_rotation_quarter_turn():
    n = 32
    g = macgrid.make_grid(n, n, 1.0 / n)
    U.rotation_velocity(g, 2.0 * math.pi, 0.5, 0.5)
    q0 = U.cell_field(g, lambda x, y: bump(x, y, 0.5, 0.75, 0.2))
    exact = U.cell_field(g, lambda x, y: bump(x, y, 0.25, 0.5, 0.2))
    q = q0
    for _ in range(16):
        q = U.maccormack(g, q, 1.0 / 64.0)
    assert abs(U.max_error(q, exact) - 0.1876) < 1e-3
    assert min(map(min, q)) >= 0.0 and max(map(max, q)) <= 1.0


def test_limiters_keep_the_range_of_a_step():
    g = macgrid.make_grid(24, 24, 1.0 / 24.0)
    U.constant_velocity(g, 1.0, 0.4)
    q0 = U.cell_field(g, lambda x, y: 1.0 if 0.2 < x < 0.5 and 0.3 < y < 0.6 else 0.0)
    q = q0
    for _ in range(5):
        q = U.maccormack(g, q, 0.03, limiter=None)
    assert max(map(max, q)) > 1.3 and min(map(min, q)) < -0.25
    for lim in ("clamp", "revert"):
        q = q0
        for _ in range(5):
            lo, hi = U.stencil_bounds(g, q, 0.03)
            q = U.maccormack(g, q, 0.03, limiter=lim)
            assert all(lo[a][b] <= q[a][b] <= hi[a][b] for a in range(24) for b in range(24))
        assert 0.0 <= min(map(min, q)) and max(map(max, q)) <= 1.0


def test_velocity_and_errors():
    g = macgrid.make_grid(6, 6, 1.0 / 6.0)
    U.constant_velocity(g, 0.8, -0.3)
    u, v = U.maccormack_velocity(g, 0.5)
    assert U.max_error(u, g.u) < 1e-14 and U.max_error(v, g.v) < 1e-14
    with pytest.raises(ValueError):
        U.maccormack(g, [[0.0] * 6 for _ in range(6)], 0.1, limiter="minmod")
