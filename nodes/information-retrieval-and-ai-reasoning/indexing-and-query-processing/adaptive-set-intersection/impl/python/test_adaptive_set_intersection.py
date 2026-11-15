# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-set-intersection/. The authors are listed in prov/340HGS.jsonl.

import math
import random
from typing import Any

import irtoy
from adaptive_set_intersection import adaptive_intersect


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


def counted(lists: list[list[int]]) -> tuple[list[int], int, dict[str, Any]]:
    c = Counter()
    stats: dict[str, Any] = {}
    r = adaptive_intersect([[Key(x, c) for x in lst] for lst in lists], stats)
    return [k.v for k in r], c.n, stats


def run_bound(stats: dict[str, Any]) -> float:
    """The bound of the proof: 2 r log2(1 + n / r) + 2 r for each list."""
    total = 0.0
    for r, n in zip(stats["runs"], stats["lengths"]):
        if r > 0:
            total += 2 * r * math.log2(1 + n / r) + 2 * r
    return total


def two_list_bound(la: int, lb: int) -> float:
    m, n = min(la, lb), max(la, lb)
    if m == 0:
        return 0.0
    return 2 * m * math.log2(1 + n / m) + 6 * m


def postings() -> dict[str, list[int]]:
    index: dict[str, list[int]] = {}
    for d in sorted(irtoy.DOCS):
        for t in sorted(set(irtoy.tokenize(irtoy.DOCS[d]))):
            index.setdefault(t, []).append(d)
    return index


def check(lists: list[list[int]]) -> int:
    r, n, stats = counted(lists)
    expect = sorted(set(lists[0]).intersection(*lists[1:]))
    assert r == expect
    assert n <= run_bound(stats) + 1e-9
    if all(lists):
        assert all(x <= stats["eliminators"] for x in stats["runs"])
    if len(lists) == 2:
        assert n <= two_list_bound(len(lists[0]), len(lists[1])) + 1e-9
        if all(lists):
            m = min(len(lists[0]), len(lists[1]))
            assert n <= 8 * math.log2(math.comb(len(lists[0]) + len(lists[1]), m))
    return n


def test_example() -> None:
    a = [7, 20, 40]
    b = list(range(2, 41, 2))
    r, n, stats = counted([b, a])
    assert r == [20, 40]
    assert n == 22
    assert stats["runs"] == [2, 3]
    assert stats["eliminators"] == 5
    ix = postings()
    r, n, stats = counted([ix["sorted"], ix["array"], ix["search"]])
    assert r == [1]
    r, n, stats = counted([ix["posting"], ix["list"]])
    assert r == [3, 4]


def test_irtoy() -> None:
    ix = postings()
    terms = sorted(ix)
    for i, s in enumerate(terms):
        for t in terms[i + 1:]:
            check([ix[s], ix[t]])
    for q in irtoy.QUERIES.values():
        check([ix.get(t, []) for t in irtoy.tokenize(q)])
    rng = random.Random(35)
    for _ in range(300):
        check([ix[t] for t in rng.sample(terms, rng.randint(1, 5))])


def test_edges() -> None:
    assert adaptive_intersect([[]]) == []
    assert adaptive_intersect([[3, 9]]) == [3, 9]
    assert adaptive_intersect([[1, 2], []]) == []
    assert adaptive_intersect([[4], [4], [4]]) == [4]
    assert adaptive_intersect([[1, 2, 3], [1, 2, 3]]) == [1, 2, 3]
    assert adaptive_intersect([[1, 3, 5], [2, 4, 6]]) == []
    assert adaptive_intersect([[1, 2, 3], [4, 5, 6], [1, 6]]) == []
    assert adaptive_intersect([[10], list(range(100))]) == [10]


def test_random_against_sets() -> None:
    rng = random.Random(2000)
    for _ in range(1200):
        u = rng.choice([20, 300, 100000])
        a = sorted(rng.sample(range(u), rng.randint(0, min(u, rng.choice([3, 30, 200])))))
        b = sorted(rng.sample(range(u), rng.randint(0, min(u, rng.choice([3, 30, 2000])))))
        check([a, b])
    for _ in range(500):
        u = rng.choice([30, 200, 5000])
        k = rng.randint(1, 6)
        lists = [sorted(rng.sample(range(u), rng.randint(0, min(u, rng.choice([5, 50, 500]))))) for _ in range(k)]
        check(lists)


def test_lower_bound_inputs() -> None:
    """Two disjoint lists that interleave in blocks; the count stays within 8 log2 C(m+n, m)."""
    rng = random.Random(743)
    for _ in range(200):
        m = rng.randint(1, 40)
        n = rng.randint(m, 2000)
        values = list(range(m + n))
        chosen = set(rng.sample(values, m))
        a = [v for v in values if v in chosen]
        b = [v for v in values if v not in chosen]
        assert check([a, b]) >= 1
