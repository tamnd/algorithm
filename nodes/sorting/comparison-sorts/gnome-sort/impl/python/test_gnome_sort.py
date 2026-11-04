# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gnome-sort/. The authors are listed in prov/6HS4Z7.jsonl.

import itertools
import random

from gnome_sort import gnome_sort


def inversions(a: list[int]) -> int:
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def test_example() -> None:
    a = [3, 1, 4, 2]
    assert gnome_sort(a) == 10
    assert a == [1, 2, 3, 4]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)]):
        b = list(a)
        gnome_sort(b)
        assert b == sorted(a)


def test_steps_are_n_plus_2d() -> None:
    for n in range(0, 7):
        for p in itertools.permutations(range(n)):
            b = list(p)
            assert gnome_sort(b) == n + 2 * inversions(list(p))
            assert b == list(range(n))


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(2, "a"), Key(1, "b"), Key(2, "c"), Key(1, "d")]
    gnome_sort(a)
    assert [x.tag for x in a] == ["b", "d", "a", "c"]


def test_random_against_sorted() -> None:
    rng = random.Random(2000)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 50))]
        b = list(a)
        gnome_sort(b)
        assert b == sorted(a)
