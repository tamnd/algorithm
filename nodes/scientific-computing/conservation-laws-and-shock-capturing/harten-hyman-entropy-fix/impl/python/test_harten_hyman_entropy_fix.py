# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harten-hyman-entropy-fix/. The authors are listed in prov/QYXKT4.jsonl.

import random
from fractions import Fraction
from math import sqrt

from harten_hyman_entropy_fix import (
    cons_to_prim,
    euler_flux,
    fixed_speed,
    prim_to_cons,
    roe_flux,
    roe_scalar,
    solve_euler,
    step,
)

BURGERS = (lambda v: v * v / 2), (lambda v: v)
TORO1 = ((1.0, 0.75, 1.0), (0.125, 0.0, 0.1))  # Sod's tube with u_L = 0.75: the rarefaction is transonic


def normal_shock(mach, g=1.4):
    """A shock at rest: the supersonic state (1, M c, 1) and the subsonic state behind it."""
    u = mach * sqrt(g)
    r = (g + 1.0) * mach**2 / ((g - 1.0) * mach**2 + 2.0)
    p = (2.0 * g * mach**2 - (g - 1.0)) / (g + 1.0)
    return (1.0, u, 1.0), (r, u / r, p)


def run_steps(cells, n, fix, cfl=0.9):
    dx = 1.0 / len(cells)
    for _ in range(n):
        smax = max(abs(cons_to_prim(q)[1]) + sqrt(1.4 * cons_to_prim(q)[2] / q[0]) for q in cells)
        cells = step(cells, cfl * dx / smax, dx, lambda a, b: roe_flux(a, b, fix=fix))
    return cells


def burgers_rarefaction_l1(m, fix, t=0.5):
    """L1 error on [-1, 1] for u_L = -1, u_R = 1 against the exact fan u = x / t."""
    f, df = BURGERS
    dx = 2.0 / m
    u = [-1.0 if (j + 0.5) * dx < 1.0 else 1.0 for j in range(m)]
    s = 0.0
    while s < t - 1e-14:
        dt = min(0.9 * dx / max(abs(v) for v in u), t - s)
        u = step(u, dt, dx, lambda a, b: roe_scalar(a, b, f, df, fix))
        s += dt
    exact = [sum(max(-1.0, min(1.0, (-1.0 + (j + (k + 0.5) / 16) * dx) / t)) for k in range(16)) / 16 for j in range(m)]
    return sum(abs(a - b) for a, b in zip(u, exact)) * dx


def largest_drop_in_fan(m, fix):
    """The largest density drop between two neighbor cells in the rarefaction of TORO1 at t = 0.2."""
    cells = [prim_to_cons(TORO1[0] if (j + 0.5) / m < 0.3 else TORO1[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.2, fix=fix)
    return max(cells[j][0] - cells[j + 1][0] for j in range(int(0.1 * m), int(0.4 * m)))


def test_fixed_speed_is_never_smaller_than_the_roe_speed() -> None:
    rng = random.Random(5)
    for _ in range(200):
        lam_l, lam_r = rng.uniform(-2, 0), rng.uniform(0, 2)
        lam = rng.uniform(lam_l, lam_r)
        assert fixed_speed(lam, lam_l, lam_r) >= abs(lam) - 1e-15
    assert fixed_speed(0.3, 0.5, 1.0) == 0.3 and fixed_speed(-0.3, -1.0, -0.5) == 0.3  # no sonic point: no change


def test_burgers_transonic_flux_is_half_ul_ur() -> None:
    f, df = BURGERS
    assert roe_scalar(-1.0, 1.0, f, df, fix=False) == 0.5  # Roe alone: f(-1) = f(1), the jump stays
    assert roe_scalar(-1.0, 1.0, f, df) == -0.5
    rng = random.Random(6)
    for _ in range(50):
        ul, ur = Fraction(-rng.randint(1, 20), 7), Fraction(rng.randint(1, 20), 7)
        assert roe_scalar(ul, ur, f, df) == ul * ur / 2  # the HLL flux with S_L = u_L and S_R = u_R


def test_burgers_expansion_shock_opens_into_the_fan() -> None:
    assert burgers_rarefaction_l1(100, fix=False) == 0.5  # the expansion shock does not move at all
    e1, e2 = burgers_rarefaction_l1(100, fix=True), burgers_rarefaction_l1(200, fix=True)
    assert e1 < 0.03 and e2 < 0.018 and e2 < e1


def test_admissible_shock_at_rest_is_still_exact() -> None:
    a, b = normal_shock(2.0)
    cells = [prim_to_cons(a if j < 20 else b) for j in range(40)]
    out = run_steps(cells, 30, fix=True)
    assert all(abs(x - y) < 1e-12 for p, q in zip(cells, out) for x, y in zip(p, q))


def test_expansion_shock_at_rest_is_broken() -> None:
    a, b = normal_shock(2.0)
    cells = [prim_to_cons(b if j < 20 else a) for j in range(40)]
    kept = run_steps(cells, 30, fix=False)
    assert all(abs(x - y) < 1e-12 for p, q in zip(cells, kept) for x, y in zip(p, q))
    fixed = run_steps(cells, 30, fix=True)
    assert max(abs(p[0] - q[0]) for p, q in zip(cells, fixed)) > 0.3


def test_no_change_without_a_sonic_point() -> None:
    ql, qr = prim_to_cons((1.0, 0.0, 1.0)), prim_to_cons((0.125, 0.0, 0.1))  # Sod: the fan is not transonic
    assert roe_flux(ql, qr) == roe_flux(ql, qr, fix=False)


def test_consistency() -> None:
    rng = random.Random(1)
    for _ in range(50):
        q = prim_to_cons((rng.uniform(0.1, 2), rng.uniform(-2, 2), rng.uniform(0.1, 2)))
        assert all(abs(a - b) < 1e-12 for a, b in zip(roe_flux(q, q), euler_flux(q)))


def test_glitch_in_the_transonic_rarefaction() -> None:
    d100, d200 = largest_drop_in_fan(100, False), largest_drop_in_fan(200, False)
    assert d100 > 0.1 and d200 > 0.1  # without the fix: a jump that does not shrink
    f100, f200 = largest_drop_in_fan(100, True), largest_drop_in_fan(200, True)
    assert f100 < 0.05 and f200 < 0.03 and f200 < 0.6 * f100  # with the fix: it shrinks with the cell size
