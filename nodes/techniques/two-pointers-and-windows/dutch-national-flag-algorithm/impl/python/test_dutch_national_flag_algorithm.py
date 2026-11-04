# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dutch-national-flag-algorithm/. The authors are listed in prov/302WGD.jsonl.

import random
from collections import Counter

from dutch_national_flag_algorithm import sort_colors, three_way_partition


def check(before: list[int], after: list[int], pivot: int, lt: int, gt: int) -> None:
    assert Counter(before) == Counter(after)
    assert 0 <= lt <= gt <= len(after)
    assert all(x < pivot for x in after[:lt])
    assert all(x == pivot for x in after[lt:gt])
    assert all(x > pivot for x in after[gt:])


def test_example() -> None:
    a = [1, 2, 0, 1, 2, 0, 1]
    assert three_way_partition(a, 1) == (2, 5)
    assert a == [0, 0, 1, 1, 1, 2, 2]


def test_edges() -> None:
    a: list[int] = []
    assert three_way_partition(a, 1) == (0, 0)
    a = [1]
    assert three_way_partition(a, 1) == (0, 1)
    a = [2, 0]
    assert three_way_partition(a, 1) == (1, 1) and a == [0, 2]
    a = [1, 2, 0]
    assert three_way_partition(a, 1) == (1, 2) and a == [0, 1, 2]
    a = [1, 0]
    assert three_way_partition(a, 1) == (1, 2) and a == [0, 1]
    a = [5, 5, 5]
    assert three_way_partition(a, 5) == (0, 3)
    a = [3, 9, 1]
    assert three_way_partition(a, 4) == (2, 2) and sorted(a[:2]) == [1, 3]
    a = [2, 0, 2, 1, 1, 0]
    sort_colors(a)
    assert a == [0, 0, 1, 1, 2, 2]


def test_against_brute_force() -> None:
    rng = random.Random(20261104)
    for _ in range(2000):
        n = rng.randrange(0, 15)
        a = [rng.randrange(0, 6) for _ in range(n)]
        pivot = rng.randrange(-1, 7)
        b = a[:]
        lt, gt = three_way_partition(b, pivot)
        check(a, b, pivot, lt, gt)
        assert lt == sum(x < pivot for x in a)
        assert gt - lt == a.count(pivot)
        c = a[:]
        if all(x in (0, 1, 2) for x in c):
            sort_colors(c)
            assert c == sorted(a)
