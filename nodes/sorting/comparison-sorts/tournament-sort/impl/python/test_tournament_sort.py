# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-sort/. The authors are listed in prov/15RWNV.jsonl.

import math
import random

from tournament_sort import tournament_sort


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 3, 7, 6]
    assert tournament_sort(a) == 15
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_comparison_bound() -> None:
    rng = random.Random(1)
    for n in (2, 3, 7, 8, 9, 100, 1000):
        a = list(range(n))
        rng.shuffle(a)
        c = tournament_sort(a)
        assert a == list(range(n))
        assert c <= (n - 1) + (n - 1) * math.ceil(math.log2(n))


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1]):
        b = list(a)
        tournament_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(4)
    for _ in range(200):
        pairs = [(rng.randint(0, 4), i) for i in range(rng.randint(0, 40))]
        b = [Key(k, t) for k, t in pairs]
        tournament_sort(b)
        assert [(x.k, x.tag) for x in b] == sorted(pairs)


def test_random_against_sorted() -> None:
    rng = random.Random(6)
    for _ in range(100):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 300))]
        b = list(a)
        tournament_sort(b)
        assert b == sorted(a)
