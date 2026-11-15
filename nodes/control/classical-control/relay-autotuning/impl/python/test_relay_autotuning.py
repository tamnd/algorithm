# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relay-autotuning/. The authors are listed in prov/WBZ78H.jsonl.

import cmath
import math
import random

import pytest

from ctlmat import matvec
from ctlsim import lti, simulate
from relay_autotuning import (analyze_cycle, exact_relay_cycle, relay_autotune,
                              relay_estimate, relay_experiment,
                              ultimate_cycle_rule)

# Plant 1/(s + 1)^3 as a chain of three lags, y = x3. K_u = 8 and
# T_u = 2 pi/sqrt(3) for this plant.
A3 = [[-1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [0.0, 1.0, -1.0]]
B3 = [[1.0], [0.0], [0.0]]
C3 = [0.0, 0.0, 1.0]
TU3 = 2 * math.pi / math.sqrt(3)
DT = 0.005


def test_exact_cycle_is_a_cycle():
    T, a, x0 = exact_relay_cycle(A3, B3, C3, 1.0)
    assert abs(matvec([C3], x0)[0]) < 1e-12
    # From x0 with u = +d for T/2, y stays below 0 and returns to 0, and
    # the state reaches -x0 (the symmetric half of the cycle).
    ts, xs, _ = simulate(lti(A3, B3), x0, 0.0, T / 2, T / 2 / 4000, control=lambda t, x: 1.0)
    ys = [x[2] for x in xs]
    assert max(ys[1:-1]) < 0
    assert max(abs(u + v) for u, v in zip(xs[-1], x0)) < 1e-10
    assert abs(-min(ys) - a) < 1e-9


def test_exact_cycle_against_ultimate_point():
    # The describing function gives the period and the gain with a small
    # error for this plant: measured 1.4 percent and 2.4 percent.
    T, a, _ = exact_relay_cycle(A3, B3, C3, 1.0)
    ku = 4 / (math.pi * a)
    assert 0 < (T - TU3) / TU3 < 0.02
    assert 0 < (8 - ku) / 8 < 0.03


def test_simulated_cycle_matches_exact_cycle():
    T, a, _ = exact_relay_cycle(A3, B3, C3, 1.0)
    ts, ys, us = relay_experiment(A3, B3, C3, 1.0, 40.0, DT)
    assert len(ts) == round(40.0 / DT) + 1
    Tm, am, center = analyze_cycle(ts, ys)
    # The relay acts at the steps only, which delays each switch by at most
    # one step. Measured: the period is 2 dt longer.
    assert 0 < Tm - T < 3 * DT
    assert abs(am - a) / a < 0.01
    assert abs(center) < 1e-6


@pytest.mark.parametrize("theta", [0.5, 1.0, 2.0])
def test_first_order_plus_delay_closed_form(theta):
    # P = e^(-theta s)/(s + 1): the half period is theta + ln(2 - e^(-theta))
    # and the amplitude is d (1 - e^(-theta)).
    dt = 0.002
    d = 1.5
    ts, ys, _ = relay_experiment([[-1.0]], [[1.0]], [1.0], d, 12 * (theta + 1), dt, delay=theta)
    Tm, am, _ = analyze_cycle(ts, ys)
    T = 2 * (theta + math.log(2 - math.exp(-theta)))
    assert abs(Tm - T) < 3 * dt
    assert abs(am - d * (1 - math.exp(-theta))) < 2e-3 * d


def test_amplitude_scales_with_d():
    _, a1, _ = analyze_cycle(*relay_experiment(A3, B3, C3, 1.0, 40.0, DT)[:2])
    _, a2, _ = analyze_cycle(*relay_experiment(A3, B3, C3, 2.5, 40.0, DT)[:2])
    assert abs(a2 - 2.5 * a1) < 1e-9


def test_hysteresis_moves_the_point():
    # With hysteresis the estimate lies near the point where the phase of P
    # is -180 + asin(eps/a) degrees. Measured: 1.3 degrees and 0.1 percent
    # off for this plant.
    eps = 0.05
    ts, ys, _ = relay_experiment(A3, B3, C3, 1.0, 40.0, DT, eps=eps)
    Tm, am, _ = analyze_cycle(ts, ys)
    k, ph = relay_estimate(1.0, am, eps)
    w = 2 * math.pi / Tm
    P = 1 / (1j * w + 1) ** 3
    assert abs(cmath.phase(P) - ph) < 0.04
    assert abs(k * abs(P) - 1) < 0.02


def test_analyze_cycle_on_a_sine():
    rng = random.Random(5)
    for _ in range(3):
        T, a, c = rng.uniform(0.5, 3.0), rng.uniform(0.1, 2.0), rng.uniform(-1.0, 1.0)
        dt = T / 1000
        ts = [k * dt for k in range(10001)]
        ys = [c + a * math.sin(2 * math.pi * t / T + 0.3) for t in ts]
        Tm, am, cm = analyze_cycle(ts, ys, r=c)
        assert abs(Tm - T) < 1e-6 * T
        assert abs(am - a) < 1e-4 * a and abs(cm - c) < 1e-4 * a
    with pytest.raises(ValueError):
        analyze_cycle(ts[:1500], ys[:1500], r=c)


def test_relay_estimate_errors():
    assert relay_estimate(1.0, 4 / math.pi) == (1.0, -math.pi)
    with pytest.raises(ValueError):
        relay_estimate(1.0, 0.1, eps=0.2)
    with pytest.raises(ValueError):
        relay_experiment(A3, B3, C3, 0.0, 1.0, DT)


def test_autotune_and_closed_loop():
    K, Ti, Td, ku, tu, a = relay_autotune(A3, B3, C3, 1.0, 40.0, DT)
    assert (K, Ti, Td) == ultimate_cycle_rule(ku, tu, "PID")
    assert abs(K / 4.8 - 1) < 0.05 and abs(Ti / (TU3 / 2) - 1) < 0.03
    N = 20.0

    def f(t, x, _):
        y = x[2]
        u = K * (1.0 - y) + x[3] - K * N * (y - x[4])
        return [-x[0] + u, -x[1] + x[0], -x[2] + x[1], K / Ti * (1.0 - y), N / Td * (y - x[4])]

    ts, xs, _ = simulate(f, [0.0] * 5, 0.0, 60.0, 0.01)
    ys = [x[2] for x in xs]
    assert abs(ys[-1] - 1) < 1e-6
    # Measured overshoot of this loop: 0.504.
    assert 0.4 < max(ys) - 1 < 0.6
