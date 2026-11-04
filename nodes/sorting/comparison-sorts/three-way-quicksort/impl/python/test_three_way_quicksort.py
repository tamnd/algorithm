# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-way-quicksort/. The authors are listed in prov/JD10F7.jsonl.

import itertools
import random

from three_way_quicksort import partition3, three_way_quicksort


class Counted:
    count = 0

    def __init__(self, v: int) -> None:
        self.v = v

    def __lt__(self, other: "Counted") -> bool:
        Counted.count += 1
        return self.v < other.v


def test_example() -> None:
    a = [3, 1, 3, 2, 2, 1, 2, 3]
    three_way_quicksort(a)
    assert a == [1, 1, 2, 2, 2, 3, 3, 3]


def test_first_partition() -> None:
    a = [3, 1, 3, 2, 2, 1, 2, 3]
    lt, gt = partition3(a, 0, len(a))
    assert (lt, gt) == (2, 5)
    assert a == [1, 1, 2, 2, 2, 3, 3, 3]


def test_partition_postcondition() -> None:
    rng = random.Random(4)
    for _ in range(300):
        a = [rng.randint(0, 5) for _ in range(rng.randint(1, 40))]
        before = sorted(a)
        v = a[len(a) // 2]
        lt, gt = partition3(a, 0, len(a))
        assert sorted(a) == before
        assert all(x < v for x in a[:lt])
        assert all(x == v for x in a[lt:gt])
        assert all(x > v for x in a[gt:])
        assert lt < gt


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1], [5, 5, 5, 5], [2, 1, 2, 1]):
        b = list(a)
        three_way_quicksort(b)
        assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(7):
        for p in itertools.permutations(range(n)):
            a = list(p)
            three_way_quicksort(a)
            assert a == list(range(n))


def test_multisets() -> None:
    for p in set(itertools.permutations([0, 0, 1, 1, 1, 2, 2])):
        a = list(p)
        three_way_quicksort(a)
        assert a == [0, 0, 1, 1, 1, 2, 2]


def test_example_count() -> None:
    a = [Counted(x) for x in [3, 1, 3, 2, 2, 1, 2, 3]]
    Counted.count = 0
    three_way_quicksort(a)
    assert Counted.count == 24


def test_equal_keys_are_linear() -> None:
    n = 5000
    a = [Counted(7) for _ in range(n)]
    Counted.count = 0
    three_way_quicksort(a)
    assert Counted.count == 2 * n


def test_random_and_sorted() -> None:
    rng = random.Random(9)
    for _ in range(100):
        a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 80))]
        b = list(a)
        three_way_quicksort(b)
        assert b == sorted(a)
    a = list(range(3000))
    three_way_quicksort(a)
    assert a == list(range(3000))
