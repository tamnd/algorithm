# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-fuse-filter/. The authors are listed in prov/WV9S0Z.jsonl.

import random

import pytest

from binary_fuse_filter import BinaryFuseFilter, Key, fuse_size

TABLE: dict[Key, tuple[tuple[int, int, int], int]] = {
    "a": ((0, 2, 4), 6),
    "b": ((1, 2, 5), 10),
    "c": ((2, 4, 6), 1),
    "d": ((3, 5, 7), 13),
    "x": ((1, 3, 4), 7),
    "y": ((3, 4, 6), 2),
}


class FixedFuse(BinaryFuseFilter):
    def _hash(self, key: Key) -> tuple[tuple[int, int, int], int]:
        return TABLE[key]


def test_example() -> None:
    f = FixedFuse("abcd", r=4, seg_len=2, seg_count=2)
    assert f._peel(list("abcd")) == [("a", 0), ("b", 1), ("d", 3), ("c", 6)]
    assert f.B == [6, 10, 0, 13, 0, 0, 1, 0]
    assert all(f.query(k) for k in "abcd")
    assert f.query("x")  # 10 ^ 13 ^ 0 = 7, a false positive
    assert not f.query("y")


def test_sizes() -> None:
    assert fuse_size(1000) == (128, 9)
    assert fuse_size(10**6) == (8192, 136)
    L, c = fuse_size(10**7)
    assert (c + 2) * L / 10**7 < 1.13


def test_edges() -> None:
    f = BinaryFuseFilter([])
    assert (f.L, f.count) == (4, 1) and f.bits() == 12 * 8
    g = BinaryFuseFilter(["k", "k"], r=16)
    assert g.n == 1 and g.query("k")
    with pytest.raises(ValueError):
        BinaryFuseFilter([1], r=0)


def test_random_against_set() -> None:
    rng = random.Random(2022)
    for _ in range(500):
        n = rng.randint(0, 150)
        r = rng.randint(1, 12)
        keys = rng.sample(range(10**6), n)
        f = BinaryFuseFilter(keys, r=r, seed=rng.randrange(1000))
        assert all(f.query(x) for x in keys)
        for x in keys:
            (a, b, c), fp = f._hash(x)
            assert a // f.L + 1 == b // f.L and b // f.L + 1 == c // f.L < f.count + 2
            assert f.B[a] ^ f.B[b] ^ f.B[c] == fp


def test_rate() -> None:
    keys = [f"k{i}" for i in range(20000)]
    f = BinaryFuseFilter(keys, r=8, seed=5)
    assert f.bits() / len(keys) < 1.3 * 8
    fp = sum(f.query(f"z{i}") for i in range(40000))
    assert abs(fp / 40000 - 2**-8) < 0.0015
