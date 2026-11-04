# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavl-tree/. The authors are listed in prov/9VPK2S.jsonl.

import math
import random

from wavl_tree import WAVLTree, rank


def shape(t):
    if t is None:
        return None
    label = f"{t.key}:{t.rank}"
    if t.left is None and t.right is None:
        return label
    return (shape(t.left), label, shape(t.right))


def heights_equal_ranks(t):
    if t is None:
        return -1
    hl, hr = heights_equal_ranks(t.left), heights_equal_ranks(t.right)
    h = 1 + max(hl, hr)
    assert h == t.rank and abs(hl - hr) <= 1
    return h


def test_page_example_insert():
    w = WAVLTree()
    w.insert(1)
    w.insert(2)
    assert shape(w.root) == (None, "1:1", "2:0")
    w.insert(3)  # 1 is a 0,2 node: single rotation
    assert shape(w.root) == ("1:0", "2:1", "3:0") and w.rotations == 1
    w.insert(4)  # promote 3, then promote 2
    assert shape(w.root) == ("1:0", "2:2", (None, "3:1", "4:0"))
    for k in [5, 6, 7]:
        w.insert(k)
    assert shape(w.root) == (("1:0", "2:1", "3:0"), "4:2", ("5:0", "6:1", "7:0"))
    w.check_invariant()


def test_page_example_delete():
    w = WAVLTree()
    for k in [1, 2, 3, 4]:
        w.insert(k)
    r = w.rotations
    w.delete(1)  # nil under 2 has rank difference 3: single rotation at 3
    assert shape(w.root) == ("2:0", "3:2", "4:0")  # 3 is a 2,2 node: not AVL
    assert w.rotations == r + 1 and w.height() == 1 and w.root.rank == 2
    w.check_invariant()


def test_insert_only_is_avl():
    rng = random.Random(2015)
    for _ in range(50):
        w = WAVLTree()
        for k in rng.sample(range(1000), 200):
            w.insert(k)
        heights_equal_ranks(w.root)
    w = WAVLTree()
    for k in range(4000):
        w.insert(k)
    heights_equal_ranks(w.root)
    assert w.height() <= 1.4405 * math.log2(len(w) + 2)


def test_edges_and_height_with_deletions():
    w = WAVLTree()
    assert not w.delete(1) and w.height() == -1 and rank(None) == -1
    assert w.insert(1) and not w.insert(1) and w.delete(1) and w.root is None
    rng = random.Random(9)
    for k in range(3000):
        w.insert(k)
    for k in rng.sample(range(3000), 2500):
        w.delete(k)
    w.check_invariant()
    assert w.root.rank <= 2 * math.log2(len(w) + 1)


def test_random_against_set_and_rotation_bound():
    rng = random.Random(2009)
    for case in range(700):
        w = WAVLTree()
        ref = set()
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(0, 40)
            before = w.rotations
            if rng.random() < 0.55:
                assert w.insert(k) == (k not in ref)
                ref.add(k)
            else:
                assert w.delete(k) == (k in ref)
                ref.discard(k)
            assert w.rotations - before <= 2
            w.check_invariant()
        assert w.keys() == sorted(ref)
        for k in range(-1, 42):
            assert (k in w) == (k in ref)
