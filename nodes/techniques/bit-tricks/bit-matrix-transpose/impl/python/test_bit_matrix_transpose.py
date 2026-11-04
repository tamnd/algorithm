# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-matrix-transpose/. The authors are listed in prov/SYYJVH.jsonl.

import itertools
import random

import pytest

from bit_matrix_transpose import transpose, transpose8x8


def naive(a: list[int]) -> list[int]:
    """Oracle: copy the bits one at a time."""
    n = len(a)
    return [sum(((a[r] >> c) & 1) << r for r in range(n)) for c in range(n)]


def naive8x8(x: int) -> int:
    return sum(((x >> (8 * r + c)) & 1) << (8 * c + r) for r in range(8) for c in range(8))


def test_example() -> None:
    assert transpose([0b0011, 0b0101, 0b1001, 0b0000]) == [7, 1, 2, 4]


@pytest.mark.parametrize("n", [1, 2, 4])
def test_exhaustive_small(n: int) -> None:
    for rows in itertools.product(range(1 << n), repeat=n):
        assert transpose(list(rows)) == naive(list(rows))


@pytest.mark.parametrize("n", [8, 16, 32, 64])
def test_random_against_oracle(n: int) -> None:
    rng = random.Random(1000 + n)
    for _ in range(60):
        a = [rng.getrandbits(n) for _ in range(n)]
        b = transpose(list(a))
        assert b == naive(a)
        assert transpose(list(b)) == a


def test_identity_is_fixed() -> None:
    for n in [1, 2, 4, 8, 16, 32]:
        eye = [1 << i for i in range(n)]
        assert transpose(list(eye)) == eye


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        transpose([1, 2, 3])
    with pytest.raises(ValueError):
        transpose([4, 0])


def test_one_word() -> None:
    assert transpose8x8(0xFF) == 0x0101010101010101
    assert transpose8x8(0x8040201008040201) == 0x8040201008040201
    rng = random.Random(8)
    for _ in range(4000):
        x = rng.getrandbits(64)
        assert transpose8x8(x) == naive8x8(x)
        assert transpose8x8(transpose8x8(x)) == x
