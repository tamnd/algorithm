# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leftist-heap/. The authors are listed in prov/Z662CN.jsonl.

import heapq
import random

import pytest

from leftist_heap import LeftistHeap, Node, merge


def sh(v: "Node[int] | None") -> str:
    """The tree as key(left, right), as written on the page."""
    if v is None:
        return "-"
    if v.left is None and v.right is None:
        return str(v.key)
    return f"{v.key}({sh(v.left)}, {sh(v.right)})"


def test_example_inserts() -> None:
    h: LeftistHeap[int] = LeftistHeap()
    seen = []
    for k in [5, 3, 8, 1, 7, 2]:
        h.insert(k)
        h.check_invariant()
        seen.append(sh(h.root))
    assert seen == ["5", "3(5, -)", "3(5, 8)", "1(3(5, 8), -)", "1(3(5, 8), 7)", "1(3(5, 8), 2(7, -))"]
    assert h.delete_min() == 1
    assert sh(h.root) == "2(3(5, 8), 7)"
    assert h.delete_min() == 2
    assert sh(h.root) == "3(5, 7(8, -))"
    h.check_invariant()


def test_example_meld() -> None:
    x: LeftistHeap[int] = LeftistHeap()
    for k in [1, 3, 8, 5, 7, 2]:
        x.insert(k)
    y: LeftistHeap[int] = LeftistHeap()
    for k in [4, 6, 9, 10]:
        y.insert(k)
    assert sh(x.root) == "1(5(8, 7), 2(3, -))"
    assert sh(y.root) == "4(6, 9(10, -))"
    x.meld(y)
    x.check_invariant()
    assert sh(x.root) == "1(5(8, 7), 2(4(6, 9(10, -)), 3))"
    assert x.root is not None and x.root.s == 3
    assert len(x) == 10 and len(y) == 0 and y.is_empty()


def test_empty() -> None:
    h: LeftistHeap[int] = LeftistHeap()
    h.check_invariant()
    assert h.is_empty() and len(h) == 0
    assert merge(None, None) is None
    with pytest.raises(IndexError):
        h.delete_min()
    with pytest.raises(IndexError):
        h.find_min()


def test_duplicates_and_sorted_inputs() -> None:
    for data in ([2] * 50, list(range(200)), list(range(200, 0, -1))):
        h = LeftistHeap(data)
        h.check_invariant()
        out = [h.delete_min() for _ in range(len(data))]
        assert out == sorted(data)


def test_increasing_inserts_keep_spine_short() -> None:
    h: LeftistHeap[int] = LeftistHeap()
    for k in range(10000):
        h.insert(k)
    h.check_invariant()
    assert h.root is not None and h.root.s <= 13


def test_random_against_heapq() -> None:
    rng = random.Random(20240611)
    for _ in range(600):
        heaps = [LeftistHeap[int]() for _ in range(3)]
        refs: list[list[int]] = [[] for _ in range(3)]
        for _ in range(rng.randrange(1, 60)):
            i = rng.randrange(3)
            op = rng.random()
            if op < 0.55:
                k = rng.randrange(-20, 20)
                heaps[i].insert(k)
                heapq.heappush(refs[i], k)
            elif op < 0.85:
                if refs[i]:
                    assert heaps[i].find_min() == refs[i][0]
                    assert heaps[i].delete_min() == heapq.heappop(refs[i])
            else:
                j = rng.randrange(3)
                if i != j:
                    heaps[i].meld(heaps[j])
                    refs[i] = refs[i] + refs[j]
                    heapq.heapify(refs[i])
                    refs[j] = []
            heaps[i].check_invariant()
            assert sorted(heaps[i].keys()) == sorted(refs[i])
