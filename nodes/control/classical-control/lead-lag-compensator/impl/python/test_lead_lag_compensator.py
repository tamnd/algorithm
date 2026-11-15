# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lead-lag-compensator/. The authors are listed in prov/8T0JHX.jsonl.

import math
import random

import pytest

import ctlmat as cm
from lead_lag_compensator import (
    alpha_for_phase,
    closed_loop_poles,
    design,
    design_lag,
    freq,
    lag,
    lead,
    margins,
    max_lead,
    phase_deg,
    place_lead,
    series,
)

PLANT = ([10.0], [1.0, 1.0, 0.0])


def test_ctlmat_self_test():
    assert cm._self_test()


def test_dc_and_high_frequency_gain():
    num, den = lead(4.0, 0.5)
    assert freq(num, den, 0.0) == 1.0
    assert abs(freq(num, den, 1e9) - 4.0) < 1e-6
    num, den = lag(8.0, 2.0)
    assert freq(num, den, 0.0) == 1.0
    assert abs(freq(num, den, 1e9) - 1.0 / 8.0) < 1e-6


@pytest.mark.parametrize("alpha", [1.5, 2.0, 4.0, 10.0, 100.0])
def test_max_lead_formula_against_sweep(alpha):
    T = 0.7
    num, den = lead(alpha, T)
    phi, wm, gain = max_lead(alpha, T)
    best = max((phase_deg(num, den, 10 ** (k / 2000.0)), 10 ** (k / 2000.0)) for k in range(-8000, 8001))
    assert abs(best[0] - phi) < 1e-5
    assert abs(math.log(best[1] / wm)) < 2e-3
    assert abs(abs(freq(num, den, wm)) - gain) < 1e-12
    assert abs(wm - math.sqrt((1 / T) * (1 / (alpha * T)))) < 1e-12


def test_known_lead_angles():
    assert abs(max_lead(2.0, 1.0)[0] - 19.4712206) < 1e-6
    assert abs(max_lead(4.0, 1.0)[0] - 36.8698976) < 1e-6
    assert abs(max_lead(10.0, 1.0)[0] - 54.9031988) < 1e-6
    assert abs(max_lead(10.0, 1.0)[1] - 0.316227766) < 1e-9


def test_alpha_for_phase_inverts_max_lead():
    rng = random.Random(8)
    for _ in range(50):
        phi = rng.uniform(1.0, 85.0)
        alpha = alpha_for_phase(phi)
        assert abs(max_lead(alpha, 1.0)[0] - phi) < 1e-9


def test_lag_is_inverse_of_lead():
    rng = random.Random(80)
    for _ in range(20):
        r = rng.uniform(1.5, 30.0)
        T = rng.uniform(0.1, 10.0)
        a, b = lead(r, T)
        c, d = lag(r, T)
        for w in (0.01, 0.3, 1.0, 7.0):
            assert abs(freq(a, b, w) * freq(c, d, w) - 1.0) < 1e-12
            assert abs(phase_deg(a, b, w) + phase_deg(c, d, w)) < 1e-9


def test_check_loop_margins():
    m = margins([1.0], [1.0, 3.0, 2.0, 0.0])
    assert abs(m["pm"] - 53.4108) < 1e-3
    assert abs(m["wgc"][0] - 0.445748) < 1e-5
    assert abs(m["gm"] - 6.0) < 1e-9
    assert abs(m["wpc"][0] - math.sqrt(2.0)) < 1e-9


def test_three_lags_gain_margin():
    m = margins([3.0], [1.0, 3.0, 3.0, 1.0])
    assert abs(m["gm"] - 8.0 / 3.0) < 1e-9
    assert abs(m["wpc"][0] - math.sqrt(3.0)) < 1e-9


def test_uncompensated_plant():
    m = margins(*PLANT)
    assert abs(m["wgc"][0] - 3.08423) < 1e-5
    assert abs(m["pm"] - 17.9642) < 1e-3
    assert m["gm"] == math.inf
    assert abs(m["ms"] - 3.35157) < 1e-5


