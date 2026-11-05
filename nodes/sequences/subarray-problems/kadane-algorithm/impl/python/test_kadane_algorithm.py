# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kadane-algorithm/. The authors are listed in prov/W9Q826.jsonl.

import random

import pytest

from kadane_algorithm import kadane, kadane_allow_empty


def brute(a: list[int]) -> int:
    return max(sum(a[i : j + 1]) for i in range(len(a)) for j in range(i, len(a)))


def test_example() -> None:
    assert kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == (6, 3, 6)
    assert kadane([31, -41, 59, 26, -53, 58, 97, -93, -23, 84]) == (187, 2, 6)
    clrs = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    assert kadane(clrs) == (43, 7, 10)


def test_edges() -> None:
    assert kadane([5]) == (5, 0, 0)
    assert kadane([-5]) == (-5, 0, 0)
    assert kadane([-3, -1, -2]) == (-1, 1, 1)
    assert kadane_allow_empty([-3, -1, -2]) == 0
    assert kadane_allow_empty([]) == 0
    assert kadane([0, 0, 0]) == (0, 0, 0)
    assert kadane([1, 2, 3]) == (6, 0, 2)
    assert kadane([2, -2, 2]) == (2, 0, 0)
    assert kadane([1.5, -0.5, 2.0]) == (3.0, 0, 2)
    with pytest.raises(ValueError):
        kadane([])


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(3000):
        n = rng.randrange(1, 25)
        a = [rng.randrange(-10, 11) for _ in range(n)]
        best, i, j = kadane(a)
        assert best == brute(a)
        assert 0 <= i <= j < n
        assert sum(a[i : j + 1]) == best
        assert kadane_allow_empty(a) == max(best, 0)
