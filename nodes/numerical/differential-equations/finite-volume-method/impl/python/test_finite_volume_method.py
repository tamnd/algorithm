# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-volume-method/. The authors are listed in prov/80XDHS.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from finite_volume_method import (cell_averages, finite_volume, rusanov_flux,
                                  total_variation, upwind_flux)

burgers = rusanov_flux(lambda v: v * v / 2, lambda v: v)


def test_worked_example_exact():
    u = [Fr(0), Fr(0), Fr(1), Fr(0), Fr(0)]
    r = finite_volume(u, Fr(1), Fr(1, 2), Fr(1), upwind_flux(1))
    assert r.u == [0, 0, Fr(1, 4), Fr(1, 2), Fr(1, 4)] and r.steps == 2 and r.flux_evals == 12
    r = finite_volume([Fr(1), Fr(1), Fr(0), Fr(0)], Fr(1), Fr(1, 2), Fr(1, 2), burgers,
                      bc="transmissive")
    assert r.u == [1, Fr(7, 8), Fr(3, 8), 0] and r.mass_change == Fr(1, 4)


def test_random_exact_conservation_fractions():
    rng = random.Random(3)
    for case in range(500):
        m = rng.randint(1, 8)
        u = [Fr(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(m)]
        dt = Fr(1, rng.randint(2, 8))
        t_end = dt * rng.randint(0, 3) + (Fr(1, 17) if rng.random() < 0.3 else 0)
        bc = rng.choice(["periodic", "transmissive"])
        r = finite_volume(u, Fr(1), dt, t_end, burgers, bc=bc)
        # sum of averages changes exactly by the boundary flux balance
        assert sum(r.u) - sum(u) == r.mass_change
        if bc == "periodic":
            assert sum(r.u) == sum(u)


def test_random_upwind_matches_difference_formula():
    rng = random.Random(4)
    for case in range(500):
        m = rng.randint(1, 10)
        a = rng.choice([1.0, -1.0]) * rng.uniform(0.1, 3.0)
        dx = rng.uniform(0.05, 1.0)
        nu = rng.uniform(0.0, 1.0)
        dt = nu * dx / abs(a)
        steps = rng.randint(0, 4)
        u = [rng.uniform(-1, 1) for _ in range(m)]
        r = finite_volume(u, dx, dt, steps * dt, upwind_flux(a))
        w = list(u)
        for _ in range(steps):
            if a > 0:
                w = [w[i] - nu * (w[i] - w[i - 1]) for i in range(m)]
            else:
                w = [w[i] + nu * (w[(i + 1) % m] - w[i]) for i in range(m)]
        assert r.u == pytest.approx(w, abs=1e-12)


def test_random_burgers_monotone_and_tvd_under_cfl():
    rng = random.Random(5)
    for case in range(500):
        m = rng.randint(2, 12)
        u = [rng.uniform(-2, 2) for _ in range(m)]
        smax = max(abs(v) for v in u) or 1.0
        dx = 1.0 / m
        dt = rng.uniform(0.1, 1.0) * dx / smax
        r = finite_volume(u, dx, dt, 3 * dt, burgers)
        assert min(u) - 1e-12 <= min(r.u) and max(r.u) <= max(u) + 1e-12
        assert total_variation(r.u) <= total_variation(u) + 1e-12


def test_exact_shift_at_courant_one():
    u = [float(i * i % 7) for i in range(9)]
    r = finite_volume(u, 0.5, 0.5, 1.5, upwind_flux(1.0))
    assert r.u == u[-3:] + u[:-3]


def test_first_order_convergence_smooth():
    errs = []
    for m in (50, 100, 200, 400):
        dx = 1 / m
        u = cell_averages(lambda x: math.sin(2 * math.pi * x), 0, 1, m)
        r = finite_volume(u, dx, 0.5 * dx, 1.0, upwind_flux(1.0))
        exact = cell_averages(lambda x: math.sin(2 * math.pi * (x - 1.0)), 0, 1, m)
        errs.append(dx * sum(abs(p - q) for p, q in zip(r.u, exact)))
    assert errs[0] == pytest.approx(0.11411, rel=1e-3)
    for k in range(3):
        assert 1.85 < errs[k] / errs[k + 1] < 2.05


def test_cfl_limit_just_above_and_below():
    rng = random.Random(6)
    m = 64
    u = [rng.uniform(-1, 1) for _ in range(m)]
    below = finite_volume(u, 1.0, 0.99, 400 * 0.99, upwind_flux(1.0))
    assert max(abs(v) for v in below.u) <= 1.0
    above = finite_volume(u, 1.0, 1.05, 400 * 1.05, upwind_flux(1.0))
    assert max(abs(v) for v in above.u) > 1e3


def test_edge_cases():
    assert finite_volume([], 1.0, 0.1, 1.0, burgers).u == []
    r = finite_volume([1.0, 2.0], 1.0, 0.1, 0.0, burgers)
    assert r.u == [1.0, 2.0] and r.steps == 0
    # dt larger than the whole interval: one shortened step
    r = finite_volume([0.0, 1.0, 0.0], 1.0, 10.0, 0.25, upwind_flux(1.0))
    assert r.steps == 1 and r.u == pytest.approx([0.0, 0.75, 0.25])
    # off-grid final time: 0.3 = 0.125 + 0.125 + 0.05
    r = finite_volume([0.0, 1.0, 0.0, 0.0], 1.0, 0.125, 0.3, upwind_flux(1.0))
    assert r.steps == 3 and sum(r.u) == pytest.approx(1.0)
    # single cell, periodic: stays constant
    assert finite_volume([Fr(3)], Fr(1), Fr(1, 2), Fr(2), burgers).u == [3]
    with pytest.raises(ValueError):
        finite_volume([1.0], 0.0, 0.1, 1.0, burgers)
    with pytest.raises(ValueError):
        finite_volume([1.0], 1.0, 0.1, 1.0, burgers, bc="reflect")
