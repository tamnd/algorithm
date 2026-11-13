# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sampling-theorem/. The authors are listed in prov/JHNYYV.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from sampling_theorem import cardinal_series, sinc, tone_amplitudes


def test_sine_at_b_sampled_at_2b_hits_only_zeros() -> None:
    # The phase of sample n of sin(2 pi B t) at fs = 2B is n / 2 cycles, exactly 0 or 1/2.
    for b in (1, 3, Fraction(5, 2), 440):
        fs = 2 * b
        phases = {(Fraction(b) * n / fs) % 1 for n in range(-50, 51)}
        assert phases <= {Fraction(0), Fraction(1, 2)}
        samples = [math.sin(2 * math.pi * float(p)) for p in ((Fraction(b) * n / fs) % 1 for n in range(-50, 51))]
        assert all(abs(v) <= 1e-15 for v in samples)
        # The zero signal has the same samples, so the series returns 0 where the sine is 1.
        t = 1 / (4 * float(b))
        assert abs(cardinal_series(samples, -50, float(fs), t)) <= 1e-12
        assert abs(math.sin(2 * math.pi * float(b) * t) - 1) <= 1e-12


def test_cosine_at_b_loses_its_phase_at_2b() -> None:
    # cos(2 pi B t + phi) and cos(phi) cos(2 pi B t) agree at every sample n / (2B).
    b, fs = 2.0, 4.0
    for phi in (0.3, 1.0, 2.5):
        for n in range(-20, 21):
            t = n / fs
            assert abs(math.cos(2 * math.pi * b * t + phi) - math.cos(phi) * math.cos(2 * math.pi * b * t)) <= 1e-12
        t = 0.1
        assert abs(math.cos(2 * math.pi * b * t + phi) - math.cos(phi) * math.cos(2 * math.pi * b * t)) > 0.1


def test_tones_inside_the_band_are_recovered() -> None:
    rng = random.Random(1)
    for _ in range(50):
        fs = 10.0
        count = rng.randint(1, 6)
        # well separated frequencies in the open band (-fs/2, fs/2)
        grid = rng.sample(range(-9, 10), count)
        freqs = [g * 0.5 + rng.uniform(-0.1, 0.1) for g in grid]
        amps = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in freqs]
        samples = [sum(a * cmath.exp(2j * math.pi * f * n / fs) for a, f in zip(amps, freqs)) for n in range(count)]
        got = tone_amplitudes(freqs, samples, fs)
        assert all(abs(g - a) <= 1e-7 for g, a in zip(got, amps))


def test_tones_at_both_band_edges_cannot_be_separated() -> None:
    with pytest.raises(ValueError):
        tone_amplitudes([-5.0, 5.0], [1.0, -1.0], 10.0)
    with pytest.raises(ValueError):
        tone_amplitudes([1.0, 11.0, 3.0], [1.0, 0.0, 2.0], 10.0)


def test_slightly_above_2b_the_sine_is_seen() -> None:
    # At fs = 2.2 B the sine at B has nonzero samples and its two tones are recovered.
    b, fs = 1.0, 2.2
    samples = [math.sin(2 * math.pi * b * n / fs) for n in range(2)]
    amps = tone_amplitudes([b, -b], samples, fs)
    assert abs(amps[0] - (-0.5j)) <= 1e-9 and abs(amps[1] - 0.5j) <= 1e-9


def test_finite_energy_signal_at_exactly_twice_its_band() -> None:
    # sinc(t)^2 has the spectrum max(0, 1 - |f|): band B = 1 Hz, zero at the edge.
    # At fs = 2 the cardinal series reconstructs it; the truncation error falls like 1 / N^3.
    worst = {}
    for n_max in (50, 100, 200):
        samples = [sinc(n / 2) ** 2 for n in range(-n_max, n_max + 1)]
        worst[n_max] = max(
            abs(cardinal_series(samples, -n_max, 2.0, -2.5 + j * 0.025) - sinc(-2.5 + j * 0.025) ** 2) for j in range(201)
        )
    assert worst[50] < 2e-6 and worst[100] < 2.5e-7 and worst[200] < 3e-8
    # Four times the window, about 4^3 = 64 times smaller error.
    assert 50 < worst[50] / worst[200] < 80


def test_sampling_below_twice_the_band_fails() -> None:
    # At fs = 1 the samples of sinc(t)^2 are those of sinc(t), and the series rebuilds sinc(t).
    samples = [sinc(n) ** 2 for n in range(-50, 51)]
    assert samples[50] == 1 and all(abs(v) <= 1e-30 for k, v in enumerate(samples) if k != 50)
    assert abs(cardinal_series(samples, -50, 1.0, 0.5) - 2 / math.pi) <= 1e-12
    assert abs(sinc(0.5) ** 2 - 4 / math.pi**2) <= 1e-12


def test_samples_carry_the_energy() -> None:
    # T times the sum of x(nT)^2 equals the integral of sinc^4, which is 2/3.
    total = 0.5 * sum(sinc(n / 2) ** 4 for n in range(-2000, 2001))
    assert abs(total - 2 / 3) <= 1e-10
