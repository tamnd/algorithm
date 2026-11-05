# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-kadane-algorithm/. The authors are listed in prov/00F99T.jsonl.

import random

import pytest

from circular_kadane_algorithm import circular_kadane, circular_kadane_arc


def brute(a: list[int]) -> int:
    n = len(a)
    return max(
        sum(a[(s + k) % n] for k in range(length))
        for s in range(n)
        for length in range(1, n + 1)
    )


def arc_sum(a: list[int], start: int, length: int) -> int:
    return sum(a[(start + k) % len(a)] for k in range(length))


def test_example() -> None:
    assert circular_kadane([8, -4, 3, -5, 4]) == 12
    assert circular_kadane_arc([8, -4, 3, -5, 4]) == (12, 4, 2)
    assert circular_kadane([5, -3, 5]) == 10
    assert circular_kadane([1, -2, 3, -2]) == 3


def test_edges() -> None:
    assert circular_kadane([-3, -2, -3]) == -2
    assert circular_kadane_arc([-3, -2, -3]) == (-2, 1, 1)
    assert circular_kadane([7]) == 7
    assert circular_kadane([-7]) == -7
    assert circular_kadane([5, -10]) == 5
    assert circular_kadane([-1, 0]) == 0
    assert circular_kadane([1, 2, 3]) == 6
    assert circular_kadane([0.5, -1.0, 0.5]) == 1.0
    with pytest.raises(ValueError):
        circular_kadane([])
    with pytest.raises(ValueError):
        circular_kadane_arc([])


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(3000):
        n = rng.randrange(1, 15)
        a = [rng.randrange(-10, 11) for _ in range(n)]
        expected = brute(a)
        assert circular_kadane(a) == expected
        value, start, length = circular_kadane_arc(a)
        assert value == expected
        assert 0 <= start < n and 1 <= length <= n
        assert arc_sum(a, start, length) == expected
