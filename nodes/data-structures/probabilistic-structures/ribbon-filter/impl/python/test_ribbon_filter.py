# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ribbon-filter/. The authors are listed in prov/K1BXC2.jsonl.

import random

import pytest

from ribbon_filter import Key, RibbonFilter

TABLE: dict[Key, tuple[int, int, int]] = {
    "a": (0, 0b1011, 5),
    "b": (0, 0b0111, 9),
    "c": (1, 0b0101, 3),
    "d": (2, 0b1001, 12),
    "e": (0, 0b1011, 6),  # the row of a with another fingerprint
    "x": (1, 0b0011, 15),
    "y": (2, 0b0111, 1),
}


class FixedRibbon(RibbonFilter):
    def _hash(self, key: Key) -> tuple[int, int, int]:
        return TABLE[key]


def test_example() -> None:
    f = FixedRibbon("abcd", r=4, w=4, m=6)
    C, B = f._band(list("abcd"))
    assert C == [0b1011, 0b0101, 0b0011, 0b0101, 0, 0]
    assert B == [5, 3, 12, 0, 0, 0]
    assert f.Z == [6, 3, 12, 0, 0, 0]
    assert all(f.query(k) for k in "abcd")
    assert f.query("x")  # 3 ^ 12 = 15, a false positive
    assert not f.query("y")
    assert f._band(list("abcda")) is not None  # a repeated key is a redundant row
    assert f._band(list("abcde")) is None  # an inconsistent row


def test_edges() -> None:
    f = RibbonFilter([])
    assert f.m == 64 and not any(f.Z)
    g = RibbonFilter([3, 3, 3], r=16, w=8)
    assert g.query(3)
    with pytest.raises(ValueError):
        RibbonFilter([1], r=0)


def test_random_against_set() -> None:
    rng = random.Random(2021)
    for _ in range(500):
        n = rng.randint(0, 150)
        r = rng.randint(1, 12)
        w = rng.choice([8, 16, 32, 64])
        keys = rng.sample(range(10**6), n)
        f = RibbonFilter(keys, r=r, w=w, overhead=0.15, seed=rng.randrange(1000))
        assert f.m >= w and all(0 <= z < 1 << r for z in f.Z)
        assert all(f.query(x) for x in keys)
        for x in keys:
            s, c, fp = f._hash(x)
            assert c & 1 and s + c.bit_length() <= f.m
            acc = 0
            for j in range(w):
                if c >> j & 1:
                    acc ^= f.Z[s + j]
            assert acc == fp


def test_rate() -> None:
    keys = [f"k{i}" for i in range(4000)]
    f = RibbonFilter(keys, r=8, seed=3)
    assert f.bits() / len(keys) < 1.07 * 8
    fp = sum(f.query(f"z{i}") for i in range(30000))
    assert abs(fp / 30000 - 2**-8) < 0.0015
