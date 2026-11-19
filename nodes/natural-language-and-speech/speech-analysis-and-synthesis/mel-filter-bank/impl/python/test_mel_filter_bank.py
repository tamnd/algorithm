# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mel-filter-bank/. The authors are listed in prov/3Y1ZJS.jsonl.

import cmath
import math
import random

from mel_filter_bank import (
    apply_filter_bank,
    edge_frequencies,
    hz_to_mel,
    log_energies,
    log_mel_spectrogram,
    mel_filter_bank,
    mel_to_hz,
)
from nlsdsp import hamming, sine


def test_mel_check_values():
    assert round(hz_to_mel(700.0), 2) == 781.17
    assert round(hz_to_mel(1000.0), 2) == 999.99
    # the area brief gives 2146.07; 2595 log_10(1 + 4000 / 700) = 2146.0645
    assert round(hz_to_mel(4000.0), 2) == 2146.06
    assert round(hz_to_mel(8000.0), 2) == 2840.02
    for f in (0.0, 123.4, 1000.0, 7999.0):
        assert abs(mel_to_hz(hz_to_mel(f)) - f) < 1e-9
    # the same scale in natural log: 1127 ln(1 + f / 700), to the 4 digits of 1127
    for f in (300.0, 3000.0):
        assert abs(hz_to_mel(f) - 1127.0 * math.log(1 + f / 700.0)) < 0.05


def test_edges_are_equally_spaced_in_mel():
    edges = edge_frequencies(26, 0.0, 8000.0)
    assert len(edges) == 28
    assert edges[0] == 0.0 and abs(edges[-1] - 8000.0) < 1e-9
    mels = [hz_to_mel(f) for f in edges]
    steps = [b - a for a, b in zip(mels, mels[1:])]
    assert max(steps) - min(steps) < 1e-9


def test_shape_and_triangles():
    w = mel_filter_bank(26, 512, 16000.0)
    assert len(w) == 26 and all(len(row) == 257 for row in w)
    edges = edge_frequencies(26, 0.0, 8000.0)
    for m, row in enumerate(w):
        assert all(0.0 <= v <= 1.0 for v in row)
        nz = [k for k, v in enumerate(row) if v > 0]
        assert nz, "every filter of this bank covers a bin"
        # the support is inside (f_m, f_{m+2}) in 0 based edges
        assert all(edges[m] < k * 16000.0 / 512 < edges[m + 2] for k in nz)
        # the largest weight sits on the bin nearest the center, from either side
        kmax = max(range(257), key=lambda k: row[k])
        assert abs(kmax * 16000.0 / 512 - edges[m + 1]) <= 16000.0 / 512


def test_peak_is_one_at_the_center():
    # with a fine grid the bin nearest each center has weight close to 1
    nfft = 1 << 14
    w = mel_filter_bank(10, nfft, 16000.0)
    df = 16000.0 / nfft
    edges = edge_frequencies(10, 0.0, 8000.0)
    for m, row in enumerate(w):
        bound = df / min(edges[m + 1] - edges[m], edges[m + 2] - edges[m + 1])
        assert 1.0 - bound <= max(row) <= 1.0


def test_filters_overlap_by_half():
    # between the first and the last center, the weights of each bin sum to 1
    fs, nfft = 16000.0, 512
    w = mel_filter_bank(26, nfft, fs, 100.0, 7000.0)
    edges = edge_frequencies(26, 100.0, 7000.0)
    for k in range(nfft // 2 + 1):
        f = k * fs / nfft
        total = sum(row[k] for row in w)
        nonzero = sum(1 for row in w if row[k] > 0)
        if edges[1] <= f <= edges[26]:
            assert abs(total - 1.0) < 1e-12
            assert nonzero in (1, 2)
        if f <= edges[0] or f >= edges[27]:
            assert total == 0.0


def _triangle(f, left, center, right):
    if left < f <= center:
        return (f - left) / (center - left)
    if center < f < right:
        return (right - f) / (right - center)
    return 0.0


def test_band_energies_against_direct_dft():
    rng = random.Random(5)
    fs, nfft, n, m_count = 8000.0, 64, 50, 8
    frame = [rng.uniform(-1, 1) for _ in range(n)]
    padded = frame + [0.0] * (nfft - n)
    power = []
    for k in range(nfft // 2 + 1):
        xk = sum(padded[t] * cmath.exp(-2j * math.pi * k * t / nfft) for t in range(nfft))
        power.append(abs(xk) ** 2)
    lo, hi = 2595 * math.log10(1 + 0 / 700), 2595 * math.log10(1 + 4000 / 700)
    edges = [700 * (10 ** ((lo + i * (hi - lo) / (m_count + 1)) / 2595) - 1) for i in range(m_count + 2)]
    ref = [
        sum(_triangle(k * fs / nfft, edges[m], edges[m + 1], edges[m + 2]) * power[k] for k in range(nfft // 2 + 1))
        for m in range(m_count)
    ]
    from nlsdsp import power_spectrum

    got = apply_filter_bank(mel_filter_bank(m_count, nfft, fs), power_spectrum(frame, nfft))
    assert all(abs(g - r) < 1e-9 * max(1.0, abs(r)) for g, r in zip(got, ref))


def test_sine_lands_in_the_filter_of_its_frequency():
    fs = 16000.0
    edges = edge_frequencies(26, 0.0, 8000.0)
    win = hamming(400)
    for m in (3, 10, 20):
        f = edges[m + 1]
        x = sine(f, fs, 400)
        from nlsdsp import power_spectrum

        e = apply_filter_bank(mel_filter_bank(26, 512, fs), power_spectrum([a * b for a, b in zip(x, win)], 512))
        assert max(range(26), key=lambda i: e[i]) == m


def test_log_floor_and_spectrogram():
    assert log_energies([0.0, 1.0, math.e]) == [math.log(1e-10), 0.0, 1.0]
    rows = log_mel_spectrogram([0.0] * 1600)
    assert len(rows) == 8 and all(len(r) == 40 for r in rows)
    assert all(v == math.log(1e-10) for r in rows for v in r)
    # doubling the amplitude adds ln 4 to every log energy
    x = sine(440.0, 16000.0, 560)
    a = log_mel_spectrogram(x, num_filters=20)
    b = log_mel_spectrogram([2 * v for v in x], num_filters=20)
    for ra, rb in zip(a, b):
        for u, v in zip(ra, rb):
            if u > math.log(1e-10) + 30:
                assert abs(v - u - math.log(4.0)) < 1e-9


def test_bad_arguments():
    for args in ((0, 512, 16000.0), (26, 512, 16000.0, 0.0, 9000.0), (26, 512, 16000.0, 5000.0, 4000.0)):
        try:
            mel_filter_bank(*args)
        except ValueError:
            continue
        raise AssertionError(args)
