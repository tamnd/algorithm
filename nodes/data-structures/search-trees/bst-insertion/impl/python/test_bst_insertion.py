# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-insertion/. The authors are listed in prov/82JNAM.jsonl.

import random

from bst_insertion import Node, Tree, depth, inorder, tree_insert


def check(t: Tree) -> None:
    """The BST property, the parent links and the count."""
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


def test_example() -> None:
    t: Tree[int, None] = Tree()
    keys = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]
    depths = [depth(tree_insert(t, k)) for k in keys]
    check(t)
    assert depths == [0, 1, 1, 2, 2, 2, 2, 3, 3, 3]
    assert sum(depths) == 19
    z = tree_insert(t, 42)
    assert z.p is not None and z.p.key == 45 and z is z.p.left and depth(z) == 4
    assert inorder(t) == sorted(keys + [42])


def test_duplicate_replaces_value() -> None:
    t: Tree[int, str] = Tree()
    a = tree_insert(t, 5, "a")
    b = tree_insert(t, 5, "b")
    assert a is b and t.n == 1 and a.value == "b"


def test_sorted_input_cost() -> None:
    t: Tree[int, None] = Tree()
    n = 2000
    total = sum(depth(tree_insert(t, k)) for k in range(n))
    assert total == n * (n - 1) // 2
    check(t)


def test_random_against_sorted() -> None:
    rng = random.Random(9031)
    for _ in range(500):
        t: Tree[int, int] = Tree()
        keys = [rng.randint(0, 50) for _ in range(rng.randint(0, 40))]
        for i, k in enumerate(keys):
            tree_insert(t, k, i)
        check(t)
        assert inorder(t) == sorted(set(keys))
        last = {k: i for i, k in enumerate(keys)}
        stack = [t.root] if t.root else []
        while stack:
            x: Node = stack.pop()
            assert x.value == last[x.key]
            stack += [c for c in (x.left, x.right) if c is not None]
