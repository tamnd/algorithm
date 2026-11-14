# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-spending-function/. The authors are listed in prov/9MKH4V.jsonl.
import math
import random

import pytest

from alpha_spending_function import (
    crossing_by_stage,
    hsd_spending,
    norm_quantile,
    obf_spending,
    pocock_spending,
    power_spending,
    spending_boundaries,
)

TIMES = [0.2, 0.4, 0.6, 0.8, 1.0]


def phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def upper(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def second_look_mass(c1: float, c2: float, t1: float, n: int = 400) -> float:
    """P(|Z1| < c1, |Z2| >= c2) by a 1-D Simpson rule, with Z2 | Z1 = z ~ N(sqrt(t1) z, 1 - t1)."""
    s, v = math.sqrt(t1), math.sqrt(1.0 - t1)
    h = 2.0 * c1 / n
    acc = 0.0
    for i in range(n + 1):
        z = -c1 + i * h
        w = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        acc += w * phi(z) * (upper((c2 - s * z) / v) + upper((c2 + s * z) / v))
    return acc * h / 3.0


def test_spending_functions_end_at_alpha():
    for f in (obf_spending(0.05), pocock_spending(0.05), power_spending(0.05, 2.0), hsd_spending(0.05, -4.0),
              hsd_spending(0.05, 0.0)):
        assert f(0.0) == pytest.approx(0.0, abs=1e-15)
        assert f(1.0) == pytest.approx(0.05, abs=1e-12)
        values = [f(t / 20) for t in range(21)]
        assert all(a <= b for a, b in zip(values, values[1:]))


def test_worked_example_obf_type():
    c = spending_boundaries(obf_spending(0.05), TIMES)
    expected = [4.3826, 3.0997, 2.5534, 2.2538, 2.0635]
    assert all(abs(a - b) < 1e-4 for a, b in zip(c, expected))


def test_per_tail_convention_gives_the_software_table():
    # Spending 2 - 2 Phi(z_(1 - 0.025/2) / sqrt t) in each tail.
    g = obf_spending(0.025)
    c = spending_boundaries(lambda t: 2.0 * g(t), TIMES)
    expected = [4.8769, 3.3570, 2.6803, 2.2898, 2.0310]
    assert all(abs(a - b) < 1e-4 for a, b in zip(c, expected))


@pytest.mark.parametrize("f", [obf_spending(0.05), pocock_spending(0.05), power_spending(0.05, 3.0),
                               hsd_spending(0.05, 1.0)])
def test_each_stage_spends_its_increment(f):
    c = spending_boundaries(f, TIMES)
    stage = crossing_by_stage(c, TIMES)
    prev = 0.0
    for t, p in zip(TIMES, stage):
        assert abs(p - (f(t) - prev)) < 1e-8
        prev = f(t)
    assert abs(sum(stage) - 0.05) < 1e-8


def test_one_look_is_fixed_sample():
    c = spending_boundaries(power_spending(0.05, 1.0), [1.0])
    assert abs(c[0] - norm_quantile(0.975)) < 1e-12


def test_two_looks_against_quadrature():
    f = obf_spending(0.05)
    c1, c2 = spending_boundaries(f, [0.5, 1.0])
    assert abs(c1 - norm_quantile(1.0 - f(0.5) / 2.0)) < 1e-12
    assert abs(second_look_mass(c1, c2, 0.5) - (0.05 - f(0.5))) < 1e-7


def test_random_two_look_designs_against_quadrature():
    rng = random.Random(1983)
    for _ in range(500):
        t1 = rng.uniform(0.15, 0.85)
        alpha = rng.uniform(0.01, 0.1)
        rho = rng.uniform(0.5, 4.0)
        f = power_spending(alpha, rho)
        c1, c2 = spending_boundaries(f, [t1, 1.0])
        # Both sides use Simpson grids; their discretization errors stay below 1e-7.
        assert abs(second_look_mass(c1, c2, t1) - (f(1.0) - f(t1))) < 1e-7


def test_unplanned_times_keep_the_level():
    f = obf_spending(0.05)
    for times in ([0.3, 0.7, 1.0], [0.1, 0.25, 0.5, 0.55, 1.0], [0.9, 1.0]):
        c = spending_boundaries(f, times)
        assert abs(sum(crossing_by_stage(c, times)) - 0.05) < 1e-8


def test_bad_input():
    with pytest.raises(ValueError):
        spending_boundaries(obf_spending(0.05), [0.5, 0.5])
    with pytest.raises(ValueError):
        spending_boundaries(lambda t: 0.0, [0.5, 1.0])
    with pytest.raises(ValueError):
        power_spending(0.05, 0.0)
