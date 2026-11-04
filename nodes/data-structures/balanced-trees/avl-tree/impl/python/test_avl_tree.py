# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/avl-tree/. The authors are listed in prov/195NAP.jsonl.

import math
import random

from avl_tree import AVLTree, Node


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


def test_page_example() -> None:
    a: AVLTree[int] = AVLTree()
    for k in [10, 20, 30, 40, 50, 25]:
        a.insert(k)
        a.check_invariant()
    assert shape(a.root) == ((10, 20, 25), 30, (None, 40, 50))
    a.delete(40)
    a.check_invariant()
    assert shape(a.root) == ((10, 20, 25), 30, 50)
    a.delete(50)
    a.check_invariant()
    assert shape(a.root) == (10, 20, (25, 30, None))


def test_sorted_input_is_perfect() -> None:
    a: AVLTree[int] = AVLTree()
    for k in range(1, 8):
        a.insert(k)
    assert shape(a.root) == ((1, 2, 3), 4, (5, 6, 7))
    for k in range(8, 1024):
        a.insert(k)
    a.check_invariant()
    assert a.height() == 10


def test_child_with_zero_balance_after_delete() -> None:
    a: AVLTree[int] = AVLTree()
    for k in [1, 7, 2, 6, 3, 5, 8, 4]:
        a.insert(k)
    assert shape(a.root) == ((1, 2, None), 3, ((4, 5, None), 6, (None, 7, 8)))
    a.delete(1)
    a.check_invariant()
    assert shape(a.root) == ((2, 3, (4, 5, None)), 6, (None, 7, 8))


def test_edges() -> None:
    a: AVLTree[int] = AVLTree()
    assert not a.delete(1) and not a.contains(1) and a.height() == 0
    assert a.insert(5) and not a.insert(5)
    assert len(a) == 1 and a.keys() == [5]
    assert a.delete(5) and len(a) == 0 and a.root is None
    for k in [3, 3, 3]:
        a.insert(k)
    assert a.keys() == [3]


def test_height_bound() -> None:
    rng = random.Random(4)
    a: AVLTree[int] = AVLTree()
    for _ in range(3000):
        a.insert(rng.randint(0, 10**6))
        n = len(a)
        assert a.height() < 1.4405 * math.log2(n + 2) - 0.3277


def test_random_against_set() -> None:
    rng = random.Random(1962)
    for _ in range(500):
        a: AVLTree[int] = AVLTree()
        model: set[int] = set()
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(0, 40)
            if rng.random() < 0.6:
                assert a.insert(k) == (k not in model)
                model.add(k)
            else:
                assert a.delete(k) == (k in model)
                model.discard(k)
            assert a.contains(k) == (k in model)
        a.check_invariant()
        assert a.keys() == sorted(model)
