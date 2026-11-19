# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mel-frequency-cepstral-coefficients/. The authors are listed in prov/85RNE7.jsonl.

import cmath
import math
import random

import nlsdsp
from mel_frequency_cepstral_coefficients import (
    hz_to_mel,
    lifter,
    mel_to_hz,
    mel_weights,
    mfcc,
    mfcc_of_frame,
    pre_emphasis,
)
from nlsdsp import (
    all_pole,
    autocorr,
    dct2,
    fft,
    frames,
    hamming,
    hann,
    levinson,
    power_spectrum,
    pulse_train,
    sine,
    white_noise,
)


# ---------------------------------------------------------------- the shared helper nlsdsp.py


def test_helper_header():
    with open(nlsdsp.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1] == (
        "# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/."
        " The authors are listed in prov/."
    )


def test_frames_check_value():
    x = [0.0] * 16000
    fr = frames(x, 400, 160)
    assert len(fr) == 98
    assert all(len(f) == 400 for f in fr)
    assert len(frames(x[:399], 400, 160)) == 0
    assert len(frames(x[:400], 400, 160)) == 1
    assert len(frames(x[:559], 400, 160)) == 1
    assert len(frames(x[:560], 400, 160)) == 2
    y = list(range(10))
    assert frames(y, 4, 3) == [[0, 1, 2, 3], [3, 4, 5, 6], [6, 7, 8, 9]]


def test_windows():
    w = hamming(400)
    assert abs(w[0] - 0.08) < 1e-12 and abs(w[-1] - 0.08) < 1e-12
    assert all(abs(w[i] - w[399 - i]) < 1e-12 for i in range(400))
    assert abs(max(w) - 1.0) < 1e-4
    h = hann(5)
    assert [round(v, 12) for v in h] == [0.0, 0.5, 1.0, 0.5, 0.0]
    assert hamming(1) == [1.0] and hann(1) == [1.0]


