# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buffer-tree/. The authors are listed in prov/5H2XC9.jsonl.

import math
import random

import pytest

from buffer_tree import BufferTree, Leaf, Node


def shape(x: "Node[int] | Leaf[int]") -> str:
    if isinstance(x, Leaf):
        return "[" + " ".join(map(str, x.keys)) + "]"
    inner = " ".join(shape(c) for c in x.children)
    return "<" + " ".join(map(str, x.routing)) + "|" + str(len(x.buf)) + ">(" + inner + ")"


def test_example() -> None:
    t: BufferTree[int] = BufferTree(block_size=2, fanout=4)
    assert t.M == 8
    for k in [50, 20, 80, 10, 60, 30, 70, 40]:
        t.insert(k)
    # eight operations wait in the root buffer, nothing has reached a leaf
    assert shape(t.root) == "<|8>([])"
    q = t.query(30)
    # the ninth operation overflows the buffer: the root applies all nine
    assert shape(t.root) == "<30 50 70|0>([10 20] [30 40] [50 60] [70 80])"
    assert t.answers == {q: True}
    for k in [90, 15, 25]:
        t.insert(k)
    t.delete(30)
    q2 = t.query(30)
    q3 = t.query(25)
    assert q2 not in t.answers
    t.check_invariant()
    answers = t.flush()
    assert answers[q2] is False and answers[q3] is True
    assert t.keys() == [10, 15, 20, 25, 40, 50, 60, 70, 80, 90]
    assert shape(t.root) == "<60|0>(<20 40|0>([10 15] [20 25] [40 50]) <80|0>([60 70] [80 90]))"
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        BufferTree(1, 3)
    t: BufferTree[int] = BufferTree(1, 4)
    q = t.query(5)
    t.delete(5)
    assert t.flush() == {q: False}
    assert t.keys() == []
    t.insert(5)
    t.insert(5)
    assert t.keys() == [5]
    t.check_invariant()


def run_oracle(ops: list[tuple[int, int]]) -> tuple[dict[int, bool], list[int]]:
    s: set[int] = set()
    ans: dict[int, bool] = {}
    q = 0
    for kind, k in ops:
        if kind == 0:
            s.add(k)
        elif kind == 1:
            s.discard(k)
        else:
            ans[q] = k in s
            q += 1
    return ans, sorted(s)


def test_against_set() -> None:
    rng = random.Random(3)
    for _ in range(500):
        B = rng.randrange(1, 4)
        m = rng.randrange(4, 7)
        t: BufferTree[int] = BufferTree(B, m)
        ops = [(rng.choice((0, 0, 1, 2)), rng.randrange(80)) for _ in range(rng.randrange(1, 250))]
        for i, (kind, k) in enumerate(ops):
            if kind == 0:
                t.insert(k)
            elif kind == 1:
                t.delete(k)
            else:
                t.query(k)
            if i % 37 == 0:
                t.check_invariant()
        want_ans, want_keys = run_oracle(ops)
        assert t.flush() == want_ans
        t.check_invariant()
        assert t.keys() == want_keys


def test_io_bound() -> None:
    B, m = 16, 8
    t: BufferTree[int] = BufferTree(B, m)
    rng = random.Random(9)
    N = 40000
    for k in rng.sample(range(10 * N), N):
        t.insert(k)
    t.flush()
    t.check_invariant()
    n = N / B
    bound = n * math.log(n, m)
    assert t.ios <= 6 * bound
    # fewer than one I/O per insert; a B-tree makes one read per level
    assert t.ios < N
