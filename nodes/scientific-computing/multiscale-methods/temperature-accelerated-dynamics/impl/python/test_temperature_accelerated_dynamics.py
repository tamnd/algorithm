# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temperature-accelerated-dynamics/. The authors are listed in prov/FJ0MZ4.jsonl.
import math
import random

import pytest

from temperature_accelerated_dynamics import catalog_high_temperature_run, temperature_accelerated_dynamics

K_B = 8.617333262e-5          # eV / K
KT_LOW = K_B * 300.0
KT_HIGH = K_B * 600.0
# event: (prefactor in 1/ps, barrier in eV)
EVENTS = {"a": (1.0, 0.50), "b": (5.0, 0.55), "c": (10.0, 0.60)}


def barrier(event):
    return EVENTS[event][1]


def low_temperature_law():
    rates = {e: nu * math.exp(-ea / KT_LOW) for e, (nu, ea) in EVENTS.items()}
    total = sum(rates.values())
    return {e: r / total for e, r in rates.items()}, 1.0 / total


class Scripted:
    def __init__(self, escapes):
        self.escapes = list(escapes)

    def __call__(self, rng):
        return self.escapes.pop(0)


def test_extrapolation_and_stop_time_by_hand():
    # kT_low = 1, kT_high = 2, nu_min = 1, ln(1/delta) = 1.
    run = Scripted([(1.0, "a"), (0.5, "b"), (9.0, "a")])
    energies = {"a": 2.0, "b": 0.4}
    event, t_low, t_high, escapes, seen = temperature_accelerated_dynamics(
        run, energies.get, 1.0, 2.0, 1.0, math.exp(-1.0), None)
    # a at t_high = 1: t_low = e; t_stop = e^(1/2) = 1.6487.
    assert seen["a"] == pytest.approx(math.e)
    # b at t_high = 1.5: t_low = 1.5 e^0.2 = 1.83210; t_stop = 1.35355 < 1.5, stop.
    assert seen["b"] == pytest.approx(1.5 * math.exp(0.2))
    assert event == "b" and t_low == pytest.approx(1.832104, abs=1e-6)
    assert t_high == 1.5 and escapes == 2
    assert run.escapes == [(9.0, "a")]


def test_repeated_events_keep_the_first_time():
    run = Scripted([(1.0, "a"), (1.0, "a"), (1.0, "b"), (100.0, "b")])
    energies = {"a": 6.0, "b": 6.0}
    event, t_low, t_high, escapes, seen = temperature_accelerated_dynamics(
        run, energies.get, 1.0, 2.0, 1.0, math.exp(-1.0), None)
    # a first at t_high = 1: t_low = e^3, t_stop = e^1.5 = 4.48. The second a
    # is ignored. b at t_high = 3 has t_low = 3 e^3, which is longer.
    assert event == "a" and t_low == pytest.approx(math.exp(3.0))
    assert seen == {"a": pytest.approx(math.exp(3.0)), "b": pytest.approx(3.0 * math.exp(3.0))}
    assert t_high == pytest.approx(math.exp(1.5)) and escapes == 4


def test_low_temperature_law_is_reproduced():
    fractions, mean_time = low_temperature_law()
    run = catalog_high_temperature_run(EVENTS, KT_HIGH)
    rng = random.Random(4)
    n = 1000
    counts = {e: 0 for e in EVENTS}
    times = []
    for _ in range(n):
        event, t_low, _, _, _ = temperature_accelerated_dynamics(run, barrier, KT_LOW, KT_HIGH, 1.0, 1e-3, rng)
        counts[event] += 1
        times.append(t_low)
    for e, p in fractions.items():
        assert abs(counts[e] / n - p) < 3.0 * math.sqrt(p * (1.0 - p) / n)
    mean = sum(times) / n
    se = math.sqrt(sum((v - mean) ** 2 for v in times) / (n - 1) / n)
    assert abs(mean - mean_time) < 3.0 * se


def test_a_wrong_minimum_prefactor_breaks_the_law():
    # nu_min = 100 is above every prefactor, so the run stops too early and
    # misses the slow event a, which has the lowest barrier.
    fractions, _ = low_temperature_law()
    run = catalog_high_temperature_run(EVENTS, KT_HIGH)
    rng = random.Random(4)
    n = 1000
    to_a = sum(temperature_accelerated_dynamics(run, barrier, KT_LOW, KT_HIGH, 100.0, 1e-3, rng)[0] == "a"
               for _ in range(n))
    assert fractions["a"] == pytest.approx(0.5177, abs=1e-4)
    assert to_a / n < 0.4


def test_max_escapes():
    run = catalog_high_temperature_run(EVENTS, KT_HIGH)
    with pytest.raises(RuntimeError):
        temperature_accelerated_dynamics(run, barrier, KT_LOW, KT_HIGH, 1.0, 1e-3, random.Random(1), max_escapes=1)
