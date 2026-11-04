# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-deletion/. The authors are listed in prov/RSMQKE.jsonl.

import random

from bst_deletion import Tree, inorder, tree_delete


def check(t: Tree) -> None:
    count, stack = 0, []
    if t.root is not None:
        assert t.root.p is None
        stack.append((t.root, None, None))
    while stack:
        x, lo, hi = stack.pop()
        count += 1
        assert (lo is None or lo < x.key) and (hi is None or x.key < hi)
        for c, a, b in ((x.left, lo, x.key), (x.right, x.key, hi)):
            if c is not None:
                assert c.p is x
                stack.append((c, a, b))
    assert count == t.n


def shape(x) -> object:
    return None if x is None else (x.key, shape(x.left), shape(x.right))


def test_example() -> None:
    t: Tree[int, int] = Tree()
    for k in [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]:
        t.insert(k, k)
    assert tree_delete(t, 60)
    check(t)
    assert shape(t.root.right) == (70, (65, None, None), (80, None, None))
    assert tree_delete(t, 30)
    check(t)
    assert shape(t.root.left) == (35, (20, None, None), (40, None, (45, None, None)))
    assert tree_delete(t, 20)
    check(t)
    assert tree_delete(t, 50)
    check(t)
    assert t.root.key == 65 and t.root.value == 65
    assert shape(t.root) == (65, (35, None, (40, None, (45, None, None))), (70, None, (80, None, None)))
    assert not tree_delete(t, 50)
    assert inorder(t) == [35, 40, 45, 65, 70, 80]


def test_edges() -> None:
    t: Tree[int, None] = Tree()
    assert not tree_delete(t, 1)
    t.insert(1)
    assert tree_delete(t, 1) and t.root is None and t.n == 0
    for k in (2, 1, 3):
        t.insert(k)
    assert tree_delete(t, 2)
    check(t)
    assert t.root.key == 3 and t.root.left.key == 1


def test_chain() -> None:
    t: Tree[int, None] = Tree()
    for k in range(3000):
        t.insert(k)
    for k in range(0, 3000, 3):
        assert tree_delete(t, k)
    check(t)
    assert inorder(t) == [k for k in range(3000) if k % 3]


def test_random_against_model() -> None:
    rng = random.Random(6620)
    for _ in range(500):
        t: Tree[int, int] = Tree()
        model: dict[int, int] = {}
        for step in range(rng.randint(0, 50)):
            k = rng.randint(0, 25)
            if rng.random() < 0.55:
                t.insert(k, step)
                model[k] = step
            else:
                assert tree_delete(t, k) == (k in model)
                model.pop(k, None)
            check(t)
        assert inorder(t) == sorted(model)
        stack = [t.root] if t.root else []
        while stack:
            x = stack.pop()
            assert x.value == model[x.key]
            stack += [c for c in (x.left, x.right) if c is not None]
