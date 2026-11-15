# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baeza-yates-intersection/. The authors are listed in prov/SRAJ81.jsonl.

import math
import random

import irtoy
from baeza_yates_intersection import baeza_yates, baeza_yates_all


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


def counted(a: list[int], b: list[int]) -> tuple[list[int], int]:
    c = Counter()
    r = baeza_yates([Key(x, c) for x in a], [Key(x, c) for x in b])
    return [k.v for k in r], c.n


def bound(la: int, lb: int) -> float:
    m, n = min(la, lb), max(la, lb)
    if m == 0:
        return 0.0
    return 2 * m * math.log2(2 + n / m) + 6 * m


def postings() -> dict[str, list[int]]:
    index: dict[str, list[int]] = {}
    for d in sorted(irtoy.DOCS):
        for t in sorted(set(irtoy.tokenize(irtoy.DOCS[d]))):
            index.setdefault(t, []).append(d)
    return index


def test_example() -> None:
    a = [7, 20, 40]
    b = list(range(2, 41, 2))
    r, n = counted(a, b)
    assert r == [20, 40]
    assert n == 13
    r2, n2 = counted(b, a)
    assert r2 == [20, 40] and n2 == n
    ix = postings()
    assert baeza_yates_all([ix["sorted"], ix["array"], ix["search"]]) == [1]
    r, n = counted(ix["sorted"], ix["array"])
    assert r == [1, 2, 8]


def test_irtoy_all_pairs() -> None:
    ix = postings()
    terms = sorted(ix)
    for i, s in enumerate(terms):
        for t in terms[i + 1:]:
            r, n = counted(ix[s], ix[t])
            assert r == sorted(set(ix[s]) & set(ix[t]))
            assert n <= bound(len(ix[s]), len(ix[t])) + 1e-9
    for q in irtoy.QUERIES.values():
        lists = [ix.get(t, []) for t in irtoy.tokenize(q)]
        assert baeza_yates_all(lists) == sorted(set(lists[0]).intersection(*lists[1:]))


def test_edges() -> None:
    assert baeza_yates([], []) == []
    assert baeza_yates([1], []) == []
    assert baeza_yates([], [1, 2]) == []
    assert baeza_yates([4], [4]) == [4]
    assert baeza_yates([1, 2, 3], [1, 2, 3]) == [1, 2, 3]
    assert baeza_yates([1, 3, 5], [2, 4, 6]) == []
    assert baeza_yates_all([[2, 5]]) == [2, 5]


def test_random_against_sets() -> None:
    rng = random.Random(2004)
    for _ in range(1500):
        u = rng.choice([20, 300, 100000])
        a = sorted(rng.sample(range(u), rng.randint(0, min(u, rng.choice([3, 30, 200])))))
        b = sorted(rng.sample(range(u), rng.randint(0, min(u, rng.choice([3, 30, 2000])))))
        r, n = counted(a, b)
        assert r == sorted(set(a) & set(b))
        assert n <= bound(len(a), len(b)) + 1e-9
        if a and b:
            assert n <= 10 * math.log2(math.comb(len(a) + len(b), min(len(a), len(b))))
    for _ in range(300):
        lists = [sorted(rng.sample(range(100), rng.randint(0, 50))) for _ in range(rng.randint(1, 5))]
        assert baeza_yates_all(lists) == sorted(set(lists[0]).intersection(*lists[1:]))
