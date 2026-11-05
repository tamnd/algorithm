# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distinct-count-two-pointers/. The authors are listed in prov/9MW95T.jsonl.

import random

import pytest

from distinct_count_two_pointers import (
    count_at_most_k_distinct,
    count_exactly_k_distinct,
    longest_at_most_k_distinct,
)


def brute_longest(a: list[int], k: int) -> int:
    n = len(a)
    return max(
        (j - i for i in range(n + 1) for j in range(i, n + 1) if len(set(a[i:j])) <= k),
        default=0,
    )


def brute_count(a: list[int], k: int, exact: bool) -> int:
    n = len(a)
    total = 0
    for i in range(n):
        for j in range(i + 1, n + 1):
            d = len(set(a[i:j]))
            if (d == k) if exact else (d <= k):
                total += 1
    return total


def test_example() -> None:
    assert longest_at_most_k_distinct([1, 2, 1, 2, 3, 3, 4, 1], 2) == (4, 0)
    assert longest_at_most_k_distinct([1, 2, 3, 2, 2], 2) == (4, 1)
    big = [10**9, -5, 10**9, 3, -5, -5, 3]
    assert longest_at_most_k_distinct(big, 2) == (4, 3)


def test_counts() -> None:
    assert count_at_most_k_distinct([1, 2, 1, 2, 3], 2) == 12
    assert count_at_most_k_distinct([1, 2, 1, 2, 3], 1) == 5
    assert count_exactly_k_distinct([1, 2, 1, 2, 3], 2) == 7
    assert count_exactly_k_distinct([1, 2, 1, 2, 3], 0) == 0


def test_edges() -> None:
    assert longest_at_most_k_distinct([], 3) == (0, 0)
    assert longest_at_most_k_distinct([5, 5, 5], 0) == (0, 0)
    assert longest_at_most_k_distinct([5, 5, 5], 1) == (3, 0)
    assert longest_at_most_k_distinct([1, 2, 3], 5) == (3, 0)
    assert longest_at_most_k_distinct("aabbbc", 1) == (3, 2)
    with pytest.raises(ValueError):
        longest_at_most_k_distinct([1], -1)


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(2000):
        n = rng.randrange(0, 13)
        a = [rng.randrange(0, rng.randrange(1, 6)) for _ in range(n)]
        k = rng.randrange(0, 5)
        length, start = longest_at_most_k_distinct(a, k)
        assert length == brute_longest(a, k)
        assert len(set(a[start:start + length])) <= k
        assert 0 <= start <= n - length
        assert count_at_most_k_distinct(a, k) == brute_count(a, k, False)
        assert count_exactly_k_distinct(a, k) == brute_count(a, k, True)
