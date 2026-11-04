# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-union-find/. The authors are listed in prov/YNSV90.jsonl.

import random

import pytest

from blum_union_find import BlumUnionFind


def test_example() -> None:
    u = BlumUnionFind(9, k=3)
    for x, y in [(0, 1), (2, 3), (0, 2), (4, 5), (6, 4), (7, 8), (0, 4), (7, 0)]:
        assert u.union(x, y)
        u.check_invariant()
    a = u.parent[0]
    assert sorted(u.children[a]) == [0, 1, 2, 3, 7, 8]
    assert sorted(u.children[u.parent[4]]) == [4, 5, 6]
    assert u.height[u._root(0)] == 2
    assert len({u.find(x) for x in range(9)}) == 1
    assert not u.union(3, 6)


def test_edges() -> None:
    u = BlumUnionFind(0)
    assert u.count == 0
    u = BlumUnionFind(1)
    assert u.find(0) == 0
    with pytest.raises(IndexError):
        u.find(1)
    with pytest.raises(ValueError):
        BlumUnionFind(3, k=1)


def test_height_bound() -> None:
    n = 1 << 14
    u = BlumUnionFind(n)
    for x in range(1, n):
        u.union(x, x - 1)
    u.check_invariant()
    h = u.height[u._root(0)]
    assert u.k ** (h - 1) * 2 <= n


def test_random_against_labels() -> None:
    rng = random.Random(99)
    for _ in range(500):
        n = rng.randrange(1, 40)
        u = BlumUnionFind(n, k=rng.choice([None, 2, 3, 4]))
        label = list(range(n))
        for _ in range(2 * n):
            x, y = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.6:
                assert u.union(x, y) == (label[x] != label[y])
                old = label[x]
                label = [label[y] if v == old else v for v in label]
            else:
                assert u.connected(x, y) == (label[x] == label[y])
                assert (u.find(x) == u.find(y)) == (label[x] == label[y])
        u.check_invariant()
