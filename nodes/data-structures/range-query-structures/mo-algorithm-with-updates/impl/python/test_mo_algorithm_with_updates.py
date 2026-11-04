# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mo-algorithm-with-updates/. The authors are listed in prov/XFPAYN.jsonl.

import random

import pytest

from mo_algorithm_with_updates import default_block, distinct_counts_with_updates, mo_with_updates


def brute(a: list[int], ops: list[tuple[str, int, int]]) -> list[int]:
    arr = list(a)
    out = []
    for kind, u, w in ops:
        if kind == "U":
            arr[u] = w
        else:
            out.append(len(set(arr[u:w])))
    return out


def test_example() -> None:
    a = [1, 2, 1, 3, 2]
    ops = [("Q", 0, 3), ("U", 1, 1), ("Q", 0, 3), ("Q", 1, 5), ("U", 3, 2), ("Q", 1, 5)]
    assert default_block(5) == 3
    assert distinct_counts_with_updates(a, ops) == [2, 1, 3, 2]


def test_moves_and_sum() -> None:
    a = [4, 1, 7]
    s = [0]

    def add(x: int) -> None:
        s[0] += x

    def remove(x: int) -> None:
        s[0] -= x

    queries = [(0, 3, 2), (0, 3, 0), (1, 2, 1), (2, 2, 2)]
    updates = [(1, 10), (0, 0)]
    assert mo_with_updates(a, queries, updates, add, remove, lambda: s[0], block=1) == [17, 12, 10, 0]
    assert a == [4, 1, 7]


def test_edges() -> None:
    assert distinct_counts_with_updates([], [("Q", 0, 0)]) == [0]
    assert distinct_counts_with_updates([5], [("U", 0, 5), ("Q", 0, 1)]) == [1]
    assert distinct_counts_with_updates([1, 2], []) == []
    with pytest.raises(IndexError):
        distinct_counts_with_updates([1], [("U", 1, 0)])
    with pytest.raises(IndexError):
        distinct_counts_with_updates([1], [("Q", 1, 0)])


def test_random() -> None:
    rng = random.Random(5)
    for _ in range(600):
        n = rng.randint(1, 12)
        a = [rng.randint(0, 4) for _ in range(n)]
        ops: list[tuple[str, int, int]] = []
        for _ in range(rng.randint(0, 15)):
            if rng.random() < 0.4:
                ops.append(("U", rng.randrange(n), rng.randint(0, 4)))
            else:
                l = rng.randint(0, n)
                ops.append(("Q", l, rng.randint(l, n)))
        assert distinct_counts_with_updates(a, ops) == brute(a, ops)
