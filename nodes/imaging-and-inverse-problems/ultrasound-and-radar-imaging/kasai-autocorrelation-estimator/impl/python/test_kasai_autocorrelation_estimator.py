# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasai-autocorrelation-estimator/. The authors are listed in prov/CC9PV7.jsonl.

import cmath
import math
import random

from kasai_autocorrelation_estimator import (aliasing_velocity, doppler_iq, kasai, kasai_image, lag_correlations,
                                             periodogram_peak_velocity)

C, PRF, F0 = 1540.0, 5000.0, 5.0e6
VA = aliasing_velocity(C, PRF, F0)


def _noise(rng, n, sigma):
    s = sigma / math.sqrt(2.0)
    return [complex(rng.gauss(0, s), rng.gauss(0, s)) for _ in range(n)]


def test_aliasing_velocity_check_value() -> None:
    assert abs(VA - 0.385) < 1e-12


def test_single_tone_is_exact_inside_the_nyquist_range() -> None:
    for v in (-0.38, -0.2, -0.01, 0.0, 0.05, 0.2, 0.3849):
        x = doppler_iq(8, v, C, PRF, F0, amp=2.5, phase0=1.1)
        est, power, width = kasai([x], C, PRF, F0)
        assert abs(est - v) < 1e-12
        assert abs(power - 6.25) < 1e-12
        assert width < 1e-6


def test_aliasing_wraps_by_twice_the_nyquist_velocity() -> None:
    est = kasai([doppler_iq(8, 0.5, C, PRF, F0)], C, PRF, F0)[0]
    assert abs(est - (0.5 - 2 * VA)) < 1e-12
    assert abs(est + 0.27) < 1e-12


def test_gain_conjugation_and_reversal() -> None:
    rng = random.Random(5101)
    x = [a + b for a, b in zip(doppler_iq(10, 0.12, C, PRF, F0), _noise(rng, 10, 0.3))]
    v = kasai([x], C, PRF, F0)[0]
    g = 0.3 * cmath.exp(2.0j)
    assert abs(kasai([[g * a for a in x]], C, PRF, F0)[0] - v) < 1e-12
    assert abs(kasai([[a.conjugate() for a in x]], C, PRF, F0)[0] + v) < 1e-12
    assert abs(kasai([x[::-1]], C, PRF, F0)[0] + v) < 1e-12


def test_symmetric_spectrum_gives_its_centre_exactly() -> None:
    # R(T) = sum_k S_k exp(i 2 pi f_k T) for a spectrum symmetric about fbar with
    # half-width below prf / 4: the phase of R(T) is exactly 2 pi fbar T.
    t = 1.0 / PRF
    for fbar in (-1700.0, 300.0, 1100.0):
        r = 0j
        for u, s in ((0.0, 1.0), (200.0, 0.6), (450.0, 0.25), (900.0, 0.05)):
            for sign in ((1,) if u == 0.0 else (1, -1)):
                r += s * cmath.exp(2j * math.pi * (fbar + sign * u) * t)
        assert abs(cmath.phase(r) - 2 * math.pi * fbar * t) < 1e-12


def test_random_process_with_symmetric_spectrum() -> None:
    # Many gates, each a sum of tones at fbar +- u with random phases: the
    # pooled estimate approaches the centre velocity.
    rng = random.Random(5102)
    v_true = 0.15
    fbar = 2 * v_true * F0 / C
    gates = []
    for _ in range(200):
        x = [0j] * 12
        for u, a in ((0.0, 1.0), (150.0, 0.7), (300.0, 0.4)):
            for sign in ((1,) if u == 0.0 else (1, -1)):
                ph = rng.uniform(0, 2 * math.pi)
                f = fbar + sign * u
                x = [xk + a * cmath.exp(1j * (ph + 2 * math.pi * f * k / PRF)) for k, xk in enumerate(x)]
        gates.append(x)
    est, _, width = kasai(gates, C, PRF, F0)
    assert abs(est - v_true) < 0.01
    assert width > 0.0


def test_noisy_tone_matches_the_periodogram_reference() -> None:
    rng = random.Random(5103)
    err_k, err_p = 0.0, 0.0
    trials = 20
    for _ in range(trials):
        v = rng.uniform(-0.3, 0.3)
        x = [a + b for a, b in zip(doppler_iq(16, v, C, PRF, F0, phase0=rng.uniform(0, 6.3)),
                                   _noise(rng, 16, 0.3))]
        vk = kasai([x], C, PRF, F0)[0]
        vp = periodogram_peak_velocity(x, C, PRF, F0, grid=512)
        err_k += (vk - v) ** 2
        err_p += (vp - v) ** 2
        assert abs(vk - vp) < 0.02
    assert math.sqrt(err_k / trials) < 0.01
    assert math.sqrt(err_p / trials) < 0.01


def test_gate_averaging_lowers_the_error() -> None:
    rng = random.Random(5104)
    v = 0.1
    single, pooled = 0.0, 0.0
    for _ in range(30):
        gates = [[a + b for a, b in zip(doppler_iq(8, v, C, PRF, F0, phase0=rng.uniform(0, 6.3)),
                                        _noise(rng, 8, 1.0))] for _ in range(5)]
        single += (kasai(gates[:1], C, PRF, F0)[0] - v) ** 2
        pooled += (kasai(gates, C, PRF, F0)[0] - v) ** 2
    assert pooled < single


def test_lag_correlations_by_hand() -> None:
    r0, r1 = lag_correlations([[1, 1j, -1, -1j]])
    assert abs(r0 - 1) < 1e-15
    assert abs(r1 - 1j) < 1e-15


def test_unfiltered_clutter_biases_toward_zero() -> None:
    blood = doppler_iq(8, 0.25, C, PRF, F0)
    tissue = [10.0 + 0j] * 8
    v = kasai([[a + b for a, b in zip(blood, tissue)]], C, PRF, F0)[0]
    assert abs(v) < 0.05


def test_velocity_image() -> None:
    rows, cols = 6, 4
    ens = [[doppler_iq(8, 0.2 if 1 <= i <= 3 and j >= 2 else 0.0, C, PRF, F0, phase0=0.3 * i + j) for j in range(cols)]
           for i in range(rows)]
    img = kasai_image(ens, C, PRF, F0, gate_avg=1)
    for i in range(rows):
        for j in range(cols):
            want = 0.2 if 1 <= i <= 3 and j >= 2 else 0.0
            assert abs(img[i][j] - want) < 1e-12
