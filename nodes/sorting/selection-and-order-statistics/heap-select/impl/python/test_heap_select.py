# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-select/. The authors are listed in prov/0YXEH5.jsonl.

import random

import pytest

from heap_select import heap_select, sift_down


def test_example() -> None:
    a = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]
    assert heap_select(a, 3) == [23, 26, 31]
    assert heap_select(a, 1) == [23]
    assert heap_select(a, 10) == sorted(a)


def test_sift_down() -> None:
    h = [3, 9, 8, 5, 7]
    sift_down(h, 0, 5)
    assert h == [9, 7, 8, 5, 3]


def test_edges() -> None:
    assert heap_select([], 3) == []
    assert heap_select([5, 1], 0) == []
    assert heap_select([5, 1], 5) == [1, 5]
    assert heap_select([4, 4, 4, 4], 2) == [4, 4]
    assert heap_select(iter(range(100, 0, -1)), 4) == [1, 2, 3, 4]
    with pytest.raises(ValueError):
        heap_select([1], -1)


def test_random_against_sorted() -> None:
    rng = random.Random(4471)
    for _ in range(800):
        n = rng.randint(0, 60)
        a = [rng.randint(-15, 15) for _ in range(n)]
        k = rng.randint(0, n + 2)
        assert heap_select(a, k) == sorted(a)[:k]
