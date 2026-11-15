# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/describing-function/. The authors are listed in prov/4JVRZW.jsonl.

import math

import pytest

from describing_function import (
    dead_zone,
    describing_function,
    describing_function_hysteresis,
    df_dead_zone,
    df_relay,
    df_relay_hysteresis,
    df_saturation,
    harmonic_balance,
    harmonic_balance_complex,
    measure_cycle,
    relay,
    saturation,
    simulate_loop,
    tf,
)

DEN = [1, 3, 2, 0]  # s (s + 1) (s + 2)


def exact_relay_cycle():
    """Exact symmetric oscillation of the relay loop with 1 / (s (s + 1) (s + 2)).

    G = 1/(2s) - 1/(s + 1) + 1/(2 (s + 2)). For a square wave input of
    half period h, the periodic response of each mode is known in closed
    form, and y(0) = 0 gives -h/4 + tanh(h/2) - tanh(h)/4 = 0.
    """
    def g(h):
        return -h / 4 + math.tanh(h / 2) - math.tanh(h) / 4

    lo, hi = 2.0, 2.5
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
    h = (lo + hi) / 2
    x1, x2 = -math.tanh(h / 2), -math.tanh(h) / 2

    def y(t):
        e1, e2 = math.exp(-t), math.exp(-2 * t)
        return 0.5 * (t - h / 2) - (e1 * x1 + 1 - e1) + 0.5 * (e2 * x2 + (1 - e2) / 2)

    vals = [y(h * k / 20000) for k in range(1, 20000)]
    assert max(vals) < 0  # one sign change per half period
    return 2 * h, -min(vals)


def test_closed_forms_match_fourier_integrals():
    for a in (0.3, 1.0, 2.5, 7.0):
        assert describing_function(relay(1.5), a).real == pytest.approx(df_relay(1.5, a), rel=1e-5)
        assert describing_function(saturation(2.0, 1.0), a).real == pytest.approx(df_saturation(2.0, 1.0, a), rel=1e-6)
        assert describing_function(dead_zone(2.0, 1.0), a).real == pytest.approx(df_dead_zone(2.0, 1.0, a), abs=1e-6)
        assert abs(describing_function(relay(1.5), a).imag) < 1e-9
    for a in (0.2, 0.5, 3.0):
        num = describing_function_hysteresis(1.0, 0.1, a, m=20000)
        assert abs(num - df_relay_hysteresis(1.0, 0.1, a)) < 1e-3 * abs(num)


def test_inverse_hysteresis_df_is_a_horizontal_line():
    d, h = 2.0, 0.3
    for a in (0.31, 0.5, 1.0, 4.0):
        z = -1 / df_relay_hysteresis(d, h, a)
        assert z.imag == pytest.approx(-math.pi * h / (4 * d))
        assert z.real == pytest.approx(-math.pi * math.sqrt(a * a - h * h) / (4 * d))


def test_saturation_and_dead_zone_limits():
    assert df_saturation(3.0, 1.0, 0.5) == 3.0
    assert df_saturation(3.0, 1.0, 1e6) == pytest.approx(4 * 3.0 / (math.pi * 1e6), rel=1e-6)
    assert df_dead_zone(3.0, 1.0, 1.0) == pytest.approx(0.0)
    vals = [df_saturation(1.0, 1.0, 1 + 0.5 * k) for k in range(20)]
    assert all(x > y for x, y in zip(vals, vals[1:]))


def test_relay_prediction():
    r = harmonic_balance(tf([1], DEN), lambda a: df_relay(1.0, a), 0.5, 5.0, 1e-3, 10.0)
    assert r["w"] == pytest.approx(math.sqrt(2), rel=1e-10)
    assert r["gain"] == pytest.approx(6.0, rel=1e-10)
    assert r["a"] == pytest.approx(2 / (3 * math.pi), rel=1e-10)
    assert r["period"] == pytest.approx(math.pi * math.sqrt(2), rel=1e-10)
    assert r["attracting"]
    assert r["filter"] == pytest.approx(0.06917, abs=1e-5)


def test_relay_prediction_against_the_true_cycle():
    T, A = exact_relay_cycle()
    assert T == pytest.approx(4.5511, abs=1e-4)
    assert A == pytest.approx(0.22004, abs=1e-5)
    ys = simulate_loop([1], DEN, relay(1.0), [0.1, 0.0, 0.0], 1e-3, 30.0)
    m = measure_cycle(ys, 1e-3)
    assert m["period"] == pytest.approx(T, rel=5e-3)
    assert m["a"] == pytest.approx(A, rel=5e-3)
    # The prediction is low by about 2.4 % in the period and 3.6 % in the amplitude.
    assert (math.pi * math.sqrt(2) - T) / T == pytest.approx(-0.0238, abs=1e-3)
    assert (2 / (3 * math.pi) - A) / A == pytest.approx(-0.0356, abs=1e-3)


def test_saturation_loop():
    K = 10
    r = harmonic_balance(tf([K], DEN), lambda a: df_saturation(1.0, 1.0, a), 0.5, 5.0, 1.0 + 1e-9, 100.0)
    assert df_saturation(1.0, 1.0, r["a"]) == pytest.approx(0.6)
    assert r["a"] == pytest.approx(2.0331, abs=1e-4)
    assert r["attracting"]
    ys = simulate_loop([K], DEN, saturation(1.0, 1.0), [0.1, 0.0, 0.0], 4e-3, 50.0)
    m = measure_cycle(ys, 4e-3)
    assert m["a"] == pytest.approx(r["a"], rel=0.03)
    assert m["period"] == pytest.approx(r["period"], rel=0.02)


def test_no_cycle_when_the_linear_loop_is_asymptotically_stable():
    K = 3  # the loop with gain 1 is asymptotically stable for K < 6
    r = harmonic_balance(tf([K], DEN), lambda a: df_saturation(1.0, 1.0, a), 0.5, 5.0, 1.0 + 1e-9, 100.0)
    assert r is None
    ys = simulate_loop([K], DEN, saturation(1.0, 1.0), [3.0, 0.0, 0.0], 4e-3, 60.0)
    assert max(abs(v) for v in ys[-500:]) < 0.05


def test_second_order_plant_has_no_phase_crossover():
    assert harmonic_balance(tf([1], [1, 1, 0]), lambda a: df_relay(1.0, a), 0.01, 100.0, 1e-3, 10.0) is None


def test_relay_with_hysteresis():
    d, h = 1.0, 0.1
    G = tf([1], DEN)
    r = harmonic_balance_complex(G, lambda a: df_relay_hysteresis(d, h, a), 1.0, 0.3)
    assert abs(G(1j * r["w"]) * df_relay_hysteresis(d, h, r["a"]) + 1) < 1e-10
    assert G(1j * r["w"]).imag == pytest.approx(-math.pi * h / (4 * d))
    assert r["a"] == pytest.approx(0.36836, abs=1e-5)
    assert r["period"] == pytest.approx(5.9667, abs=1e-4)
    ys = simulate_loop([1], DEN, None, [0.1, 0.0, 0.0], 2e-3, 40.0, hysteresis=(d, h))
    m = measure_cycle(ys, 2e-3)
    assert m["a"] == pytest.approx(r["a"], rel=0.05)
    assert m["period"] == pytest.approx(r["period"], rel=0.03)
