# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cepstral-pitch-detection/. The authors are listed in prov/AZJ97D.jsonl.

import cmath
import math
import random

from cepstral_pitch_detection import (
    all_pole_cepstrum,
    cepstral_pitch,
    quefrency_range,
    real_cepstrum,
    real_cepstrum_direct,
    track,
)
from nlsdsp import all_pole, pulse_train, white_noise

FS = 8000
R = 0.9
THETA = 2 * math.pi * 500 / FS
A = [2 * R * math.cos(THETA), -R * R]  # one resonance at 500 Hz with pole radius 0.9


def voiced(f0, n=800):
    return all_pole(pulse_train(f0, FS, n), A)


def test_fft_cepstrum_matches_the_definition():
    rng = random.Random(1)
    frame = [rng.uniform(-1, 1) for _ in range(40)]
    fast = real_cepstrum(frame, 64)
    slow = real_cepstrum_direct(frame, 64)
    assert max(abs(u - v) for u, v in zip(fast, slow)) < 1e-9


def test_cepstrum_is_even():
    rng = random.Random(2)
    frame = [rng.uniform(-1, 1) for _ in range(100)]
    c = real_cepstrum(frame, 128)
    for q in range(1, 64):
        assert abs(c[q] - c[128 - q]) < 1e-9


def test_all_pole_cepstrum_recursion_matches_the_poles():
    poles = [R * cmath.exp(1j * THETA), R * cmath.exp(-1j * THETA)]
    h = all_pole_cepstrum(A, 30)
    assert h[0] == 0.0
    for n in range(1, 30):
        assert abs(h[n] - sum(p ** n for p in poles).real / n) < 1e-12


def test_model_signal_has_the_closed_form_cepstrum():
    # x = h * p, with p a train of 6 pulses of period 50 and amplitudes 0.8^j, no window.
    beta, period, count, m = 0.8, 50, 6, 4096
    p = [0.0] * m
    for j in range(count):
        p[j * period] = beta ** j
    c = real_cepstrum(all_pole(p, A), m, window=False)
    h = all_pole_cepstrum(A, 2 * period + 1)
    assert abs(c[3] - h[3] / 2) < 1e-9
    assert abs(c[period] - (h[period] + beta) / 2) < 1e-9
    assert abs(c[2 * period] - (h[2 * period] + beta ** 2 / 2) / 2) < 1e-9
    assert abs(c[period + 7] - h[period + 7] / 2) < 1e-9


def test_integer_periods_are_found_exactly():
    for f0 in (100, 125, 160, 200):
        x = voiced(f0)
        est, q, _ = cepstral_pitch(x[100:500], FS, 60, 400, 512)
        assert q == FS // f0
        assert est == f0


def test_the_peak_is_the_brute_force_argmax_in_the_range():
    x = voiced(160)
    c = real_cepstrum(x[100:500], 512)
    qmin, qmax = quefrency_range(FS, 60, 400)
    assert (qmin, qmax) == (20, 133)
    best = max(range(qmin, qmax + 1), key=lambda q: (c[q], -q))
    assert cepstral_pitch(x[100:500], FS, 60, 400, 512)[1] == best


def test_example_values():
    x = voiced(160)
    c = real_cepstrum(x[100:500], 512)
    assert abs(c[50] - 1.2539) < 1e-4
    assert abs(c[100] - 0.4304) < 1e-4
    assert abs(c[1] - 0.8079) < 1e-4


def test_fractional_period_is_within_one_sample():
    x = voiced(150)  # period 53.33 samples
    est, q, _ = cepstral_pitch(x[100:500], FS, 60, 400, 512)
    assert q in (53, 54)
    assert abs(FS / est - FS / 150) < 1


def test_noise_is_unvoiced_and_the_track_follows_the_voicing():
    rng = random.Random(7)
    noise = white_noise(rng, 800, 0.5)
    assert cepstral_pitch(noise[:400], FS, 60, 400, 512, threshold=0.3)[0] is None
    x = voiced(125) + noise
    out = track(x, FS, 400, 400, 60, 400, threshold=0.3)
    assert out == [125.0, 125.0, None, None]
