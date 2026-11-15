# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-versus-small-intersection/. The authors are listed in prov/39S9T4.jsonl.

import bisect
import math
import random

import irtoy
from small_versus_small_intersection import gallop, svs


class Counter:
    def __init__(self) -> None:
        self.n = 0


class Key:
    """An integer that counts each test it takes part in."""

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


def counted(lists: list[list[int]]) -> tuple[list[int], int]:
    c = Counter()
    r = svs([[Key(x, c) for x in lst] for lst in lists])
    return [k.v for k in r], c.n


def bound(lengths: list[int]) -> float:
    ns = sorted(lengths)
    m = ns[0]
    if m == 0:
        return 0.0
    return sum(2 * m * math.log2(1 + n / m) + 3 * m for n in ns[1:])


def postings() -> dict[str, list[int]]:
    index: dict[str, list[int]] = {}
    for d in sorted(irtoy.DOCS):
        for t in sorted(set(irtoy.tokenize(irtoy.DOCS[d]))):
            index.setdefault(t, []).append(d)
    return index


def test_example() -> None:
    a = [7, 20, 40]
    b = list(range(2, 41, 2))
    r, n = counted([b, a])
    assert r == [20, 40]
    assert n == 19
    assert n <= bound([3, 20])
    ix = postings()
    r, n = counted([ix["sorted"], ix["array"], ix["search"]])
    assert r == [1] and n == 7


def test_irtoy_queries() -> None:
    ix = postings()
    terms = sorted(ix)
    rng = random.Random(8)
    for _ in range(400):
        q = rng.sample(terms, rng.randint(1, 4))
        lists = [ix[t] for t in q]
        r, n = counted(lists)
        assert r == sorted(set(lists[0]).intersection(*lists[1:]))
        assert n <= bound([len(x) for x in lists]) + 1e-9
    for q in irtoy.QUERIES.values():
        lists = [ix.get(t, []) for t in irtoy.tokenize(q)]
        assert svs(lists) == sorted(set(lists[0]).intersection(*lists[1:]))


def test_edges() -> None:
    assert svs([[]]) == []
    assert svs([[], [1, 2]]) == []
    assert svs([[1, 2, 3]]) == [1, 2, 3]
    assert svs([[5], [5], [5]]) == [5]
    assert svs([[1, 2], [3, 4]]) == []
    assert gallop([], 3, 0) == 0
    assert gallop([1, 2, 3], 9, 0) == 3


def test_gallop_against_bisect() -> None:
    rng = random.Random(5)
    for _ in range(1000):
        lst = sorted(rng.sample(range(300), rng.randint(0, 80)))
        lo = rng.randint(0, len(lst))
        x = rng.randint(-3, 303)
        c = Counter()
        p = gallop([Key(v, c) for v in lst], Key(x, c), lo)
        assert p == max(lo, bisect.bisect_left(lst, x))
        g = p - lo
        if lo < len(lst):
            assert c.n <= (1 if g == 0 else 2 * math.floor(math.log2(g)) + 2)


def test_random_against_sets() -> None:
    rng = random.Random(2009)
    for _ in range(700):
        k = rng.randint(1, 5)
        u = rng.choice([30, 500, 100000])
        lists = [sorted(rng.sample(range(u), rng.randint(0, min(u, rng.choice([5, 40, 400]))))) for _ in range(k)]
        r, n = counted(lists)
        assert r == sorted(set(lists[0]).intersection(*lists[1:]))
        assert n <= bound([len(x) for x in lists]) + 1e-9
