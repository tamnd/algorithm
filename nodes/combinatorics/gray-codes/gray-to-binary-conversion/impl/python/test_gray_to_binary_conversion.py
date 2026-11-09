# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gray-to-binary-conversion/. The authors are listed in prov/09XZRF.jsonl.

import random

import pytest

from gray_to_binary_conversion import from_gray, from_gray_bits, from_gray_fast


def reflect(n: int) -> list[int]:
    """Reference: the reflected Gray code built from its definition."""
    lst = [0]
    for i in range(n):
        lst = lst + [x | (1 << i) for x in reversed(lst)]
    return lst


def bits_of(x: int, n: int) -> list[int]:
    return [(x >> j) & 1 for j in range(n)]


def test_example() -> None:
    assert from_gray(0b1011) == 13
    assert from_gray_fast(0b1011, 4) == 13
    assert from_gray_bits([1, 1, 0, 1]) == [1, 0, 1, 1]
    assert from_gray(6) == 4


def test_edges() -> None:
    assert from_gray(0) == 0
    assert from_gray_fast(0) == 0
    assert from_gray_fast(1, 1) == 1
    assert from_gray_bits([]) == []
    with pytest.raises(ValueError):
        from_gray(-1)
    with pytest.raises(ValueError):
        from_gray_fast(8, 3)


def test_rank_matches_position() -> None:
    for n in range(0, 12):
        for b, a in enumerate(reflect(n)):
            assert from_gray(a) == b
            assert from_gray_fast(a, max(1, n)) == b
            assert from_gray_bits(bits_of(a, n)) == bits_of(b, n)


def test_random_inverse() -> None:
    rng = random.Random(11)
    for _ in range(3000):
        n = rng.randrange(1, 300)
        b = rng.getrandbits(n)
        a = b ^ (b >> 1)
        assert from_gray(a) == b
        assert from_gray_fast(a, n) == b
        assert from_gray_fast(a, 1 << n.bit_length()) == b
        assert from_gray_bits(bits_of(a, n)) == bits_of(b, n)
        assert from_gray(a) & 1 == bin(a).count("1") % 2
