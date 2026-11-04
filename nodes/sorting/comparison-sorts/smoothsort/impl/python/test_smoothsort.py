# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smoothsort/. The authors are listed in prov/WX5SGY.jsonl.

import itertools
import random

from smoothsort import leonardo, smoothsort

count = [0]


class Counted:
    __slots__ = ("k",)

    def __init__(self, k: int) -> None:
        self.k = k

    def __lt__(self, other: "Counted") -> bool:
        count[0] += 1
        return self.k < other.k


def comparisons(keys: list[int]) -> int:
    count[0] = 0
    b = [Counted(k) for k in keys]
    smoothsort(b)
    assert [x.k for x in b] == sorted(keys)
    return count[0]


def test_leonardo() -> None:
    assert leonardo(100) == [1, 1, 3, 5, 9, 15, 25, 41, 67, 109]


def test_example() -> None:
    assert comparisons([7, 2, 9, 4, 1, 8, 3, 6]) == 33


def test_all_permutations() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            smoothsort(b)
            assert b == list(range(n))


def test_sorted_input_is_linear() -> None:
    for n in (100, 1000, 10000):
        assert comparisons(list(range(n))) <= 6 * n


def test_random_against_sorted() -> None:
    rng = random.Random(3)
    for _ in range(200):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 300))]
        b = list(a)
        smoothsort(b)
        assert b == sorted(a)
