# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threaded-binary-tree/. The authors are listed in prov/EJENNS.jsonl.

import random

from threaded_binary_tree import ThreadedBinarySearchTree


def test_example() -> None:
    t: ThreadedBinarySearchTree[int] = ThreadedBinarySearchTree()
    for k in [50, 30, 70, 20, 40, 60, 80]:
        assert t.insert(k)
        t.check_invariant()
    th = t.threads()
    assert th[20] == (None, 30) and th[40] == (30, 50)
    assert th[60] == (50, 70) and th[80] == (70, None)
    assert th[50] == ("-", "-")
    assert t.insert(45)
    t.check_invariant()
    th = t.threads()
    assert th[45] == (40, 50) and th[40] == (30, "-")
    assert list(t) == [20, 30, 40, 45, 50, 60, 70, 80]
    assert t.successor(45) == 50 and t.successor(30) == 40
    assert t.predecessor(60) == 50 and t.successor(80) is None


def test_edges() -> None:
    t: ThreadedBinarySearchTree[int] = ThreadedBinarySearchTree()
    assert list(t) == [] and t.search(1) is None
    assert t.insert(1) and not t.insert(1)
    assert list(t) == [1] and len(t) == 1
    assert t.successor(1) is None and t.predecessor(1) is None


def test_chain() -> None:
    t: ThreadedBinarySearchTree[int] = ThreadedBinarySearchTree()
    for k in range(2000, 0, -1):
        t.insert(k)
    t.check_invariant()
    assert list(t) == list(range(1, 2001))


def test_random_against_sorted() -> None:
    rng = random.Random(1960)
    for _ in range(500):
        t: ThreadedBinarySearchTree[int] = ThreadedBinarySearchTree()
        s: set[int] = set()
        for _ in range(rng.randint(0, 40)):
            k = rng.randint(0, 60)
            assert t.insert(k) == (k not in s)
            s.add(k)
        t.check_invariant()
        ks = sorted(s)
        assert list(t) == ks
        for i, k in enumerate(ks):
            assert t.successor(k) == (ks[i + 1] if i + 1 < len(ks) else None)
            assert t.predecessor(k) == (ks[i - 1] if i else None)
        for q in range(-1, 62):
            assert (t.search(q) is not None) == (q in s)
