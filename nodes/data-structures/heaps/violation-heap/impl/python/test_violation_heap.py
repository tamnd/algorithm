# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/violation-heap/. The authors are listed in prov/HWWSW6.jsonl.

import heapq
import math
import random
from typing import Dict, List

import pytest

from violation_heap import Node, ViolationHeap, formula_rank


def show(x: Node[int]) -> str:
    """Write a tree as key:rank(children, oldest first)."""
    kids: List[Node[int]] = []
    c = x.last
    while c is not None:
        kids.append(c)
        c = c.left
    kids.reverse()
    s = f"{x.key}:{x.rank}"
    return s if not kids else s + "(" + ", ".join(show(k) for k in kids) + ")"


def dump(h: ViolationHeap[int]) -> str:
    return "  ".join(show(r) for r in h.roots)


def test_page_example() -> None:
    h: ViolationHeap[int] = ViolationHeap()
    nd = {k: h.insert(k) for k in range(10, 110, 10)}
    assert h.delete_min() == 10 and h.joins == 4
    assert dump(h) == "20:2(40:0, 30:0, 80:1(100:0, 90:0), 50:1(70:0, 60:0))"
    steps = []
    for old, new in [(90, 5), (50, 45), (40, 35), (50, 15), (100, 8)]:
        h.rank_steps = 0
        h.decrease_key(nd[old], new)
        h.check_invariant()
        steps.append(h.rank_steps)
    assert steps == [0, 0, 0, 0, 2]
    assert dump(h) == "20:1(30:0, 80:0, 60:0)  5:0  35:0  15:1(70:0)  8:0"
    h.joins = 0
    assert h.delete_min() == 5 and h.joins == 0
    assert dump(h) == "20:1(30:0, 80:0, 60:0)  15:1(70:0)  35:0  8:0"
    h.check_invariant()


def test_formula() -> None:
    z: Node[int] = Node(0)
    assert formula_rank(z) == 0
    h: ViolationHeap[int] = ViolationHeap()
    for k in range(4):
        h.insert(k)
    h.delete_min()
    (r,) = h.roots
    assert r.key == 1 and r.rank == 1 and formula_rank(r) == 1


def test_empty_and_single() -> None:
    h: ViolationHeap[int] = ViolationHeap()
    with pytest.raises(IndexError):
        h.delete_min()
    with pytest.raises(IndexError):
        h.find_min()
    x = h.insert(7)
    with pytest.raises(ValueError):
        h.decrease_key(x, 8)
    h.decrease_key(x, 3)
    assert h.find_min() == 3 and h.delete_min() == 3 and len(h) == 0
    h.check_invariant()


def test_duplicates_and_meld() -> None:
    a: ViolationHeap[int] = ViolationHeap()
    b: ViolationHeap[int] = ViolationHeap()
    for k in [5, 5, 1, 5]:
        a.insert(k)
    for k in [1, 2, 5]:
        b.insert(k)
    a.meld(b)
    assert len(b) == 0 and len(a) == 7
    assert [a.delete_min() for _ in range(7)] == [1, 1, 2, 5, 5, 5, 5]


def test_rank_bound_after_many_joins() -> None:
    h: ViolationHeap[int] = ViolationHeap()
    for k in range(3**6 + 1):
        h.insert(k)
    h.delete_min()
    (r,) = h.roots
    assert r.rank == 6
    h.check_invariant()


def test_random_against_heapq() -> None:
    rng = random.Random(20100627)
    for case in range(600):
        h: ViolationHeap[int] = ViolationHeap()
        ref: List[tuple[int, int]] = []
        handles: Dict[int, Node[int]] = {}
        keys: Dict[int, int] = {}
        nxt = 0
        cost = 0
        budget = 0.0
        for _ in range(rng.randint(1, 120)):
            op = rng.random()
            if op < 0.4 or not keys:
                k = rng.randint(0, 60)
                handles[nxt] = h.insert(k)
                keys[nxt] = k
                heapq.heappush(ref, (k, nxt))
                nxt += 1
                budget += 1
            elif op < 0.75:
                i = rng.choice(list(keys))
                k = keys[i] - rng.randint(0, 20)
                h.rank_steps = 0
                h.decrease_key(handles[i], k)
                cost += h.rank_steps
                keys[i] = k
                heapq.heappush(ref, (k, i))
                budget += 1
            else:
                while ref[0][0] != keys.get(ref[0][1]):
                    heapq.heappop(ref)
                m = h.find_min()
                assert m == ref[0][0]
                n_before = len(h)
                h.joins = 0
                assert h.delete_min() == m
                cost += h.joins + len(h.roots)
                budget += math.log2(n_before) + 1
                for i, v in list(keys.items()):
                    if v == m and handles[i].right is None and handles[i] not in h.roots:
                        del keys[i]
                        break
            if case % 20 == 0:
                h.check_invariant()
        h.check_invariant()
        assert len(h) == len(keys)
        assert cost <= 8 * budget
        out = []
        while len(h):
            out.append(h.delete_min())
        assert out == sorted(keys.values())
