# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-tree/. The authors are listed in prov/KEZ9RE.jsonl.

import math
import random

import pytest

from b_tree import BTree, Node


def shape(x: Node[int]) -> str:
    if x.leaf:
        return "[" + " ".join(map(str, x.keys)) + "]"
    return "[" + " ".join(map(str, x.keys)) + "](" + " ".join(shape(c) for c in x.children) + ")"


def test_example() -> None:
    t: BTree[int] = BTree(2)
    for k in [8, 3, 12, 5, 1, 9, 15, 7, 4, 10]:
        assert t.insert(k)
        t.check_invariant()
    assert shape(t.root) == "[3 8 12]([1] [4 5 7] [9 10] [15])"
    want = {
        12: "[3 8 10]([1] [4 5 7] [9] [15])",
        3: "[4 8 10]([1] [5 7] [9] [15])",
        8: "[4 7 10]([1] [5] [9] [15])",
        9: "[4 7]([1] [5] [10 15])",
        4: "[7]([1 5] [10 15])",
        7: "[5]([1] [10 15])",
    }
    for k, s in want.items():
        assert t.delete(k)
        t.check_invariant()
        assert shape(t.root) == s


def test_edges() -> None:
    with pytest.raises(ValueError):
        BTree(1)
    t: BTree[int] = BTree(3)
    assert not t.search(1)
    assert not t.delete(1)
    assert t.insert(1)
    assert not t.insert(1)
    assert t.keys() == [1]
    assert t.delete(1)
    assert t.keys() == []
    t.check_invariant()
    assert t.height() == 0


def test_height_bound_and_io() -> None:
    for tt in [2, 3, 5, 16]:
        t: BTree[int] = BTree(tt)
        n = 3000
        for k in range(n):
            t.insert(k)
        t.check_invariant()
        h = t.height()
        assert h <= math.log((n + 1) / 2, tt) + 1e-9
        r0 = t.reads
        assert t.search(n - 1)
        assert t.reads - r0 == h


def test_against_set() -> None:
    rng = random.Random(18)
    for _ in range(500):
        tt = rng.randrange(2, 5)
        t: BTree[int] = BTree(tt)
        model: set[int] = set()
        for _ in range(rng.randrange(1, 60)):
            k = rng.randrange(40)
            op = rng.randrange(3)
            if op == 0:
                assert t.insert(k) == (k not in model)
                model.add(k)
            elif op == 1:
                assert t.delete(k) == (k in model)
                model.discard(k)
            else:
                assert t.search(k) == (k in model)
            t.check_invariant()
            assert t.keys() == sorted(model)
