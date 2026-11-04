# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thin-heap/. The authors are listed in prov/DBACA1.jsonl.

import random

import pytest

from thin_heap import Node, ThinHeap, is_thin


def show(x: Node[int]) -> str:
    """Write a tree as key:rank(children), with t after the rank of a thin node."""
    s = f"{x.key}:{x.rank}{'t' if is_thin(x) else ''}"
    parts = []
    c = x.child
    while c is not None:
        parts.append(show(c))
        c = c.right
    return s + ("(" + ", ".join(parts) + ")" if parts else "")


def dump(h: ThinHeap[int]) -> str:
    return " ".join(show(r) for r in h._roots())


def test_page_example() -> None:
    h: ThinHeap[int] = ThinHeap()
    nodes = {k: h.insert(k) for k in range(10, 100, 10)}
    assert h.delete_min() == 10
    assert h.links == 7
    assert dump(h) == "20:3(60:2(80:1(90:0), 70:0), 40:1(50:0), 30:0)"
    h.decrease_key(nodes[50], 5)
    assert dump(h) == "20:3(60:2(80:1(90:0), 70:0), 40:1t, 30:0) 5:0"
    h.decrease_key(nodes[30], 3)
    assert dump(h) == "20:3(60:2t(70:0), 80:1(90:0), 40:0) 5:0 3:0"
    h.decrease_key(nodes[70], 7)
    assert dump(h) == "20:2(80:1(90:0), 40:0) 5:0 3:0 7:0 60:0"
    h.check_invariant()
    h.links = 0
    assert h.delete_min() == 3
    assert h.links == 1
    assert dump(h) == "60:0 5:1(7:0) 20:2(80:1(90:0), 40:0)"
    assert h.find_min() == 5
    h.check_invariant()


def test_edge_cases() -> None:
    h: ThinHeap[int] = ThinHeap()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    x = h.insert(4)
    h.decrease_key(x, 1)
    assert h.find_min() == 1
    with pytest.raises(ValueError):
        h.decrease_key(x, 2)
    assert h.delete_min() == 1
    assert len(h) == 0
    h.check_invariant()


def test_meld() -> None:
    a: ThinHeap[int] = ThinHeap()
    b: ThinHeap[int] = ThinHeap()
    for k in [5, 9, 1]:
        a.insert(k)
    for k in [7, 0, 3]:
        b.insert(k)
    a.meld(b)
    assert len(a) == 6 and len(b) == 0
    a.check_invariant()
    assert [a.delete_min() for _ in range(6)] == [0, 1, 3, 5, 7, 9]


def alive(h: ThinHeap[int]) -> set[int]:
    seen = set()
    stack = list(h._roots())
    while stack:
        v = stack.pop()
        seen.add(id(v))
        c = v.child
        while c is not None:
            stack.append(c)
            c = c.right
    return seen


def test_random_against_model() -> None:
    rng = random.Random(2008)
    for _ in range(600):
        h: ThinHeap[int] = ThinHeap()
        ref: dict[int, Node[int]] = {}
        for _ in range(rng.randrange(1, 80)):
            op = rng.random()
            if op < 0.45 or not ref:
                x = h.insert(rng.randrange(1000))
                ref[id(x)] = x
            elif op < 0.75:
                x = rng.choice(list(ref.values()))
                h.decrease_key(x, x.key - rng.randrange(0, 60))
            else:
                smallest = min(x.key for x in ref.values())
                assert h.delete_min() == smallest
                live = alive(h)
                gone = [k for k in ref if k not in live]
                assert len(gone) == 1
                del ref[gone[0]]
            h.check_invariant()
            assert len(h) == len(ref)
