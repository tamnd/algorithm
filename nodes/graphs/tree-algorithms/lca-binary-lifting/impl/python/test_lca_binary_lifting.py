# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lca-binary-lifting/. The authors are listed in prov/T1VPR2.jsonl.

import random

import pytest

from lca_binary_lifting import LcaBinaryLifting

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


def test_example() -> None:
    t = LcaBinaryLifting(12, tree_edges(PARENT), 0)
    assert t.K == 4
    assert t.up[1] == [0, 0, 0, 1, 2, 3, 1, 2, 0, 0, 2, 6]
    assert t.up[2] == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    assert t.lca(5, 11) == 2
    assert t.lca(10, 9) == 0
    assert t.lca(4, 10) == 3
    assert t.lca(7, 2) == 2
    assert t.lca(6, 6) == 6
    assert t.kth_ancestor(11, 5) == 0
    assert t.kth_ancestor(5, 3) == 2
    assert t.distance(5, 11) == 6


def test_single_vertex() -> None:
    t = LcaBinaryLifting(1, [], 0)
    assert t.lca(0, 0) == 0
    assert t.kth_ancestor(0, 0) == 0
    with pytest.raises(ValueError):
        t.kth_ancestor(0, 1)


def test_star() -> None:
    n = 50
    t = LcaBinaryLifting(n, [(0, i) for i in range(1, n)], 0)
    assert all(t.lca(i, j) == (i if i == j else 0) for i in range(1, n) for j in range(1, n))
    t2 = LcaBinaryLifting(n, [(0, i) for i in range(1, n)], 7)
    assert t2.lca(3, 9) == 0
    assert t2.lca(0, 9) == 0
    assert t2.lca(7, 9) == 7


def test_long_path() -> None:
    n = 100_000
    t = LcaBinaryLifting(n, [(i, i + 1) for i in range(n - 1)], 0)
    assert t.lca(n - 1, 12345) == 12345
    assert t.kth_ancestor(n - 1, n - 1) == 0
    assert t.distance(0, n - 1) == n - 1
    # n = 2^j + 1 needs a jump of 2^j
    m = 2**10 + 1
    s = LcaBinaryLifting(m, [(i, i + 1) for i in range(m - 1)], 0)
    assert s.kth_ancestor(m - 1, m - 1) == 0
    assert s.lca(m - 1, 1) == 1


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        LcaBinaryLifting(0, [], 0)
    with pytest.raises(ValueError):
        LcaBinaryLifting(4, [(0, 1), (2, 3), (0, 1)], 0)


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(1, 40)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        perm = list(range(n))
        rng.shuffle(perm)
        relabeled = [-1] * n
        for v in range(1, n):
            relabeled[perm[v]] = perm[parent[v]]
        root = perm[0]
        t = LcaBinaryLifting(n, tree_edges(relabeled), root)
        for _ in range(20):
            u, v = rng.randrange(n), rng.randrange(n)
            assert t.lca(u, v) == naive_lca(relabeled, u, v)
