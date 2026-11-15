# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/posting-list/. The authors are listed in prov/CHQP94.jsonl.

import bisect
import math
import random

import irtoy
from posting_list import PostingList, build_postings


class Counter:
    def __init__(self) -> None:
        self.n = 0


class Key:
    """An integer that counts each comparison it takes part in."""

    def __init__(self, v: int, c: Counter) -> None:
        self.v, self.c = v, c

    def __lt__(self, other: "Key") -> bool:
        self.c.n += 1
        return self.v < other.v

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Key)
        self.c.n += 1
        return self.v == other.v

    def __hash__(self) -> int:
        return hash(self.v)


def make(ids: list[int]) -> PostingList:
    p = PostingList()
    for d in ids:
        p.append(d)
    return p


def test_example() -> None:
    index = build_postings({d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()})
    p = index["sorted"]
    assert p.ids == [1, 2, 4, 8]
    assert p.tf == [1, 2, 1, 1]
    assert p.access(1) == (2, 2)
    c = Counter()
    q = PostingList()
    for d in p.ids:
        q.append(Key(d, c))
    c.n = 0
    assert q.next_geq(Key(5, c), 0) == 3
    assert c.n == 4
    assert p.next_geq(4, 0) == 2
    assert p.next_geq(9, 0) == 4
    assert p.next_geq(1, 2) == 2


def test_irtoy_statistics() -> None:
    index = build_postings({d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()})
    assert len(index) == 50
    assert sum(len(p) for p in index.values()) == 74
    for term, p in index.items():
        p.check_invariant()
        assert len(p) == irtoy.df(term)
        assert sum(p.tf) == irtoy.cf(term)
        for d, f in zip(p.ids, p.tf):
            assert f == irtoy.tf(term, d)


def test_edges() -> None:
    p = PostingList()
    assert len(p) == 0
    assert p.next_geq(5) == 0
    p.check_invariant()
    p.append(3, 2)
    assert p.next_geq(3) == 0 and p.next_geq(4) == 1 and p.next_geq(4, 1) == 1
    for bad in (3, 1):
        try:
            p.append(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("append out of order was accepted")
    p.check_invariant()


def test_random_against_bisect() -> None:
    rng = random.Random(20261115)
    for _ in range(800):
        n = rng.randint(0, 60)
        ids = sorted(rng.sample(range(200), n))
        c = Counter()
        p = make([Key(d, c) for d in ids])
        p.check_invariant()
        for _ in range(5):
            lo = rng.randint(0, n + 1)
            x = rng.randint(-5, 205)
            c.n = 0
            got = p.next_geq(Key(x, c), lo)
            want = max(lo, bisect.bisect_left(ids, x)) if lo <= n else lo
            assert got == want
            g = got - lo
            if lo < n:
                bound = 1 if g == 0 else 2 * math.floor(math.log2(g)) + 2
                assert c.n <= bound
            else:
                assert c.n == 0
