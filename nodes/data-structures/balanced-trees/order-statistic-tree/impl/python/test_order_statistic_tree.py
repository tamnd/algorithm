# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/order-statistic-tree/. The authors are listed in prov/S2AJN7.jsonl.

import bisect
import random

import pytest

from order_statistic_tree import Node, OrderStatisticTree


def sizes(h: "Node[str] | None") -> object:
    if h is None:
        return None
    return (sizes(h.left), (h.key, h.size), sizes(h.right))


def test_page_example() -> None:
    t: OrderStatisticTree[str] = OrderStatisticTree()
    for c in "SEARCHXMPL":
        assert t.insert(c)
        t.check_invariant()
    assert sizes(t.root) == (
        (((None, ("A", 1), None), ("C", 2), None), ("E", 5), ((None, ("H", 1), None), ("L", 2), None)),
        ("M", 10),
        ((None, ("P", 1), None), ("R", 4), ((None, ("S", 1), None), ("X", 2), None)),
    )
    assert t.select(6) == "P"
    assert t.rank("Q") == 7
    assert t.rank("L") == 4
    assert t.insert("D")
    t.check_invariant()
    assert t.root is not None and t.root.size == 11
    assert t.root.left is not None and t.root.left.size == 6
    assert t.root.left.left is not None and t.root.left.left.key == "C"
    assert t.root.left.left.size == 3
    assert [t.select(i) for i in range(11)] == sorted("SEARCHXMPLD")


def test_edge_cases() -> None:
    t: OrderStatisticTree[int] = OrderStatisticTree()
    assert len(t) == 0
    assert t.rank(5) == 0
    with pytest.raises(IndexError):
        t.select(0)
    assert t.insert(5)
    assert not t.insert(5)
    assert t.select(0) == 5
    assert t.rank(5) == 0
    assert t.rank(6) == 1
    assert t.rank(4) == 0
    with pytest.raises(IndexError):
        t.select(1)
    with pytest.raises(IndexError):
        t.select(-1)
    assert t.delete(5)
    assert not t.delete(5)
    assert len(t) == 0
    t.check_invariant()


def test_ranks_start_at_zero() -> None:
    # Pitfall: select(rank(k)) == k for a present key, with 0-based ranks.
    t: OrderStatisticTree[int] = OrderStatisticTree()
    for k in [30, 10, 20]:
        t.insert(k)
    assert t.select(0) == 10
    assert t.rank(10) == 0
    for k in [10, 20, 30]:
        assert t.select(t.rank(k)) == k


def test_sizes_after_rotations() -> None:
    # Pitfall: a rotation must recompute the lower node first.
    t: OrderStatisticTree[int] = OrderStatisticTree()
    for k in range(1000):
        t.insert(k)
    t.check_invariant()
    for k in range(0, 1000, 3):
        t.delete(k)
    t.check_invariant()
    rest = [k for k in range(1000) if k % 3]
    assert [t.select(i) for i in range(len(rest))] == rest


def test_random_against_sorted_list() -> None:
    rng = random.Random(1990)
    for _ in range(500):
        t: OrderStatisticTree[int] = OrderStatisticTree()
        s: list[int] = []
        for _ in range(rng.randrange(1, 70)):
            k = rng.randrange(50)
            j = bisect.bisect_left(s, k)
            present = j < len(s) and s[j] == k
            if rng.random() < 0.6:
                assert t.insert(k) == (not present)
                if not present:
                    s.insert(j, k)
            else:
                assert t.delete(k) == present
                if present:
                    del s[j]
            t.check_invariant()
            assert len(t) == len(s)
            q = rng.randrange(-1, 52)
            assert t.rank(q) == bisect.bisect_left(s, q)
            if s:
                i = rng.randrange(len(s))
                assert t.select(i) == s[i]
        assert list(t.keys()) == s
