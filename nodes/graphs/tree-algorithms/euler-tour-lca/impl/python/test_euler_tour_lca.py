# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-tour-lca/. The authors are listed in prov/SKXZFC.jsonl.

import random

import pytest

from euler_tour_lca import EulerTourLca

PARENT = [-1, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]


def tree_edges(parent: list[int]) -> list[tuple[int, int]]:
    return [(v, p) for v, p in enumerate(parent) if p >= 0]


def naive_lca(parent: list[int], u: int, v: int) -> int:
    seen = set()
    while u != -1:
        seen.add(u)
        u = parent[u]
    while v not in seen:
        v = parent[v]
    return v


def test_page_example() -> None:
    t = EulerTourLca(12, tree_edges(PARENT), 0)
    assert t.euler == [0, 1, 2, 3, 4, 5, 4, 3, 10, 3, 2, 6, 7, 11, 7, 6, 2, 1, 0, 8, 9, 8, 0]
    assert t.first == [0, 1, 2, 3, 4, 5, 11, 12, 19, 20, 8, 13]
    assert t.lca(5, 11) == 2
    assert t.lca(11, 5) == 2
    assert t.lca(9, 10) == 0
    assert t.lca(4, 10) == 3
    assert t.lca(5, 4) == 4
    assert t.lca(7, 7) == 7
    assert t.distance(5, 11) == 6


def test_single_vertex() -> None:
    t = EulerTourLca(1, [], 0)
    assert t.euler == [0]
    assert t.lca(0, 0) == 0


def test_star() -> None:
    n = 6
    t = EulerTourLca(n, [(0, i) for i in range(1, n)], 0)
    assert t.euler == [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0]
    for a in range(1, n):
        for b in range(1, n):
            assert t.lca(a, b) == (a if a == b else 0)
    # rooted at a leaf
    t = EulerTourLca(n, [(0, i) for i in range(1, n)], 3)
    assert t.lca(1, 2) == 0
    assert t.lca(1, 3) == 3


def test_long_path() -> None:
    n = 100_000
    t = EulerTourLca(n, [(i, i + 1) for i in range(n - 1)], 0)
    assert len(t.euler) == 2 * n - 1
    rng = random.Random(1)
    for _ in range(2000):
        u, v = rng.randrange(n), rng.randrange(n)
        assert t.lca(u, v) == min(u, v)
    # the same path rooted in the middle
    t = EulerTourLca(n, [(i, i + 1) for i in range(n - 1)], n // 2)
    assert t.lca(0, n - 1) == n // 2
    assert t.lca(10, 20) == 20


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        EulerTourLca(0, [], 0)
    with pytest.raises(ValueError):
        EulerTourLca(3, [(0, 1)], 0)
    with pytest.raises(ValueError):
        EulerTourLca(4, [(0, 1), (1, 0), (2, 3)], 0)
    t = EulerTourLca(2, [(0, 1)], 0)
    with pytest.raises(IndexError):
        t.lca(0, 2)


def test_random_against_naive() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(1, 40)
        perm = list(range(n))
        rng.shuffle(perm)
        parent = [-1] * n
        for i in range(1, n):
            parent[perm[i]] = perm[rng.randrange(i)]
        root = perm[0]
        t = EulerTourLca(n, tree_edges(parent), root)
        assert len(t.euler) == 2 * n - 1
        for _ in range(30):
            u, v = rng.randrange(n), rng.randrange(n)
            assert t.lca(u, v) == naive_lca(parent, u, v)
