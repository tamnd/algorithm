# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aa-tree/. The authors are listed in prov/TPBFGF.jsonl.

import math
import random

from aa_tree import AATree, Node, skew, split


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if t.left is None and t.right is None:
        return f"{t.key}:{t.level}"
    return (shape(t.left), f"{t.key}:{t.level}", shape(t.right))


def test_page_example() -> None:
    t: AATree[int] = AATree()
    steps = {
        2: (None, "1:1", "2:1"),
        3: ("1:1", "2:2", "3:1"),
        5: ("1:1", "2:2", ("3:1", "4:2", "5:1")),
        7: (("1:1", "2:2", "3:1"), "4:3", ("5:1", "6:2", "7:1")),
    }
    for k in range(1, 8):
        assert t.insert(k)
        t.check_invariant()
        if k in steps:
            assert shape(t.root) == steps[k]
    assert t.delete(1)
    t.check_invariant()
    assert shape(t.root) == ((None, "2:1", "3:1"), "4:2", ("5:1", "6:2", "7:1"))
    assert t.delete(4)
    t.check_invariant()
    assert shape(t.root) == ("2:1", "3:2", ("5:1", "6:2", "7:1"))
    assert list(t.keys()) == [2, 3, 5, 6, 7]


def test_skew_and_split() -> None:
    a, b = Node(1), Node(2)
    b.left = a  # horizontal left link: 1 and 2 both at level 1
    r = skew(b)
    assert r is a and a.right is b and b.left is None
    c = Node(3)
    b.right = c  # now 1 -> 2 -> 3 all at level 1
    r2 = split(a)
    assert r2 is b and b.level == 2 and b.left is a and b.right is c


def test_edge_cases() -> None:
    t: AATree[int] = AATree()
    assert not t.contains(1)
    assert not t.delete(1)
    t.check_invariant()
    assert t.insert(1)
    assert not t.insert(1)
    assert len(t) == 1
    assert t.delete(1)
    assert t.root is None
    t.check_invariant()


def test_delete_needs_all_three_skews() -> None:
    # Pitfall: the deletion fix-up must skew t, t.right and t.right.right.
    # Deleting 7 lowers the root and its right child 18 to level 1; then
    # 13 and 15 are horizontal left links at two places on the right spine.
    t: AATree[int] = AATree()
    for k in [18, 15, 19, 7, 3, 13]:
        t.insert(k)
    assert shape(t.root) == ("3:1", "7:2", ((None, "13:1", "15:1"), "18:2", "19:1"))
    assert t.delete(7)
    t.check_invariant()
    assert shape(t.root) == ("3:1", "13:2", ("15:1", "18:2", "19:1"))


def test_sorted_input_height() -> None:
    t: AATree[int] = AATree()
    n = 2000
    for k in range(n):
        t.insert(k)
    t.check_invariant()
    assert t.height() <= 2 * math.log2(n + 1)
    for k in range(n - 1, -1, -2):
        assert t.delete(k)
    t.check_invariant()
    assert list(t.keys()) == list(range(0, n, 2))


def test_random_against_set() -> None:
    rng = random.Random(1993)
    for _ in range(600):
        t: AATree[int] = AATree()
        s: set[int] = set()
        for _ in range(rng.randrange(1, 80)):
            k = rng.randrange(60)
            if rng.random() < 0.55:
                assert t.insert(k) == (k not in s)
                s.add(k)
            else:
                assert t.delete(k) == (k in s)
                s.discard(k)
            t.check_invariant()
            assert t.contains(k) == (k in s)
        assert list(t.keys()) == sorted(s)
        if s:
            assert t.height() <= 2 * math.log2(len(s) + 1)
