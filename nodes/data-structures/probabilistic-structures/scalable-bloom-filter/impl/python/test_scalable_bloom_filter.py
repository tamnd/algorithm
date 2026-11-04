# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scalable-bloom-filter/. The authors are listed in prov/Q55J7F.jsonl.

import math
import random

import pytest

from scalable_bloom_filter import Key, ScalableBloomFilter

TABLE: dict[Key, dict[int, list[int]]] = {
    "a": {0: [1, 2]},
    "b": {0: [1, 3]},
    "c": {0: [2, 0], 1: [0, 5, 2]},
    "d": {0: [3, 1], 1: [3, 5, 7]},
    "e": {0: [0, 0], 1: [6, 1, 2]},
    "x": {0: [1, 0], 1: [3, 5, 2]},
    "y": {0: [0, 2], 1: [0, 1, 1]},
}


class FixedSBF(ScalableBloomFilter):
    def __init__(self) -> None:
        super().__init__(b0=4, eps0=0.25, r=0.5, s=2)

    def _positions(self, key: Key, i: int) -> list[int]:
        return TABLE[key][i]


def test_example() -> None:
    f = FixedSBF()
    f.insert("a")
    f.insert("b")
    assert len(f.slices) == 1 and f.slices[0].k == 2 and f.slices[0].capacity == 2
    assert [list(p) for p in f.slices[0].bits] == [[0, 1, 0, 0], [0, 0, 1, 1]]
    for key in "cde":
        f.insert(key)
    assert len(f.slices) == 2
    s1 = f.slices[1]
    assert (s1.k, s1.b, s1.capacity, s1.count) == (3, 8, 4, 3)
    assert [[j for j in range(8) if p[j]] for p in s1.bits] == [[0, 3, 6], [1, 5], [2, 7]]
    assert all(f.query(key) for key in "abcde")
    assert f.query("x")  # a false positive in slice 1
    assert not f.query("y")
    assert f.rate_bound() == 0.375


def test_edges() -> None:
    f = ScalableBloomFilter(b0=2, eps0=0.5, r=0.5)
    assert not f.query(1) and f.slices == []
    f.insert(1)
    assert f.query(1) and len(f.slices) == 1 and f.slices[0].capacity == 1
    for bad in [dict(b0=1), dict(eps0=1.0), dict(r=1.0), dict(s=0)]:
        with pytest.raises(ValueError):
            ScalableBloomFilter(**bad)


def test_random_against_set() -> None:
    rng = random.Random(2007)
    for _ in range(500):
        b0 = rng.randint(2, 20)
        eps0 = rng.choice([0.5, 0.2, 0.1, 0.01])
        r = rng.choice([0.5, 0.8, 0.9])
        s = rng.randint(1, 3)
        f = ScalableBloomFilter(b0, eps0, r, s, seed=rng.randrange(1000))
        stored: list[int] = []
        for _ in range(rng.randint(0, 80)):
            x = rng.randrange(200)
            f.insert(x)
            stored.append(x)
        assert all(f.query(x) for x in stored)
        for i, sl in enumerate(f.slices):
            assert sl.b == b0 * s**i
            assert sl.k == max(1, math.ceil(math.log2(1 / (eps0 * r**i)) - 1e-9))
            assert 1 <= sl.count <= sl.capacity
        assert all(sl.count == sl.capacity for sl in f.slices[:-1])


def test_rate_stays_bounded() -> None:
    f = ScalableBloomFilter(b0=32, eps0=0.02, r=0.5, seed=3)
    for x in range(3000):
        f.insert(x)
    assert len(f.slices) >= 5
    fp = sum(f.query(x) for x in range(10**6, 10**6 + 20000))
    assert fp / 20000 < 0.04  # the bound is 0.02 / (1 - 0.5)
