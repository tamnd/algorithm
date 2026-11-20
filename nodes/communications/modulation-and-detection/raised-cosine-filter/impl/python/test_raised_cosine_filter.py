# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raised-cosine-filter/. The authors are listed in prov/QN0P95.jsonl.

import math

from raised_cosine_filter import rc_pulse, rc_spectrum, rc_taps, sinc


def test_check_values() -> None:
    assert abs(rc_pulse(0.5, 0.5) - 0.60021) < 5e-6
    assert abs(rc_pulse(1.5, 0.5) - (-0.12004)) < 5e-6
    assert abs(rc_pulse(0.5, 0.25) - 0.62737) < 5e-6
    assert abs(rc_pulse(1.5, 0.25) - (-0.18562)) < 5e-6
    assert abs(rc_pulse(0.5, 1.0) - 0.5) < 1e-12
    assert abs(rc_pulse(1.0, 0.5)) < 1e-12
    # The pulse scales with T: h(t) for period T equals h(t/T) for period 1.
    assert abs(rc_pulse(1.0, 0.5, 2.0) - rc_pulse(0.5, 0.5)) < 1e-15


def test_zero_at_nonzero_multiples_of_t() -> None:
    for beta in (0.0, 0.1, 0.25, 0.35, 0.5, 0.75, 1.0):
        assert rc_pulse(0.0, beta) == 1.0
        for k in range(1, 30):
            assert abs(rc_pulse(k, beta)) < 1e-12
            assert abs(rc_pulse(-k, beta)) < 1e-12


def test_beta_zero_is_sinc() -> None:
    for t in (0.1, 0.5, 1.3, 7.7):
        assert abs(rc_pulse(t, 0.0) - sinc(t)) < 1e-15


def test_continuity_at_singular_points() -> None:
    for beta in (0.2, 0.25, 0.35, 0.5, 1.0):
        t0 = 1 / (2 * beta)
        at = rc_pulse(t0, beta)
        for eps in (1e-6, -1e-6):
            assert abs(rc_pulse(t0 + eps, beta) - at) < 1e-5
            assert abs(rc_pulse(-t0 + eps, beta) - at) < 1e-5


def test_folded_spectrum_is_flat() -> None:
    for beta in (0.0, 0.25, 0.5, 1.0):
        for i in range(-50, 51):
            f = i / 100
            fold = sum(rc_spectrum(f - m, beta) for m in range(-3, 4))
            assert abs(fold - 1.0) < 1e-12
    assert abs(rc_spectrum(0.4, 0.5) - 0.79389) < 5e-6
    assert abs(rc_spectrum(0.6, 0.5) - 0.20611) < 5e-6
    assert rc_spectrum(0.5, 0.5) == 0.5


def test_bandwidth() -> None:
    assert rc_spectrum(0.625, 0.25) == 0.0
    assert rc_spectrum(0.6249, 0.25) > 0.0


def test_energy_in_time_and_frequency() -> None:
    for beta in (0.25, 0.5, 1.0):
        want = 1 - beta / 4
        # Simpson's rule on H^2 over the band.
        n = 2000
        hi = (1 + beta) / 2
        step = 2 * hi / n
        s = 0.0
        for i in range(n + 1):
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            s += w * rc_spectrum(-hi + i * step, beta) ** 2
        assert abs(s * step / 3 - want) < 1e-6
        # A Riemann sum of h^2 with step 1/16 over |t| <= 100: the pulse is band-limited
        # to below 8, so the sum is exact apart from the tail beyond 100.
        e = sum(rc_pulse(n / 16, beta) ** 2 for n in range(-1600, 1601)) / 16
        assert abs(e - want) < 1e-5


def test_decay() -> None:
    def peak(beta: float, k: int) -> float:
        return max(abs(rc_pulse(k + i / 1000, beta)) for i in range(1001))

    assert abs(peak(0.0, 10) - 0.0303) < 5e-5
    assert abs(peak(0.25, 10) - 4.79e-4) < 5e-6
    assert abs(peak(0.5, 10) - 2.21e-4) < 5e-6


def test_taps() -> None:
    taps = rc_taps(0.25, 8, 8)
    assert len(taps) == 2 * 8 * 8 + 1
    assert taps[64] == 1.0
    assert all(abs(taps[64 + 8 * k]) < 1e-12 for k in range(-8, 9) if k != 0)
    assert all(abs(taps[i] - taps[-1 - i]) < 1e-15 for i in range(len(taps)))
    assert math.isclose(taps[68], rc_pulse(0.5, 0.25))
