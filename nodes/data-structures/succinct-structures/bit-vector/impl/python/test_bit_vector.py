# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-vector/. The authors are listed in prov/6G48XR.jsonl.

import random

import pytest

from bit_vector import BitVector


def oracle(b: list[int]) -> tuple[list[int], list[int], list[int]]:
    rank = [0]
    for x in b:
        rank.append(rank[-1] + x)
    return rank, [i for i, x in enumerate(b) if x], [i for i, x in enumerate(b) if not x]


def check_all(b: list[int]) -> None:
    v = BitVector(b)
    v.check_invariant()
    rank, ones, zeros = oracle(b)
    assert len(v) == len(b)
    for i in range(len(b)):
        assert v.access(i) == b[i]
    for i in range(len(b) + 1):
        assert v.rank1(i) == rank[i]
        assert v.rank0(i) == i - rank[i]
    for j, p in enumerate(ones, 1):
        assert v.select1(j) == p
    for j, p in enumerate(zeros, 1):
        assert v.select0(j) == p


def test_page_example() -> None:
    b = [int(c) for c in "1011001011000111"]
    v = BitVector(b)
    assert v.access(9) == 1
    assert v.rank1(13) == 6
    assert v.rank0(13) == 7
    assert v.select1(7) == 13
    assert v.select0(4) == 7
    assert v.rank1(v.select1(7)) == 6
    with pytest.raises(IndexError):
        v.select1(10)
    check_all(b)


def test_edges() -> None:
    check_all([])
    check_all([0])
    check_all([1])
    check_all([1] * 64)
    check_all([0] * 64)
    check_all([1] * 128 + [0])
    check_all([0] * 130)
    check_all([0] * 63 + [1])
    v = BitVector([1] * 64)
    assert v.rank1(64) == 64
    with pytest.raises(IndexError):
        v.select0(1)


def test_random_against_oracle() -> None:
    rng = random.Random(6048)
    for _ in range(600):
        n = rng.randrange(0, 300)
        p = rng.random()
        check_all([1 if rng.random() < p else 0 for _ in range(n)])
