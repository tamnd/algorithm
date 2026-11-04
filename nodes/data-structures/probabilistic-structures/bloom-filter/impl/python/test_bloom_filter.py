# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloom-filter/. The authors are listed in prov/3RBEYS.jsonl.

import math
import random

import pytest

from bloom_filter import BloomFilter, Key


class FixedBloom(BloomFilter):
    """A filter whose positions come from a table, as in the example of the page."""

    def __init__(self, table: dict[Key, list[int]]) -> None:
        super().__init__(16, 3)
        self.table = table

    def _positions(self, key: Key) -> list[int]:
        return self.table[key]


def test_example() -> None:
    table: dict[Key, list[int]] = {
        "cat": [1, 6, 11],
        "dog": [4, 6, 13],
        "owl": [2, 9, 13],
        "fox": [3, 9, 11],
        "emu": [2, 4, 11],
    }
    f = FixedBloom(table)
    f.insert("cat")
    assert f.ones() == 3
    f.insert("dog")
    assert f.ones() == 5
    f.insert("owl")
    assert f.ones() == 7
    assert [i for i in range(16) if f._get(i)] == [1, 2, 4, 6, 9, 11, 13]
    assert f.query("cat") and f.query("dog") and f.query("owl")
    assert not f.query("fox")
    assert f.query("emu")  # a false positive


def test_edges() -> None:
    f = BloomFilter(1, 1)
    assert not f.query("a")
    f.insert("a")
    assert f.query("a") and f.query("b")  # one bit: everything is a false positive now
    g = BloomFilter(64, 4, seed=3)
    assert not any(g.query(x) for x in range(100))
    g.insert(b"x")
    g.insert("x")
    g.insert(0)
    assert g.query(b"x") and g.query("x") and g.query(0)
    with pytest.raises(ValueError):
        BloomFilter(0, 1)
    with pytest.raises(ValueError):
        BloomFilter(8, 0)


def test_no_false_negatives_random() -> None:
    rng = random.Random(1970)
    for _ in range(500):
        m = rng.randint(1, 200)
        k = rng.randint(1, 6)
        f = BloomFilter(m, k, seed=rng.randrange(1000))
        inserted: set[int] = set()
        for _ in range(rng.randint(0, 40)):
            x = rng.randrange(1000)
            if rng.random() < 0.5:
                f.insert(x)
                inserted.add(x)
            else:
                # an inserted key is always found; others may or may not be
                assert f.query(x) or x not in inserted
        assert all(f.query(x) for x in inserted)
        assert f.ones() <= min(m, k * len(inserted))


def test_union() -> None:
    a, b = BloomFilter(500, 3, seed=7), BloomFilter(500, 3, seed=7)
    both = BloomFilter(500, 3, seed=7)
    for x in range(40):
        (a if x % 2 else b).insert(x)
        both.insert(x)
    assert a.union(b).bits == both.bits
    with pytest.raises(ValueError):
        a.union(BloomFilter(500, 3, seed=8))


def test_false_positive_rate() -> None:
    m, n, k = 10_000, 1_000, 7
    f = BloomFilter(m, k, seed=11)
    for x in range(n):
        f.insert(x)
    trials = 50_000
    fp = sum(f.query(x) for x in range(n, n + trials)) / trials
    exact_given_bits = (f.ones() / m) ** k
    expected = (1 - math.exp(-k * n / m)) ** k
    assert abs(fp - exact_given_bits) < 0.003
    assert abs(fp - expected) < 0.003
