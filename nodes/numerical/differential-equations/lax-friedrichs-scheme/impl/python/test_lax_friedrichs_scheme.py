# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lax-friedrichs-scheme/. The authors are listed in prov/5WKGZC.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from lax_friedrichs_scheme import amplification_factor, lax_friedrichs, lf_step, step_count


def l1(u, ex, dx):
    return dx * sum(abs(a - b) for a, b in zip(u, ex))


def sine_error(m, nu, t_end=0.5):
    dx = 1 / m
    u0 = [math.sin(2 * math.pi * j * dx) for j in range(m)]
    r = lax_friedrichs(u0, lambda v: v, dx, nu * dx, t_end)
    return l1(r.u, [math.sin(2 * math.pi * (j * dx - t_end)) for j in range(m)], dx)


def test_observed_order_one_at_fixed_courant_number():
    errs = [sine_error(m, 0.5) for m in (100, 200, 400, 800)]
    assert [round(e, 6) for e in errs] == [0.087644, 0.045427, 0.023132, 0.011673]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(0.9 < p < 1.1 for p in orders)


def test_error_grows_as_courant_number_shrinks():
    e = [sine_error(200, nu) for nu in (0.1, 0.25, 0.5, 0.9)]
    assert e[0] > e[1] > e[2] > e[3]
    assert sine_error(200, 1.0) < 1e-13  # nu = 1 is the exact shift


def test_nu_one_is_exact_shift_and_negative_speed():
    u0 = [Fraction(j * j % 7) for j in range(9)]
    r = lax_friedrichs(u0, lambda v: v, Fraction(1, 9), Fraction(1, 9), Fraction(2, 9))
    assert r.u == u0[-2:] + u0[:-2]
    r = lax_friedrichs(u0, lambda v: -v, Fraction(1, 9), Fraction(1, 9), Fraction(1, 9))
    assert r.u == u0[1:] + u0[:1]


def test_conservation_exact_with_fractions():
    rng = random.Random(3)
    u0 = [Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(17)]
    r = lax_friedrichs(u0, lambda v: v * v / 2, Fraction(1, 17), Fraction(1, 40), Fraction(1, 4))
    assert sum(r.u) == sum(u0)


def test_maximum_principle_on_step_data():
    for nu in (0.2, 0.5, 0.8, 1.0):
        m = 120
        dx = 1 / m
        u0 = [1.0 if 0.25 <= j * dx < 0.5 else 0.0 for j in range(m)]
        r = lax_friedrichs(u0, lambda v: v, dx, nu * dx, 0.5)
        assert min(r.u) >= -1e-15 and max(r.u) <= 1 + 1e-15


def test_courant_number_just_above_and_below_one():
    rng = random.Random(1)
    m = 100
    dx = 1 / m
    u0 = [math.sin(2 * math.pi * j * dx) + 1e-3 * rng.random() for j in range(m)]
    below = lax_friedrichs(u0, lambda v: v, dx, 0.95 * dx, 5.0)
    above = lax_friedrichs(u0, lambda v: v, dx, 1.05 * dx, 5.0)
    assert max(abs(v) for v in below.u) <= max(abs(v) for v in u0)
    assert max(abs(v) for v in above.u) > 1e5


def test_amplification_factor_matches_one_step():
    m, nu = 16, 0.6
    for k in range(m):
        theta = 2 * math.pi * k / m
        mode = [cmath.exp(1j * theta * j) for j in range(m)]
        out = lf_step(mode, lambda v: nu * v, 1.0, "periodic")
        g = amplification_factor(nu, theta)
        assert all(abs(out[j] - g * mode[j]) < 1e-12 for j in range(m))
        assert abs(g) ** 2 == pytest.approx(math.cos(theta) ** 2 + nu ** 2 * math.sin(theta) ** 2)


def test_checkerboard_mode_is_not_damped():
    u0 = [(-1) ** j * 1.0 for j in range(10)]
    r = lax_friedrichs(u0, lambda v: 0.3 * v, 0.1, 0.1, 0.3)
    assert r.u == [(-1) ** (j + 1) * 1.0 for j in range(10)]


def test_burgers_shock_speed_and_rarefaction():
    m, dx = 200, 1 / 200
    dt = 0.8 * dx
    u0 = [1.0 if (j + 0.5) * dx < 0.3 else 0.0 for j in range(m)]
    r = lax_friedrichs(u0, lambda v: v * v / 2, dx, dt, 0.4, bc="transmissive")
    ex = [1.0 if (j + 0.5) * dx < 0.5 else 0.0 for j in range(m)]
    assert l1(r.u, ex, dx) < 0.01
    u0 = [0.0 if (j + 0.5) * dx < 0.3 else 1.0 for j in range(m)]
    r = lax_friedrichs(u0, lambda v: v * v / 2, dx, dt, 0.4, bc="transmissive")
    fan = lambda x: min(1.0, max(0.0, (x - 0.3) / 0.4))
    assert l1(r.u, [fan((j + 0.5) * dx) for j in range(m)], dx) < 0.03


def test_edge_cases():
    u0 = [1.0, 2.0, 3.0]
    r = lax_friedrichs(u0, lambda v: v, 0.1, 0.05, 0.0)
    assert r.steps == 0 and r.u == u0 and r.flux_evals == 0
    r = lax_friedrichs(u0, lambda v: v, 1.0, 5.0, 0.5)  # dt larger than the interval: one step
    assert r.steps == 1 and r.t == 0.5
    r = lax_friedrichs([Fraction(1)] * 4, lambda v: v, Fraction(1, 4), Fraction(1, 10), Fraction(1, 4))
    assert r.steps == 3 and r.t == Fraction(1, 4) and r.u == [1, 1, 1, 1]
    assert step_count(0.3, 0.1) == 3
    assert lax_friedrichs([5.0], lambda v: v, 1.0, 0.5, 1.0).u == [5.0]
    with pytest.raises(ValueError):
        lax_friedrichs(u0, lambda v: v, 0.1, 0.05, 1.0, bc="reflect")
    with pytest.raises(ValueError):
        step_count(1.0, 0.0)
