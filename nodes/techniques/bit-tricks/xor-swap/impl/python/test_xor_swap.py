# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-swap/. The authors are listed in prov/G8X0J3.jsonl.

import random

from xor_swap import xor_swap, xor_swap_unguarded


def test_example() -> None:
    a = [180, 105]
    xor_swap(a, 0, 1)
    assert a == [105, 180]


def test_all_8_bit_pairs() -> None:
    for x in range(256):
        for y in range(256):
            a = [x, y, 7]
            xor_swap(a, 0, 1)
            assert a == [y, x, 7]


def test_same_cell() -> None:
    for x in range(256):
        a = [x]
        xor_swap(a, 0, 0)
        assert a == [x]
        b = [x]
        xor_swap_unguarded(b, 0, 0)
        assert b == [0]


def test_negative_and_wide() -> None:
    a = [-5, 2**64 - 1]
    xor_swap(a, 0, 1)
    assert a == [2**64 - 1, -5]


def test_random_against_tuple_swap() -> None:
    rng = random.Random(20)
    for _ in range(2000):
        n = rng.randrange(1, 8)
        a = [rng.randrange(-(2**63), 2**64) for _ in range(n)]
        i, j = rng.randrange(n), rng.randrange(n)
        want = list(a)
        want[i], want[j] = want[j], want[i]
        xor_swap(a, i, j)
        assert a == want
