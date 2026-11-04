# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sqrt-tree/. The authors are listed in prov/RBM9RY.jsonl.

import math
import operator
import random

import pytest

from sqrt_tree import SqrtTree

A = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 2, 5, 1, 8, 3, 7]


def test_example() -> None:
    t = SqrtTree(A, operator.add)
    assert t.ks == [4, 2] and t.bs == [2, 1]
    assert t.layer_of == [-1, 1, 0, 0]
    assert t.suf[0][1] == 11 and t.pre[0][14] == 12
    assert t.btw[0][(1, 2)] == 36
    assert t.query(1, 14) == 59
    assert t.query(2, 7) == 32
    assert t.query(5, 6) == 10
    assert t.query(8, 9) == 6
    assert t.query(0, 15) == 71
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(IndexError):
        SqrtTree([], operator.add).query(0, 0)
    one = SqrtTree([4], operator.add)
    assert one.query(0, 0) == 4
    one.check_invariant()
    two = SqrtTree([4, 5], operator.add)
    assert two.query(0, 1) == 9
    with pytest.raises(IndexError):
        two.query(1, 0)


def test_counts_combines() -> None:
    calls = [0]

    def op(x: int, y: int) -> int:
        calls[0] += 1
        return x + y

    t = SqrtTree(list(range(300)), op)
    for l in range(0, 300, 7):
        for r in range(l, 300, 11):
            calls[0] = 0
            assert t.query(l, r) == sum(range(l, r + 1))
            assert calls[0] <= 2


def test_random_against_brute_force() -> None:
    rng = random.Random(7)
    ops = [(operator.add, 0), (min, None), (math.gcd, None)]
    cases = 0
    for _ in range(60):
        n = rng.randint(1, 140)
        vals = [rng.randint(-50, 50) for _ in range(n)]
        op, _ = rng.choice(ops)
        t = SqrtTree(vals, op)
        t.check_invariant()
        for _ in range(12):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            want = vals[l]
            for x in vals[l + 1 : r + 1]:
                want = op(want, x)
            assert t.query(l, r) == want
            cases += 1
    for _ in range(30):
        n = rng.randint(1, 90)
        words = [rng.choice("abc") for _ in range(n)]
        t = SqrtTree(words, operator.add)  # string concatenation is not commutative
        t.check_invariant()
        for _ in range(10):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            assert t.query(l, r) == "".join(words[l : r + 1])
            cases += 1
    assert cases >= 500
