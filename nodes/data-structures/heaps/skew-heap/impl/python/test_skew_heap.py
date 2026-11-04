# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skew-heap/. The authors are listed in prov/PY5NQC.jsonl.

import heapq
import random

import pytest

from skew_heap import Node, SkewHeap, merge


def sh(v: "Node[int] | None") -> str:
    """The tree as key(left, right), as written on the page."""
    if v is None:
        return "-"
    if v.left is None and v.right is None:
        return str(v.key)
    return f"{v.key}({sh(v.left)}, {sh(v.right)})"


def test_example_inserts() -> None:
    h: SkewHeap[int] = SkewHeap()
    seen = []
    for k in [5, 3, 8, 1, 7, 2]:
        h.insert(k)
        h.check_invariant()
        seen.append(sh(h.root))
    assert seen == ["5", "3(5, -)", "3(8, 5)", "1(3(8, 5), -)", "1(7, 3(8, 5))", "1(2(3(8, 5), -), 7)"]
    assert h.delete_min() == 1
    assert sh(h.root) == "2(7, 3(8, 5))"


def test_example_meld() -> None:
    x: SkewHeap[int] = SkewHeap()
    for k in [1, 3, 8, 5, 7, 2]:
        x.insert(k)
    y: SkewHeap[int] = SkewHeap()
    for k in [4, 6, 9, 10]:
        y.insert(k)
    assert sh(x.root) == "1(2(3(5, -), -), 7(8, -))"
    assert sh(y.root) == "4(6(10, -), 9)"
    x.meld(y)
    x.check_invariant()
    assert sh(x.root) == "1(4(7(9, 8), 6(10, -)), 2(3(5, -), -))"
    assert len(x) == 10 and y.is_empty()


def test_empty() -> None:
    h: SkewHeap[int] = SkewHeap()
    assert merge(None, None) is None
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    assert h.heavy_count() == 0


def test_long_paths_no_recursion() -> None:
    h: SkewHeap[int] = SkewHeap()
    for k in range(20000, 0, -1):
        h.insert(k)
    other: SkewHeap[int] = SkewHeap()
    for k in range(20001, 40001):
        other.insert(k)
    h.meld(other)
    out = [h.delete_min() for _ in range(2000)]
    assert out == list(range(1, 2001))


def test_random_against_heapq() -> None:
    rng = random.Random(1986)
    for _ in range(600):
        heaps = [SkewHeap[int]() for _ in range(3)]
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
            assert 0 <= heaps[i].heavy_count() <= len(heaps[i])
