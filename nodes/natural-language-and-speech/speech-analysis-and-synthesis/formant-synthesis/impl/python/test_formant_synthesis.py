# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/formant-synthesis/. The authors are listed in prov/D7ZPSZ.jsonl.

import math
import random

from formant_synthesis import (
    antiresonator_coeffs,
    filter_signal,
    resonator_coeffs,
    response,
    synthesize,
)

FS = 10000


def test_unit_gain_at_zero_hertz():
    for f, bw in ((500, 60), (1500, 90), (3000, 250), (0, 100)):
        k = resonator_coeffs(f, bw, FS)
        assert abs(sum(filter_signal([1.0] * 3000, k)[-1:]) - 1.0) < 1e-6  # a step settles at gain 1
        assert abs(response(k, 0, FS) - 1.0) < 1e-12
        assert abs(response(antiresonator_coeffs(f, bw, FS), 0, FS) - 1.0) < 1e-12


def test_coefficients_of_the_example():
    a, b, c = resonator_coeffs(500, 60, FS)
    assert abs(a - 0.0964078) < 1e-7
    assert abs(b - 1.8665948) < 1e-7
    assert abs(c + 0.9630027) < 1e-7


def test_impulse_response_is_a_damped_sinusoid():
    f, bw = 500, 60
    k = resonator_coeffs(f, bw, FS)
    r = math.exp(-math.pi * bw / FS)
    theta = 2 * math.pi * f / FS
    h = filter_signal([1.0] + [0.0] * 199, k)
    for n, v in enumerate(h):
        assert abs(v - k[0] * r**n * math.sin((n + 1) * theta) / math.sin(theta)) < 1e-12


def test_peak_is_where_the_closed_form_says_and_near_the_center():
    for f, bw in ((500, 60), (1200, 80), (2500, 200), (300, 150)):
        k = resonator_coeffs(f, bw, FS)
        r = math.exp(-math.pi * bw / FS)
        theta = 2 * math.pi * f / FS
        want = math.acos((1 + r * r) * math.cos(theta) / (2 * r)) * FS / (2 * math.pi)
        grid = [f - 200 + i * 0.01 for i in range(40001)]
        got = max(grid, key=lambda g: abs(response(k, g, FS)))
        assert abs(got - want) < 0.02
        assert abs(got - f) < bw  # the peak is close to the center, closer when bw is small


def test_half_power_bandwidth_is_close_to_bw_for_narrow_resonances():
    for f, bw in ((500, 60), (1500, 90), (2500, 120)):
        k = resonator_coeffs(f, bw, FS)
        top = abs(response(k, f, FS))
        grid = [f - 300 + i * 0.05 for i in range(12001)]
        inside = [g for g in grid if abs(response(k, g, FS)) >= top / math.sqrt(2)]
        assert abs((inside[-1] - inside[0]) - bw) < 0.03 * bw  # a measurement, not a theorem


def test_antiresonator_undoes_the_resonator():
    rng = random.Random(1)
    x = [rng.uniform(-1, 1) for _ in range(500)]
    y = filter_signal(filter_signal(x, resonator_coeffs(800, 100, FS)), antiresonator_coeffs(800, 100, FS), anti=True)
    assert max(abs(a - b) for a, b in zip(x, y)) < 1e-9


def test_cascade_is_the_product_of_the_sections():
    fmts = [(700, 130), (1220, 70), (2600, 160)]
    ks = [resonator_coeffs(f, bw, FS) for f, bw in fmts]
    h = [1.0] + [0.0] * 2047
    for k in ks:
        h = filter_signal(h, k)
    for f in (100, 700, 1220, 2000, 2600, 4000):
        z = [complex(math.cos(2 * math.pi * f * n / FS), -math.sin(2 * math.pi * f * n / FS)) for n in range(2048)]
        dtft = sum(v * w for v, w in zip(h, z))
        prod = 1.0
        for k in ks:
            prod *= response(k, f, FS)
        assert abs(dtft - prod) < 1e-6


def test_synthesized_vowel_has_the_pitch_period_and_formant_peaks():
    frames = [(100, 1.0, [(700, 130), (1220, 70), (2600, 160)])] * 40  # 0.2 s of a vowel like /a/
    x = synthesize(frames, FS)
    assert len(x) == 2000
    # the output repeats every 100 samples once the start has decayed
    assert max(abs(x[n] - x[n + 100]) for n in range(1500, 1900)) < 1e-6
    # the harmonics near the formants are stronger than those between them
    seg = x[1000:2000]

    def harmonic(f):
        return abs(sum(v * complex(math.cos(2 * math.pi * f * n / FS), -math.sin(2 * math.pi * f * n / FS)) for n, v in enumerate(seg)))

    assert harmonic(700) > 3 * harmonic(1000)
    assert harmonic(1200) > 3 * harmonic(1900)


def test_silence_when_f0_is_zero():
    assert synthesize([(0, 1.0, [(500, 60)])] * 3, FS) == [0.0] * 150
