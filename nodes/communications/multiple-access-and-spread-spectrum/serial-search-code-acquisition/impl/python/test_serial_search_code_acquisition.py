# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serial-search-code-acquisition/. The authors are listed in prov/3AJ158.jsonl.

import math
import random

from cbb import cn, wilson
from serial_search_code_acquisition import (
    correlate,
    dwell_probabilities,
    marcum_q1,
    mean_acquisition_time,
    mseq_code,
    received_block,
    serial_search,
)

C31 = mseq_code([5, 2, 0])


def bessel_i0(x: float) -> float:
    total, term, k = 1.0, 1.0, 0
    while term > 1e-17 * total:
        k += 1
        term *= (x / (2 * k)) ** 2
        total += term
    return total


def marcum_by_integration(a: float, b: float) -> float:
    # Simpson's rule on the Rice density x exp(-(x^2 + a^2)/2) I0(a x) from b to b + 40.
    steps = 4000
    h = 40.0 / steps
    f = [(b + i * h) * math.exp(-((b + i * h) ** 2 + a * a) / 2) * bessel_i0(a * (b + i * h)) for i in range(steps + 1)]
    return h / 3 * (f[0] + f[-1] + 4 * sum(f[1:-1:2]) + 2 * sum(f[2:-1:2]))


def test_marcum_q_check_values() -> None:
    for b in (0.0, 0.5, 1.0, 3.0):
        assert abs(marcum_q1(0.0, b) - math.exp(-b * b / 2)) < 1e-14
    for a in (0.5, 2.0, 5.0):
        assert abs(marcum_q1(a, 0.0) - 1.0) < 1e-14
    for a, b in ((1.0, 1.0), (2.0, 3.0), (4.0, 2.5), (6.0, 7.0)):
        assert abs(marcum_q1(a, b) - marcum_by_integration(a, b)) < 1e-9


def test_correlator_peak() -> None:
    r = received_block(random.Random(0), C31, 9, 4.0, 0.0)
    for k in range(31):
        expected = 2.0 if k == 9 else 2.0 * (-1 / 31)
        assert abs(correlate(r, C31, k) - expected) < 1e-12


def test_noiseless_search_finds_the_phase() -> None:
    rng = random.Random(1)
    for tau in range(31):
        start = rng.randrange(31)
        r = received_block(rng, C31, tau, 1.0, 0.0)
        cell, time = serial_search(lambda k: correlate(r, C31, k), 31, 0.5, lambda k: k == tau, 10, start)
        assert cell == tau
        assert time == (tau - start) % 31 + 1


def test_dwell_probabilities_by_simulation() -> None:
    rng = random.Random(2)
    es, n0, gamma = 4.0, 1.0, 3.0
    pd, pfa = dwell_probabilities(es, n0, 31, gamma)
    trials = 3000
    hits = sum(abs(correlate(received_block(rng, C31, 5, es, n0), C31, 5)) ** 2 > gamma for _ in range(trials))
    alarms = sum(abs(correlate(received_block(rng, C31, 5, es, n0), C31, 17)) ** 2 > gamma for _ in range(trials))
    lo, hi = wilson(hits, trials)
    assert lo <= pd <= hi
    lo, hi = wilson(alarms, trials)
    assert lo <= pfa <= hi


def test_mean_time_by_simulation() -> None:
    rng = random.Random(3)
    q, es, n0, gamma, k_pen = 63, 3.0, 1.0, 2.5, 6
    pd, pfa = dwell_probabilities(es, n0, q, gamma)
    a = math.sqrt(es)

    def run() -> int:
        tau = rng.randrange(q)
        # The exact law of the correlator output: CN(sqrt(Es) R, N0), R = 1 at tau and -1/q elsewhere.
        def dwell(k: int) -> complex:
            mean = a if k == tau else -a / q
            return mean + cn(rng, n0)

        cell, time = serial_search(dwell, q, gamma, lambda k: k == tau, k_pen, 0)
        assert cell == tau
        return time

    times = [run() for _ in range(3000)]
    m = sum(times) / len(times)
    sd = math.sqrt(sum((t - m) ** 2 for t in times) / (len(times) - 1))
    expected = mean_acquisition_time(q, pd, pfa, k_pen)
    assert abs(m - expected) < 4 * sd / math.sqrt(len(times))


def test_mean_time_formula_limits() -> None:
    assert mean_acquisition_time(1, 1.0, 0.0, 10) == 1.0
    for q in (2, 10, 1023):
        assert abs(mean_acquisition_time(q, 1.0, 0.0, 10) - (q + 1) / 2) < 1e-9
    # Each false alarm adds K dwells: with Pd = 1, E[T] = 1 + (q - 1)(1 + K Pfa) / 2.
    assert abs(mean_acquisition_time(11, 1.0, 0.1, 10) - (1 + 10 * 2 / 2)) < 1e-12


def test_max_dwells_stops_a_search_that_cannot_succeed() -> None:
    cell, time = serial_search(lambda k: 0j, 7, 1.0, lambda k: True, 3, 0, max_dwells=50)
    assert cell is None and time == 50
