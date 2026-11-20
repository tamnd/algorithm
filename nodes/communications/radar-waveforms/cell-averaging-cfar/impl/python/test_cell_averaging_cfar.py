# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cell-averaging-cfar/. The authors are listed in prov/AFY7TQ.jsonl.

import math
import random
from fractions import Fraction

import pytest

from cbb import cn, wilson
from cell_averaging_cfar import (
    ca_cfar,
    ca_cfar_direct,
    detection_probability_swerling1,
    exact_tau,
    false_alarm_probability,
    threshold_factor,
)


def test_check_values():
    tau = threshold_factor(16, 1e-6)
    assert abs(tau - 1.37137) < 1e-5
    assert abs(16 * tau - 21.942) < 1e-3
    # Rohling 1983, Table I: the factor on the mean for Pfa = 1e-6.
    assert abs(32 * threshold_factor(32, 1e-6) - 17.28) < 5e-3
    assert abs(64 * threshold_factor(64, 1e-6) - 15.42) < 5e-3
    assert abs(false_alarm_probability(16, tau) - 1e-6) < 1e-15


def test_worked_example():
    x = [3, 1, 2, 2, 1, 30, 9, 2, 1, 3, 2, 1, 2]
    tau = threshold_factor(4, 1e-2)
    assert abs(tau - 2.16228) < 1e-5
    det, thr = ca_cfar(x, 4, 1, tau)
    assert det == [5]
    sums = [43, 14, 7, 7, 36, 42, 14]
    for i, z in zip(range(3, 10), sums):
        assert thr[i] == pytest.approx(tau * z, rel=1e-12)
    assert thr[:3] == [None] * 3 and thr[10:] == [None] * 3


def test_short_and_empty_inputs():
    assert ca_cfar([], 4, 1, 2.0) == ([], [])
    det, thr = ca_cfar([5, 1, 1, 1, 1, 1], 4, 1, 2.0)
    assert det == [] and thr == [None] * 6
    det, thr = ca_cfar([1, 1, 1, 9, 1, 1, 1], 6, 0, 1.0)
    assert det == [3] and thr[3] == 6
    with pytest.raises(ValueError):
        ca_cfar([1] * 10, 3, 1, 1.0)


def test_running_sum_equals_direct_sum_exactly():
    rng = random.Random(4101)
    for _ in range(600):
        n_ref = rng.choice([2, 4, 6, 8])
        guard = rng.randint(0, 3)
        x = [rng.randint(0, 20) for _ in range(rng.randint(0, 40))]
        tau = Fraction(rng.randint(1, 40), rng.randint(1, 20))
        assert ca_cfar(x, n_ref, guard, tau) == ca_cfar_direct(x, n_ref, guard, tau)


def test_scale_invariance_exact():
    rng = random.Random(4102)
    tau = exact_tau(8, Fraction(2, 3))
    for _ in range(200):
        x = [rng.randint(1, 30) for _ in range(30)]
        c = rng.randint(2, 1000)
        assert ca_cfar(x, 8, 2, tau)[0] == ca_cfar([c * v for v in x], 8, 2, tau)[0]


def gamma_pdf(z, n):
    return math.exp((n - 1) * math.log(z) - z - math.lgamma(n)) if z > 0 else 0.0


@pytest.mark.parametrize("n_ref,pfa", [(4, 1e-2), (16, 1e-6), (24, 1e-4)])
def test_pfa_closed_form_against_integral(n_ref, pfa):
    """Pfa = E exp(-tau Z) with Z ~ Gamma(N, 1), by Simpson's rule on [0, 120]."""
    tau = threshold_factor(n_ref, pfa)
    m, top = 6000, 120.0
    hstep = top / m
    s = 0.0
    for i in range(m + 1):
        z = i * hstep
        f = math.exp(-tau * z) * gamma_pdf(z, n_ref)
        s += f * (1 if i in (0, m) else (4 if i % 2 else 2))
    assert s * hstep / 3 == pytest.approx(pfa, rel=1e-6)


def square_law(rng, power):
    return abs(cn(rng, power)) ** 2


def false_alarms(rng, n_ref, guard, tau, power, trials):
    cells = n_ref + 2 * guard + 1
    mid = cells // 2
    k = 0
    for _ in range(trials):
        x = [square_law(rng, power) for _ in range(cells)]
        det, _ = ca_cfar(x, n_ref, guard, tau)
        k += det == [mid]
    return k


def test_false_alarm_rate_by_simulation_for_two_noise_powers():
    # N = 8, G = 1, design Pfa = 0.05; n = 4000 independent windows per noise
    # power, about 200 expected false alarms, seed 4103, Wilson z = 3.29.
    n_ref, guard, pfa, n = 8, 1, 0.05, 4000
    tau = threshold_factor(n_ref, pfa)
    rng = random.Random(4103)
    for power in (1.0, 50.0):
        k = false_alarms(rng, n_ref, guard, tau, power, n)
        lo, hi = wilson(k, n, 3.29)
        assert lo <= pfa <= hi


def test_swerling1_detection_probability_by_simulation():
    # N = 8, G = 1, Pfa = 0.05, mean SNR 10: Pd = (1 + tau / 11)^(-8) = 0.723.
    # n = 2000 windows (about 550 misses expected), seed 4104, Wilson z = 3.29.
    n_ref, guard, n, snr = 8, 1, 2000, 10.0
    tau = threshold_factor(n_ref, 0.05)
    pd = detection_probability_swerling1(n_ref, tau, snr)
    assert abs(pd - 0.723) < 1e-3
    rng = random.Random(4104)
    cells = n_ref + 2 * guard + 1
    mid = cells // 2
    k = 0
    for _ in range(n):
        x = [square_law(rng, 1.0) for _ in range(cells)]
        x[mid] = square_law(rng, 1.0 + snr)
        k += ca_cfar(x, n_ref, guard, tau)[0] == [mid]
    lo, hi = wilson(k, n, 3.29)
    assert lo <= pd <= hi


def test_masking_by_a_second_target():
    tau = threshold_factor(8, 1e-2)
    x = [2, 1, 3, 1, 2, 1, 2, 30, 1, 2, 24, 2, 1, 3, 1, 2, 1, 2]
    det, thr = ca_cfar(x, 8, 1, tau)
    assert 7 in det
    assert 10 not in det and thr[10] > 24
    alone = list(x)
    alone[7] = 2
    assert 10 in ca_cfar(alone, 8, 1, tau)[0]


def test_guard_cells_keep_target_spill_out_of_the_window():
    tau = threshold_factor(4, 1e-2)
    x = [2, 1, 2, 1, 2, 30, 25, 1, 2, 1, 2, 1]
    assert 5 not in ca_cfar(x, 4, 0, tau)[0]
    assert 5 in ca_cfar(x, 4, 1, tau)[0]
