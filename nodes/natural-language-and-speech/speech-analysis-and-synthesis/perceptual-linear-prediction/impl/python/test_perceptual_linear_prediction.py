# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perceptual-linear-prediction/. The authors are listed in prov/H7TRFV.jsonl.

import cmath
import math
import random

from nlsdsp import all_pole, levinson, pulse_train, white_noise
from perceptual_linear_prediction import (
    autocorrelation_of_spectrum,
    band_centers,
    bark_to_hz,
    critical_band_weights,
    equal_loudness,
    hz_to_bark,
    lpc_to_cepstrum,
    masking_curve,
    model_spectrum,
    plp_frame,
)


def test_bark_scale():
    assert round(hz_to_bark(5000.0), 1) == 16.9
    assert abs(hz_to_bark(600.0) - 6.0 * math.log(1.0 + math.sqrt(2.0))) < 1e-12
    for f in (0.0, 100.0, 1000.0, 3999.0):
        assert abs(bark_to_hz(hz_to_bark(f)) - f) < 1e-9


def test_masking_curve():
    assert masking_curve(0.0) == 1.0
    assert masking_curve(-0.5) == 1.0 and masking_curve(0.5) == 1.0
    assert abs(masking_curve(-1.3) - 0.01) < 1e-12
    assert abs(masking_curve(1.5) - 0.1) < 1e-12
    assert abs(masking_curve(2.5) - 0.01) < 1e-12
    assert masking_curve(-1.31) == 0.0 and masking_curve(2.51) == 0.0


def test_equal_loudness_rises_to_one():
    vals = [equal_loudness(f) for f in (50.0, 100.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0)]
    assert all(a < b for a, b in zip(vals, vals[1:]))
    assert all(0.0 < v < 1.0 for v in vals)
    assert equal_loudness(0.0) == 0.0
    assert abs(equal_loudness(1e7) - 1.0) < 1e-3


def test_band_centers_and_weights():
    c = band_centers(8000.0)
    assert len(c) == 17 and c[0] == 0.0 and abs(c[-1] - hz_to_bark(4000.0)) < 1e-12
    assert all(0.9 < b - a < 1.0 for a, b in zip(c, c[1:]))
    centers, w = critical_band_weights(256, 8000.0)
    assert len(w) == 17 and all(len(row) == 129 for row in w)
    # each band reaches 2.5 Bark below its center and 1.3 Bark above
    for ci, row in zip(centers, w):
        for k, v in enumerate(row):
            z = hz_to_bark(k * 8000.0 / 256)
            if v > 0:
                assert ci - 2.5 <= z <= ci + 1.3


def test_autocorrelation_of_spectrum_is_an_inverse_dft():
    rng = random.Random(3)
    phi = [rng.uniform(0.1, 2.0) for _ in range(9)]
    full = phi + phi[-2:0:-1]  # the even extension, 16 points
    n = len(full)
    ref = [(sum(full[i] * cmath.exp(2j * math.pi * k * i / n) for i in range(n)) / n).real for k in range(6)]
    got = autocorrelation_of_spectrum(phi, 5)
    assert all(abs(g - r) < 1e-12 for g, r in zip(got, ref))
    # a flat spectrum is white: r = [phi, 0, 0, ...]
    flat = autocorrelation_of_spectrum([2.0] * 9, 4)
    assert abs(flat[0] - 2.0) < 1e-12 and all(abs(v) < 1e-12 for v in flat[1:])


def _solve(m, b):
    # Gauss elimination with partial pivoting, for the Toeplitz check
    n = len(b)
    a = [row[:] + [b[i]] for i, row in enumerate(m)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        a[col], a[piv] = a[piv], a[col]
        for r in range(n):
            if r != col:
                f = a[r][col] / a[col][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def test_levinson_on_an_auditory_spectrum_matches_a_direct_solve():
    rng = random.Random(8)
    x = white_noise(rng, 200, 0.3)
    _, a, gain, phi = plp_frame(x, 8000.0, order=5)
    r = autocorrelation_of_spectrum(phi, 5)
    toeplitz = [[r[abs(i - j)] for j in range(5)] for i in range(5)]
    direct = _solve(toeplitz, r[1:6])
    assert all(abs(u - v) < 1e-9 for u, v in zip(a, direct))
    assert abs(gain - (r[0] - sum(ak * rk for ak, rk in zip(a, r[1:6])))) < 1e-9


def test_lpc_to_cepstrum_matches_the_log_spectrum():
    a, gain, n = [1.2, -0.7, 0.2], 0.5, 1024
    c = lpc_to_cepstrum(a, gain, 12)
    log_s = [math.log(model_spectrum(a, gain, 2 * math.pi * i / n)) for i in range(n)]
    for m in range(12):
        # c is the inverse DFT of the log model spectrum: ln S(w) = sum over all m of c_|m| e^{-j w m}
        ref = sum(log_s[i] * math.cos(2 * math.pi * m * i / n) for i in range(n)) / n
        assert abs(c[m] - ref) < 1e-9


def test_end_samples_copy_their_neighbors():
    rng = random.Random(1)
    _, _, _, phi = plp_frame(white_noise(rng, 200, 0.2), 8000.0)
    assert phi[0] == phi[1] and phi[-1] == phi[-2]


def test_gain_changes_only_c0():
    rng = random.Random(5)
    x = white_noise(rng, 200, 0.2)
    c1, a1, _, _ = plp_frame(x, 8000.0)
    c2, a2, _, _ = plp_frame([4.0 * v for v in x], 8000.0)
    # power scales by 16, the cube root law by 16^0.33, the gain by the same
    assert abs(c2[0] - c1[0] - 0.33 * math.log(16.0)) < 1e-9
    assert all(abs(u - v) < 1e-9 for u, v in zip(c1[1:], c2[1:]))
    assert all(abs(u - v) < 1e-9 for u, v in zip(a1, a2))


def test_model_peak_near_a_formant():
    fs = 8000.0
    top = hz_to_bark(fs / 2.0)
    for formant in (500.0, 1000.0, 1500.0, 2000.0):
        r = math.exp(-math.pi * 80.0 / fs)
        th = 2.0 * math.pi * formant / fs
        x = all_pole(pulse_train(100.0, fs, 600), [2.0 * r * math.cos(th), -r * r])
        _, a, gain, _ = plp_frame(x[200:400], fs, order=5)
        best = max(range(401), key=lambda i: model_spectrum(a, gain, math.pi * i / 400))
        # the model lives on the Bark axis: omega = pi means fs / 2
        assert abs(best / 400.0 * top - hz_to_bark(formant)) < 1.0
