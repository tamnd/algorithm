# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fractal-noise/. The authors are listed in prov/KJNY6S.jsonl.

"""Tests of fractal noise.

The sum is checked against a direct sum of the base noise, octave by octave.
The tests also check determinism for a fixed seed, the amplitude bound, the
sign of turbulence, the zeros at integer points when every octave has
lacunarity 2 and no offset, and the octave limit.
"""

import random

from fractal_noise import (
    GradientNoise2D,
    amplitude_sum,
    fbm,
    musgrave_gain,
    octave_limit,
    octave_offsets,
    turbulence,
)


def test_equals_sum_of_base_noise():
    noise = GradientNoise2D(seed=1)
    offs = octave_offsets(7, seed=2)
    rng = random.Random(1)
    for _ in range(500):
        x, y = rng.uniform(-30, 30), rng.uniform(-30, 30)
        K, lac, g = rng.randint(1, 7), rng.choice((2.0, 1.92, 2.5)), rng.uniform(0.3, 0.7)
        want, amp, freq = 0.0, 1.0, 1.0
        for i in range(K):
            want += amp * noise(x * freq + offs[i][0], y * freq + offs[i][1])
            amp, freq = amp * g, freq * lac
        assert abs(fbm(noise, x, y, K, lac, g, offs) - want) < 1e-12
        assert abs(fbm(noise, x, y, 1, lac, g) - noise(x, y)) < 1e-15


def test_deterministic_for_seed():
    a, b, c = GradientNoise2D(4), GradientNoise2D(4), GradientNoise2D(5)
    rng = random.Random(2)
    pts = [(rng.uniform(-50, 50), rng.uniform(-50, 50)) for _ in range(400)]
    va = [fbm(a, x, y) for x, y in pts]
    assert va == [fbm(b, x, y) for x, y in pts]
    assert va != [fbm(c, x, y) for x, y in pts]


def test_amplitude_bound_and_turbulence_sign():
    noise = GradientNoise2D(seed=3)
    rng = random.Random(3)
    bound = 2 * amplitude_sum(8, 0.5)
    for _ in range(1000):
        x, y = rng.uniform(-20, 20), rng.uniform(-20, 20)
        assert abs(fbm(noise, x, y, 8)) <= bound
        t = turbulence(noise, x, y, 8)
        assert 0 <= t <= bound
        assert t >= abs(fbm(noise, x, y, 8)) - 1e-12


def test_zero_at_integers_without_offsets():
    noise = GradientNoise2D(seed=6)
    offs = octave_offsets(6, seed=6)
    nonzero = 0
    for i in range(-10, 10):
        for j in range(-10, 10):
            # With lacunarity 2, every octave samples its own lattice points.
            assert fbm(noise, i, j, 6, 2.0, 0.5) == 0.0
            if fbm(noise, i, j, 6, 2.0, 0.5, offs) != 0.0:
                nonzero += 1
    assert nonzero == 400


def test_musgrave_gain_and_octave_limit():
    assert musgrave_gain(0.5) == 2 ** -0.5
    assert musgrave_gain(1.0) == 0.5
    # A pixel covers 1/256 of a unit: periods 1, 1/2, ..., 1/128 are >= 2 pixels.
    assert octave_limit(1 / 256) == 8
    assert octave_limit(1 / 256, base_frequency=4.0) == 6
    assert octave_limit(1.0) == 0
    for fp in (0.001, 0.003, 0.02, 0.1):
        k = octave_limit(fp)
        assert 2.0 ** (k - 1) <= 1 / (2 * fp) < 2.0 ** k
