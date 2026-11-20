# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-locked-loop/. The authors are listed in prov/YWG207.jsonl.

import cmath
import math
import random

from phase_locked_loop import closed_loop, is_stable, loop_gains, noise_bandwidth, pll


def impulse_response(kp, ki, n):
    """h[0..n-1] of the linear loop, from the difference equation of H(z)."""
    (b0, b1), (a1, a2) = closed_loop(kp, ki)
    h = []
    for k in range(n):
        x1 = 1.0 if k == 1 else 0.0  # input delayed by one: z^-1 numerator term b0
        x2 = 1.0 if k == 2 else 0.0
        y = b0 * x1 + b1 * x2
        if k >= 1:
            y -= a1 * h[k - 1]
        if k >= 2:
            y -= a2 * h[k - 2]
        h.append(y)
    return h


def spectral_radius(kp, ki):
    _, (a1, a2) = closed_loop(kp, ki)
    d = cmath.sqrt(a1 * a1 - 4.0 * a2)
    return max(abs((-a1 + d) / 2.0), abs((-a1 - d) / 2.0))


def test_noise_bandwidth_closed_form_matches_impulse_response() -> None:
    for kp, ki in [(0.0266667, 0.000355556), (0.3, 0.05), (1.0, 0.5), (1.5, 0.8)]:
        h = impulse_response(kp, ki, 20000)
        assert abs(0.5 * sum(x * x for x in h) - noise_bandwidth(kp, ki)) < 1e-9


def test_design_rule_gives_the_bandwidth_for_small_values() -> None:
    for bl in (0.005, 0.01, 0.02):
        kp, ki = loop_gains(bl)
        assert abs(noise_bandwidth(kp, ki) / bl - 1.0) < 0.05
    kp, ki = loop_gains(0.02)
    assert abs(kp - 8 * 0.02 / 3) < 1e-15 and abs(ki - 32 * 0.02**2 / 9) < 1e-15
    assert abs(noise_bandwidth(kp, ki) - 0.020738169) < 1e-8


def test_jury_region_matches_the_poles() -> None:
    for i in range(-2, 43):
        for j in range(-2, 45):
            kp, ki = 0.05 * i + 0.013, 0.1 * j + 0.017
            assert is_stable(kp, ki) == (spectral_radius(kp, ki) < 1.0)


def test_linear_model_for_a_small_step() -> None:
    # A step of 1e-4 rad keeps sin(x) = x to about 2e-13, so the loop follows H(z)
    # to about 1e-6 of the step size.
    kp, ki = loop_gains(0.02)
    th = 1e-4
    est = pll([cmath.exp(1j * th)] * 300, kp, ki)
    h = impulse_response(kp, ki, 300)
    step = 0.0
    for k in range(300):
        step += h[k]
        assert abs(est[k] - th * step) < 1e-10


def test_phase_step_of_0_7_rad() -> None:
    kp, ki = loop_gains(0.02)
    est = pll([cmath.exp(0.7j)] * 1000, kp, ki)
    err = [0.7 - p for p in est]
    assert err[0] == 0.7
    assert max(abs(e) for e in err[300:]) < 1e-3
    assert abs(min(err) + 0.147) < 0.001  # the overshoot of a damping of 1/sqrt(2)
    assert err.index(min(err)) == 58


def test_frequency_step_gives_zero_steady_state_error() -> None:
    kp, ki = loop_gains(0.02)
    w = 2 * math.pi * 0.002
    r = [cmath.exp(1j * (w * k + 0.7)) for k in range(2000)]
    est = pll(r, kp, ki)
    err = [w * k + 0.7 - est[k] for k in range(2000)]
    assert max(abs(e) for e in err[400:]) < 1e-5
    assert max(abs(e) for e in err[600:]) < 1e-6
    assert abs(err[-1]) < 1e-12


def test_unstable_gains_do_not_lock() -> None:
    # 2 kp + ki = 4.3 > 4: a pole lies outside the unit circle. A tiny error grows
    # until the sine of the detector limits it, and the loop keeps swinging.
    kp, ki = 1.9, 0.5
    assert not is_stable(kp, ki)
    est = pll([cmath.exp(1e-6j)] * 200, kp, ki)
    assert min(abs(1e-6 - p) for p in est[-20:]) > 0.5


def test_phase_error_variance_in_noise() -> None:
    # SNR = 10 (10 dB), B_L T = 0.01: the linear model gives var = B_L T / SNR.
    snr = 10.0
    sd = math.sqrt(0.5 / snr)
    kp, ki = loop_gains(0.01)
    rng = random.Random(5)
    r = [cmath.exp(0.7j) + complex(rng.gauss(0, sd), rng.gauss(0, sd)) for _ in range(60000)]
    err = [0.7 - p for p in pll(r, kp, ki)[2000:]]
    m = sum(err) / len(err)
    var = sum((e - m) ** 2 for e in err) / len(err)
    ratio = var / (noise_bandwidth(kp, ki) / snr)
    assert abs(m) < 0.005
    assert 0.8 < ratio < 1.25
