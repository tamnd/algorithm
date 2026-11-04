# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balance-sort/. The authors are listed in prov/A6ZN06.jsonl.

import random

import pytest

from balance_sort import Rec, Stats, balance_sort, distribute, read_cost, splitters_of, striped


class Item:
    def __init__(self, key: int, pos: int) -> None:
        self.key, self.pos = key, pos

    def __lt__(self, other: "Item") -> bool:
        return self.key < other.key


F = [19, 8, 9, 2, 16, 12, 4, 1, 15, 14, 5, 6, 17, 13, 11, 3, 18, 10, 7, 20]


def test_example() -> None:
    f = striped([Rec(x, i) for i, x in enumerate(F)], 1, 4)
    st = Stats()
    sp = splitters_of(f, 12, 1, 4, 4, st)
    assert [r.key for r in sp] == [5, 8, 12]
    out = distribute(f, sp, 1, 4, st)
    assert [[[blk[0].key for blk in disk] for disk in g] for g in out][0] == [[4], [3], [], [2, 1]]
    assert st.writes == [(4, 4), (4, 4), (4, 4), (4, 3), (5, 4), (1, 1)]
    g = list(F)
    assert balance_sort(g, 12, 1, 4) == 31
    assert g == list(range(1, 21))


def test_edges() -> None:
    for f in ([], [1], [2, 1], [3] * 50, list(range(60, 0, -1))):
        want = sorted(f)
        balance_sort(f, 12, 1, 4)
        assert f == want
    with pytest.raises(ValueError):
        balance_sort([1], 11, 1, 4)


def test_balance_invariant() -> None:
    rng = random.Random(1993)
    for _ in range(200):
        d = rng.randint(1, 9)
        b = rng.randint(1, 4)
        m = (2 * d + 4) * b + rng.randint(0, 30)
        n = rng.randint(m + 1, 6 * m)
        recs = [Rec(rng.randint(0, 9), i) for i in range(n)]
        f = striped(recs, b, d)
        st = Stats()
        sp = splitters_of(f, m, b, d, 4, st)
        st.writes = []
        for g in distribute(f, sp, b, d, st):
            x = sum(len(disk) for disk in g)
            assert read_cost(g) <= 2 * -(-x // d)
        for ready, written in st.writes:
            assert written >= min(ready, d // 2 + 1)


def test_stable() -> None:
    rng = random.Random(7)
    for _ in range(100):
        n = rng.randint(0, 300)
        f = [Item(rng.randint(0, 5), i) for i in range(n)]
        balance_sort(f, 24, 2, 3)
        assert [(r.key, r.pos) for r in f] == sorted((r.key, r.pos) for r in f)


def test_random_against_sorted() -> None:
    rng = random.Random(1990)
    for _ in range(600):
        n = rng.randint(0, 500)
        d = rng.randint(1, 6)
        b = rng.randint(1, 5)
        m = (2 * d + 4) * b + rng.randint(0, 40)
        f = [rng.randint(-50, 50) for _ in range(n)]
        want = sorted(f)
        balance_sort(f, m, b, d)
        assert f == want
