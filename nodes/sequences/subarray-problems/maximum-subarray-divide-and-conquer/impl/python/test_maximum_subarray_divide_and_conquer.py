# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-subarray-divide-and-conquer/. The authors are listed in prov/NXBA0T.jsonl.

import random

import pytest

from maximum_subarray_divide_and_conquer import max_subarray_dc, max_subarray_linear_dc


def brute(a: list[int]) -> int:
    return max(sum(a[i : j + 1]) for i in range(len(a)) for j in range(i, len(a)))


def test_example() -> None:
    assert max_subarray_dc([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == (6, 3, 6)
    assert max_subarray_dc([31, -41, 59, 26, -53, 58, 97, -93, -23, 84]) == (187, 2, 6)
    clrs = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    assert max_subarray_dc(clrs) == (43, 7, 10)
    assert max_subarray_linear_dc(clrs) == 43


def test_edges() -> None:
    assert max_subarray_dc([5]) == (5, 0, 0)
    assert max_subarray_dc([-5]) == (-5, 0, 0)
    assert max_subarray_dc([-3, -1, -2]) == (-1, 1, 1)
    assert max_subarray_dc([1, 2, 3]) == (6, 0, 2)
    assert max_subarray_dc([1.5, -0.5, 2.0]) == (3.0, 0, 2)
    assert max_subarray_linear_dc([-3, -1, -2]) == -1
    with pytest.raises(ValueError):
        max_subarray_dc([])
    with pytest.raises(ValueError):
        max_subarray_linear_dc([])


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(2000):
        n = rng.randrange(1, 30)
        a = [rng.randrange(-10, 11) for _ in range(n)]
        best, i, j = max_subarray_dc(a)
        assert best == brute(a)
        assert 0 <= i <= j < n
        assert sum(a[i : j + 1]) == best
        assert max_subarray_linear_dc(a) == best
