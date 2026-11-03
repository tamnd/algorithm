# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

import random

from insertion_sort import insertion_sort


def test_example() -> None:
    a = [5, 2, 4, 6, 1, 3]
    insertion_sort(a)
    assert a == [1, 2, 3, 4, 5, 6]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1]):
        b = list(a)
        insertion_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    a = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    class Key:
        def __init__(self, p: tuple[int, str]) -> None:
            self.p = p

        def __lt__(self, other: "Key") -> bool:
            return self.p[0] < other.p[0]

    b = [Key(p) for p in a]
    insertion_sort(b)
    assert [k.p for k in b] == [(1, "b"), (1, "d"), (2, "a"), (2, "c")]


def test_random_against_sorted() -> None:
    rng = random.Random(2150)
    for _ in range(500):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        b = list(a)
        insertion_sort(b)
        assert b == sorted(a)
