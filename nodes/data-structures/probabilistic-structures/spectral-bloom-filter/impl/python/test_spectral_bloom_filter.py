# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-bloom-filter/. The authors are listed in prov/MMBG5S.jsonl.

import random
from collections import Counter

import pytest

from spectral_bloom_filter import Key, SpectralBloomFilter

TABLE: dict[Key, list[int]] = {
    "a": [0, 3, 7],
    "b": [3, 5, 9],
    "c": [1, 5, 7],
    "d": [0, 1, 9],
    "e": [3, 5, 7],
}
STREAM = "aabcace"


class FixedSBF(SpectralBloomFilter):
    def __init__(self, mi: bool) -> None:
        super().__init__(10, 3, minimal_increase=mi)

    def _positions(self, key: Key) -> list[int]:
        return TABLE[key]


def test_example_minimum_selection() -> None:
    f = FixedSBF(False)
    for x in STREAM:
        f.insert(x)
    assert f.counters == [3, 2, 0, 5, 0, 4, 0, 6, 0, 1]
    assert [f.estimate(x) for x in "abcde"] == [3, 1, 2, 1, 4]
    f.delete("e")
    assert [f.estimate(x) for x in "abcde"] == [3, 1, 2, 1, 3]


def test_example_minimal_increase() -> None:
    f = FixedSBF(True)
    for x in STREAM:
        f.insert(x)
    assert f.counters == [3, 2, 0, 3, 0, 3, 0, 3, 0, 1]
    assert [f.estimate(x) for x in "abcde"] == [3, 1, 2, 1, 3]
    assert f.query("a", 3) and not f.query("b", 2)
    with pytest.raises(ValueError):
        f.delete("e")


def test_edges() -> None:
    f = SpectralBloomFilter(1, 4)
    assert f.estimate("z") == 0 and not f.query("z")
    f.insert("z", 5)
    assert f.counters == [5]  # one distinct position, counted once
    f.insert("y", 0)
    assert f.estimate("y") == 5
    with pytest.raises(ValueError):
        SpectralBloomFilter(0, 1)
    with pytest.raises(ValueError):
        f.insert("z", -1)


def test_random_against_counter() -> None:
    rng = random.Random(2003)
    for _ in range(500):
        m = rng.randint(1, 40)
        k = rng.randint(1, 5)
        seed = rng.randrange(1000)
        ms = SpectralBloomFilter(m, k, False, seed)
        mi = SpectralBloomFilter(m, k, True, seed)
        ms_only = SpectralBloomFilter(m, k, False, seed)
        f: Counter[int] = Counter()
        g: Counter[int] = Counter()
        for _ in range(rng.randint(0, 60)):
            x = rng.randrange(25)
            w = rng.randint(0, 3)
            ms.insert(x, w)
            mi.insert(x, w)
            f[x] += w
            # a second filter with deletes, checked against its own multiset
            if rng.random() < 0.3 and g[x] > 0:
                d = rng.randint(1, g[x])
                ms_only.delete(x, d)
                g[x] -= d
            else:
                ms_only.insert(x, w)
                g[x] += w
        assert all(a <= b for a, b in zip(mi.counters, ms.counters))
        h = {x: set(ms._set(x)) for x in range(30)}

        def exact(mult: Counter[int], x: int) -> int:
            # minimum selection is f_x plus the least collision mass on a position of x
            return mult[x] + min(
                sum(c for y, c in mult.items() if y != x and p in h[y]) for p in h[x]
            )

        for x in range(30):
            assert ms.estimate(x) == exact(f, x)
            assert f[x] <= mi.estimate(x) <= ms.estimate(x)
            assert ms_only.estimate(x) == exact(g, x)
