# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-dominated-sorting/. The authors are listed in prov/PQCHE1.jsonl.

import random

from non_dominated_sorting import (
    dominates,
    fast_non_dominated_sort,
    non_dominated_sort_2d,
    ranks_from_fronts,
)


def peel(points):
    """Reference: take the non-dominated points of the rest, one front at a time."""
    rest = list(range(len(points)))
    fronts = []
    while rest:
        front = [i for i in rest if not any(dominates(points[j], points[i]) for j in rest)]
        fronts.append(front)
        rest = [i for i in rest if i not in front]
    return fronts


def norm(fronts):
    return [sorted(f) for f in fronts]


EXAMPLE = [(1, 8), (2, 5), (3, 6), (4, 2), (5, 4), (6, 7), (7, 1), (8, 3)]


def test_example() -> None:
    want = [[0, 1, 3, 6], [2, 4, 7], [5]]
    assert norm(fast_non_dominated_sort(EXAMPLE)) == want
    assert non_dominated_sort_2d(EXAMPLE) == want
    assert ranks_from_fronts(want, 8) == [1, 1, 2, 1, 2, 3, 1, 2]


def test_edges() -> None:
    assert fast_non_dominated_sort([]) == []
    assert non_dominated_sort_2d([]) == []
    assert fast_non_dominated_sort([(3, 3)]) == [[0]]
    # equal points share a front
    assert norm(fast_non_dominated_sort([(1, 1), (1, 1), (2, 2)])) == [[0, 1], [2]]
    assert non_dominated_sort_2d([(1, 1), (1, 1), (2, 2)]) == [[0, 1], [2]]
    # a chain gives one point per front
    chain = [(k, k, k) for k in range(5, 0, -1)]
    assert fast_non_dominated_sort(chain) == [[4], [3], [2], [1], [0]]


def test_against_peeling() -> None:
    rng = random.Random(7)
    for _ in range(400):
        p = rng.randint(1, 4)
        n = rng.randint(0, 25)
        pts = [tuple(rng.randint(0, 5) for _ in range(p)) for _ in range(n)]
        want = norm(peel(pts))
        assert norm(fast_non_dominated_sort(pts)) == want
        if p == 2:
            assert non_dominated_sort_2d(pts) == want


def test_front_properties() -> None:
    rng = random.Random(11)
    for _ in range(200):
        pts = [tuple(rng.randint(0, 9) for _ in range(3)) for _ in range(20)]
        fronts = fast_non_dominated_sort(pts)
        rank = ranks_from_fronts(fronts, len(pts))
        assert sorted(i for f in fronts for i in f) == list(range(len(pts)))
        for f in fronts:
            for a in f:
                for b in f:
                    assert not dominates(pts[a], pts[b])
        for i in range(len(pts)):
            for j in range(len(pts)):
                if dominates(pts[i], pts[j]):
                    assert rank[i] < rank[j]
            if rank[i] > 1:
                assert any(rank[j] == rank[i] - 1 and dominates(pts[j], pts[i]) for j in range(len(pts)))
