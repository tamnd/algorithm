# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monotonic-deque/. The authors are listed in prov/S8NDWC.jsonl.

import random

import pytest

from monotonic_deque import MonotonicDeque, sliding_min


def test_example() -> None:
    assert sliding_min([4, 2, 12, 3, 8, 5, 1, 7], 3) == [2, 2, 3, 3, 1, 1]


def test_example_states() -> None:
    q: MonotonicDeque[int] = MonotonicDeque()
    states = []
    for r, x in enumerate([4, 2, 12, 3, 8, 5, 1, 7]):
        q.push(x)
        if len(q) > 3:
            q.pop()
        q.check_invariant()
        states.append(list(q.d))
    assert states[3] == [(1, 2), (3, 3)]
    assert states[4] == [(3, 3), (4, 8)]
    assert states[6] == [(6, 1)]


def test_edges() -> None:
    assert sliding_min([], 1) == []
    assert sliding_min([5], 1) == [5]
    assert sliding_min([3, 1, 2], 1) == [3, 1, 2]
    assert sliding_min([3, 1, 2], 3) == [1]
    assert sliding_min([3, 1], 5) == []
    assert sliding_min([7, 7, 7, 7], 2) == [7, 7, 7]
    assert sliding_min([1, 2, 3, 4], 2) == [1, 2, 3]
    assert sliding_min([4, 3, 2, 1], 2) == [3, 2, 1]
    assert sliding_min([-(2**63), 2**63 - 1, 0], 2) == [-(2**63), 0]


def test_pitfalls() -> None:
    # tie rule: two equal items, the first leaves, a 2 is still in the window
    assert sliding_min([2, 2, 5], 2) == [2, 2]
    # window test off by one
    assert sliding_min([1, 3], 2) == [1]


def test_empty_errors() -> None:
    q: MonotonicDeque[int] = MonotonicDeque()
    with pytest.raises(IndexError):
        q.pop()
    with pytest.raises(IndexError):
        q.min()
    with pytest.raises(ValueError):
        sliding_min([1], 0)


def test_random_operations_against_list() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        q: MonotonicDeque[int] = MonotonicDeque()
        model: list[int] = []
        for _ in range(rng.randint(0, 60)):
            op = rng.random()
            if op < 0.55 or not model:
                x = rng.randint(-5, 5)
                q.push(x)
                model.append(x)
            elif op < 0.8:
                q.pop()
                model.pop(0)
            else:
                assert q.min() == min(model)
            q.check_invariant()
            assert len(q) == len(model)
            if model:
                assert q.min() == min(model)


def test_random_windows_against_brute_force() -> None:
    rng = random.Random(90210)
    for _ in range(500):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
        k = rng.randint(1, 8)
        want = [min(a[i : i + k]) for i in range(len(a) - k + 1)]
        assert sliding_min(a, k) == want
