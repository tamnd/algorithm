# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mel-scale/. The authors are listed in prov/AJSQPY.jsonl.

import math

from mel_scale import hz_to_mel, hz_to_mel_slaney, mel_to_hz, mel_to_hz_slaney


def test_check_values():
    assert round(hz_to_mel(700.0), 2) == 781.17
    assert round(hz_to_mel(1000.0), 2) == 999.99
    assert round(hz_to_mel(4000.0), 2) == 2146.06
    assert round(hz_to_mel(8000.0), 2) == 2840.02
    assert hz_to_mel(0.0) == 0.0


def test_inverse():
    for f in (0.0, 50.0, 999.0, 1000.0, 1001.0, 4000.0, 11025.0):
        assert abs(mel_to_hz(hz_to_mel(f)) - f) < 1e-9
        assert abs(mel_to_hz_slaney(hz_to_mel_slaney(f)) - f) < 1e-9


def test_natural_log_form_agrees_to_four_digits():
    # 2595 / ln 10 = 1126.99..., so 1127 ln(1 + f / 700) is the same scale rounded
    assert abs(2595.0 / math.log(10.0) - 1127.0) < 0.01
    for f in range(0, 8001, 250):
        assert abs(hz_to_mel(f) - 1127.0 * math.log(1.0 + f / 700.0)) < 0.02


def test_shape_linear_then_log():
    # equal ratios of f give nearly equal mel steps far above 700 Hz
    a = hz_to_mel(8000.0) - hz_to_mel(4000.0)
    b = hz_to_mel(16000.0) - hz_to_mel(8000.0)
    assert abs(a - b) / a < 0.1
    # near 0 Hz the slope is 2595 / (700 ln 10), about 1.61 mel per Hz
    slope = (hz_to_mel(1.0) - hz_to_mel(0.0)) / 1.0
    assert abs(slope - 2595.0 / (700.0 * math.log(10.0))) < 2e-3


def test_slaney_scale():
    assert abs(hz_to_mel_slaney(1000.0) - 15.0) < 1e-12
    assert abs(hz_to_mel_slaney(500.0) - 7.5) < 1e-12
    # 27 mel above 1 kHz is a factor 6.4 in frequency
    assert abs(mel_to_hz_slaney(15.0 + 27.0) - 6400.0) < 1e-9
    # continuous at 1 kHz
    assert abs(hz_to_mel_slaney(999.999999) - hz_to_mel_slaney(1000.0)) < 1e-6
    # the two scales differ: in Slaney units scaled so 1 kHz is 1000, 4 kHz is about 2344, not 2146
    scaled = hz_to_mel_slaney(4000.0) * 1000.0 / 15.0
    assert abs(scaled - 2344.2) < 0.1


def test_monotone_and_bad_input():
    fs = [i * 37.0 for i in range(300)]
    for g in (hz_to_mel, hz_to_mel_slaney):
        vals = [g(f) for f in fs]
        assert all(u < v for u, v in zip(vals, vals[1:]))
        try:
            g(-1.0)
        except ValueError:
            continue
        raise AssertionError(g)
