# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sd-array/. The authors are listed in prov/PZD3RH.jsonl.

import random

import pytest

from sd_array import SDArray


def check_all(bits: list[int]) -> None:
    v = SDArray(bits)
    n = len(bits)
    r = 0
    for i in range(n + 1):
        assert v.rank1(i) == r
        assert v.rank0(i) == i - r
        if i < n:
            assert v.access(i) == bits[i]
            r += bits[i]
    ones = [i for i, x in enumerate(bits) if x]
    zeros = [i for i, x in enumerate(bits) if not x]
    for j, p in enumerate(ones, 1):
        assert v.select1(j) == p
    for j, p in enumerate(zeros, 1):
        assert v.select0(j) == p


def example() -> list[int]:
    bits = [0] * 64
    for p in (3, 4, 7, 13, 14, 15, 21, 43):
        bits[p] = 1
    return bits


def test_page_example() -> None:
    v = SDArray(example())
    assert v.ell == 3
    assert v.lo == [3, 4, 7, 5, 6, 7, 5, 3]
    assert v.size_in_bits() == 40
    assert v.select1(7) == 21
    assert v.rank1(14) == 4
    assert v.rank1(40) == 7
    assert v.access(21) == 1 and v.access(22) == 0
    assert v.select0(10) == 12
    check_all(example())


def test_edges() -> None:
    check_all([])
    check_all([0])
    check_all([1])
    check_all([0] * 100)
    check_all([1] * 100)
    check_all([0] * 99 + [1])
    check_all([1] + [0] * 999)
    with pytest.raises(IndexError):
        SDArray([0, 0]).select1(1)


def test_random_against_lists() -> None:
    rng = random.Random(2007)
    for _ in range(500):
        n = rng.randrange(0, 160)
        p = rng.choice([0.005, 0.02, 0.1, 0.5, 0.9])
        check_all([1 if rng.random() < p else 0 for _ in range(n)])
