# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyphase-resampling/. The authors are listed in prov/1Y8M5W.jsonl.

import math
import random
from fractions import Fraction

from polyphase_resampling import lowpass_design, resample, resample_direct, resample_poly


def rand_fracs(rng, n):
    return [Fraction(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(n)]


def test_equals_three_stage_exact() -> None:
    rng = random.Random(12101)
    for _ in range(300):
        l, m = rng.randint(1, 7), rng.randint(1, 7)
        h = rand_fracs(rng, rng.randint(1, 25))
        x = rand_fracs(rng, rng.randint(1, 25))
        assert resample_poly(x, h, l, m) == resample_direct(x, h, l, m)


def test_special_cases() -> None:
    rng = random.Random(12102)
    for _ in range(50):
        h = rand_fracs(rng, rng.randint(1, 12))
        x = rand_fracs(rng, rng.randint(1, 20))
        f = rng.randint(1, 5)
        full = [Fraction(0)] * (len(h) + len(x) - 1)
        for i, a in enumerate(h):
            for j, b in enumerate(x):
                full[i + j] += a * b
        assert resample_poly(x, h, 1, f) == full[::f]  # L = 1 is a decimator
        u = [Fraction(0)] * (len(x) * f)
        u[::f] = x
        conv = [Fraction(0)] * (len(h) + len(u) - 1)
        for i, a in enumerate(h):
            for j, b in enumerate(u):
                conv[i + j] += a * b
        assert resample_poly(x, h, f, 1) == conv  # M = 1 is an interpolator
        assert resample_poly(x, h, 1, 1) == full


def test_output_length() -> None:
    for l, m, k, n in [(3, 2, 7, 10), (160, 147, 1, 147), (2, 5, 4, 13), (1, 1, 1, 1)]:
        y = resample_poly([1] * n, [1] * k, l, m)
        assert len(y) == (k + l * n - 2) // m + 1


def test_multiplies_per_output() -> None:
    """Each output uses one phase, which has ceil(K / L) or floor(K / L) taps."""
    l, m = 160, 147
    k = 2 * 10 * l + 1
    sizes = {len(list(range(k))[r::l]) for r in range(l)}
    assert sizes <= {k // l, -(-k // l)}


def test_tone_survives() -> None:
    """A slow sine sampled at rate 1 comes out as the same sine sampled at rate L/M, after the filter delay."""
    for l, m in [(3, 2), (2, 3), (4, 5), (5, 4)]:
        f = 0.03  # cycles per input sample, far below both Nyquist limits
        x = [math.sin(2 * math.pi * f * n) for n in range(400)]
        y = resample(x, l, m)
        h = lowpass_design(l, m)
        delay = (len(h) - 1) / 2  # in high-rate samples
        for n in range(len(y)):
            t = (n * m - delay) / l  # the input time of output n
            if 40 <= t <= 360:
                assert abs(y[n] - math.sin(2 * math.pi * f * t)) < 2e-3


def test_reduced_fraction_same_rate() -> None:
    x = [math.cos(0.1 * n) for n in range(100)]
    assert resample(x, 6, 4) == resample(x, 3, 2)
