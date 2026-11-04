# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-quickselect/. The authors are listed in prov/3SWVRD.jsonl.

import random
from collections import Counter

import pytest

from randomized_quickselect import partition3, randomized_quickselect


class FixedChoices:
    """A stand-in for random.Random that returns given indices in order."""

    def __init__(self, choices: list[int]) -> None:
        self.choices = list(choices)

    def randrange(self, lo: int, hi: int) -> int:
        i = self.choices.pop(0)
        assert lo <= i < hi
        return i


def test_page_example() -> None:
    a = [7, 2, 9, 4, 4, 1, 8, 5]
    rows: list[tuple[int, int, int, int, int, int, list[int]]] = []

    def trace(lo: int, hi: int, i: int, p: int, lt: int, gt: int) -> None:
        rows.append((lo, hi, i, p, lt, gt, list(a)))

    assert randomized_quickselect(a, 3, FixedChoices([6, 0, 2]), trace) == 4
    assert rows == [
        (0, 8, 6, 8, 6, 7, [7, 2, 5, 4, 4, 1, 8, 9]),
        (0, 6, 0, 7, 5, 6, [2, 5, 4, 4, 1, 7, 8, 9]),
        (0, 5, 2, 4, 2, 4, [2, 1, 4, 4, 5, 7, 8, 9]),
    ]


def test_edges() -> None:
    assert randomized_quickselect([5], 0) == 5
    assert randomized_quickselect([2, 1], 0) == 1
    assert randomized_quickselect([2, 1], 1) == 2
    assert randomized_quickselect([3, 3, 3, 3], 2) == 3
    for k in range(6):
        assert randomized_quickselect([1, 2, 3, 4, 5, 6], k) == k + 1
        assert randomized_quickselect([6, 5, 4, 3, 2, 1], k) == k + 1
    with pytest.raises(IndexError):
        randomized_quickselect([], 0)
    with pytest.raises(IndexError):
        randomized_quickselect([1, 2], 2)
    with pytest.raises(IndexError):
        randomized_quickselect([1, 2], -1)


def test_keeps_items_and_places_rank() -> None:
    rng = random.Random(7)
    a = [rng.randrange(10) for _ in range(50)]
    before = Counter(a)
    x = randomized_quickselect(a, 20, rng)
    assert Counter(a) == before
    assert a[20] == x
    assert all(y <= x for y in a[:20]) and all(x <= y for y in a[21:])


def test_partition3() -> None:
    a = [3, 1, 3, 5, 0, 3, 9]
    lt, gt = partition3(a, 0, len(a), 3)
    assert (lt, gt) == (2, 5)
    assert sorted(a[:lt]) == [0, 1] and a[lt:gt] == [3, 3, 3] and sorted(a[gt:]) == [5, 9]


def test_strings() -> None:
    words = ["pear", "fig", "apple", "kiwi", "date"]
    assert randomized_quickselect(list(words), 2, random.Random(1)) == "fig"


def test_random_against_sorted() -> None:
    rng = random.Random(20261104)
    for _ in range(800):
        n = rng.randint(1, 40)
        a = [rng.randint(-5, rng.choice([5, 1000])) for _ in range(n)]
        k = rng.randrange(n)
        oracle = sorted(a)[k]
        b = list(a)
        assert randomized_quickselect(b, k, rng) == oracle
        assert Counter(b) == Counter(a)


def test_expected_comparisons_below_4n() -> None:
    # Each round makes hi - lo three-way comparisons, one for each item of the range.
    rng = random.Random(5)
    for n in (50, 200):
        for k in (0, n // 2, n - 1):
            runs, total = 300, 0
            for _ in range(runs):
                cost = [0]

                def trace(lo: int, hi: int, i: int, p: int, lt: int, gt: int) -> None:
                    cost[0] += hi - lo

                a = list(range(n))
                rng.shuffle(a)
                randomized_quickselect(a, k, rng, trace)
                assert n <= cost[0] <= n * (n + 1) // 2
                total += cost[0]
            assert total / runs <= 4 * n
