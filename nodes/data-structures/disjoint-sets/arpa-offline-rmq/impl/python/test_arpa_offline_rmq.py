# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arpa-offline-rmq/. The authors are listed in prov/2G2RRV.jsonl.

import random

import pytest

from arpa_offline_rmq import arpa_offline_rmq


def brute(a: list[int], lo: int, hi: int) -> int:
    best = lo
    for t in range(lo, hi + 1):
        if a[t] < a[best]:
            best = t
    return best


def test_example() -> None:
    a = [3, 1, 4, 1, 5, 9, 2, 6]
    qs = [(0, 2), (2, 5), (5, 5), (2, 6), (4, 7), (0, 7)]
    assert arpa_offline_rmq(a, qs) == [1, 3, 5, 3, 6, 1]


def test_edges() -> None:
    assert arpa_offline_rmq([], []) == []
    assert arpa_offline_rmq([7], [(0, 0)]) == [0]
    assert arpa_offline_rmq([2, 2, 2], [(0, 2), (1, 2)]) == [0, 1]
    with pytest.raises(ValueError):
        arpa_offline_rmq([1, 2], [(1, 0)])
    with pytest.raises(ValueError):
        arpa_offline_rmq([1, 2], [(0, 2)])


def test_long_decreasing_chain() -> None:
    n = 100000
    a = list(range(n, 0, -1))
    qs = [(0, n - 1), (0, 0), (5, n // 2)]
    assert arpa_offline_rmq(a, qs) == [n - 1, 0, n // 2]


def test_random_against_scan() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(1, 30)
        a = [rng.randrange(6) for _ in range(n)]
        qs = []
        for _ in range(rng.randrange(1, 20)):
            lo = rng.randrange(n)
            qs.append((lo, rng.randrange(lo, n)))
        assert arpa_offline_rmq(a, qs) == [brute(a, lo, hi) for lo, hi in qs]
