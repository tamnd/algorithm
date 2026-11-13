# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-leakage/. The authors are listed in prov/SQWQYP.jsonl.

import cmath
import math
import random

from spectral_leakage import blackman, dft, far_leakage, hann, predicted_magnitude, tone, windowed


def test_whole_number_of_cycles_does_not_leak() -> None:
    n = 16
    mags = [abs(v) for v in dft(tone(n, 4))]
    assert abs(mags[4] - 8) <= 1e-9 and abs(mags[12] - 8) <= 1e-9
    assert all(m <= 1e-9 for k, m in enumerate(mags) if k not in (4, 12))


def test_half_cycle_leaks_into_every_bin() -> None:
    n = 16
    mags = [abs(v) for v in dft(tone(n, 4.5))]
    want = [1.0000, 1.0569, 1.2705, 1.8860, 5.2225, 5.0254, 1.7051, 1.1295, 1.0000]
    assert all(abs(mags[k] - w) <= 1e-4 for k, w in enumerate(want))
    assert all(m > 0.99 for m in mags)


def test_closed_form_dirichlet_prediction() -> None:
    rng = random.Random(1)
    for _ in range(30):
        n = rng.randint(4, 40)
        c = rng.uniform(0.3, n / 2 - 0.3)
        mags = [abs(v) for v in dft(tone(n, c))]
        assert all(abs(mags[k] - predicted_magnitude(n, c, k)) <= 1e-9 * n for k in range(n))


def test_scalloping_of_a_complex_tone_tends_to_two_over_pi() -> None:
    for n in (16, 256):
        x = [cmath.exp(2j * math.pi * (5.5) * k / n) for k in range(n)]
        peak = max(abs(v) for v in dft(x))
        assert abs(peak / n - 1 / (n * math.sin(math.pi / (2 * n)))) <= 1e-9
    assert abs(1 / (256 * math.sin(math.pi / 512)) - 2 / math.pi) <= 1e-5


def test_leakage_moves_energy_but_keeps_its_total() -> None:
    rng = random.Random(2)
    x = tone(32, rng.uniform(1, 15), 1.0, rng.uniform(0, 6))
    assert abs(sum(abs(v) ** 2 for v in dft(x)) - 32 * sum(v * v for v in x)) <= 1e-8


def test_windows_cut_far_leakage() -> None:
    n = 64
    rect, hn, bl = (far_leakage(windowed(tone(n, 10.5), w), 10.5, 3) for w in ([1.0] * n, hann(n), blackman(n)))
    assert abs(rect - 6.550e-2) <= 1e-5
    assert abs(hn - 1.124e-4) <= 1e-7
    assert abs(bl - 3.846e-6) <= 1e-8
    assert rect > hn > bl


def test_weak_tone_hidden_by_rectangular_found_by_hann_and_blackman() -> None:
    # Strong tone at 10.5 cycles, weak tone 60 dB down at 20 cycles, N = 64.
    n = 64
    x = [a + b for a, b in zip(tone(n, 10.5, 1.0), tone(n, 20, 1e-3))]

    def local_peak_at_20(w) -> bool:
        mags = [abs(v) for v in dft(windowed(x, w))]
        return mags[20] > mags[19] and mags[20] > mags[21]

    assert not local_peak_at_20([1.0] * n)
    assert local_peak_at_20(hann(n))
    assert local_peak_at_20(blackman(n))


def test_zero_padding_samples_the_same_leaky_spectrum() -> None:
    n = 16
    x = tone(n, 4.5)
    padded = dft(x + [0.0] * (3 * n))
    plain = dft(x)
    # every fourth padded value is an old bin, so the leakage at the bins is unchanged
    assert all(abs(padded[4 * k] - plain[k]) <= 1e-9 for k in range(n))
    # between the bins the padded DFT shows the side lobes of the Dirichlet kernel
    assert all(abs(abs(padded[k]) - predicted_magnitude(n, 4.5, k / 4)) <= 1e-9 for k in range(4 * n))
