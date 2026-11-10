# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gustafsons-law/. The authors are listed in prov/0Z9QC0.jsonl.

import random
from fractions import Fraction as F

from gustafsons_law import (amdahl_speedup, from_amdahl_parallel_fraction, scaled_efficiency,
                            scaled_speedup, to_amdahl_parallel_fraction)


def fractions(rng, k):
    yield F(0)
    yield F(1)
    for _ in range(k):
        d = rng.randint(1, 1000)
        yield F(rng.randint(0, d), d)


PS = (1, 2, 3, 8, 64, 1024)


def test_formula():
    assert scaled_speedup(F(5, 100), 1024) == F(97285, 100)  # 972.85
    assert scaled_speedup(F(5, 100), 8) == F(153, 20)  # 7.65
    for p in PS:
        assert scaled_speedup(0, p) == p
        assert scaled_speedup(1, p) == 1
    rng = random.Random(1)
    for s in fractions(rng, 200):
        assert scaled_speedup(s, 1) == 1
        for p in PS:
            assert scaled_speedup(s, p) == p - (p - 1) * s
            assert scaled_efficiency(s, p) == (1 - s) + s / p


def test_conversion_gives_the_same_speedup():
    rng = random.Random(2)
    for s in fractions(rng, 300):
        for p in PS:
            f = to_amdahl_parallel_fraction(s, p)
            assert 0 <= f <= 1
            assert amdahl_speedup(f, p) == scaled_speedup(s, p)
            assert from_amdahl_parallel_fraction(f, p) == s


def test_inverse_conversion():
    rng = random.Random(3)
    for f in fractions(rng, 300):
        for p in PS:
            s = from_amdahl_parallel_fraction(f, p)
            assert to_amdahl_parallel_fraction(s, p) == f
            assert scaled_speedup(s, p) == amdahl_speedup(f, p)


def test_fractions_differ_when_p_grows():
    # a fixed serial fraction of the parallel run is a vanishing serial fraction of the serial run
    s = F(5, 100)
    serial_parts = [1 - to_amdahl_parallel_fraction(s, p) for p in PS[1:]]
    assert all(x > y for x, y in zip(serial_parts, serial_parts[1:]))
    assert serial_parts[-1] < F(1, 10000)
