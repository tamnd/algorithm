# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-slip/. The authors are listed in prov/4GQF6S.jsonl.

import math

from cycle_slip import (
    bessel_i0,
    bessel_i1,
    count_slips,
    first_order_bandwidth,
    mean_samples_between_slips,
    simulate_errors,
)


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    return s * h / 3


def test_bessel_against_the_integral() -> None:
    # Reference: I_n(x) = (1/pi) integral_0^pi e^(x cos t) cos(n t) dt.
    for x in (0.0, 0.5, 1.5, 3.0, 10.0):
        i0 = simpson(lambda t: math.exp(x * math.cos(t)), 0, math.pi) / math.pi
        i1 = simpson(lambda t: math.exp(x * math.cos(t)) * math.cos(t), 0, math.pi) / math.pi
        assert abs(bessel_i0(x) - i0) < 1e-9 * i0
        assert abs(bessel_i1(x) - i1) < 1e-9 * max(i1, 1.0)


def test_bandwidth_of_the_first_order_loop() -> None:
    # B_L T = (1/2) sum h_k^2 with the impulse response h_k = K (1 - K)^k.
    for k in (0.01, 0.05, 0.3, 1.0, 1.5):
        s = 0.5 * sum((k * (1 - k) ** i) ** 2 for i in range(20000))
        assert abs(first_order_bandwidth(k) - s) < 1e-12


def test_closed_form_and_its_high_snr_limit() -> None:
    bl = first_order_bandwidth(0.05)
    assert abs(mean_samples_between_slips(1.5, bl) - 1565.6) < 0.5
    assert abs(mean_samples_between_slips(2.0, bl) - 4000.5) < 0.5
    # pi^2 rho I0(rho)^2 / (2 B_L) ~ pi e^(2 rho) / (4 B_L) (1 + 1/(8 rho))^2 as rho grows.
    for rho in (20.0, 40.0):
        approx = math.pi * math.exp(2 * rho) / (4 * bl) * (1 + 1 / (8 * rho)) ** 2
        assert abs(mean_samples_between_slips(rho, bl) / approx - 1) < 2e-3


def test_linear_regime_has_no_slips() -> None:
    # rho = 20: variance close to 1/rho, and no slip in 20000 samples.
    k = 0.05
    bl = first_order_bandwidth(k)
    e = simulate_errors(k, 20 * bl, 20000, 1)
    tail = e[1000:]
    var = sum(x * x for x in tail) / len(tail)
    assert 0.8 < var * 20 < 1.3
    assert count_slips(e) == 0


def test_slip_rate_against_the_closed_form() -> None:
    # Measurement: K = 0.05, 80000 samples per loop SNR, seed 7.
    k, n = 0.05, 80000
    bl = first_order_bandwidth(k)
    counts = {}
    for rho in (1.5, 2.0):
        e = simulate_errors(k, rho * bl, n, 7)
        counts[rho] = count_slips(e)
        measured = n / counts[rho]
        assert 0.6 < measured / mean_samples_between_slips(rho, bl) < 1.7
        if rho == 1.5:
            # The phase error modulo 2 pi follows the Tikhonov density: E cos = I1/I0.
            c = sum(math.cos(x) for x in e[2000:]) / (n - 2000)
            assert abs(c - bessel_i1(rho) / bessel_i0(rho)) < 0.05
    assert counts[1.5] > 2 * counts[2.0]
