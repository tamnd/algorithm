# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-positive-sum/. The authors are listed in prov/7FDZS3.jsonl.

import random

import pytest

from sliding_window_positive_sum import count_windows_below, min_window, min_window_length


def brute(a: list[int], s: int) -> int:
    best = 0
    for i in range(len(a)):
        for j in range(i, len(a)):
            if sum(a[i : j + 1]) >= s and (best == 0 or j - i + 1 < best):
                best = j - i + 1
    return best


def test_example() -> None:
    assert min_window_length([2, 3, 1, 2, 4, 3], 7) == 2
    assert min_window([2, 3, 1, 2, 4, 3], 7) == (4, 5)


def test_edges() -> None:
    assert min_window_length([], 5) == 0
    assert min_window([], 5) is None
    assert min_window_length([1, 1, 1], 4) == 0
    assert min_window_length([1, 1, 1], 3) == 3
    assert min_window_length([7], 7) == 1
    assert min_window_length([1, 4, 4], 4) == 1
    assert min_window([1, 4, 4], 4) == (1, 1)
    assert min_window_length([0, 0, 5, 0], 5) == 1
    assert min_window_length([0.5, 0.25, 0.25], 1.0) == 3
    assert count_windows_below([10, 5, 2, 6], 100) == 10
    with pytest.raises(ValueError):
        min_window_length([1, 2], 0)
    with pytest.raises(ValueError):
        min_window_length([5, -10, 4, 4], 8)


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(2000):
        n = rng.randrange(0, 20)
        a = [rng.randrange(0, 10) for _ in range(n)]
        s = rng.randrange(1, 40)
        expected = brute(a, s)
        assert min_window_length(a, s) == expected
        w = min_window(a, s)
        if expected == 0:
            assert w is None
        else:
            assert w is not None
            assert w[1] - w[0] + 1 == expected
            assert sum(a[w[0] : w[1] + 1]) >= s
        below = sum(
            1 for i in range(n) for j in range(i, n) if sum(a[i : j + 1]) < s
        )
        assert count_windows_below(a, s) == below
