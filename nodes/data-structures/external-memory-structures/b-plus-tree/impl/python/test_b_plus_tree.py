# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-plus-tree/. The authors are listed in prov/M7WT2F.jsonl.

import math
import random

import pytest

from b_plus_tree import BPlusTree, Node


def shape(x: Node[int]) -> str:
    if x.leaf:
        return "[" + " ".join(map(str, x.keys)) + "]"
    return "<" + " ".join(map(str, x.keys)) + ">(" + " ".join(shape(c) for c in x.children) + ")"


def test_example() -> None:
    t: BPlusTree[int] = BPlusTree(2)
    for k in [20, 5, 40, 10, 30, 15, 25, 35, 45, 50, 12]:
        assert t.insert(k)
        t.check_invariant()
    assert shape(t.root) == "<20 30 40>([5 10 12 15] [20 25] [30 35] [40 45 50])"
    assert t.range(12, 35) == [12, 15, 20, 25, 30, 35]
    want = [
        (40, "<20 30 40>([5 10 12 15] [20 25] [30 35] [45 50])"),
        (45, "<20 30>([5 10 12 15] [20 25] [30 35 50])"),
        (50, "<20 30>([5 10 12 15] [20 25] [30 35])"),
        (5, "<20 30>([10 12 15] [20 25] [30 35])"),
        (25, "<15 30>([10 12] [15 20] [30 35])"),
        (12, "<30>([10 15 20] [30 35])"),
        (30, "<20>([10 15] [20 35])"),
    ]
    for k, s in want:
        assert t.delete(k)
        t.check_invariant()
        assert shape(t.root) == s


def test_edges() -> None:
    with pytest.raises(ValueError):
        BPlusTree(0)
    t: BPlusTree[int] = BPlusTree(1)
    assert not t.search(3)
    assert t.range(0, 10) == []
    assert not t.delete(3)
    assert t.insert(3) and not t.insert(3)
    assert t.range(3, 3) == [3]
    assert t.range(4, 2) == []
    assert t.delete(3)
    assert t.keys() == []
    t.check_invariant()


def test_height_and_range_cost() -> None:
    d = 8
    t: BPlusTree[int] = BPlusTree(d)
    n = 5000
    for k in range(n):
        t.insert(k)
    t.check_invariant()
    h = t.height()
    # a leaf has at least d keys, an internal node other than the root at least d + 1 children
    assert h <= 1 + math.log(n / (2 * d), d + 1) + 1e-9
    r0 = t.reads
    got = t.range(1000, 1999)
    assert got == list(range(1000, 2000))
    assert t.reads - r0 <= h + math.ceil(1000 / d) + 1


def test_against_set() -> None:
    rng = random.Random(27)
    for _ in range(500):
        d = rng.randrange(1, 4)
        t: BPlusTree[int] = BPlusTree(d)
        model: set[int] = set()
        for _ in range(rng.randrange(1, 60)):
            k = rng.randrange(40)
            op = rng.randrange(4)
            if op == 0:
                assert t.insert(k) == (k not in model)
                model.add(k)
            elif op == 1:
                assert t.delete(k) == (k in model)
                model.discard(k)
            elif op == 2:
                assert t.search(k) == (k in model)
            else:
                a, b = sorted((rng.randrange(40), rng.randrange(40)))
                assert t.range(a, b) == [x for x in sorted(model) if a <= x <= b]
            t.check_invariant()
            assert t.keys() == sorted(model)
