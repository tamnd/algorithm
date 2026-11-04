# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-filter/. The authors are listed in prov/6QE9XB.jsonl.

import random

import pytest

from xor_filter import Key, XorFilter

TABLE: dict[Key, tuple[tuple[int, int, int], int]] = {
    "a": ((0, 3, 6), 5),
    "b": ((0, 4, 7), 9),
    "c": ((1, 4, 6), 3),
    "d": ((2, 5, 8), 12),
    "x": ((1, 3, 7), 15),
    "y": ((2, 4, 8), 7),
}


class FixedXor(XorFilter):
    def _hash(self, key: Key) -> tuple[tuple[int, int, int], int]:
        return TABLE[key]


def test_example() -> None:
    f = FixedXor("abcd", r=4, seg=3)
    assert f._peel(list("abcd")) == [("c", 1), ("d", 2), ("a", 3), ("b", 7)]
    assert f.B == [0, 3, 12, 5, 0, 0, 0, 9, 0]
    assert all(f.query(k) for k in "abcd")
    assert f.query("x")  # 3 ^ 5 ^ 9 = 15, a false positive
    assert not f.query("y")


def test_edges() -> None:
    f = XorFilter([])
    assert f.seg == 11 and f.bits() == 33 * 8
    assert all(f.query(x) == (f._hash(x)[1] == 0) for x in range(100))
    g = XorFilter([7, 7, 7], r=16)
    assert g.n == 1 and g.query(7)
    with pytest.raises(ValueError):
        XorFilter([1], r=0)


def test_random_against_set() -> None:
    rng = random.Random(2020)
    for _ in range(500):
        n = rng.randint(0, 120)
        r = rng.randint(1, 12)
        keys = rng.sample(range(10**6), n)
        f = XorFilter(keys, r=r, seed=rng.randrange(1000))
        assert f.seg == -(-(123 * n // 100 + 32) // 3)
        assert all(f.query(x) for x in keys)
        for x in keys:
            (a, b, c), fp = f._hash(x)
            assert f.B[a] ^ f.B[b] ^ f.B[c] == fp and 0 <= f.B[a] < 1 << r


def test_rate() -> None:
    keys = [f"k{i}" for i in range(5000)]
    f = XorFilter(keys, r=8, seed=1)
    assert f.bits() / len(keys) < 1.25 * 8
    fp = sum(f.query(f"z{i}") for i in range(40000))
    assert abs(fp / 40000 - 2**-8) < 0.0015
