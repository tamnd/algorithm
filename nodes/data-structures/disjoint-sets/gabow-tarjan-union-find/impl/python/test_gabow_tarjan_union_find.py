# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-tarjan-union-find/. The authors are listed in prov/1DC4F6.jsonl.

import random

import pytest

from gabow_tarjan_union_find import GabowTarjanUnionFind


def naive_find(parent: list[int], marked: list[bool], v: int) -> int:
    while marked[v]:
        v = parent[v]
    return v


def test_example() -> None:
    parent = [-1, 0, 0, 1, 1, 2, 5, 5]
    g = GabowTarjanUnionFind(parent, b=4)
    assert sorted(map(sorted, g.members)) == [[0], [1, 2, 5], [3, 4], [6, 7]]
    ops = [("f", 6, 6), ("l", 6, 0), ("f", 6, 5), ("l", 5, 0), ("f", 7, 7), ("f", 6, 2),
           ("l", 3, 0), ("l", 1, 0), ("f", 3, 0), ("f", 4, 4), ("l", 2, 0), ("f", 6, 0)]
    for op, v, want in ops:
        if op == "l":
            g.link(v)
        else:
            assert g.find(v) == want
        g.check_invariant()


def test_edges() -> None:
    g = GabowTarjanUnionFind([-1])
    assert g.find(0) == 0
    with pytest.raises(ValueError):
        g.link(0)
    with pytest.raises(ValueError):
        GabowTarjanUnionFind([-1, -1])
    GabowTarjanUnionFind([]).check_invariant()


def test_long_path() -> None:
    n = 100000
    parent = [i + 1 for i in range(n)]
    parent[-1] = -1
    g = GabowTarjanUnionFind(parent)
    g.check_invariant()
    for v in range(n - 1):
        g.link(v)
        if v % 997 == 0:
            assert g.find(0) == v + 1
    assert g.find(0) == n - 1


def test_random_against_marks() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n = rng.randrange(1, 40)
        parent = [-1] + [rng.randrange(v) for v in range(1, n)]
        g = GabowTarjanUnionFind(parent, b=rng.choice([None, 1, 2, 3, 5, 8]))
        g.check_invariant()
        marked = [False] * n
        free = list(range(1, n))
        rng.shuffle(free)
        for _ in range(3 * n):
            if free and rng.random() < 0.4:
                v = free.pop()
                g.link(v)
                marked[v] = True
            else:
                v = rng.randrange(n)
                assert g.find(v) == naive_find(parent, marked, v)
        g.check_invariant()
