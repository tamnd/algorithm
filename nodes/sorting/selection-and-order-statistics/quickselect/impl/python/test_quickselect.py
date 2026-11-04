# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quickselect/. The authors are listed in prov/TTGB6K.jsonl.

import random

import pytest

from quickselect import partition, quickselect


def test_example() -> None:
    a = [7, 2, 9, 4, 1, 8, 3, 6, 5]
    assert quickselect(list(a), 5, random.Random(1)) == 5
    for k in range(1, 10):
        assert quickselect(list(a), k, random.Random(k)) == k


def test_partition() -> None:
    a = [7, 2, 9, 4, 1, 8, 3, 6, 5]
    p = partition(a, 0, len(a))
    assert p == 4 and a[p] == 5
    assert all(x <= 5 for x in a[:p]) and all(x > 5 for x in a[p + 1 :])


def test_edges() -> None:
    assert quickselect([42], 1) == 42
    assert quickselect([2, 1], 1) == 1
    assert quickselect([2, 1], 2) == 2
    assert quickselect([3, 3, 3, 3], 2) == 3
    with pytest.raises(ValueError):
        quickselect([], 1)
    with pytest.raises(ValueError):
        quickselect([1, 2], 3)


def test_rearranges_around_answer() -> None:
    rng = random.Random(7)
    a = [rng.randint(0, 9) for _ in range(40)]
    v = quickselect(a, 17, rng)
    assert a[16] == v
    assert all(x <= v for x in a[:16]) and all(x >= v for x in a[17:])


def test_random_against_sorted() -> None:
    rng = random.Random(9150)
    for _ in range(800):
        n = rng.randint(1, 50)
        a = [rng.randint(-20, 20) for _ in range(n)]
        k = rng.randint(1, n)
        b = list(a)
        assert quickselect(b, k, rng) == sorted(a)[k - 1]
        assert sorted(b) == sorted(a)
