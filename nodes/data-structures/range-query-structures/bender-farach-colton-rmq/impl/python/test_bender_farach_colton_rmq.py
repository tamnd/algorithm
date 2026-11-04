# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bender-farach-colton-rmq/. The authors are listed in prov/WNYTAQ.jsonl.

import random

import pytest

from bender_farach_colton_rmq import BenderFarachColtonRMQ


def leftmost_min(a: list[int], l: int, r: int) -> int:
    best = l
    for k in range(l + 1, r + 1):
        if a[k] < a[best]:
            best = k
    return best


def test_example() -> None:
    a = [4, 2, 5, 1, 6, 3]
    t = BenderFarachColtonRMQ(a, block=3)
    t.check_invariant()
    assert t.euler == [3, 1, 0, 1, 2, 1, 3, 5, 4, 5, 3]
    assert t.depth == [0, 1, 2, 1, 2, 1, 0, 1, 2, 1, 0]
    assert t.first == [2, 1, 4, 0, 8, 7]
    assert t.block_min == [0, 3, 6, 10]
    assert t.block_shape[0] == t.block_shape[2]
    assert len(t.tables) == 3
    assert t.query(0, 2) == 1
    assert t.query(2, 5) == 3
    assert t.query(4, 5) == 5
    assert t.query(0, 5) == 3
    assert t.query(4, 4) == 4


def test_edges() -> None:
    t = BenderFarachColtonRMQ([])
    t.check_invariant()
    with pytest.raises(IndexError):
        t.query(0, 0)
    t = BenderFarachColtonRMQ([7])
    t.check_invariant()
    assert t.query(0, 0) == 0
    t = BenderFarachColtonRMQ([2, 2, 2, 2])
    t.check_invariant()
    assert t.query(1, 3) == 1
    t = BenderFarachColtonRMQ(list(range(20, 0, -1)))
    assert t.query(0, 19) == 19
    with pytest.raises(IndexError):
        t.query(3, 2)


def test_random() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n = rng.randint(1, 40)
        a = [rng.randint(0, 6) for _ in range(n)]
        block = rng.choice([0, 0, 1, 2, 3, 5])
        t = BenderFarachColtonRMQ(a, block=block)
        t.check_invariant()
        for _ in range(10):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            assert t.query(l, r) == leftmost_min(a, l, r)


def test_large_default_block() -> None:
    rng = random.Random(3)
    a = [rng.randint(0, 10**6) for _ in range(3000)]
    t = BenderFarachColtonRMQ(a)
    t.check_invariant()
    assert t.b == (len(t.depth).bit_length() - 1) // 2
    for _ in range(500):
        l = rng.randrange(3000)
        r = rng.randrange(l, 3000)
        assert t.query(l, r) == leftmost_min(a, l, r)
