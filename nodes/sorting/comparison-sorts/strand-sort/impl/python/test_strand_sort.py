# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strand-sort/. The authors are listed in prov/PWR6WE.jsonl.

import bisect
import itertools
import random

from strand_sort import merge, strand_sort, strands


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 3, 7, 6]
    assert strands(a) == [[5, 8], [1, 4, 7], [2, 3, 6]]
    strand_sort(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_merge() -> None:
    assert merge([1, 4, 5, 7, 8], [2, 3, 6]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert merge([], [1, 2]) == [1, 2]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], list(range(50, 0, -1))):
        b = list(a)
        strand_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(11)
    for _ in range(200):
        pairs = [(rng.randint(0, 4), i) for i in range(rng.randint(0, 30))]
        b = [Key(k, t) for k, t in pairs]
        strand_sort(b)
        assert [(x.k, x.tag) for x in b] == sorted(pairs)


def longest_strictly_decreasing(a: list[int]) -> int:
    tails: list[int] = []
    for x in a:
        i = bisect.bisect_left(tails, -x)
        if i == len(tails):
            tails.append(-x)
        else:
            tails[i] = -x
    return len(tails)


def test_strands_equal_longest_decreasing() -> None:
    for n in range(1, 7):
        for p in itertools.permutations(range(n)):
            assert len(strands(list(p))) == longest_strictly_decreasing(list(p))
    rng = random.Random(5)
    for _ in range(100):
        a = [rng.randint(0, 6) for _ in range(rng.randint(1, 40))]
        assert len(strands(a)) == longest_strictly_decreasing(a)


def test_random_against_sorted() -> None:
    rng = random.Random(2)
    for _ in range(100):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 200))]
        b = list(a)
        strand_sort(b)
        assert b == sorted(a)
