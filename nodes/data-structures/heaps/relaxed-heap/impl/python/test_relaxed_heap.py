# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxed-heap/. The authors are listed in prov/KN6FTW.jsonl.

import heapq
import random
from typing import Dict, List

import pytest

from relaxed_heap import Node, RelaxedHeap


def show(x: Node[int]) -> str:
    """Write a tree as key(children in order of rank), with * for an active node."""
    s = f"{x.key}" + ("*" if x.active else "")
    return s if not x.children else s + "(" + ", ".join(show(c) for c in x.children) + ")"


def dump(h: RelaxedHeap[int]) -> str:
    return "  ".join(show(h.roots[k]) for k in sorted(h.roots))


def test_page_example() -> None:
    h: RelaxedHeap[int] = RelaxedHeap()
    nd = {k: h.insert(k) for k in range(10, 170, 10)}
    assert dump(h) == "10(20, 30(40), 50(60, 70(80)), 90(100, 110(120), 130(140, 150(160))))"
    trace = []
    for old, new in [(60, 5), (120, 15), (140, 25)]:
        t = h.transformations
        h.decrease_key(nd[old], new)
        h.check_invariant()
        trace.append((h.transformations - t, dump(h)))
    assert trace == [
        (1, "10(20, 30(40), 50(80, 70(5*)), 90(100, 110(120), 130(140, 150(160))))"),
        (2, "10(20, 30(40), 50(80, 70(110)), 90(100, 150(160), 130(140, 5*(15))))"),
        (1, "10(20, 30(40), 50(80, 70(110)), 90(100, 150(160), 5*(15, 130(25*))))"),
    ]
    assert h.find_min() == 5
    assert h.delete_min() == 5
    assert dump(h) == "20  30(40)  50(80, 70(110))  90(100, 150(160), 10*(15, 130(25*)))"
    h.check_invariant()
    assert [h.delete_min() for _ in range(len(h))] == [10, 15, 20, 25, 30, 40, 50, 70, 80, 90, 100, 110, 130, 150, 160]


def test_empty_and_errors() -> None:
    h: RelaxedHeap[int] = RelaxedHeap()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    x = h.insert(4)
    with pytest.raises(ValueError):
        h.decrease_key(x, 5)
    h.decrease_key(x, 4)
    assert h.delete_min() == 4 and len(h) == 0
    h.check_invariant()


def test_duplicates() -> None:
    h: RelaxedHeap[int] = RelaxedHeap()
    xs = [h.insert(3) for _ in range(9)]
    for x in xs[::2]:
        h.decrease_key(x, 1)
        h.check_invariant()
    assert [h.delete_min() for _ in range(9)] == [1] * 5 + [3] * 4


def test_many_new_minima() -> None:
    rng = random.Random(7)
    h: RelaxedHeap[int] = RelaxedHeap()
    nodes = [h.insert(rng.randint(0, 10**6)) for _ in range(1024)]
    low = 0
    for _ in range(3000):
        low -= 1
        h.decrease_key(rng.choice(nodes), low)
        assert sum(len(a) for a in h.actives.values()) <= 11
    h.check_invariant()
    out = [h.delete_min() for _ in range(len(h))]
    assert out == sorted(out)


def test_random_against_heapq() -> None:
    rng = random.Random(19881101)
    for case in range(600):
        h: RelaxedHeap[int] = RelaxedHeap()
        ref: List[tuple[int, int]] = []
        handles: Dict[int, Node[int]] = {}
        keys: Dict[int, int] = {}
        nxt = 0
        scale = rng.choice([1, 10, 1000])
        for _ in range(rng.randint(1, 120)):
            op = rng.random()
            if op < 0.45 or not keys:
                k = rng.randint(0, 1000)
                handles[nxt] = h.insert(k)
                keys[nxt] = k
                heapq.heappush(ref, (k, nxt))
                nxt += 1
            elif op < 0.8:
                i = rng.choice(list(keys))
                k = keys[i] - rng.randint(0, 30) * scale
                h.decrease_key(handles[i], k)
                keys[i] = k
                heapq.heappush(ref, (k, i))
            else:
                while ref[0][0] != keys.get(ref[0][1]):
                    heapq.heappop(ref)
                m = ref[0][0]
                assert h.find_min() == m
                assert h.delete_min() == m
                alive = {id(v) for v in h.nodes()}
                gone = [i for i in keys if id(handles[i]) not in alive]
                assert len(gone) == 1 and keys[gone[0]] == m
                del keys[gone[0]]
            if case % 10 == 0:
                h.check_invariant()
        h.check_invariant()
        out = [h.delete_min() for _ in range(len(h))]
        assert out == sorted(keys.values())
