# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lomuto-partition/. The authors are listed in prov/N086ME.jsonl.

import itertools
import random

import pytest

from lomuto_partition import lomuto_partition


def check(a: list[int], lo: int, hi: int) -> None:
    old = list(a)
    x = a[hi - 1]
    p = lomuto_partition(a, lo, hi)
    assert lo <= p < hi
    assert a[p] == x
    assert all(v <= x for v in a[lo:p])
    assert all(v > x for v in a[p + 1 : hi])
    assert sorted(a[lo:hi]) == sorted(old[lo:hi])
    assert a[:lo] == old[:lo] and a[hi:] == old[hi:]


def test_example() -> None:
    a = [6, 3, 9, 1, 7, 2, 8, 5]
    assert lomuto_partition(a) == 3
    assert a == [3, 1, 2, 5, 7, 9, 8, 6]


def test_one_item() -> None:
    a = [4]
    assert lomuto_partition(a) == 0
    assert a == [4]


def test_empty_range() -> None:
    with pytest.raises(ValueError):
        lomuto_partition([], 0, 0)


def test_equal_items_go_left() -> None:
    a = [7, 7, 7, 7]
    assert lomuto_partition(a) == 3


def test_extreme_pivots() -> None:
    a = [1, 2, 3, 4, 5]
    assert lomuto_partition(a) == 4
    b = [5, 4, 3, 2, 1]
    assert lomuto_partition(b) == 0
    assert b == [1, 4, 3, 2, 5]


def test_all_small_inputs() -> None:
    for n in range(1, 7):
        for p in itertools.product(range(3), repeat=n):
            check(list(p), 0, n)


def test_subrange() -> None:
    rng = random.Random(11)
    for _ in range(400):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(1, 40))]
        lo = rng.randrange(len(a))
        hi = rng.randint(lo + 1, len(a))
        check(a, lo, hi)
