# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-inverse-square-root/. The authors are listed in prov/10WFYW.jsonl.

import math
import random
from fractions import Fraction

import pytest

from fast_inverse_square_root import (
    LARGEST,
    SMALLEST,
    bits32,
    f32,
    fast_inverse_square_root,
    float32,
    initial_guess,
    relative_error,
)

LOW, HIGH = -0.0017525, 2e-7  # the proved bound of proofs/correctness.md
LOW0, HIGH0 = -0.0343758, 0.0339603  # the proved bound on the initial guess


def test_example_table() -> None:
    rows = [
        (0.15625, 0x3E200000, 0x402759DF, 2.6148602962493896, 2.5254862308502197),
        (1.0, 0x3F800000, 0x3F7759DF, 0.9662150740623474, 0.9983071684837341),
        (2.0, 0x40000000, 0x3F3759DF, 0.7162150740623474, 0.7069300413131714),
        (3.7297205924987793, 0x406EB3BE, 0x3F000000, 0.5, 0.5168924331665039),
        (4.0, 0x40800000, 0x3EF759DF, 0.4831075370311737, 0.49915358424186707),
        (100.0, 0x42C80000, 0x3DD359DF, 0.10319875925779343, 0.09984488040208817),
    ]
    for x, bx, g, y0, y1 in rows:
        assert bits32(x) == bx
        assert 0x5F3759DF - (bx >> 1) == g
        assert initial_guess(x) == y0 == float32(g)
        assert fast_inverse_square_root(x) == y1


def test_worst_case_input() -> None:
    x = 2.0 * (1 + Fraction(7254974, 2**23))
    xf = float(x)
    assert f32(xf) == xf
    assert initial_guess(xf) == 0.5
    e0 = relative_error(xf, 0.5)
    assert abs(e0 - (-0.0343758)) < 1e-7
    e1 = relative_error(xf, fast_inverse_square_root(xf))
    assert LOW <= e1 <= -0.0017522


def test_scaling_by_four() -> None:
    rng = random.Random(7)
    for _ in range(300):
        x = f32(rng.uniform(1.0, 4.0))
        g = initial_guess(x)
        for k in range(-60, 60):
            xs = x * 4.0**k
            assert initial_guess(xs) == g * 2.0**-k


def test_domain_edges() -> None:
    for x in (SMALLEST, LARGEST, 2.0**-124, 2.0**127, 1.0, f32(math.pi)):
        e0 = relative_error(x, initial_guess(x))
        e1 = relative_error(x, fast_inverse_square_root(x))
        assert LOW0 <= e0 <= HIGH0
        assert LOW <= e1 <= HIGH
    for bad in (0.0, -0.0, -1.0, math.inf, -math.inf, math.nan, 2.0**-126, 1e-40, 2.0**-149):
        with pytest.raises(ValueError):
            fast_inverse_square_root(bad)


def test_random_against_oracle() -> None:
    rng = random.Random(20240501)
    worst = 0.0
    for _ in range(20000):
        x = f32(2.0 ** rng.uniform(-124.9, 127.9))
        if not (SMALLEST <= x <= LARGEST):
            continue
        y = fast_inverse_square_root(x)
        e1 = relative_error(x, y)
        assert LOW <= e1 <= HIGH
        e0 = relative_error(x, initial_guess(x))
        assert LOW0 <= e0 <= HIGH0
        oracle = 1.0 / math.sqrt(x)
        assert abs(y - oracle) <= 0.0017525 * oracle
        worst = min(worst, e1)
    assert worst < -0.0015  # the bound is nearly reached on random inputs


def test_dense_slice_near_the_worst_case() -> None:
    start = bits32(3.7297205924987793) - 3000
    for i in range(start, start + 6000):
        x = float32(i)
        assert LOW0 <= relative_error(x, initial_guess(x)) <= HIGH0
        assert LOW <= relative_error(x, fast_inverse_square_root(x)) <= HIGH


def test_two_steps_and_other_constants() -> None:
    rng = random.Random(99)
    for _ in range(2000):
        x = f32(rng.uniform(1.0, 4.0))
        assert abs(relative_error(x, fast_inverse_square_root(x, newton_steps=2))) < 5e-6
        assert abs(relative_error(x, fast_inverse_square_root(x, 0x5F375A86))) < 0.0017513
        assert abs(relative_error(x, initial_guess(x, 0x5F37642F))) < 0.034213
