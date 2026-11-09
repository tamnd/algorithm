# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-to-gray-conversion/. The authors are listed in prov/JSK194.jsonl.

import random

import pytest

from binary_to_gray_conversion import to_gray, to_gray_bits


def reflect(n: int) -> list[int]:
    """Reference: the reflected Gray code built from its definition."""
    lst = [0]
    for i in range(n):
        lst = lst + [x | (1 << i) for x in reversed(lst)]
    return lst


def bits_of(b: int, n: int) -> list[int]:
    return [(b >> j) & 1 for j in range(n)]


def test_example() -> None:
    assert to_gray(13) == 11
    assert to_gray_bits([1, 0, 1, 1]) == [1, 1, 0, 1]  # 1101 -> 1011, lowest bit first
    assert [to_gray(b) for b in range(8)] == [0, 1, 3, 2, 6, 7, 5, 4]


def test_edges() -> None:
    assert to_gray(0) == 0
    assert to_gray_bits([]) == []
    assert to_gray_bits([1]) == [1]
    with pytest.raises(ValueError):
        to_gray(-1)


def test_against_reflection() -> None:
    for n in range(0, 12):
        ref = reflect(n)
        for b in range(1 << n):
            assert to_gray(b) == ref[b]
            assert to_gray_bits(bits_of(b, n)) == bits_of(ref[b], n)


def test_properties_random() -> None:
    rng = random.Random(3)
    for _ in range(3000):
        n = rng.randrange(1, 200)
        b = rng.getrandbits(n)
        g = to_gray(b)
        assert to_gray_bits(bits_of(b, n)) == bits_of(g, n)
        assert g.bit_length() == b.bit_length()
        assert bin(g).count("1") % 2 == b % 2
        c = rng.getrandbits(n)
        assert to_gray(b ^ c) == g ^ to_gray(c)
        if b > 0:
            assert to_gray(b) ^ to_gray(b - 1) == b & -b
