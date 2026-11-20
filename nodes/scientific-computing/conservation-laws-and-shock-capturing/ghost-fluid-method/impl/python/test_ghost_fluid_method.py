# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ghost-fluid-method/. The authors are listed in prov/73K8P0.jsonl.

import math

import pytest

from ghost_fluid_method import (cons, gfm_poisson_1d, gfm_step, ghost_states, naive_step,
                                primitives, run)

AIR, HELIUM = 1.4, 5.0 / 3.0


# ---------------------------------------------------------------- reference
def exact_riemann(WL, WR, gl, gr, s):
    """Exact solution of the Riemann problem for two ideal gases at x / t = s."""
    rl, ul, pl = WL
    rr, ur, pr = WR
    cl, cr = math.sqrt(gl * pl / rl), math.sqrt(gr * pr / rr)

    def fk(p, rk, pk, ck, g):
        if p > pk:
            A, B = 2 / ((g + 1) * rk), (g - 1) / (g + 1) * pk
            return (p - pk) * math.sqrt(A / (p + B))
        return 2 * ck / (g - 1) * ((p / pk) ** ((g - 1) / (2 * g)) - 1)

    lo, hi = 1e-12, 1e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if fk(mid, rl, pl, cl, gl) + fk(mid, rr, pr, cr, gr) + ur - ul > 0:
            hi = mid
        else:
            lo = mid
    ps = 0.5 * (lo + hi)
    us = 0.5 * (ul + ur) + 0.5 * (fk(ps, rr, pr, cr, gr) - fk(ps, rl, pl, cl, gl))
    if s <= us:
        g, mu = gl, (gl - 1) / (gl + 1)
        if ps > pl:
            if s <= ul - cl * math.sqrt((g + 1) / (2 * g) * ps / pl + (g - 1) / (2 * g)):
                return WL
            return rl * (ps / pl + mu) / (mu * ps / pl + 1), us, ps
        if s <= ul - cl:
            return WL
        if s >= us - cl * (ps / pl) ** ((g - 1) / (2 * g)):
            return rl * (ps / pl) ** (1 / g), us, ps
        c = 2 / (g + 1) * (cl + (g - 1) / 2 * (ul - s))
        return rl * (c / cl) ** (2 / (g - 1)), 2 / (g + 1) * (cl + (g - 1) / 2 * ul + s), \
            pl * (c / cl) ** (2 * g / (g - 1))
    g, mu = gr, (gr - 1) / (gr + 1)
    if ps > pr:
        if s >= ur + cr * math.sqrt((g + 1) / (2 * g) * ps / pr + (g - 1) / (2 * g)):
            return WR
        return rr * (ps / pr + mu) / (mu * ps / pr + 1), us, ps
    if s >= ur + cr:
        return WR
    if s <= us + cr * (ps / pr) ** ((g - 1) / (2 * g)):
        return rr * (ps / pr) ** (1 / g), us, ps
    c = 2 / (g + 1) * (cr - (g - 1) / 2 * (ur - s))
    return rr * (c / cr) ** (2 / (g - 1)), 2 / (g + 1) * (-cr + (g - 1) / 2 * ur + s), \
        pr * (c / cr) ** (2 * g / (g - 1))


def setup(m, WL, WR, x0=0.5):
    dx = 1.0 / m
    xs = [(i + 0.5) * dx for i in range(m)]
    phi = [x - x0 for x in xs]
    U = [cons(*(WL if x < x0 else WR), AIR if x < x0 else HELIUM) for x in xs]
    return xs, dx, U, phi


# ---------------------------------------------------------------- tests
def test_ghost_states_keep_pressure_velocity_and_own_entropy():
    W = [(1.0, 0.1, 1.0), (1.0, 0.1, 1.0), (0.2, 0.1, 1.0), (0.2, 0.1, 1.0)]
    side = [0, 0, 1, 1]
    ext = ghost_states(W, side, 0, AIR)
    assert ext[:2] == W[:2]
    assert all(abs(r - 1.0) < 1e-15 and u == 0.1 and p == 1.0 for r, u, p in ext[2:])
    ext = ghost_states(W, side, 1, HELIUM)
    assert all(abs(r - 0.2) < 1e-15 for r, _, _ in ext[:2])


