# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subband-coding/. The authors are listed in prov/WGFYEV.jsonl.

import math
import random

from subband_coding import (
    allocate,
    analyze,
    ar1,
    ar1_band_variances,
    coding_gain,
    model_distortion,
    subband_code,
    synthesize,
    weights,
)

RHO = 0.95


def close(a, b, tol=1e-9):
    return all(abs(p - q) <= tol for p, q in zip(a, b)) and len(a) == len(b)


def test_worked_example() -> None:
    s = 1 / math.sqrt(2)
    bands = analyze([1, 2, 3, 4, 5, 6, 7, 8], 3)
    assert [len(b) for b in bands] == [1, 1, 2, 4]
    assert close(bands[0], [36 / math.sqrt(8)])  # the sum over sqrt(8): 12.7279
    assert close(bands[1], [-8 * s])
    assert close(bands[2], [-2, -2])
    assert close(bands[3], [-s] * 4)
    packet = analyze([1, 2, 3, 4, 5, 6, 7, 8], 2, full=True)
    assert close(packet[0], [5, 13]) and close(packet[2] + packet[3], [-1, -1, 0, 0])


def test_perfect_reconstruction_and_energy() -> None:
    rng = random.Random(1)
    for full in (False, True):
        for levels in range(0, 6):
            x = [rng.uniform(-10, 10) for _ in range(64)]
            bands = analyze(x, levels, full)
            assert sum(len(b) for b in bands) == len(x)  # critically sampled
            assert close(synthesize(bands, full), x)
            e = sum(v * v for v in x)
            assert abs(sum(v * v for b in bands for v in b) - e) < 1e-9 * e  # orthonormal bank


def test_ar1_band_variances_and_gain() -> None:
    v1 = ar1_band_variances(RHO, 1)
    assert close(v1, [1 + RHO, 1 - RHO])
    expected_db = {1: 5.055, 2: 7.174, 3: 7.942, 4: 8.182, 5: 8.243, 6: 8.254}
    prev = 1.0
    for levels, db in expected_db.items():
        v = ar1_band_variances(RHO, levels)
        w = weights(analyze([0.0] * 2 ** levels, levels))
        assert abs(sum(a * b for a, b in zip(w, v)) - 1) < 1e-12  # the variance is kept
        g = coding_gain(v, w)
        assert abs(10 * math.log10(g) - db) < 1e-3
        assert prev < g < 1 / (1 - RHO ** 2)  # below the spectral flatness bound, 10.11 dB
        prev = g
    # The full tree of depth 3 gains only 0.004 dB over the dyadic tree on this source.
    vf = ar1_band_variances(RHO, 3, full=True)
    assert abs(10 * math.log10(coding_gain(vf, [1 / 8] * 8)) - 7.946) < 1e-3


def test_measured_band_variances() -> None:
    x = ar1(1 << 15, RHO, 1)
    for levels in (1, 2, 3):
        for band, v in zip(analyze(x, levels), ar1_band_variances(RHO, levels)):
            assert abs(sum(a * a for a in band) / len(band) - v) < 0.1 * v


def test_bit_allocation() -> None:
    v = ar1_band_variances(RHO, 3)
    w = [1 / 8, 1 / 8, 1 / 4, 1 / 2]
    gm = math.exp(sum(a * math.log(b) for a, b in zip(w, v)))
    for rate in (1, 2, 3):
        b = allocate(v, w, rate)
        bh = allocate(v, w, rate, clip=False)
        assert close(b, bh, 1e-6)  # no band is clipped at these rates
        assert abs(sum(a * c for a, c in zip(w, b)) - rate) < 1e-9
        d = [vk * 2 ** (-2 * bk) for vk, bk in zip(v, b)]
        assert max(d) - min(d) < 1e-9  # equal distortion in every band
        assert abs(model_distortion(v, w, b) - gm * 2 ** (-2 * rate)) < 1e-9
        assert abs(2 ** (-2 * rate) / model_distortion(v, w, b) - coding_gain(v, w)) < 1e-6
    assert close([round(a, 3) for a in allocate(v, w, 1)], [3.725, 1.801, 0.92, 0.158])
    # At 0.5 bits per sample the rule of Huang and Schultheiss gives the top band -0.342 bits.
    assert round(allocate(v, w, 0.5, clip=False)[3], 3) == -0.342
    b = allocate(v, w, 0.5)
    assert b[3] == 0 and abs(sum(a * c for a, c in zip(w, b)) - 0.5) < 1e-9
    # No other allocation with the same rate and no negative bits does better.
    rng = random.Random(2)
    best = model_distortion(v, w, b)
    for _ in range(2000):
        raw = [rng.random() for _ in v]
        scale = 0.5 / sum(a * c for a, c in zip(w, raw))
        assert model_distortion(v, w, [r * scale for r in raw]) >= best - 1e-12


def test_subband_coder_against_pcm() -> None:
    x = ar1(1 << 15, RHO, 1)
    for step in (0.05, 0.1, 0.2):
        y0, r0 = subband_code(x, 0, step)  # zero levels: plain PCM with an entropy coder
        y3, r3 = subband_code(x, 3, step)
        for y in (y0, y3):
            mse = sum((a - b) ** 2 for a, b in zip(x, y)) / len(x)
            assert abs(mse - step ** 2 / 12) < 0.03 * step ** 2 / 12
        gain_bits = 0.5 * math.log2(coding_gain(ar1_band_variances(RHO, 3), [1 / 8, 1 / 8, 1 / 4, 1 / 2]))
        assert abs((r0 - r3) - gain_bits) < 0.05  # 1.32 bits per sample saved
