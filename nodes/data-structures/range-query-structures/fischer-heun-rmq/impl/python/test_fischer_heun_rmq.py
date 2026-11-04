# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fischer-heun-rmq/. The authors are listed in prov/6H7AGY.jsonl.

import random

import pytest

from fischer_heun_rmq import FischerHeunRMQ


def leftmost_min(a: list[int], l: int, r: int) -> int:
    best = l
    for k in range(l + 1, r + 1):
        if a[k] < a[best]:
            best = k
    return best


def test_example() -> None:
    a = [4, 2, 5, 1, 6, 3]
    t = FischerHeunRMQ(a)
    t.check_invariant()
    assert t.bits() == "(((())())(()))"
    assert t.query(0, 2) == 1
    assert t.query(2, 5) == 3
    assert t.query(4, 5) == 5
    assert t.query(1, 2) == 1
    assert t.query(0, 5) == 3


def test_edges() -> None:
    t = FischerHeunRMQ([])
    t.check_invariant()
    assert t.bits() == "()"
    with pytest.raises(IndexError):
        t.query(0, 0)
    t = FischerHeunRMQ([9])
    assert t.query(0, 0) == 0
    t = FischerHeunRMQ([3, 3, 3])
    t.check_invariant()
    assert t.query(0, 2) == 0 and t.query(1, 2) == 1
    with pytest.raises(IndexError):
        t.query(2, 1)


def test_random() -> None:
    rng = random.Random(6)
    for _ in range(600):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 5) for _ in range(n)]
        t = FischerHeunRMQ(a)
        t.check_invariant()
        for _ in range(12):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            assert t.query(l, r) == leftmost_min(a, l, r)


def test_long() -> None:
    rng = random.Random(4)
    for a in ([rng.randint(0, 50) for _ in range(700)], list(range(400)), list(range(400, 0, -1))):
        t = FischerHeunRMQ(a)
        t.check_invariant()
        for _ in range(300):
            l = rng.randrange(len(a))
            r = rng.randrange(l, len(a))
            assert t.query(l, r) == leftmost_min(a, l, r)
