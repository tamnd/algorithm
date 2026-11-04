# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-epsilon-tree/. The authors are listed in prov/NA7JW5.jsonl.

import math
import random

import pytest

from b_epsilon_tree import BEpsilonTree, Inner, Leaf


def shape(x: "Inner[int, str] | Leaf[int, str]") -> str:
    if isinstance(x, Leaf):
        return "[" + " ".join(map(str, x.keys)) + "]"
    buf = " ".join(("+" if m[0] == 0 else "-") + str(k) for k, m in sorted(x.buf.items()))
    inner = " ".join(shape(c) for c in x.children)
    return "<" + " ".join(map(str, x.pivots)) + "|" + buf + ">(" + inner + ")"


def test_example() -> None:
    t: BEpsilonTree[int, str] = BEpsilonTree(block_size=4, fanout=3)
    for k in [10, 20, 30, 40, 50]:
        t.put(k, str(k))
    assert shape(t.root) == "<30|>([10 20] [30 40 50])"
    for k in [60, 70, 80, 90]:
        t.put(k, str(k))
    assert shape(t.root) == "<30|+60 +70 +80 +90>([10 20] [30 40 50])"
    t.put(15, "15")
    assert shape(t.root) == "<30 60|+15>([10 20] [30 40 50] [60 70 80 90])"
    for k in [25, 35, 45]:
        t.put(k, str(k))
    t.delete(20)
    assert shape(t.root) == "<30 60|+35 +45>([10 15 25] [30 40 50] [60 70 80 90])"
    t.put(55, "55")
    t.delete(70)
    assert shape(t.root) == "<30 60|+35 +45 +55 -70>([10 15 25] [30 40 50] [60 70 80 90])"
    # the answers come from the buffers, before the messages reach a leaf
    assert t.get(20) is None and t.get(70) is None
    assert t.get(45) == "45" and t.get(80) == "80"
    t.put(5, "5")
    assert shape(t.root) == (
        "<45|>(<30|+5>([10 15 25] [30 35 40]) <60|-70>([45 50 55] [60 70 80 90]))"
    )
    t.check_invariant()
    assert [k for k, _ in t.items()] == [5, 10, 15, 25, 30, 35, 40, 45, 50, 55, 60, 80, 90]


def test_edges() -> None:
    with pytest.raises(ValueError):
        BEpsilonTree(4, 2)
    t: BEpsilonTree[int, int] = BEpsilonTree(2, 3)
    assert t.get(1) is None and 1 not in t and len(t) == 0
    t.delete(1)
    t.put(1, 1)
    t.put(1, 2)
    assert t.get(1) == 2 and len(t) == 1
    t.delete(1)
    assert 1 not in t
    t.check_invariant()


def test_against_dict() -> None:
    rng = random.Random(7)
    for _ in range(500):
        t: BEpsilonTree[int, int] = BEpsilonTree(rng.randrange(2, 7), rng.randrange(3, 6))
        d: dict[int, int] = {}
        for i in range(rng.randrange(1, 300)):
            k = rng.randrange(120)
            r = rng.random()
            if r < 0.25:
                t.delete(k)
                d.pop(k, None)
            elif r < 0.7:
                t.put(k, i)
                d[k] = i
            else:
                assert t.get(k) == d.get(k)
            if i % 31 == 0:
                t.check_invariant()
        t.check_invariant()
        assert t.items() == sorted(d.items())


def test_io_bound() -> None:
    B, F = 64, 8  # F = B^(1/2)
    t: BEpsilonTree[int, int] = BEpsilonTree(B, F)
    rng = random.Random(1)
    N = 20000
    for k in rng.sample(range(10 * N), N):
        t.put(k, k)
    upd = t.ios
    h = t.height()
    # an update pays about F/B per level, far below one I/O
    assert upd < N * (h * 4 * F / B)
    assert upd < N / 2
    t.ios = 0
    for k in rng.sample(range(10 * N), 1000):
        t.get(k)
    assert t.ios <= 1000 * h
    assert h <= 2 + math.log(N, F / 2)
