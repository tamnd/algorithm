# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bennett-acceptance-ratio/. The authors are listed in prov/Y2JYEC.jsonl.
import math
import random

import pytest

from bennett_acceptance_ratio import (
    bar,
    bar_error,
    bar_residual,
    fep_forward,
    fep_reverse,
    fermi,
)

EXACT = 0.5 * math.log(2.0)  # U_0 = x^2 / 2, U_1 = x^2, kT = 1


def harmonic(n0, n1, rng):
    wf = [0.5 * rng.gauss(0.0, 1.0) ** 2 for _ in range(n0)]
    wr = [-0.5 * rng.gauss(0.0, math.sqrt(0.5)) ** 2 for _ in range(n1)]
    return wf, wr


def test_fermi_function():
    assert fermi(0.0) == 0.5
    assert fermi(800.0) == pytest.approx(0.0, abs=1e-300)
    assert fermi(-800.0) == 1.0
    assert fermi(1.3) + fermi(-1.3) == pytest.approx(1.0, abs=1e-15)


def test_one_sample_in_each_state_gives_the_mean_of_the_two_differences():
    # U_1 - U_0 is 1.0 at the state-0 sample and 0.2 at the state-1 sample.
    assert bar([1.0], [-0.2]) == pytest.approx(0.6, abs=1e-9)


def test_constant_difference_is_exact():
    assert bar([1.7] * 5, [-1.7] * 3) == pytest.approx(1.7, abs=1e-9)


def test_swapping_the_states_changes_the_sign():
    wf, wr = harmonic(50, 70, random.Random(7))
    assert bar(wr, wf) == pytest.approx(-bar(wf, wr), abs=1e-9)


def test_root_solves_the_bennett_equation_and_residual_is_monotone():
    wf, wr = harmonic(40, 60, random.Random(8))
    da = bar(wf, wr)
    c = da + math.log(60 / 40)
    assert abs(bar_residual(wf, wr, c)) < 1e-7
    cs = [-5 + 0.5 * i for i in range(21)]
    rs = [bar_residual(wf, wr, x) for x in cs]
    assert all(a > b for a, b in zip(rs, rs[1:]))


def test_harmonic_wells_against_exact_value():
    wf, wr = harmonic(1000, 1000, random.Random(1))
    da = bar(wf, wr)
    se = bar_error(wf, wr, 1.0, da)
    assert abs(da - EXACT) < 4 * se
    assert se < 0.012


def test_unequal_sample_sizes():
    wf, wr = harmonic(3000, 300, random.Random(5))
    da = bar(wf, wr)
    assert abs(da - EXACT) < 4 * bar_error(wf, wr, 1.0, da)


def test_temperature_scaling():
    kT = 2.5
    beta = 1.0 / kT
    rng = random.Random(9)
    # reduced differences beta * (U_1 - U_0) do not depend on kT for these wells
    xs0 = [rng.gauss(0.0, math.sqrt(kT)) for _ in range(800)]
    xs1 = [rng.gauss(0.0, math.sqrt(kT / 2)) for _ in range(800)]
    wf = [beta * 0.5 * x * x for x in xs0]
    wr = [-beta * 0.5 * x * x for x in xs1]
    da = bar(wf, wr, beta)
    assert abs(da - kT * EXACT) < 4 * bar_error(wf, wr, beta, da)


def test_lower_spread_than_either_one_sided_estimate():
    rng = random.Random(4)
    b, f, r = [], [], []
    for _ in range(200):
        wf, wr = harmonic(50, 50, rng)
        b.append(bar(wf, wr))
        f.append(fep_forward(wf))
        r.append(fep_reverse(wr))

    def sd(v):
        m = sum(v) / len(v)
        return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))

    assert sd(b) < sd(f) < sd(r)
    assert abs(sum(b) / len(b) - EXACT) < 4 * sd(b) / math.sqrt(len(b))


def test_error_formula_matches_spread_over_replicas():
    rng = random.Random(6)
    vals, ses = [], []
    for _ in range(150):
        wf, wr = harmonic(200, 200, rng)
        da = bar(wf, wr)
        vals.append(da)
        ses.append(bar_error(wf, wr, 1.0, da))
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))
    assert sum(ses) / len(ses) == pytest.approx(sd, rel=0.25)


def test_poor_overlap_bar_stays_near_truth_while_forward_fep_fails():
    # Shift a unit well by a = 3; the exact answer is 0.
    a = 3.0
    rng = random.Random(1)
    x0 = [rng.gauss(0.0, 1.0) for _ in range(1000)]
    x1 = [a + rng.gauss(0.0, 1.0) for _ in range(1000)]
    wf = [0.5 * (x - a) ** 2 - 0.5 * x * x for x in x0]
    wr = [0.5 * x * x - 0.5 * (x - a) ** 2 for x in x1]
    da = bar(wf, wr)
    assert abs(da) < 4 * bar_error(wf, wr, 1.0, da)
    assert fep_forward(wf) > 0.5


def test_empty_input_raises():
    with pytest.raises(ValueError):
        bar([], [1.0])
    with pytest.raises(ValueError):
        bar([1.0], [])
