# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parent-pointer-tree/. The authors are listed in prov/87C07Z.jsonl.

import random

import pytest

from parent_pointer_tree import NIL, ParentPointerTree, from_bfs, is_forest

PARENT = [NIL, 3, 0, 0, 3, 2, 4]


def test_example() -> None:
    t = ParentPointerTree(PARENT)
    assert list(t.path_to_root(6)) == [6, 4, 3, 0]
    assert t.depth(6) == 3
    assert t.depth(0) == 0
    assert t.root_of(5) == 0
    off, kids = t.child_lists()
    assert off == [0, 2, 2, 3, 5, 6, 6, 6]
    assert kids == [2, 3, 5, 1, 4, 6]
    assert t.children(3) == [1, 4]
    assert t.lca(1, 6) == 3
    assert t.lca(5, 6) == 0
    assert t.lca(4, 6) == 4


def test_add_child() -> None:
    t = ParentPointerTree()
    a = t.add_child(0)
    b = t.add_child(0)
    c = t.add_child(a)
    assert (a, b, c) == (1, 2, 3)
    assert t.parent == [NIL, 0, 0, 1]
    assert t.children(0) == [1, 2]
    with pytest.raises(IndexError):
        t.add_child(9)


def test_is_forest() -> None:
    assert is_forest([NIL])
    assert is_forest([NIL, NIL, 0])
    assert not is_forest([1, 0])
    assert not is_forest([0])
    assert not is_forest([NIL, 5])
    assert not is_forest([NIL, 2, 3, 1])
    with pytest.raises(ValueError):
        ParentPointerTree([1, 2, 0])


def test_forest_lca() -> None:
    t = ParentPointerTree([NIL, 0, NIL, 2])
    assert t.lca(1, 3) == NIL
    assert t.root_of(3) == 2


def test_bfs_tree() -> None:
    adj = [[1, 2], [0, 2, 3], [0, 1], [1]]
    assert from_bfs(adj, 0) == [NIL, 0, 0, 1]


def test_random() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 40)
        t = ParentPointerTree()
        for _ in range(n - 1):
            t.add_child(rng.randrange(t.size()))
        off, kids = t.child_lists()
        assert off[-1] == n - 1
        for v in range(n):
            assert kids[off[v]:off[v + 1]] == t.children(v)
        for x in range(n):
            path = list(t.path_to_root(x))
            assert path[-1] == 0 and len(path) == t.depth(x) + 1
            for a, b in zip(path, path[1:]):
                assert t.parent[a] == b
        u, v = rng.randrange(n), rng.randrange(n)
        w = t.lca(u, v)
        assert w in set(t.path_to_root(u)) & set(t.path_to_root(v))
        assert all(c not in set(t.path_to_root(v)) for c in t.children(w)
                   if c in set(t.path_to_root(u)))
