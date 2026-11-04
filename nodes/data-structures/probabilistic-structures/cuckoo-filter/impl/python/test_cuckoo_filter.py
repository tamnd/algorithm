# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuckoo-filter/. The authors are listed in prov/131BXM.jsonl.

import random
from collections import Counter

import pytest

from cuckoo_filter import CuckooFilter, Key

TABLE: dict[Key, tuple[int, int]] = {
    "a": (5, 0), "b": (6, 0), "c": (9, 0), "d": (7, 1), "e": (13, 0), "x": (7, 2), "y": (3, 3),
}


class FixedCF(CuckooFilter):
    def __init__(self) -> None:
        super().__init__(4, b=2, f=4)

    def _fp_index(self, key: Key) -> tuple[int, int]:
        return TABLE[key]

    def _alt(self, i: int, fp: int) -> int:
        return i ^ (fp % self.m)

    def _choose(self, n: int) -> int:
        return 0


def test_example() -> None:
    f = FixedCF()
    for k in "bacd":
        assert f.insert(k)
    assert f.table == [[6, 5], [9, 7], [], []]
    assert f.insert("e")  # kicks 6 from bucket 0 to bucket 0 ^ 2 = 2
    assert f.table == [[13, 5], [9, 7], [6], []]
    assert all(f.query(k) for k in "abcde")
    assert f.query("x")  # same fingerprint and buckets as d: a false positive
    assert not f.query("y")
    assert f.delete("a")
    assert f.table == [[13], [9, 7], [6], []]
    assert not f.query("a")


def test_victim() -> None:
    f = FixedCF()
    f.max_kicks = 3
    for k in "bacd":
        f.insert(k)
    f.table[2] = [1, 1]
    f.table[3] = [1, 1]  # fill the table so that e cannot be placed
    assert f.insert("e") and f.victim is not None
    assert not f.insert("y")  # full: no change
    assert all(f.query(k) for k in "abcde")
    assert f.delete("d")  # room again: the victim goes back into the table
    assert f.victim is None and all(f.query(k) for k in "abce")


def test_edges() -> None:
    with pytest.raises(ValueError):
        CuckooFilter(3)
    f = CuckooFilter(1, b=1, f=1)
    assert not f.query(0) and f.insert(0) and f.query(0)
    assert f.delete(0) and not f.query(0) and not f.delete(0)


def tokens_of_table(f: CuckooFilter) -> Counter[tuple[int, frozenset[int]]]:
    t: Counter[tuple[int, frozenset[int]]] = Counter()
    for j, bucket in enumerate(f.table):
        for fp in bucket:
            t[(fp, frozenset((j, f._alt(j, fp))))] += 1
    if f.victim is not None:
        j, fp = f.victim
        t[(fp, frozenset((j, f._alt(j, fp))))] += 1
    return t


def tokens_of_keys(f: CuckooFilter, live: Counter[int]) -> Counter[tuple[int, frozenset[int]]]:
    t: Counter[tuple[int, frozenset[int]]] = Counter()
    for x, c in live.items():
        fp, i1 = f._fp_index(x)
        if c:
            t[(fp, frozenset((i1, f._alt(i1, fp))))] += c
    return t


def test_random_against_multiset() -> None:
    rng = random.Random(2014)
    for _ in range(500):
        m = 1 << rng.randint(0, 4)
        b = rng.randint(1, 4)
        f = CuckooFilter(m, b, f=rng.randint(2, 10), max_kicks=rng.randint(1, 30), seed=rng.randrange(1000))
        live: Counter[int] = Counter()
        for _ in range(rng.randint(0, 80)):
            x = rng.randrange(40)
            r = rng.random()
            if r < 0.5:
                if f.insert(x):
                    live[x] += 1
            elif r < 0.8 and live[x] > 0:
                assert f.delete(x)
                live[x] -= 1
            else:
                assert f.query(x) or live[x] == 0
            assert tokens_of_table(f) == tokens_of_keys(f, live)
            assert all(f.query(y) for y in live if live[y])
            assert all(len(t) <= b for t in f.table)


def test_load_and_rate() -> None:
    f = CuckooFilter(1 << 10, b=4, f=12, seed=7)
    n = 0
    while f.insert(("k", n)):
        n += 1
    assert n >= 0.9 * 4 * (1 << 10)
    fp = sum(f.query(("q", i)) for i in range(20000))
    assert fp / 20000 <= 2 * 4 / ((1 << 12) - 1) + 0.002