def _dft(x):
    n = len(x)
    return [sum(x[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]


def test_fft_against_dft():
    rng = random.Random(1)
    for n in (1, 2, 4, 8, 32, 64):
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        got, ref = fft(x), _dft(x)
        assert all(abs(g - r) < 1e-9 for g, r in zip(got, ref))
    x = sine(1000.0, 16000.0, 64)
    got, ref = fft(x), _dft(x)
    assert all(abs(g - r) < 1e-9 for g, r in zip(got, ref))
    # 1000 Hz at 16 kHz with 64 points falls on bin 4: |X[4]| = 64 / 2
    assert abs(abs(got[4]) - 32.0) < 1e-9
    try:
        fft([0.0] * 6)
    except ValueError:
        pass
    else:
        raise AssertionError("length 6 must fail")


def test_power_spectrum():
    x = sine(500.0, 8000.0, 16)
    ps = power_spectrum(x, 32)
    assert len(ps) == 17
    ref = _dft(x + [0.0] * 16)
    assert all(abs(ps[k] - abs(ref[k]) ** 2) < 1e-9 for k in range(17))
    # Parseval: sum |x|^2 = (1 / N) sum over all N bins of |X|^2
    full = [abs(v) ** 2 for v in ref]
    assert abs(sum(v * v for v in x) - sum(full) / 32) < 1e-9


def test_dct2_orthonormal():
    n = 8
    rows = [dct2([1.0 if i == j else 0.0 for i in range(n)], n) for j in range(n)]
    # rows[j][k] is entry (k, j) of the DCT matrix; check orthogonality of the matrix
    for a in range(n):
        for b in range(n):
            dot = sum(rows[j][a] * rows[j][b] for j in range(n))
            assert abs(dot - (1.0 if a == b else 0.0)) < 1e-12
    c = dct2([2.0] * 5, 5)
    assert abs(c[0] - 2.0 * math.sqrt(5)) < 1e-12
    assert all(abs(v) < 1e-12 for v in c[1:])


def test_autocorr():
    assert autocorr([1.0, 2.0, 3.0], 3) == [14.0, 8.0, 3.0, 0.0]


def test_levinson_order_two():
    a_true = [1.3, -0.81]  # poles at radius 0.9, angle about 43.8 degrees
    h = all_pole([1.0] + [0.0] * 599, a_true)
    r = autocorr(h, 2)
    a, e = levinson(r, 2)
    assert abs(a[0] - 1.3) < 1e-9 and abs(a[1] + 0.81) < 1e-9
    # the impulse response has prediction error exactly the first sample: e = 1
    assert abs(e - 1.0) < 1e-9
    # a higher order fit gives zeros beyond order 2
    a4, _ = levinson(autocorr(h, 4), 4)
    assert abs(a4[2]) < 1e-9 and abs(a4[3]) < 1e-9
    # noise through the same filter gives the coefficients up to sampling error
    rng = random.Random(7)
    y = all_pole(white_noise(rng, 8000, 1.0), a_true)
    a_est, _ = levinson(autocorr(y, 2), 2)
    assert abs(a_est[0] - 1.3) < 0.03 and abs(a_est[1] + 0.81) < 0.03


def test_levinson_matches_direct_solve():
    r = [4.0, 2.0, 1.0]
    a, e = levinson(r, 2)
    # normal equations [[4, 2], [2, 4]] a = [2, 1]
    assert abs(a[0] - 0.5) < 1e-12 and abs(a[1]) < 1e-12
    assert abs(e - (4.0 - 0.5 * 2.0)) < 1e-12


def test_pulse_train_and_noise():
    x = pulse_train(100.0, 16000.0, 500)
    assert [i for i, v in enumerate(x) if v] == [0, 160, 320, 480]
    x = pulse_train(120.0, 8000.0, 300)
    assert [i for i, v in enumerate(x) if v] == [0, 67, 133, 200, 267]
    n1 = white_noise(random.Random(3), 5, 0.1)
    n2 = white_noise(random.Random(3), 5, 0.1)
    assert n1 == n2 and len(n1) == 5


def test_all_pole_first_order():
    y = all_pole([1.0, 0.0, 0.0, 0.0], [0.5])
    assert y == [1.0, 0.5, 0.25, 0.125]


# ---------------------------------------------------------------- MFCC


def test_frame_count_and_shape():
    x = sine(440.0, 16000.0, 16000)
    c = mfcc(x)
    assert len(c) == 98 and all(len(row) == 13 for row in c)
    assert mfcc(x[:399]) == []


def test_pre_emphasis_and_lifter():
    y = pre_emphasis([1.0, 1.0, 1.0, 0.0])
    assert y[0] == 1.0 and abs(y[1] - 0.03) < 1e-15 and abs(y[2] - 0.03) < 1e-15 and y[3] == -0.97
    w = lifter([1.0] * 23, 22)
    assert w[0] == 1.0 and abs(w[11] - 12.0) < 1e-12 and abs(w[22] - 1.0) < 1e-12
    assert lifter([3.0, 4.0], 0) == [3.0, 4.0]


def test_silence_gives_only_c0():
    c = mfcc([0.0] * 800)
    assert len(c) == 3
    for row in c:
        assert abs(row[0] - math.sqrt(26) * math.log(1e-10)) < 1e-9
        assert all(abs(v) < 1e-9 for v in row[1:])


def test_gain_changes_only_c0():
    rng = random.Random(11)
    x = white_noise(rng, 1200, 0.1)
    a = mfcc(x)
    b = mfcc([3.0 * v for v in x])
    for ra, rb in zip(a, b):
        assert abs(rb[0] - ra[0] - math.sqrt(26) * 2 * math.log(3.0)) < 1e-9
        assert all(abs(u - v) < 1e-9 for u, v in zip(ra[1:], rb[1:]))


def test_parseval_of_the_orthonormal_dct():
    rng = random.Random(2)
    x = white_noise(rng, 400, 0.1)
    w = mel_weights(26, 512, 16000.0)
    win = hamming(400)
    c = mfcc_of_frame(pre_emphasis(x), w, win, num_ceps=26, cep_lifter=0)
    p = power_spectrum([s * v for s, v in zip(pre_emphasis(x), win)], 512)
    log_e = [math.log(max(sum(a * b for a, b in zip(row, p)), 1e-10)) for row in w]
    assert abs(sum(v * v for v in c) - sum(v * v for v in log_e)) < 1e-8


def test_against_a_direct_computation():
    # a second, slow path: direct DFT, explicit triangles in mel edges, explicit DCT-II sums
    rng = random.Random(4)
    fs, n_len, hop, nfft, m_count, k_count, q = 8000.0, 200, 80, 256, 20, 12, 22
    x = white_noise(rng, 360, 0.2)
    got = mfcc(x, fs, m_count, k_count, n_len, hop, nfft)
    y = [x[0]] + [x[i] - 0.97 * x[i - 1] for i in range(1, len(x))]
    hi = 2595 * math.log10(1 + 4000 / 700)
    edges = [700 * (10 ** (i * hi / (m_count + 1) / 2595) - 1) for i in range(m_count + 2)]
    ref = []
    for t in range(1 + (len(y) - n_len) // hop):
        fr = [y[t * hop + i] * (0.54 - 0.46 * math.cos(2 * math.pi * i / (n_len - 1))) for i in range(n_len)]
        power = [abs(sum(fr[i] * cmath.exp(-2j * math.pi * k * i / nfft) for i in range(n_len))) ** 2 for k in range(nfft // 2 + 1)]
        log_e = []
        for m in range(m_count):
            lo, ce, hi_e = edges[m], edges[m + 1], edges[m + 2]
            e = 0.0
            for k, pk in enumerate(power):
                f = k * fs / nfft
                if lo < f <= ce:
                    e += pk * (f - lo) / (ce - lo)
                elif ce < f < hi_e:
                    e += pk * (hi_e - f) / (hi_e - ce)
            log_e.append(math.log(max(e, 1e-10)))
        row = []
        for j in range(k_count):
            s = math.sqrt((1 if j == 0 else 2) / m_count)
            cj = s * sum(log_e[i] * math.cos(math.pi * j * (i + 0.5) / m_count) for i in range(m_count))
            row.append((1 + q / 2 * math.sin(math.pi * j / q)) * cj)
        ref.append(row)
    assert len(got) == len(ref) == 3
    for g, r in zip(got, ref):
        assert all(abs(u - v) < 1e-7 for u, v in zip(g, r))


def test_tone_moves_energy_to_its_filter():
    # the log mel energies of a pure tone peak in the filter whose center is the tone
    w = mel_weights(26, 512, 16000.0)
    lo, hi = 0.0, hz_to_mel(8000.0)
    center = mel_to_hz(lo + 8 * (hi - lo) / 27)
    x = sine(center, 16000.0, 400)
    win = hamming(400)
    p = power_spectrum([s * v for s, v in zip(x, win)], 512)
    e = [sum(a * b for a, b in zip(row, p)) for row in w]
    assert max(range(26), key=lambda i: e[i]) == 7


def test_bad_arguments():
    try:
        mfcc([0.0] * 400, num_filters=10, num_ceps=13)
    except ValueError:
        pass
    else:
        raise AssertionError("num_ceps > num_filters must fail")
