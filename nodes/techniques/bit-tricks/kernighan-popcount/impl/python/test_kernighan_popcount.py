# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernighan-popcount/. The authors are listed in prov/TVK2SZ.jsonl.

import random

import pytest

from kernighan_popcount import kernighan_popcount


def test_example() -> None:
    assert kernighan_popcount(180) == 4


def test_edges() -> None:
    assert kernighan_popcount(0) == 0
    assert kernighan_popcount(1) == 1
    assert kernighan_popcount(2**64 - 1) == 64
    assert kernighan_popcount(2**63) == 1
    assert kernighan_popcount((-1) & 0xFFFFFFFF) == 32


def test_negative_rejected() -> None:
    with pytest.raises(ValueError):
        kernighan_popcount(-1)


def test_all_16_bit_words() -> None:
    for x in range(1 << 16):
        assert kernighan_popcount(x) == bin(x).count("1")


def test_random_64_bit() -> None:
    rng = random.Random(136)
    for _ in range(5000):
        x = rng.getrandbits(64)
        assert kernighan_popcount(x) == bin(x).count("1")
