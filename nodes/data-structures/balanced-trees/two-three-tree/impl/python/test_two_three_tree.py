# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-three-tree/. The authors are listed in prov/3W4BM4.jsonl.

import math
import random

from two_three_tree import Node, TwoThreeTree


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if not t.kids:
        return t.keys
    return [t.keys] + [shape(c) for c in t.kids]


def test_page_example() -> None:
    t: TwoThreeTree[int] = TwoThreeTree()
    steps = {
        80: [[50], [20], [80]],
        30: [[20, 50], [10], [30], [80]],
        90: [[50], [[20], [10], [30]], [[80], [60], [90]]],
        25: [[50], [[20, 30], [10], [25], [40]], [[80], [60, 70], [90]]],
    }
    for k in [50, 20, 80, 10, 30, 60, 90, 40, 70, 25]:
        assert t.insert(k)
        t.check_invariant()
        if k in steps:
            assert shape(t.root) == steps[k]
    assert t.height() == 3
    deletes = {
        10: [[50], [[30], [20, 25], [40]], [[80], [60, 70], [90]]],
        50: [[60], [[30], [20, 25], [40]], [[80], [70], [90]]],
        90: [[30, 60], [20, 25], [40], [70, 80]],
        20: [[30, 60], [25], [40], [70, 80]],
        40: [[30, 70], [25], [60], [80]],
    }
    for k, want in deletes.items():
        assert t.delete(k)
        t.check_invariant()
        assert shape(t.root) == want
    assert t.height() == 2
    assert list(t.keys()) == [25, 30, 60, 70, 80]


def test_edge_cases() -> None:
    t: TwoThreeTree[int] = TwoThreeTree()
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


def test_duplicate_does_not_split() -> None:
    # inserting a key already in a full leaf must not split it
    t: TwoThreeTree[int] = TwoThreeTree()
    t.insert(1)
    t.insert(2)
    assert not t.insert(2)
    assert shape(t.root) == [1, 2]


def test_sorted_input_and_height() -> None:
    t: TwoThreeTree[int] = TwoThreeTree()
    n = 2000
    for k in range(n):
        t.insert(k)
        if k % 97 == 0:
            t.check_invariant()
    t.check_invariant()
    # height between log3(n + 1) and lg(n + 1)
    h = t.height()
    assert math.log(n + 1, 3) <= h <= math.log2(n + 1)
    for k in range(0, n, 2):
        assert t.delete(k)
    t.check_invariant()
    assert list(t.keys()) == list(range(1, n, 2))


def test_random_against_set() -> None:
    rng = random.Random(1970)
    for _ in range(600):
        t: TwoThreeTree[int] = TwoThreeTree()
        model: set[int] = set()
        for _ in range(rng.randrange(1, 60)):
            k = rng.randrange(40)
            if rng.random() < 0.6:
                assert t.insert(k) == (k not in model)
                model.add(k)
            else:
                assert t.delete(k) == (k in model)
                model.discard(k)
            t.check_invariant()
            assert len(t) == len(model)
        assert list(t.keys()) == sorted(model)
        for k in range(40):
            assert t.contains(k) == (k in model)
        if model:
            assert t.height() <= math.log2(len(model) + 1)
