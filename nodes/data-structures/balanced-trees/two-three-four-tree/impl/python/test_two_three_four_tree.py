# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-three-four-tree/. The authors are listed in prov/0AZZFQ.jsonl.

import math
import random

from two_three_four_tree import Node, TwoThreeFourTree


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if not t.kids:
        return t.keys
    return [t.keys] + [shape(c) for c in t.kids]


def test_page_example() -> None:
    t: TwoThreeFourTree[int] = TwoThreeFourTree()
    steps = {
        80: [20, 50, 80],
        10: [[50], [10, 20], [80]],
        40: [[20, 50], [10], [30, 40], [60, 80, 90]],
        70: [[20, 50, 80], [10], [30, 40], [60, 70], [90]],
        25: [[50], [[20], [10], [25, 30, 40]], [[80], [60, 70], [90]]],
    }
    for k in [50, 20, 80, 10, 30, 60, 90, 40, 70, 25]:
        assert t.insert(k)
        t.check_invariant()
        if k in steps:
            assert shape(t.root) == steps[k]
    assert t.height() == 3
    deletes = {
        10: [[25, 50, 80], [20], [30, 40], [60, 70], [90]],
        50: [[25, 40, 80], [20], [30], [60, 70], [90]],
        90: [[25, 40, 70], [20], [30], [60], [80]],
        20: [[40, 70], [25, 30], [60], [80]],
        40: [[30, 70], [25], [60], [80]],
    }
    for k, want in deletes.items():
        assert t.delete(k)
        t.check_invariant()
        assert shape(t.root) == want
    assert t.height() == 2
    assert list(t.keys()) == [25, 30, 60, 70, 80]


def test_edge_cases() -> None:
    t: TwoThreeFourTree[int] = TwoThreeFourTree()
    assert not t.contains(1)
    assert not t.delete(1)
    assert t.height() == 0
    t.check_invariant()
    assert t.insert(1)
    assert not t.insert(1)
    assert len(t) == 1
    assert t.contains(1)
    assert t.delete(1)
    assert t.root is None
    assert len(t) == 0
    t.check_invariant()


def test_absent_key_reshapes_but_keeps_keys() -> None:
    # Pitfall: the top-down passes split and merge before they know whether
    # the key is there. The tree may change shape, but stays valid.
    t: TwoThreeFourTree[int] = TwoThreeFourTree()
    for k in [1, 2, 3]:
        t.insert(k)
    assert not t.insert(2)
    assert shape(t.root) == [[2], [1], [3]]
    t.check_invariant()
    assert not t.delete(5)
    assert shape(t.root) == [1, 2, 3]
    t.check_invariant()
    assert list(t.keys()) == [1, 2, 3]


def test_sorted_input_height() -> None:
    t: TwoThreeFourTree[int] = TwoThreeFourTree()
    n = 4000
    for k in range(n):
        t.insert(k)
    t.check_invariant()
    assert t.height() <= math.floor(math.log2(n + 1)) + 1
    for k in range(0, n, 2):
        assert t.delete(k)
    t.check_invariant()
    assert list(t.keys()) == list(range(1, n, 2))


def test_random_against_set() -> None:
    rng = random.Random(1972)
    for _ in range(600):
        t: TwoThreeFourTree[int] = TwoThreeFourTree()
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
        assert len(t) == len(s)
        if s:
            assert t.height() <= math.log2(len(s) + 1) + 1e-9