def test_moving_contact_keeps_pressure_and_velocity():
    # Uniform p = 1 and u = 0.5, density and gamma jump: only the interface moves.
    xs, dx, U, phi = setup(100, (1.0, 0.5, 1.0), (0.1, 0.5, 1.0), x0=0.3)
    Ug, pg = run(gfm_step, U, phi, (AIR, HELIUM), dx, 0.2)
    Wg = primitives(Ug, pg, (AIR, HELIUM))
    assert max(abs(p - 1.0) for _, _, p in Wg) < 1e-12
    assert max(abs(u - 0.5) for _, u, _ in Wg) < 1e-12
    k = next(i for i, v in enumerate(pg) if v > 0)
    assert abs(xs[k] - 0.4) <= dx                    # the contact is at 0.3 + 0.5 * 0.2
    assert all(abs(r - (1.0 if i < k else 0.1)) < 1e-12 for i, (r, _, _) in enumerate(Wg))
    Un, pn = run(naive_step, U, phi, (AIR, HELIUM), dx, 0.2)
    Wn = primitives(Un, pn, (AIR, HELIUM))
    assert max(abs(p - 1.0) for _, _, p in Wn) > 0.05


def test_two_gas_shock_tube_against_the_exact_solution():
    WL, WR, T = (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.15
    errs = []
    for m in (100, 200):
        xs, dx, U, phi = setup(m, WL, WR)
        Ug, pg = run(gfm_step, U, phi, (AIR, HELIUM), dx, T)
        Wg = primitives(Ug, pg, (AIR, HELIUM))
        ex = [exact_riemann(WL, WR, AIR, HELIUM, (x - 0.5) / T) for x in xs]
        errs.append(sum(abs(a[0] - b[0]) for a, b in zip(Wg, ex)) * dx)
    assert errs[0] < 0.03 and errs[1] < 0.7 * errs[0]


def test_interface_position_and_pressure_at_the_contact():
    WL, WR, T = (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.15
    _, us, ps = exact_riemann(WL, WR, AIR, HELIUM, 0.0)
    xc = 0.5 + us * T
    xs, dx, U, phi = setup(200, WL, WR)
    Ug, pg = run(gfm_step, U, phi, (AIR, HELIUM), dx, T)
    k = next(i for i, v in enumerate(pg) if v > 0)
    assert abs(xs[k] - xc) < 0.015
    near = [i for i, x in enumerate(xs) if abs(x - xc) < 0.03]
    Wg = primitives(Ug, pg, (AIR, HELIUM))
    assert max(abs(Wg[i][2] - ps) for i in near) < 1e-3
    Un, pn = run(naive_step, U, phi, (AIR, HELIUM), dx, T)
    Wn = primitives(Un, pn, (AIR, HELIUM))
    assert max(abs(Wn[i][2] - ps) for i in near) > 0.03


def test_poisson_with_jumps_is_exact_for_piecewise_linear_solutions():
    # u = 2x on the left, 3x + 1 on the right of alpha; beta = 1 and 10.
    al = 0.437
    a = (3 * al + 1) - 2 * al
    b = 10 * 3 - 1 * 2
    x, u = gfm_poisson_1d(40, al, 1.0, 10.0, lambda s: 0.0, a, b, 0.0, 4.0)
    for xi, ui in zip(x, u):
        assert abs(ui - (2 * xi if xi < al else 3 * xi + 1)) < 1e-12


def test_poisson_with_jumps_converges():
    al, bm, bp = 0.4321, 1.0, 10.0

    def exact(s):
        return math.exp(s) if s < al else math.cos(s)

    a = math.cos(al) - math.exp(al)
    b = bp * (-math.sin(al)) - bm * math.exp(al)
    f = (lambda s: math.exp(s) if s < al else -bp * math.cos(s))
    errs = []
    for n in (20, 40, 80, 160, 320):
        x, u = gfm_poisson_1d(n, al, bm, bp, f, a, b, 1.0, math.cos(1.0))
        errs.append((n, max(abs(ui - exact(xi)) for xi, ui in zip(x, u))))
    # First order: the error is below 0.25 h on every grid; it depends on theta.
    assert all(e < 0.25 / n for n, e in errs) and errs[-1][1] < 5e-4


def test_rejects_interface_on_the_boundary():
    with pytest.raises(ValueError):
        gfm_poisson_1d(10, 0.01, 1.0, 1.0, lambda s: 0.0, 0.0, 0.0, 0.0, 0.0)
