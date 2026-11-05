# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brute-force-nearest-neighbor-search/. The authors are listed in prov/VXFMJM.jsonl.

import math
import random

import pytest

from brute_force_nearest_neighbor_search import brute_force_knn, squared_euclidean

P = [(1, 1), (2, 4), (4, 2), (5, 5), (6, 1), (7, 3), (3, 6), (4, 4)]


def test_example() -> None:
    assert brute_force_knn(P, (4, 3), 3) == [(1, 2), (1, 7), (5, 1)]


def test_edges() -> None:
    assert brute_force_knn([], (0, 0), 3) == []
    assert brute_force_knn([(2, 2)], (0, 0), 1) == [(8, 0)]
    assert brute_force_knn([(1, 1)] * 4, (0, 0), 2) == [(2, 0), (2, 1)]
    assert brute_force_knn(P, (4, 3), 100) == sorted((squared_euclidean(p, (4, 3)), i) for i, p in enumerate(P))
    with pytest.raises(ValueError):
        brute_force_knn(P, (0, 0), 0)


def test_other_metric() -> None:
    def l1(a, b):
        return sum(abs(x - y) for x, y in zip(a, b))

    got = brute_force_knn(P, (4, 3), 5, l1)
    assert [i for _, i in got] == [2, 7, 1, 3, 5]


def test_decreasing_order_replaces_each_time() -> None:
    pts = [(float(10 - i),) for i in range(10)]
    assert brute_force_knn(pts, (0.0,), 2) == [(1.0, 9), (4.0, 8)]


def test_random_against_sort() -> None:
    rng = random.Random(4242)
    for _ in range(600):
        n = rng.randint(0, 40)
        d = rng.randint(1, 4)
        pts = [tuple(rng.randint(-5, 5) for _ in range(d)) for _ in range(n)]
        q = tuple(rng.randint(-5, 5) for _ in range(d))
        k = rng.randint(1, 10)
        want = sorted((squared_euclidean(p, q), i) for i, p in enumerate(pts))[:k]
        assert brute_force_knn(pts, q, k) == want
        got_l2 = brute_force_knn(pts, q, k, lambda a, b: math.dist(a, b))
        assert [i for _, i in got_l2] == [i for _, i in want]
