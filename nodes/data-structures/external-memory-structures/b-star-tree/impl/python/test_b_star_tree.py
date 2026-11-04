# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-star-tree/. The authors are listed in prov/FES1ZP.jsonl.

import math
import random

import pytest

from b_star_tree import BStarTree, Node


def shape(x: Node[int]) -> str:
    if x.leaf:
        return "[" + " ".join(map(str, x.keys)) + "]"
    return "<" + " ".join(map(str, x.keys)) + ">(" + " ".join(shape(c) for c in x.children) + ")"


def test_example() -> None:
    t: BStarTree[int] = BStarTree(4)
    assert (t.C, t.f, t.R) == (4, 3, 5)
    want_ins = {
        50: "[10 20 30 40 50]",
        60: "<40>([10 20 30] [40 50 60])",
        25: "<30>([10 15 20 25] [30 40 50 60])",
        35: "<25 40>([10 15 20] [25 30 35] [40 50 60])",
        55: "<25 45>([10 15 20] [25 30 35 40] [45 50 55 60])",
        65: "<25 40 55>([10 15 20] [25 30 35] [40 45 50] [55 60 65])",
        70: "<25 40 55>([10 15 20] [25 30 35] [40 45 50] [55 60 65 70])",
    }
    for k in [10, 20, 30, 40, 50, 60, 15, 25, 35, 45, 55, 65, 70]:
        assert t.insert(k)
        t.check_invariant()
        if k in want_ins:
            assert shape(t.root) == want_ins[k]
    assert t.range(33, 57) == [35, 40, 45, 50, 55]
    want_del = [
        (70, "<25 40 55>([10 15 20] [25 30 35] [40 45 50] [55 60 65])"),
        (65, "<25 45>([10 15 20] [25 30 35 40] [45 50 55 60])"),
        (10, "<30 45>([15 20 25] [30 35 40] [45 50 55 60])"),
        (20, "<35 50>([15 25 30] [35 40 45] [50 55 60])"),
        (15, "<45>([25 30 35 40] [45 50 55 60])"),
        (50, "<45>([25 30 35 40] [45 55 60])"),
        (55, "<40>([25 30 35] [40 45 60])"),
        (25, "[30 35 40 45 60]"),
    ]
    for k, s in want_del:
        assert t.delete(k)
        t.check_invariant()
        assert shape(t.root) == s


def test_edges() -> None:
    with pytest.raises(ValueError):
        BStarTree(3)
    t: BStarTree[int] = BStarTree(4)
    assert not t.search(1) and not t.delete(1)
    assert t.range(0, 9) == []
    assert t.insert(1) and not t.insert(1)
    assert t.delete(1) and t.keys() == []
    t.check_invariant()


def test_fill_and_height() -> None:
    for C in (4, 7, 30):
        t: BStarTree[int] = BStarTree(C)
        n = 3000
        for k in range(n):
            t.insert(k)
        t.check_invariant()
        h = t.height()
        # every non-root node has at least f entries, the root at least 2
        assert h <= 1 + math.log(n / (2 * t.f), t.f) + 1e-9
        assert t.keys() == list(range(n))


def test_against_set() -> None:
    rng = random.Random(41)
    for _ in range(600):
        C = rng.randrange(4, 9)
        t: BStarTree[int] = BStarTree(C)
        model: set[int] = set()
        for _ in range(rng.randrange(1, 120)):
            k = rng.randrange(60)
            op = rng.randrange(5)
            if op <= 1:
                assert t.insert(k) == (k not in model)
                model.add(k)
            elif op <= 3:
                assert t.delete(k) == (k in model)
                model.discard(k)
            else:
                a, b = sorted((rng.randrange(60), rng.randrange(60)))
                assert t.search(a) == (a in model)
                assert t.range(a, b) == [x for x in sorted(model) if a <= x <= b]
            t.check_invariant()
            assert t.keys() == sorted(model)
