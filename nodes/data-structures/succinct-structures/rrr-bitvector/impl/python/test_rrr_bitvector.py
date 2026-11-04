# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rrr-bitvector/. The authors are listed in prov/5SBQH9.jsonl.

import math
import random

import pytest

from rrr_bitvector import RRRBitVector

EXAMPLE = [int(c) for c in "1011001011000111"]


def check_all(bits: list[int], b: int, k: int) -> None:
    v = RRRBitVector(bits, b, k)
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
    m = len(ones)
    bound = math.log2(math.comb(n, m)) if n else 0
    assert v.offset_bits() <= bound + (n + b - 1) // b + 1


def test_page_example() -> None:
    v = RRRBitVector(EXAMPLE, b=4, k=2)
    assert v.K == [3, 1, 2, 3]
    assert v.L == [0, 2, 3, 2, 0]
    assert [v.encode(v._block(t))[1] for t in range(4)] == [2, 2, 0, 3]
    assert v.R == [0, 4, 9] and v.P == [0, 4, 9]
    assert v.RB[:4] == [0, 3, 0, 2] and v.PB[:4] == [0, 2, 0, 3]
    assert v.decode(3, 3) == 0b1110
    assert v.decode(2, 0) == 0b0011
    assert v.rank1(13) == 6
    assert v.rank1(10) == 6
    assert v.select1(5) == 8
    assert v.offset_bits() == 9
    check_all(EXAMPLE, 4, 2)


def test_encode_decode_bijection() -> None:
    v = RRRBitVector([], b=8, k=1)
    seen: dict[int, set[int]] = {}
    for x in range(256):
        c, o = v.encode(x)
        assert c == x.bit_count()
        assert 0 <= o < math.comb(8, c)
        assert o not in seen.setdefault(c, set())
        seen[c].add(o)
        assert v.decode(c, o) == x


def test_edges() -> None:
    check_all([], 4, 2)
    check_all([0], 1, 1)
    check_all([1], 1, 1)
    check_all([0] * 70, 15, 3)
    check_all([1] * 70, 15, 3)
    check_all([1] * 64 + [0] * 64, 63, 2)
    v = RRRBitVector([1, 0], 3, 1)
    with pytest.raises(IndexError):
        v.select1(2)
    with pytest.raises(IndexError):
        v.rank1(3)


def test_random_against_lists() -> None:
    rng = random.Random(2007)
    for _ in range(500):
        n = rng.randrange(0, 300)
        p = rng.choice([0.02, 0.1, 0.5, 0.9, 0.98])
        bits = [1 if rng.random() < p else 0 for _ in range(n)]
        check_all(bits, rng.randrange(1, 64), rng.randrange(1, 6))
