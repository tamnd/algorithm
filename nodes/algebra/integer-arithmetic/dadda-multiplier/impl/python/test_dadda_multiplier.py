# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dadda-multiplier/. The authors are listed in prov/Q7R1ED.jsonl.

import random

import pytest

from dadda_multiplier import dadda_heights, dadda_multiply, from_bits, stage_count, to_bits


def mul(x: int, y: int, n: int):
    bits, counts, depth = dadda_multiply(to_bits(x, n), to_bits(y, n))
    assert len(bits) == 2 * n
    return from_bits(bits), counts, depth


def test_example_4_bits():
    p, c, depth = mul(13, 11, 4)
    assert p == 143
    assert (c.full_adders, c.half_adders, c.stages) == (3, 3, 2)
    assert c.final_adder_width == 6
    assert c.reduction_depth == 3
    assert depth == 7


def test_heights_sequence():
    assert dadda_heights(64) == [2, 3, 4, 6, 9, 13, 19, 28, 42, 63]
    assert dadda_heights(2) == []
    assert dadda_heights(3) == [2]


def test_exhaustive_small():
    for n in range(1, 6):
        for x in range(1 << n):
            for y in range(1 << n):
                assert mul(x, y, n)[0] == x * y


def test_random():
    rng = random.Random(20250605)
    for _ in range(600):
        n = rng.randint(1, 24)
        x, y = rng.getrandbits(n), rng.getrandbits(n)
        assert mul(x, y, n)[0] == x * y


def test_counts_and_depth():
    # Proved: stages = number of Dadda heights below n, reduction depth = stages + 1.
    # FA = n^2 - 4n + 3 follows from the final shape; that shape and HA = n - 1 are observed.
    for n in list(range(3, 41)) + [48, 64]:
        top = (1 << n) - 1
        p, c, depth = mul(top, top, n)
        assert p == top * top
        assert c.and_gates == n * n
        assert c.full_adders == n * n - 4 * n + 3
        assert c.half_adders == n - 1
        assert c.stages == stage_count(n)
        assert c.reduction_depth == c.stages + 1
        assert c.final_adder_width == 2 * n - 2
        assert depth == 2 * n - 1  # ripple-carry final adder


def test_edges():
    for n in (1, 2, 7, 16, 33):
        top = (1 << n) - 1
        for x, y in ((0, 0), (0, top), (top, 1), (top, top), (1 << (n - 1), 1 << (n - 1))):
            assert mul(x, y, n)[0] == x * y
    with pytest.raises(ValueError):
        dadda_multiply([], [])
    with pytest.raises(ValueError):
        dadda_multiply([1, 0], [1])
