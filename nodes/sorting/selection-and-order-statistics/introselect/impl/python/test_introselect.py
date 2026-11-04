# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/introselect/. The authors are listed in prov/AQN873.jsonl.

import random

import pytest

from introselect import introselect, median3, mom_select, partition3


def test_example() -> None:
    a = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]
    assert [introselect(a, k) for k in range(1, 11)] == sorted(a)
    assert a == [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]


def test_helpers() -> None:
    for x in range(3):
        for y in range(3):
            for z in range(3):
                assert median3(x, y, z) == sorted([x, y, z])[1]
    b = [3, 7, 1, 3, 9, 2, 3, 8]
    p, q = partition3(b, 0, 8, 3)
    assert (p, q) == (2, 5)
    assert sorted(b[:2]) == [1, 2] and b[2:5] == [3, 3, 3] and sorted(b[5:]) == [7, 8, 9]
    assert mom_select(list(range(100, 0, -1)), 37) == 37


def test_edges() -> None:
    assert introselect([5], 1) == 5
    assert introselect([4] * 30, 9) == 4
    assert introselect(list(range(1000)), 500) == 499
    with pytest.raises(ValueError):
        introselect([], 1)


def test_random_against_sorted() -> None:
    rng = random.Random(1997)
    for _ in range(1500):
        n = rng.randint(1, 100)
        a = [rng.randint(-20, 20) for _ in range(n)]
        k = rng.randint(1, n)
        limit = rng.choice([0, 1, 2, 3])
        assert introselect(a, k, limit) == sorted(a)[k - 1]
