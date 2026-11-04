# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoare-partition/. The authors are listed in prov/HR9MYC.jsonl.

import itertools
import random

from hoare_partition import hoare_partition, quicksort


def check(a: list[int], lo: int, hi: int) -> None:
    before = list(a)
    j = hoare_partition(a, lo, hi)
    assert lo <= j < hi
    assert max(a[lo : j + 1]) <= min(a[j + 1 : hi + 1])
    assert sorted(a[lo : hi + 1]) == sorted(before[lo : hi + 1])
    assert a[:lo] == before[:lo] and a[hi + 1 :] == before[hi + 1 :]


def test_example() -> None:
    a = [5, 3, 8, 4, 9, 2, 7, 1, 6]
    assert hoare_partition(a, 0, 8) == 3
    assert a == [1, 3, 2, 4, 9, 8, 7, 5, 6]


def test_edges() -> None:
    a = [2, 1]
    assert hoare_partition(a, 0, 1) == 0 and a == [1, 2]
    a = [1, 2]
    assert hoare_partition(a, 0, 1) == 0 and a == [1, 2]
    a = [7] * 8
    assert hoare_partition(a, 0, 7) == 3
    a = [7] * 9
    assert hoare_partition(a, 0, 8) == 4
    check([9, 1, 2, 3, 4], 0, 4)
    check([1, 9, 8, 7], 0, 3)
    check([0, 5, 3, 5, 1, 0], 1, 4)


def test_all_permutations() -> None:
    for n in range(2, 8):
        for p in itertools.permutations(range(n)):
            check(list(p), 0, n - 1)


def test_random_partitions_and_sort() -> None:
    rng = random.Random(1961)
    for _ in range(800):
        n = rng.randint(2, 40)
        a = [rng.randint(-5, 5) for _ in range(n)]
        lo = rng.randint(0, n - 2)
        hi = rng.randint(lo + 1, n - 1)
        check(a, lo, hi)
        b = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
        c = list(b)
        quicksort(c)
        assert c == sorted(b)
