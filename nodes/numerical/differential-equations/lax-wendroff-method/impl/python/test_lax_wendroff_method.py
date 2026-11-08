# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lax-wendroff-method/. The authors are listed in prov/N95ZRW.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from lax_wendroff_method import (amplification_factor, lax_wendroff, lw_linear_step, lw_step,
                                 step_count)


def l1(u, ex, dx):
    return dx * sum(abs(a - b) for a, b in zip(u, ex))


def test_observed_order_two_on_sine():
    errs = []
    for m in (100, 200, 400, 800):
        dx = 1 / m
        u0 = [math.sin(2 * math.pi * j * dx) for j in range(m)]
        r = lax_wendroff(u0, lambda v: v, dx, 0.5 * dx, 0.5)
        errs.append(l1(r.u, [math.sin(2 * math.pi * (j * dx - 0.5)) for j in range(m)], dx))
    assert [float("%.5g" % e) for e in errs] == [0.00098687, 0.00024673, 6.1685e-05, 1.5421e-05]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(abs(p - 2) < 0.02 for p in orders)


def test_two_step_equals_one_step_for_linear_flux_exactly():
    rng = random.Random(5)
    u = [Fraction(rng.randint(-9, 9)) for _ in range(11)]
    for nu in (Fraction(1, 3), Fraction(-3, 4), Fraction(1)):
        assert lw_step(u, lambda v: nu * v, Fraction(1)) == lw_linear_step(u, nu)


def test_nu_one_exact_shift_and_conservation():
    u0 = [Fraction(j * j % 5) for j in range(7)]
    r = lax_wendroff(u0, lambda v: v, Fraction(1, 7), Fraction(1, 7), Fraction(3, 7))
    assert r.u == u0[-3:] + u0[:-3]
    rng = random.Random(2)
    u0 = [Fraction(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(13)]
    r = lax_wendroff(u0, lambda v: v * v / 2, Fraction(1, 13), Fraction(1, 50), Fraction(3, 50))  # 3 steps: exact numbers grow fast
    assert sum(r.u) == sum(u0)


def test_amplification_factor():
    m, nu = 16, 0.7
    for k in range(m):
        theta = 2 * math.pi * k / m
        mode = [cmath.exp(1j * theta * j) for j in range(m)]
        out = lw_linear_step(mode, nu)
        g = amplification_factor(nu, theta)
        assert all(abs(out[j] - g * mode[j]) < 1e-12 for j in range(m))
        want = 1 - nu ** 2 * (1 - nu ** 2) * (1 - math.cos(theta)) ** 2
        assert abs(g) ** 2 == pytest.approx(want)


def test_courant_number_just_above_and_below_one():
    rng = random.Random(1)
    m = 100
    dx = 1 / m
    u0 = [math.sin(2 * math.pi * j * dx) + 1e-3 * rng.random() for j in range(m)]
    below = lax_wendroff(u0, lambda v: v, dx, 0.99 * dx, 5.0)
    above = lax_wendroff(u0, lambda v: v, dx, 1.01 * dx, 5.0)
    assert max(abs(v) for v in below.u) < 1.001
    assert max(abs(v) for v in above.u) > 1e3


def test_oscillations_at_a_step():
    m = 200
    dx = 1 / m
    u0 = [1.0 if 0.25 <= j * dx < 0.5 else 0.0 for j in range(m)]
    r = lax_wendroff(u0, lambda v: v, dx, 0.5 * dx, 0.5)
    assert max(r.u) > 1.2 and min(r.u) < -0.2


def test_phase_lag_of_a_pulse():
    m = 100
    dx = 1 / m
    u0 = [math.exp(-100 * (j * dx - 0.5) ** 2) for j in range(m)]
    r = lax_wendroff(u0, lambda v: v, dx, 0.5 * dx, 1.0)
    peak = max(range(m), key=lambda j: r.u[j])
    assert peak == 49  # one cell behind the exact peak at x = 0.5


def test_burgers_shock_position():
    m, dx = 200, 1 / 200
    u0 = [1.0 if (j + 0.5) * dx < 0.3 else 0.0 for j in range(m)]
    r = lax_wendroff(u0, lambda v: v * v / 2, dx, 0.8 * dx, 0.4, bc="transmissive")
    ex = [1.0 if (j + 0.5) * dx < 0.5 else 0.0 for j in range(m)]
    assert l1(r.u, ex, dx) < 0.005
    assert max(r.u) > 1.1  # overshoot behind the shock


def test_edge_cases():
    u0 = [1.0, 2.0, 3.0]
    r = lax_wendroff(u0, lambda v: v, 0.1, 0.05, 0.0)
    assert r.steps == 0 and r.u == u0 and r.flux_evals == 0
    r = lax_wendroff(u0, lambda v: v, 1.0, 5.0, 0.5)
    assert r.steps == 1 and r.t == 0.5 and r.flux_evals == 6
    r = lax_wendroff([Fraction(2)] * 5, lambda v: 3 * v, Fraction(1, 5), Fraction(1, 20), Fraction(1, 7))
    assert r.steps == 3 and r.t == Fraction(1, 7) and r.u == [2] * 5
    assert lax_wendroff([4.0], lambda v: v, 1.0, 0.5, 1.0).u == [4.0]
    assert step_count(0.3, 0.1) == 3
    with pytest.raises(ValueError):
        lax_wendroff(u0, lambda v: v, 0.1, 0.05, 1.0, bc="wall")
    with pytest.raises(ValueError):
        step_count(-1.0, 0.1)
