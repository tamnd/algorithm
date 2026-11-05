# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monotonic-deque-prefix-sums/. The authors are listed in prov/HHFZR5.jsonl.

import random

import pytest

from monotonic_deque_prefix_sums import (
    max_sum_with_length_between,
    shortest_length_at_least,
    shortest_subarray_at_least,
)


def brute_shortest(a: list[int], k: int) -> int:
    n = len(a)
    best = -1
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += a[j]
            if s >= k and (best < 0 or j - i + 1 < best):
                best = j - i + 1
    return best


def brute_band(a: list[int], lo: int, hi: int):
    sums = [sum(a[i:j]) for i in range(len(a)) for j in range(i + lo, min(len(a), i + hi) + 1)]
    return max(sums) if sums else None


def test_example() -> None:
    assert shortest_subarray_at_least([84, -37, 32, 40, 95], 167) == (2, 5)
    assert shortest_length_at_least([2, -3, 4, -1, 3, -5, 6], 6) == 1
    assert shortest_length_at_least([2, -1, 2], 3) == 3
    assert shortest_length_at_least([1, 2], 4) == -1


def test_edges() -> None:
    assert shortest_subarray_at_least([], 0) is None
    assert shortest_subarray_at_least([-5], 0) is None
    assert shortest_subarray_at_least([-5], -5) == (0, 1)
    assert shortest_length_at_least([1, 1, 1], -10) == 1
    assert max_sum_with_length_between([1, -2, 3], 2, 3) == 2
    assert max_sum_with_length_between([1, 2], 3, 4) is None
    with pytest.raises(ValueError):
        max_sum_with_length_between([1], 0, 1)


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(3000):
        n = rng.randrange(0, 12)
        a = [rng.randrange(-8, 9) for _ in range(n)]
        k = rng.randrange(-6, 20)
        expected = brute_shortest(a, k)
        r = shortest_subarray_at_least(a, k)
        if expected < 0:
            assert r is None
        else:
            assert r is not None
            i, j = r
            assert j - i == expected and sum(a[i:j]) >= k
        lo = rng.randrange(1, 5)
        hi = lo + rng.randrange(0, 5)
        assert max_sum_with_length_between(a, lo, hi) == brute_band(a, lo, hi)
