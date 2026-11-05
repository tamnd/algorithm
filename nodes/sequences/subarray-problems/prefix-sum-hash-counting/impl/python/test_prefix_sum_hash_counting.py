# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefix-sum-hash-counting/. The authors are listed in prov/ASHEE3.jsonl.

import random

import pytest

from prefix_sum_hash_counting import (
    count_subarrays_divisible,
    count_subarrays_with_sum,
    longest_subarray_with_sum,
)


def sums(a: list[int]) -> list[tuple[int, int, int]]:
    return [(i, j, sum(a[i : j + 1])) for i in range(len(a)) for j in range(i, len(a))]


def test_example() -> None:
    assert count_subarrays_with_sum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
    assert count_subarrays_with_sum([1, 1, 1], 2) == 2
    assert longest_subarray_with_sum([15, -2, 2, -8, 1, 7, 10, 23], 0) == (5, 1)


def test_edges() -> None:
    assert count_subarrays_with_sum([], 0) == 0
    assert count_subarrays_with_sum([7], 7) == 1
    assert count_subarrays_with_sum([0, 0, 0, 0], 0) == 10
    assert count_subarrays_with_sum([1, 2, 3], 7) == 0
    assert longest_subarray_with_sum([1, 2, 3], 7) == (0, -1)
    assert count_subarrays_divisible([4, 5, 0, -2, -3, 1], 5) == 7
    assert count_subarrays_divisible([-3], 3) == 1
    with pytest.raises(ValueError):
        count_subarrays_divisible([1], 0)


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(2000):
        n = rng.randrange(0, 20)
        a = [rng.randrange(-5, 6) for _ in range(n)]
        k = rng.randrange(-6, 7)
        all_sums = sums(a)
        assert count_subarrays_with_sum(a, k) == sum(1 for _, _, s in all_sums if s == k)
        lengths = [j - i + 1 for i, j, s in all_sums if s == k]
        length, start = longest_subarray_with_sum(a, k)
        assert length == max(lengths, default=0)
        if length:
            assert sum(a[start : start + length]) == k
        m = rng.randrange(1, 7)
        assert count_subarrays_divisible(a, m) == sum(1 for _, _, s in all_sums if s % m == 0)
