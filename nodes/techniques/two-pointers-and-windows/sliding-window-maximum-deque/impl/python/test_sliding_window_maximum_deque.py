# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-maximum-deque/. The authors are listed in prov/N2ZTTV.jsonl.

import random

import pytest

from sliding_window_maximum_deque import sliding_window_maximum, sliding_window_minimum


def test_example() -> None:
    assert sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert sliding_window_minimum([1, 3, -1, -3, 5, 3, 6, 7], 3) == [-1, -3, -3, -3, 3, 3]


def test_edges() -> None:
    assert sliding_window_maximum([], 1) == []
    assert sliding_window_maximum([4], 1) == [4]
    assert sliding_window_maximum([1, 2], 3) == []
    assert sliding_window_maximum([5, 1, 1], 2) == [5, 1]
    assert sliding_window_maximum([2, 2, 2, 2], 2) == [2, 2, 2]
    assert sliding_window_maximum([4, 3, 2, 1], 4) == [4]
    assert sliding_window_maximum([1, 2, 3, 4], 1) == [1, 2, 3, 4]
    assert sliding_window_maximum([9, 8, 7, 6, 5], 2) == [9, 8, 7, 6]
    with pytest.raises(ValueError):
        sliding_window_maximum([1], 0)


def test_against_brute_force() -> None:
    rng = random.Random(20261104)
    for _ in range(2000):
        n = rng.randrange(0, 20)
        k = rng.randrange(1, n + 2)
        a = [rng.randrange(-5, 6) for _ in range(n)]
        want_max = [max(a[i : i + k]) for i in range(n - k + 1)]
        want_min = [min(a[i : i + k]) for i in range(n - k + 1)]
        assert sliding_window_maximum(a, k) == want_max
        assert sliding_window_minimum(a, k) == want_min
