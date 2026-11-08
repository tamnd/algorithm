# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/upwind-scheme/. The authors are listed in prov/K94YNY.jsonl.

import cmath
import math
from fractions import Fraction

import pytest

from upwind_scheme import (amplification_factor, step_count, total_variation, upwind,
                           upwind_conservative, upwind_nonconservative_burgers)


def grid(m):
    dx = 1.0 / m
    return dx, [(j + 0.5) * dx for j in range(m)]


def pulse(xs):
    return [1.0 if 0.25 <= x < 0.5 else 0.0 for x in xs]


def test_courant_one_is_an_exact_shift_in_fractions():
    u0 = [Fraction(v) for v in (0, 1, 3, 2, 0, 5)]
    r = upwind(u0, Fraction(1), Fraction(1, 6), Fraction(1, 6), Fraction(1, 2))
    assert r.steps == 3 and r.u == u0[-3:] + u0[:-3]
    r = upwind(u0, Fraction(-1), Fraction(1, 6), Fraction(1, 6), Fraction(1, 3))
    assert r.u == u0[2:] + u0[:2]  # a < 0 moves the data to the left


def test_first_order_convergence():
    errs = []
    for m in (50, 100, 200, 400):
        dx, xs = grid(m)
        r = upwind([math.sin(2 * math.pi * x) for x in xs], 1.0, dx, 0.5 * dx, 1.0)
        errs.append(max(abs(v - math.sin(2 * math.pi * (x - 1.0))) for v, x in zip(r.u, xs)))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(0.9 < q < 1.05 for q in orders)


def test_amplification_matches_one_fourier_mode():
    m, nu, N = 40, 0.3, 25
    dx, xs = grid(m)
    theta = 2 * math.pi * 3 / m
    u0 = [complex(math.cos(3 * 2 * math.pi * x), math.sin(3 * 2 * math.pi * x)) for x in xs]
    r = upwind(u0, 1.0, dx, nu * dx, N * nu * dx)
    g = amplification_factor(nu, theta)
    assert all(abs(v - g ** N * w) < 1e-12 for v, w in zip(r.u, u0))
    assert abs(abs(g) ** 2 - (1 - 2 * nu * (1 - nu) * (1 - math.cos(theta)))) < 1e-15


def test_monotone_conservative_tvd_below_limit():
    dx, xs = grid(100)
    u0 = pulse(xs)
    for nu in (0.2, 0.5, 0.99, 1.0):
        r = upwind(u0, 1.0, dx, nu * dx, 1.0)
        assert min(r.u) >= -1e-12 and max(r.u) <= 1 + 1e-12
        assert abs(sum(r.u) - sum(u0)) < 1e-10
        assert total_variation(r.u) <= total_variation(u0) + 1e-12


def test_courant_just_above_limit_blows_up():
    dx, xs = grid(100)
    u0 = pulse(xs)
    assert abs(amplification_factor(1.01, math.pi)) == pytest.approx(1.02)
    big = [max(abs(v) for v in upwind(u0, 1.0, dx, 1.01 * dx, T).u) for T in (1.0, 5.0, 10.0)]
    assert big[0] > 2 and big[1] > 1e3 and big[2] > 1e7
    ok = upwind(u0, 1.0, dx, 0.99 * dx, 10.0).u
    assert max(abs(v) for v in ok) <= 1 + 1e-12


def test_wrong_direction_is_unstable():
    # downwind differencing U_j - nu (U_(j+1) - U_j) with a > 0 has g = 1 - nu (e^(i theta) - 1)
    nu = 0.5
    assert all(abs(1 - nu * (cmath.exp(1j * t) - 1)) > 1 for t in (0.1, 1.0, 3.0))
    # the upwind choice for a < 0 is the mirror image and is stable
    assert all(abs(amplification_factor(-nu, t)) <= 1 for t in (0.1, 1.0, 3.0))


def test_steps_edge_cases():
    dx, xs = grid(10)
    u0 = pulse(xs)
    r = upwind(u0, 1.0, dx, 0.5 * dx, 0.0)
    assert r.steps == 0 and r.u == u0
    r = upwind(u0, 1.0, dx, 10.0, 0.05)  # dt larger than the interval: one short step, nu = 0.5
    assert r.steps == 1 and r.t == 0.05
    assert step_count(1.0, 0.3) == 4 and step_count(0.9, 0.3) == 3
    with pytest.raises(ValueError):
        upwind(u0, 1.0, dx, 0.0, 1.0)
    with pytest.raises(ValueError):
        upwind([], 1.0, dx, 0.1, 1.0)


def test_burgers_shock_speed_conservative_vs_not():
    dx, xs = grid(200)
    u0 = [1.0 if x < 0.25 else 0.0 for x in xs]
    r = upwind_conservative(u0, lambda v: v * v / 2, dx, 0.5 * dx, 0.5)
    front = next(x for x, v in zip(xs, r.u) if v < 0.5)
    assert abs(front - 0.5) < 3 * dx  # Rankine-Hugoniot speed 1/2
    assert r.flux_evals == 200 * r.steps
    nc = upwind_nonconservative_burgers(u0, dx, 0.5 * dx, 0.5)
    front = next(x for x, v in zip(xs, nc) if v < 0.5)
    assert abs(front - 0.25) < 3 * dx  # the non-conservative scheme never moves the shock


def test_roe_flux_keeps_an_expansion_shock():
    dx, xs = grid(200)
    u0 = [-1.0 if x < 0.5 else 1.0 for x in xs]
    r = upwind_conservative(u0, lambda v: v * v / 2, dx, 0.5 * dx, 0.25)
    assert r.u == u0  # the entropy solution is a rarefaction fan, the scheme does not see it
