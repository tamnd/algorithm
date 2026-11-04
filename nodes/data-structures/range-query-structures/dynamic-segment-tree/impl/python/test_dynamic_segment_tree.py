# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-segment-tree/. The authors are listed in prov/6P1XHV.jsonl.

import random

import pytest

from dynamic_segment_tree import DynamicSegmentTree


def test_example() -> None:
    t = DynamicSegmentTree(16)
    assert t.node_count() == 1
    t.update(3, 5)
    assert t.node_count() == 5
    t.update(10, 2)
    assert t.node_count() == 9
    t.update(11, 4)
    assert t.node_count() == 10
    assert t.val[1] == 11
    assert t.query(2, 12) == 11
    assert t.query(0, 8) == 5
    assert t.query(4, 10) == 0
    assert t.node_count() == 10
    t.check_invariant()


def test_edges() -> None:
    t = DynamicSegmentTree(1)
    assert t.query(0, 1) == 0
    t.update(0, -3)
    assert t.query(0, 1) == -3 and t.query(0, 0) == 0 and t.query(1, 1) == 0
    assert t.node_count() == 1
    with pytest.raises(IndexError):
        t.update(1, 1)
    with pytest.raises(IndexError):
        t.query(1, 0)
    with pytest.raises(ValueError):
        DynamicSegmentTree(0)
    big = DynamicSegmentTree(10**18)
    big.update(10**18 - 1, 7)
    big.update(0, 1)
    assert big.query(0, 10**18) == 8
    assert big.query(1, 10**18 - 1) == 0
    assert big.node_count() <= 1 + 2 * 60
    big.check_invariant()


def test_random_against_brute_force() -> None:
    rng = random.Random(31337)
    for _ in range(500):
        u = rng.randint(1, 70)
        t = DynamicSegmentTree(u)
        a = [0] * u
        m = 0
        for _ in range(rng.randint(0, 40)):
            if rng.random() < 0.5:
                i = rng.randrange(u)
                x = rng.randint(-9, 9)
                t.update(i, x)
                a[i] += x
                m += 1
            else:
                l = rng.randint(0, u)
                r = rng.randint(l, u)
                assert t.query(l, r) == sum(a[l:r])
        bound = 1 + m * max(0, (u - 1).bit_length())
        assert t.node_count() <= min(bound, 2 * u - 1)
        t.check_invariant()
