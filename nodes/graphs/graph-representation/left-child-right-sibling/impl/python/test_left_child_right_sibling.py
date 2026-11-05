# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-child-right-sibling/. The authors are listed in prov/NWHW83.jsonl.

import random

from left_child_right_sibling import NIL, LCRSTree, from_parent_array

# A=0, B=1, C=2, D=3, E=4, F=5, G=6
PARENT = [-1, 0, 0, 0, 1, 1, 3]


def test_example() -> None:
    t = from_parent_array(PARENT)
    assert t.child == [1, 4, NIL, 6, NIL, NIL, NIL]
    assert t.sibling == [NIL, 2, 3, NIL, 5, NIL, NIL]
    assert list(t.children(0)) == [1, 2, 3]
    assert t.preorder() == [0, 1, 4, 5, 2, 3, 6]
    assert t.postorder() == [4, 5, 1, 2, 6, 3, 0]
    assert t.preorder(1) == [1, 4, 5]
    assert t.depth(6) == 2


def test_add_child_prepends() -> None:
    t = LCRSTree()
    a = t.add_child(0)
    b = t.add_child(0)
    c = t.add_child(a)
    assert list(t.children(0)) == [b, a]
    assert list(t.children(a)) == [c]
    assert t.preorder() == [0, b, a, c]
    assert t.degree(0) == 2 and t.degree(c) == 0


def naive_preorder(kids: list[list[int]], r: int) -> list[int]:
    out = [r]
    for c in kids[r]:
        out += naive_preorder(kids, c)
    return out


def naive_postorder(kids: list[list[int]], r: int) -> list[int]:
    out: list[int] = []
    for c in kids[r]:
        out += naive_postorder(kids, c)
    return out + [r]


def test_random_trees() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randrange(1, 40)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        kids: list[list[int]] = [[] for _ in range(n)]
        for x in range(1, n):
            kids[parent[x]].append(x)
        t = from_parent_array(parent)
        for v in range(n):
            assert list(t.children(v)) == kids[v]
            assert t.preorder(v) == naive_preorder(kids, v)
            assert t.postorder(v) == naive_postorder(kids, v)
        assert sum(t.degree(v) for v in range(n)) == n - 1
