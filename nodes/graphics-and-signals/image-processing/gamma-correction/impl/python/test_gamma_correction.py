# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gamma-correction/. The authors are listed in prov/FDBZJX.jsonl.

import math
import random
from fractions import Fraction

from gamma_correction import (
    DECODE_BREAK,
    ENCODE_BREAK,
    decode_table,
    encode_to_code,
    mean_in_linear_light,
    power_decode,
    power_encode,
    srgb_decode,
    srgb_encode,
)


def test_linear_segment_is_exact() -> None:
    rng = random.Random(21)
    for _ in range(500):
        v = Fraction(rng.randint(0, 4045), 100000)
        lin = srgb_decode(v)
        assert isinstance(lin, Fraction)
        assert lin == v * 100 / 1292
        assert srgb_encode(lin) == v


def test_breakpoints_nearly_meet() -> None:
    # the two pieces of the standard curve meet only to about 1e-8
    line = float(Fraction(1292, 100) * ENCODE_BREAK)
    power = 1.055 * float(ENCODE_BREAK) ** (1 / 2.4) - 0.055
    assert abs(line - power) < 1e-7
    assert abs(line - float(DECODE_BREAK)) < 1e-6
    lin_line = float(DECODE_BREAK / Fraction(1292, 100))
    lin_power = ((0.04045 + 0.055) / 1.055) ** 2.4
    assert abs(lin_line - lin_power) < 1e-8


def test_published_values() -> None:
    assert srgb_decode(0) == 0 and math.isclose(srgb_decode(1.0), 1.0)
    assert math.isclose(srgb_encode(1.0), 1.0)
    assert round(srgb_decode(Fraction(128, 255)), 7) == 0.2158605
    assert encode_to_code(0.5) == 188
    assert encode_to_code(0.18) == 118


def test_round_trips() -> None:
    # every 8-bit code survives decode then encode
    table = decode_table(8)
    assert all(encode_to_code(table[c]) == c for c in range(256))
    assert sum(1 for t in table if t < 1 / 255) == 13
    rng = random.Random(3)
    for _ in range(1000):
        x = rng.random()
        assert math.isclose(srgb_decode(srgb_encode(x)), x, rel_tol=1e-12, abs_tol=1e-15)
        g = rng.uniform(1.5, 3.0)
        assert math.isclose(power_decode(power_encode(x, g), g), x, rel_tol=1e-12, abs_tol=1e-15)


def test_monotone() -> None:
    table = decode_table(8)
    assert all(table[c] < table[c + 1] for c in range(255))
    rng = random.Random(4)
    xs = sorted(rng.random() for _ in range(500))
    ys = [srgb_encode(x) for x in xs]
    assert all(a <= b for a, b in zip(ys, ys[1:]))


def test_blend_in_linear_light() -> None:
    # black and white averaged in linear light give code 188, not 128
    assert mean_in_linear_light([0, 255]) == 188
    assert mean_in_linear_light([77, 77]) == 77
