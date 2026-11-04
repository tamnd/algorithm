# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-bruijn-bit-scan/. The authors are listed in prov/3BENJ1.jsonl.

import random

import pytest

from de_bruijn_bit_scan import build_table, de_bruijn_bit_scan


def oracle(x: int) -> int:
    return (x & -x).bit_length() - 1


def test_page_examples() -> None:
    assert de_bruijn_bit_scan(104, 8) == 3
    assert de_bruijn_bit_scan(180, 8) == 2
    assert de_bruijn_bit_scan(0x00F00000, 32) == 20


def test_tables_on_page() -> None:
    assert build_table(0x1D, 8, 3) == (0, 1, 6, 2, 7, 5, 4, 3)
    assert build_table(0x077CB531, 32, 5)[:8] == (0, 1, 28, 2, 29, 14, 24, 3)


def test_all_8_and_16_bit_words() -> None:
    for x in range(1, 1 << 8):
        assert de_bruijn_bit_scan(x, 8) == oracle(x)
    for x in range(1, 1 << 16):
        assert de_bruijn_bit_scan(x, 16) == oracle(x)


def test_every_single_bit() -> None:
    for w in (8, 16, 32, 64):
        for k in range(w):
            assert de_bruijn_bit_scan(1 << k, w) == k
            assert de_bruijn_bit_scan((1 << w) - (1 << k), w) == k


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        de_bruijn_bit_scan(0, 32)
    with pytest.raises(ValueError):
        de_bruijn_bit_scan(1 << 32, 32)
    with pytest.raises(ValueError):
        de_bruijn_bit_scan(5, 12)
    with pytest.raises(ValueError):
        build_table(0x1F, 8, 3)


def test_random_64_bit() -> None:
    rng = random.Random(1998)
    for _ in range(5000):
        x = rng.randrange(1, 1 << 64) >> rng.randrange(64)
        x = max(x, 1)
        assert de_bruijn_bit_scan(x, 64) == oracle(x)
        y = x & 0xFFFFFFFF
        if y:
            assert de_bruijn_bit_scan(y, 32) == oracle(y)
