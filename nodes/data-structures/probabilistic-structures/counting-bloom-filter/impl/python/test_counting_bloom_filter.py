# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counting-bloom-filter/. The authors are listed in prov/EHFR24.jsonl.

import random
from collections import Counter

import pytest

from counting_bloom_filter import CountingBloomFilter, Key


class FixedCBF(CountingBloomFilter):
    def __init__(self, table: dict[Key, list[int]], c: int = 4) -> None:
        super().__init__(10, 3, c)
        self.table = table

    def _positions(self, key: Key) -> list[int]:
        return self.table[key]


TABLE: dict[Key, list[int]] = {"a": [0, 3, 7], "b": [3, 5, 9], "c": [1, 5, 7], "d": [0, 1, 9]}


def test_example() -> None:
    f = FixedCBF(TABLE)
    f.insert("a")
    assert f.counters == [1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    f.insert("b")
    assert f.counters == [1, 0, 0, 2, 0, 1, 0, 1, 0, 1]
    f.insert("c")
    assert f.counters == [1, 1, 0, 2, 0, 2, 0, 2, 0, 1]
    assert f.query("d")  # a false positive: 0, 1 and 9 are all nonzero
    f.delete("b")
    assert f.counters == [1, 1, 0, 1, 0, 1, 0, 2, 0, 0]
    assert not f.query("b") and not f.query("d")
    assert f.query("a") and f.query("c")


def test_saturation() -> None:
    f = FixedCBF(TABLE, c=2)  # counters stick at 3
    for _ in range(4):
        f.insert("a")
    assert f.counters[0] == 3 and f.saturated() == 3
    for _ in range(4):
        f.delete("a")
    assert f.counters[0] == 3  # stuck, so no false negative is possible
    assert f.query("a")


def test_edges() -> None:
    f = CountingBloomFilter(1, 1)
    assert not f.query(5)
    f.insert(5)
    f.insert(5)
    f.delete(5)
    assert f.query(5)
    f.delete(5)
    assert not f.query(5) and f.counters == [0]
    with pytest.raises(ValueError):
        CountingBloomFilter(4, 2, c=0)


def test_random_against_multiset() -> None:
    rng = random.Random(2000)
    for _ in range(500):
        m = rng.randint(1, 60)
        k = rng.randint(1, 5)
        c = rng.randint(1, 4)
        f = CountingBloomFilter(m, k, c, seed=rng.randrange(100))
        live: Counter[int] = Counter()
        ever_saturated = False
        for _ in range(rng.randint(0, 60)):
            x = rng.randrange(30)
            r = rng.random()
            if r < 0.45:
                f.insert(x)
                live[x] += 1
            elif r < 0.8 and live[x] > 0:
                f.delete(x)
                live[x] -= 1
            else:
                assert f.query(x) or live[x] == 0
            ever_saturated = ever_saturated or f.saturated() > 0
            assert all(f.query(y) for y in live if live[y] > 0)
            assert all(0 <= v <= f.cmax for v in f.counters)
        if not ever_saturated:
            # with no saturation, each counter is the exact count of positions
            want = [0] * m
            for y, mult in live.items():
                for p in f._positions(y):
                    want[p] += mult
            assert f.counters == want
