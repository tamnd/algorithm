# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

import random

from merge_sort import merge_sort


def test_example() -> None:
    a = [38, 27, 43, 3, 9, 82, 10]
    merge_sort(a)
    assert a == [3, 9, 10, 27, 38, 43, 82]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        merge_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(2, "a"), Key(1, "b"), Key(2, "c"), Key(1, "d"), Key(2, "e")]
    merge_sort(a)
    assert [x.tag for x in a] == ["b", "d", "a", "c", "e"]


def test_random_against_sorted() -> None:
    rng = random.Random(2150)
    for _ in range(500):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
        b = list(a)
        merge_sort(b)
        assert b == sorted(a)
