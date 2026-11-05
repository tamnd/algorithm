# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ladder-decomposition/. The authors are listed in prov/VJP1A9.jsonl.

import random

import pytest

from ladder_decomposition import LadderLevelAncestor

PARENT = [-1, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]


def tree_edges(parent: list[int]) -> list[tuple[int, int]]:
    return [(v, p) for v, p in enumerate(parent) if p >= 0]


def naive_la(parent: list[int], v: int, d: int) -> int | None:
    path = []
    while v != -1:
        path.append(v)
        v = parent[v]
    path.reverse()
    return path[d] if 0 <= d < len(path) else None


def test_page_example() -> None:
    t = LadderLevelAncestor(12, tree_edges(PARENT), 0)
    assert t.height == [6, 5, 4, 3, 2, 1, 3, 2, 2, 1, 1, 1]
    assert t.long_child == [1, 2, 3, 4, 5, -1, 7, 11, 9, -1, -1, -1]
    assert sorted(t.ladders) == sorted([[0, 1, 2, 3, 4, 5], [0, 8, 9], [0, 1, 2, 6, 7, 11], [3, 10]])
    assert t.level_ancestor(11, 2) == 2
    assert t.level_ancestor(10, 1) == 1
    assert t.level_ancestor(10, 3) == 3
    assert t.level_ancestor(10, 4) == 10
    assert t.level_ancestor(9, 0) == 0
    assert t.level_ancestor(9, 3) is None
    assert t.level_ancestor(5, -1) is None
    assert t.kth_ancestor(11, 4) == 1
    assert t.kth_ancestor(11, 6) is None


def test_single_vertex() -> None:
    t = LadderLevelAncestor(1, [], 0)
    assert t.ladders == [[0]]
    assert t.level_ancestor(0, 0) == 0
    assert t.level_ancestor(0, 1) is None


def test_star() -> None:
    n = 9
    t = LadderLevelAncestor(n, [(0, i) for i in range(1, n)], 0)
    assert len(t.ladders) == n - 1
    for v in range(1, n):
        assert t.level_ancestor(v, 0) == 0
        assert t.level_ancestor(v, 1) == v
    t = LadderLevelAncestor(n, [(0, i) for i in range(1, n)], 4)
    assert t.level_ancestor(7, 0) == 4
    assert t.level_ancestor(7, 1) == 0


def test_long_path() -> None:
    n = 100_000
    t = LadderLevelAncestor(n, [(i, i + 1) for i in range(n - 1)], 0)
    assert len(t.ladders) == 1
    rng = random.Random(3)
    for _ in range(5000):
        v = rng.randrange(n)
        d = rng.randrange(v + 1)
        assert t.level_ancestor(v, d) == d
    t = LadderLevelAncestor(n, [(i, i + 1) for i in range(n - 1)], n - 1)
    assert t.level_ancestor(0, 0) == n - 1
    assert t.level_ancestor(0, 10) == n - 11


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        LadderLevelAncestor(0, [], 0)
    with pytest.raises(ValueError):
        LadderLevelAncestor(3, [(0, 1)], 0)
    with pytest.raises(ValueError):
        LadderLevelAncestor(4, [(0, 1), (1, 0), (2, 3)], 0)
    t = LadderLevelAncestor(2, [(0, 1)], 0)
    with pytest.raises(IndexError):
        t.level_ancestor(2, 0)


def test_random_against_naive() -> None:
    rng = random.Random(17)
    for _ in range(600):
        n = rng.randint(1, 60)
        perm = list(range(n))
        rng.shuffle(perm)
        parent = [-1] * n
        for i in range(1, n):
            parent[perm[i]] = perm[rng.randrange(max(0, i - 3) if rng.random() < 0.5 else 0, i)]
        root = perm[0]
        t = LadderLevelAncestor(n, tree_edges(parent), root)
        assert sum(len(x) for x in t.ladders) <= 2 * n
        for _ in range(40):
            v = rng.randrange(n)
            d = rng.randint(-1, n)
            assert t.level_ancestor(v, d) == naive_la(parent, v, d)
