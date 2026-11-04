# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swar-popcount/. The authors are listed in prov/W1VS75.jsonl.

import random

import pytest

from swar_popcount import swar_popcount


def test_example() -> None:
    assert swar_popcount(0xB4E7, 16) == 10


def test_edges() -> None:
    for w in (8, 16, 32, 64, 128):
        assert swar_popcount(0, w) == 0
        assert swar_popcount((1 << w) - 1, w) == w
        assert swar_popcount(1 << (w - 1), w) == 1


def test_all_8_and_16_bit_words() -> None:
    for x in range(1 << 8):
        assert swar_popcount(x, 8) == bin(x).count("1")
    for x in range(1 << 16):
        assert swar_popcount(x, 16) == bin(x).count("1")


def test_random_wide() -> None:
    rng = random.Random(51)
    for w in (32, 64, 128):
        for _ in range(3000):
            x = rng.getrandbits(w)
            assert swar_popcount(x, w) == bin(x).count("1")


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        swar_popcount(256, 8)
    with pytest.raises(ValueError):
        swar_popcount(1, 256)
