# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aliasing/. The authors are listed in prov/2AWSJX.jsonl.

import cmath
import math
import random
from fractions import Fraction

from aliasing import alias_frequency, folded_frequency, sample_cos, sample_exp, sample_sin, sampled_spectrum


def test_f_and_f_plus_k_fs_give_identical_samples() -> None:
    rng = random.Random(1)
    for _ in range(200):
        fs = Fraction(rng.randint(1, 50), rng.randint(1, 4))
        f = Fraction(rng.randint(-200, 200), rng.randint(1, 7))
        k = rng.randint(-20, 20)
        phase = Fraction(rng.randint(0, 99), 100)
        assert sample_cos(f, fs, 64, phase) == sample_cos(f + k * fs, fs, 64, phase)
        assert sample_sin(f, fs, 64, phase) == sample_sin(f + k * fs, fs, 64, phase)
        assert sample_exp(f, fs, 64) == sample_exp(f + k * fs, fs, 64)


def test_reduction_agrees_with_the_direct_formula() -> None:
    rng = random.Random(2)
    for _ in range(100):
        fs = rng.randint(1, 100)
        f = rng.randint(-300, 300)
        got = sample_cos(f, fs, 32)
        want = [math.cos(2 * math.pi * f * n / fs) for n in range(32)]
        assert all(abs(g - w) <= 1e-9 for g, w in zip(got, want))


def test_alias_lands_in_the_baseband_with_the_same_samples() -> None:
    rng = random.Random(3)
    for _ in range(200):
        fs = Fraction(rng.randint(1, 40))
        f = Fraction(rng.randint(-500, 500), rng.randint(1, 5))
        a = alias_frequency(f, fs)
        assert -fs / 2 <= a < fs / 2
        assert (f - a) % fs == 0
        assert sample_exp(f, fs, 40) == sample_exp(a, fs, 40)


def test_real_tones_fold_about_half_the_rate() -> None:
    # fs = 10 Hz: 3, 7, 13 and 17 Hz cosines give the same samples; the sines at 7 and 17 Hz change sign.
    fs = 10
    base_cos = sample_cos(3, fs, 50)
    base_sin = sample_sin(3, fs, 50)
    for f in (7, 13, 17, 23, -3):
        assert folded_frequency(f, fs) == 3
        assert all(abs(a - b) <= 1e-12 for a, b in zip(sample_cos(f, fs, 50), base_cos))
    for f, sign in ((13, 1), (7, -1), (17, -1), (-3, -1)):
        assert all(abs(a - sign * b) <= 1e-12 for a, b in zip(sample_sin(f, fs, 50), base_sin))


def test_folded_frequency_by_brute_force() -> None:
    # The folded frequency is the distance from f to the nearest multiple of fs.
    rng = random.Random(4)
    for _ in range(300):
        fs = Fraction(rng.randint(1, 30))
        f = Fraction(rng.randint(-400, 400), rng.randint(1, 3))
        candidates = [abs(f - k * fs) for k in range(-401, 402)]
        assert folded_frequency(f, fs) == min(candidates)


def test_tone_at_half_the_rate() -> None:
    # At f = fs/2 the cosine samples are (-1)^n cos(phase) and the sine samples are zero.
    for n, v in enumerate(sample_cos(5, 10, 20, Fraction(1, 8))):
        assert abs(v - (-1) ** n * math.cos(math.pi / 4)) <= 1e-12
    assert all(abs(v) <= 1e-12 for v in sample_sin(5, 10, 20))


def test_poisson_summation_for_a_gaussian() -> None:
    # x(t) = exp(-pi t^2) has the spectrum exp(-pi f^2). The DTFT of its samples
    # equals the sum of shifted spectra; compare both sides directly.
    def gauss(f: float) -> float:
        return math.exp(-math.pi * f * f)

    for fs in (0.5, 1.0, 1.5, 2.0, 4.0):
        for f in (0.0, 0.1, 0.3, fs / 2):
            direct = sum(gauss(n / fs) * cmath.exp(-2j * math.pi * f * n / fs) for n in range(-200, 201))
            assert abs(direct - sampled_spectrum(gauss, f, fs, 40)) <= 1e-12 * (1 + abs(direct))


def test_alias_error_of_the_gaussian_shrinks_with_the_rate() -> None:
    # The relative error of the sampled spectrum at f = 0 is the sum over k != 0 of exp(-pi k^2 fs^2).
    def gauss(f: float) -> float:
        return math.exp(-math.pi * f * f)

    errors = [sampled_spectrum(gauss, 0.0, fs, 40).real / fs - 1 for fs in (1.0, 2.0, 3.0)]
    assert errors[0] > errors[1] > errors[2] > 0
    assert abs(errors[0] - 0.0864348) <= 1e-6
    assert abs(errors[1] - 2 * math.exp(-4 * math.pi)) <= 1e-12
