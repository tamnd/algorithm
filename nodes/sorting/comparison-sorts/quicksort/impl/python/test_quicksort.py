# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quicksort/. The authors are listed in prov/5TYMK3.jsonl.

import itertools
import random

from quicksort import partition, quicksort


def test_example() -> None:
    a = [6, 3, 9, 1, 7, 2, 8, 5]
    quicksort(a)
    assert a == [1, 2, 3, 5, 6, 7, 8, 9]


def test_first_partition() -> None:
    a = [6, 3, 9, 1, 7, 2, 8, 5]
    p = partition(a, 0, len(a))
    assert p == 3
    assert a == [3, 1, 2, 5, 7, 9, 8, 6]


def test_partition_postcondition() -> None:
    rng = random.Random(7)
    for _ in range(300):
        a = [rng.randint(0, 9) for _ in range(rng.randint(1, 30))]
        old = sorted(a)
        x = a[-1]
        p = partition(a, 0, len(a))
        assert a[p] == x
        assert all(v <= x for v in a[:p])
        assert all(v > x for v in a[p + 1 :])
        assert sorted(a) == old


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        quicksort(b)
        assert b == sorted(a)


def test_subrange() -> None:
    a = [9, 5, 4, 3, 2, 0]
    quicksort(a, 1, 5)
    assert a == [9, 2, 3, 4, 5, 0]


def test_all_permutations() -> None:
    for n in range(7):
        for p in itertools.permutations(range(n)):
            b = list(p)
            quicksort(b)
            assert b == list(range(n))


def test_sorted_worst_case() -> None:
    a = list(range(3000))
    quicksort(a)
    assert a == list(range(3000))


def test_random_against_sorted() -> None:
    rng = random.Random(2150)
    for _ in range(500):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
        b = list(a)
        quicksort(b)
        assert b == sorted(a)
