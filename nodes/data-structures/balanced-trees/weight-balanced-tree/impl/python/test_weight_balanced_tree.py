# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-balanced-tree/. The authors are listed in prov/0YHN5A.jsonl.

import math
import random

from weight_balanced_tree import WeightBalancedTree, balance, insert


def shape(t):
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


def test_page_example_sorted():
    w = WeightBalancedTree()
    for k in [1, 2, 3]:
        w.insert(k)
    assert shape(w.root) == (None, 1, (None, 2, 3))  # weights 1 and 3 are allowed
    w.insert(4)  # weights 1 and 4: single left rotation at 1
    assert shape(w.root) == (1, 2, (None, 3, 4))
    for k in [5, 6, 7]:
        w.insert(k)
    assert shape(w.root) == (1, 2, (3, 4, (None, 5, (None, 6, 7))))
    w.insert(8)  # weights 2 and 7 at the root 2: single left rotation
    assert shape(w.root) == ((1, 2, 3), 4, (5, 6, (None, 7, 8)))
    w.check_invariant()


def test_page_example_double_rotation():
    w = WeightBalancedTree()
    for k in [1, 4, 2]:
        w.insert(k)
    assert shape(w.root) == (None, 1, (2, 4, None))
    w.insert(3)  # at 1: weights 1 and 4, inner weight 3 is not < 2 * 1
    assert shape(w.root) == (1, 2, (3, 4, None))
    w.check_invariant()


def test_page_example_delete():
    w = WeightBalancedTree()
    for k in range(1, 11):
        w.insert(k)
    w.delete(1)
    assert shape(w.root) == ((None, 2, 3), 4, (5, 6, (7, 8, (None, 9, 10))))
    w.delete(2)  # at 4: weights 2 and 7, single left rotation
    assert shape(w.root) == ((3, 4, 5), 6, (7, 8, (None, 9, 10)))
    w.check_invariant()


def test_persistence_and_edges():
    w = WeightBalancedTree()
    assert not w.delete(3) and w.height() == -1 and w.rank(5) == 0
    assert w.insert(3) and not w.insert(3)
    old = w.root
    w.insert(9)
    assert shape(old) == 3 and shape(w.root) == (None, 3, 9)
    assert w.delete(3) and w.delete(9) and len(w) == 0
    assert shape(balance(None, 1, None)) == 1
    assert shape(insert(None, 5)) == 5


def test_height_bound():
    for keys in (list(range(5000)), list(range(5000, 0, -1))):
        w = WeightBalancedTree()
        for k in keys:
            w.insert(k)
        w.check_invariant()
        n = len(w)
        assert w.height() <= math.log((n + 1) / 2, 4 / 3)


def test_random_against_set():
    rng = random.Random(1972)
    for case in range(600):
        w = WeightBalancedTree()
        ref = set()
        for _ in range(rng.randint(0, 90)):
            k = rng.randint(0, 50)
            if rng.random() < 0.6:
                assert w.insert(k) == (k not in ref)
                ref.add(k)
            else:
                assert w.delete(k) == (k in ref)
                ref.discard(k)
            w.check_invariant()
        s = sorted(ref)
        assert w.keys() == s and len(w) == len(s)
        for i, k in enumerate(s):
            assert w.select(i) == k and w.rank(k) == i
        for k in range(-1, 52):
            assert (k in w) == (k in ref)
            assert w.rank(k) == sum(1 for x in s if x < k)
