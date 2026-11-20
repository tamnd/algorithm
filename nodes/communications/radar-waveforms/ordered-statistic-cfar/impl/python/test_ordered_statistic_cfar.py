# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-statistic-cfar/. The authors are listed in prov/3GCSWG.jsonl.

import math
import random
from fractions import Fraction

import pytest

from cbb import cn, wilson
from ordered_statistic_cfar import (
    detection_probability_swerling1,
    false_alarm_probability,
    false_alarm_probability_rohling,
    mean_order_statistic,
    os_cfar,
    os_cfar_direct,
    threshold_factor,
)


@pytest.mark.parametrize("n_ref,k,t", [(16, 12, 20.9), (24, 18, 16.3), (32, 24, 14.4), (8, 6, 46.7)])
def test_rohling_table_values(n_ref, k, t):
    """Rohling 1983, Table II: T for Pfa = 1e-6, to the one decimal printed there."""
    assert abs(threshold_factor(n_ref, k, 1e-6) - t) < 0.06


@pytest.mark.parametrize("n_ref,k,adt", [(16, 12, 27.2), (24, 18, 21.6), (32, 24, 19.3)])
def test_rohling_average_threshold(n_ref, k, adt):
    """Rohling 1983, Table IV: the average threshold T E X_(k) / mu for k = 3N/4."""
    t = threshold_factor(n_ref, k, 1e-6)
    assert abs(t * mean_order_statistic(n_ref, k) - adt) < 0.06


def test_product_equals_rohling_equation_14_exactly():
    for n_ref in range(1, 13):
        for k in range(1, n_ref + 1):
            for t in range(0, 15):
                assert false_alarm_probability(n_ref, k, t) == false_alarm_probability_rohling(n_ref, k, t)


def os_density(x, n_ref, k):
    """The density of X_(k) for N i.i.d. unit exponentials."""
    return k * math.comb(n_ref, k) * (1 - math.exp(-x)) ** (k - 1) * math.exp(-x * (n_ref - k + 1))


@pytest.mark.parametrize("n_ref,k,t", [(8, 6, 5.87), (16, 12, 20.95), (24, 3, 4.0)])
def test_pfa_against_integral(n_ref, k, t):
    """Pfa = E exp(-T X_(k)), by Simpson's rule on [0, 20]."""
    m, top = 20000, 20.0
    hstep = top / m
    s = 0.0
    for i in range(m + 1):
        x = i * hstep
        s += math.exp(-t * x) * os_density(x, n_ref, k) * (1 if i in (0, m) else (4 if i % 2 else 2))
    assert s * hstep / 3 == pytest.approx(false_alarm_probability(n_ref, k, t), rel=1e-6)


def test_worked_example():
    x = [2, 1, 3, 1, 2, 1, 2, 30, 1, 2, 24, 2, 1, 3, 1, 2, 1, 2]
    t = threshold_factor(8, 6, 1e-2)
    assert abs(t - 5.8696) < 1e-4
    det, thr = os_cfar(x, 8, 1, 6, t)
    assert det == [7, 10]
    assert thr[5] == pytest.approx(3 * t) and thr[10] == pytest.approx(2 * t)


def test_edges_and_bad_arguments():
    assert os_cfar([], 4, 1, 3, 2.0) == ([], [])
    assert os_cfar([1] * 6, 4, 1, 3, 2.0) == ([], [None] * 6)
    with pytest.raises(ValueError):
        os_cfar([1] * 10, 4, 1, 5, 2.0)
    with pytest.raises(ValueError):
        os_cfar([1] * 10, 5, 1, 2, 2.0)


def test_sliding_window_equals_sorting_each_window_exactly():
    rng = random.Random(5101)
    for _ in range(600):
        n_ref = rng.choice([2, 4, 6, 8, 10])
        guard = rng.randint(0, 3)
        k = rng.randint(1, n_ref)
        x = [rng.randint(0, 12) for _ in range(rng.randint(0, 40))]
        t = Fraction(rng.randint(1, 50), rng.randint(1, 10))
        assert os_cfar(x, n_ref, guard, k, t) == os_cfar_direct(x, n_ref, guard, k, t)


def test_up_to_n_minus_k_interferers_leave_a_noise_value_as_threshold():
    """With r <= N - k strong interferers, X_(k) is the k-th smallest of the N - r noise cells."""
    rng = random.Random(5102)
    n_ref, guard, k, big = 16, 1, 12, 10 ** 6
    i = guard + n_ref // 2
    for _ in range(300):
        x = [rng.randint(1, 10) for _ in range(2 * guard + n_ref + 1)]
        ref = [j for j in range(len(x)) if abs(j - i) > guard]
        r = rng.randint(0, n_ref - k + 1)
        hit = set(rng.sample(ref, r))
        y = [big if j in hit else v for j, v in enumerate(x)]
        thr = os_cfar(y, n_ref, guard, k, 3)[1][i]
        if r <= n_ref - k:
            noise = sorted(x[j] for j in ref if j not in hit)
            assert thr == 3 * noise[k - 1] and thr <= 30
        else:
            assert thr == 3 * big


def square_law(rng, power):
    return abs(cn(rng, power)) ** 2


def test_false_alarm_rate_by_simulation_for_two_noise_powers():
    # N = 8, k = 6, G = 1, design Pfa = 0.05; n = 4000 independent windows per
    # noise power, about 200 expected false alarms, seed 5103, Wilson z = 3.29.
    n_ref, k, guard, pfa, n = 8, 6, 1, 0.05, 4000
    t = threshold_factor(n_ref, k, pfa)
    rng = random.Random(5103)
    cells = n_ref + 2 * guard + 1
    for power in (1.0, 50.0):
        hits = 0
        for _ in range(n):
            x = [square_law(rng, power) for _ in range(cells)]
            hits += os_cfar(x, n_ref, guard, k, t)[0] == [cells // 2]
        lo, hi = wilson(hits, n, 3.29)
        assert lo <= pfa <= hi


def test_swerling1_detection_probability_by_simulation():
    # N = 8, k = 6, G = 1, Pfa = 0.05, mean SNR 10; n = 2000 windows, seed 5104.
    n_ref, k, guard, n, snr = 8, 6, 1, 2000, 10.0
    t = threshold_factor(n_ref, k, 0.05)
    pd = detection_probability_swerling1(n_ref, k, t, snr)
    rng = random.Random(5104)
    cells = n_ref + 2 * guard + 1
    mid = cells // 2
    hits = 0
    for _ in range(n):
        x = [square_law(rng, 1.0) for _ in range(cells)]
        x[mid] = square_law(rng, 1.0 + snr)
        hits += os_cfar(x, n_ref, guard, k, t)[0] == [mid]
    lo, hi = wilson(hits, n, 3.29)
    assert lo <= pd <= hi
