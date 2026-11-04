# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strict-fibonacci-heap/. The authors are listed in prov/V45MQ4.jsonl.

import random
from typing import Dict, List

import pytest

from strict_fibonacci_heap import Item, Node, StrictFibonacciHeap


def show(v: Node[int]) -> str:
    """Write a tree as key(children); an active node gets [rank,loss] after its key."""
    s = str(v.item.key) + (f"[{v.rank},{v.loss}]" if v.active else "")
    return s + ("(" + " ".join(show(c) for c in v.children) + ")" if v.children else "")


def queue(h: StrictFibonacciHeap[int]) -> List[int]:
    out: List[int] = []
    v = h.qhead
    while v is not None:
        out.append(v.item.key)
        v = v.qnext
        if v is h.qhead:
            break
    return out


def test_page_example() -> None:
    h: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    items = {}
    for k in [50, 20, 70, 10, 60]:
        items[k] = h.insert(k)
    assert show(h.root) == "10(20(50 70) 60)"  # type: ignore[arg-type]
    items[30] = h.insert(30)
    assert show(h.root) == "10(20[1,0](30[0,0](60) 50 70))"  # type: ignore[arg-type]
    assert queue(h) == [30, 60, 20, 70, 50]
    for k in [80, 40]:
        items[k] = h.insert(k)
    assert show(h.root) == "10(20[1,0](30[0,0](60) 50 70) 80 40)"  # type: ignore[arg-type]
    items[90] = h.insert(90)
    assert show(h.root) == "10(20[2,0](40[1,0](80[0,0](90)) 30[0,0](60) 50) 70)"  # type: ignore[arg-type]
    assert h.counts == {"root-degree": 2, "active-root": 1}
    assert queue(h) == [90, 40, 80, 30, 60, 20, 70, 50]
    h.check_invariant()
    assert h.delete_min() == 10
    assert show(h.root) == "20(40[1,0](80[0,0](90)) 30[0,0](60) 50 70)"  # type: ignore[arg-type]
    assert queue(h) == [80, 30, 60, 70, 50, 90, 40]
    h.check_invariant()
    h.decrease_key(items[80], 15)
    assert h.find_min() == 15
    h.check_invariant()
    assert [h.delete_min() for _ in range(len(h))] == [15, 20, 30, 40, 50, 60, 70, 90]


def test_empty() -> None:
    h: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    h.check_invariant()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    h.meld(StrictFibonacciHeap())
    assert len(h) == 0


def test_single_and_larger_key() -> None:
    h: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    it = h.insert(7)
    with pytest.raises(ValueError):
        h.decrease_key(it, 8)
    h.decrease_key(it, 3)
    assert h.find_min() == 3
    assert h.delete_min() == 3
    assert len(h) == 0
    h.check_invariant()


def test_equal_keys_and_delete() -> None:
    h: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    its = [h.insert(5) for _ in range(20)]
    h.delete(its[3])
    h.check_invariant()
    assert [h.delete_min() for _ in range(19)] == [5] * 19


def test_meld_both_ways() -> None:
    a: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    b: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    for k in range(0, 40, 2):
        a.insert(k)
    for k in range(1, 9, 2):
        b.insert(k)
    b.meld(a)  # the larger heap is the argument
    assert len(a) == 0 and len(b) == 24
    b.check_invariant()
    a.check_invariant()
    assert [b.delete_min() for _ in range(24)] == sorted(list(range(0, 40, 2)) + [1, 3, 5, 7])


def test_decrease_root_and_handles_follow_items() -> None:
    h: StrictFibonacciHeap[int] = StrictFibonacciHeap()
    its: Dict[int, Item[int]] = {k: h.insert(k) for k in range(1, 30)}
    h.delete_min()
    h.decrease_key(its[2], 0)
    for k in range(29, 10, -1):
        h.decrease_key(its[k], -k)
        h.check_invariant()
    for k in range(29, 10, -1):
        assert h.delete_min() == -k
    assert h.delete_min() == 0


def test_random() -> None:
    rng = random.Random(2012)
    for _ in range(600):
        h: StrictFibonacciHeap[int] = StrictFibonacciHeap()
        ref: Dict[Item[int], int] = {}
        for _ in range(rng.randint(1, 120)):
            r = rng.random()
            if r < 0.4 or not ref:
                k = rng.randint(0, 1000)
                ref[h.insert(k)] = k
            elif r < 0.7:
                it = rng.choice(list(ref))
                k = ref[it] - rng.randint(0, 500)
                h.decrease_key(it, k)
                ref[it] = k
            elif r < 0.75:
                it = rng.choice(list(ref))
                h.delete(it)
                del ref[it]
            elif r < 0.8:
                o: StrictFibonacciHeap[int] = StrictFibonacciHeap()
                for _ in range(rng.randint(0, 25)):
                    k = rng.randint(0, 1000)
                    ref[o.insert(k)] = k
                h.meld(o)
            else:
                assert h.find_min() == min(ref.values())
                k = h.delete_min()
                it = min(ref, key=lambda i: (ref[i], i.uid))
                assert k == ref.pop(it)
            assert len(h) == len(ref)
            h.check_invariant()
        assert [h.delete_min() for _ in range(len(h))] == sorted(ref.values())