def test_lead_example():
    cn, cd, wm, T = place_lead(*PLANT, 4.0)
    assert abs(wm - math.sqrt((-1.0 + math.sqrt(1601.0)) / 2.0)) < 1e-9
    assert abs(T - 0.113210) < 1e-6
    assert abs(phase_deg(*PLANT, wm) + 90.0 + math.degrees(math.atan(wm))) < 1e-9
    L = series(PLANT, (cn, cd))
    m = margins(*L)
    assert len(m["wgc"]) == 1
    assert abs(m["wgc"][0] - wm) < 1e-9
    assert abs(m["pm"] - 49.6276) < 1e-3
    assert abs(m["ms"] - 1.42139) < 1e-5
    assert all(p.real < 0 for p in closed_loop_poles(*L))


def test_lag_example():
    cn, cd, wc, beta, T = design_lag(*PLANT, 50.0)
    assert abs(wc - math.tan(math.radians(35.0))) < 1e-9
    assert abs(beta - 11.6987) < 1e-4
    assert abs(T - 14.2815) < 1e-4
    L = series(PLANT, (cn, cd))
    m = margins(*L)
    assert abs(m["wgc"][0] - 0.702794) < 1e-5
    assert abs(m["pm"] - 49.6989) < 1e-3
    assert abs(m["ms"] - 1.48123) < 1e-5
    poles = closed_loop_poles(*L)
    assert all(p.real < 0 for p in poles)
    slow = max(p.real for p in poles)
    assert abs(slow + 0.075732) < 1e-5


def test_lead_crossover_is_omega_m_random():
    rng = random.Random(8030)
    for _ in range(10):
        k = rng.uniform(2.0, 50.0)
        alpha = rng.uniform(2.0, 15.0)
        plant = ([k], [1.0, 1.0, 0.0])
        cn, cd, wm, T = place_lead(*plant, alpha)
        L = series(plant, (cn, cd))
        m = margins(*L)
        assert abs(m["wgc"][-1] - wm) < 1e-7 * wm
        phi = max_lead(alpha, T)[0]
        assert abs(m["pm"] - (180.0 + phase_deg(*plant, wm) + phi)) < 1e-7


def test_design_lead_meets_margin():
    cn, cd = design(*PLANT, 45.0)
    alpha = cn[0] / cd[0]
    assert abs(max_lead(alpha, cd[0])[0] - (45.0 - 17.9642 + 10.0)) < 1e-3
    m = margins(*series(PLANT, (cn, cd)))
    assert m["pm"] >= 45.0
    assert abs(m["pm"] - 49.7) < 0.2


def test_design_lag_matches_example():
    cn, cd = design(*PLANT, 50.0, kind="lag")
    cn2, cd2, wc, beta, T = design_lag(*PLANT, 50.0)
    assert max(abs(x - y) for x, y in zip(cn + cd, cn2 + cd2)) < 1e-9


def test_design_returns_one_when_margin_is_met():
    assert design([1.0], [1.0, 3.0, 2.0, 0.0], 45.0) == ([1.0], [1.0])


def test_bad_input():
    with pytest.raises(ValueError):
        design(*PLANT, 45.0, kind="notch")
    with pytest.raises(ValueError):
        lead(1.0, 1.0)
    with pytest.raises(ValueError):
        lead(2.0, 0.0)
    with pytest.raises(ValueError):
        lag(0.5, 1.0)
    with pytest.raises(ValueError):
        alpha_for_phase(90.0)
    with pytest.raises(ValueError):
        design_lag(*PLANT, 0.0)
    with pytest.raises(ValueError):
        design_lag([0.1], [1.0, 1.0, 0.0], 50.0)
    with pytest.raises(ValueError):
        place_lead([1.0], [1.0, 1.0], 1e9)
