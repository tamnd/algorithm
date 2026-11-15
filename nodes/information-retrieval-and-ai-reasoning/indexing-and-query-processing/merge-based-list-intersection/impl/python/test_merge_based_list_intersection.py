# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-based-list-intersection/. The authors are listed in prov/06R0D3.jsonl.

import itertools
import random

import irtoy
from merge_based_list_intersection import intersect, intersect_all


class Counter:
    def __init__(self) -> None:
        self.eq = 0
        self.lt = 0


class Key:
    """An integer that counts the tests it takes part in."""

    def __init__(self, v: int, c: Counter) -> None:
        self.v, self.c = v, c

    def __lt__(self, other: "Key") -> bool:
        self.c.lt += 1
        return self.v < other.v

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Key)
        self.c.eq += 1
        return self.v == other.v

    def __hash__(self) -> int:
        return hash(self.v)


def postings() -> dict[str, list[int]]:
    index: dict[str, list[int]] = {}
    for d in sorted(irtoy.DOCS):
        for t in sorted(set(irtoy.tokenize(irtoy.DOCS[d]))):
            index.setdefault(t, []).append(d)
    return index


def counted(a: list[int], b: list[int]) -> tuple[list[int], Counter]:
    c = Counter()
    r = intersect([Key(x, c) for x in a], [Key(x, c) for x in b])
    return [k.v for k in r], c


def test_example() -> None:
    ix = postings()
    r, c = counted(ix["sorted"], ix["array"])
    assert r == [1, 2, 8]
    assert c.eq == 4
    assert intersect_all([ix["sorted"], ix["array"], ix["search"]]) == [1]
    assert intersect_all([ix["posting"], ix["list"], ix["merge"]]) == []
    r, c = counted(ix["search"], ix["array"])
    assert r == [1] and c.eq == 3
    r, c = counted(r, ix["sorted"])
    assert r == [1] and c.eq == 1


def test_worst_case_is_tight() -> None:
    r, c = counted([1, 3, 5], [2, 4, 6])
    assert r == [] and c.eq == 5


def test_irtoy_all_pairs_and_triples() -> None:
    ix = postings()
    terms = sorted(ix)
    for s, t in itertools.combinations(terms, 2):
        r, c = counted(ix[s], ix[t])
        assert r == sorted(set(ix[s]) & set(ix[t]))
        assert c.eq <= len(ix[s]) + len(ix[t]) - 1
    for q in irtoy.QUERIES.values():
        lists = [ix.get(t, []) for t in irtoy.tokenize(q)]
        want = set(lists[0]).intersection(*lists[1:])
        assert intersect_all(lists) == sorted(want)


def test_edges() -> None:
    assert intersect([], []) == []
    assert intersect([1, 2], []) == []
    assert intersect([], [1]) == []
    assert intersect([5], [5]) == [5]
    assert intersect_all([[1, 2, 3]]) == [1, 2, 3]
    r, c = counted([1, 2, 3], [7])
    assert r == [] and c.eq == 3


def test_random_against_sets() -> None:
    rng = random.Random(1996)
    for _ in range(1500):
        u = rng.choice([10, 50, 1000])
        a = sorted(rng.sample(range(u), rng.randint(0, min(u, 60))))
        b = sorted(rng.sample(range(u), rng.randint(0, min(u, 60))))
        r, c = counted(a, b)
        assert r == sorted(set(a) & set(b))
        if a and b:
            assert c.eq <= len(a) + len(b) - 1
            assert c.lt <= c.eq
        else:
            assert c.eq == 0
    for _ in range(300):
        lists = [sorted(rng.sample(range(80), rng.randint(0, 40))) for _ in range(rng.randint(1, 6))]
        want = set(lists[0]).intersection(*lists[1:])
        assert intersect_all(lists) == sorted(want)
