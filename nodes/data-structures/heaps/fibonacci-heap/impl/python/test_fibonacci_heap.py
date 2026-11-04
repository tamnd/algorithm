# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-heap/. The authors are listed in prov/1EX9SR.jsonl.

import random

import pytest

from fibonacci_heap import FibonacciHeap, Node, _siblings


def shape(h: FibonacciHeap[int, None]) -> list[str]:
    def t(x: Node[int, None]) -> str:
        kids = [] if x.child is None else _siblings(x.child)
        s = str(x.key) + ("*" if x.mark else "")
        return s + ("(" + " ".join(t(c) for c in kids) + ")" if kids else "")

    return sorted(t(r) for r in h.roots())


def test_example() -> None:
    h: FibonacciHeap[int, None] = FibonacciHeap()
    nodes = {k: h.insert(k) for k in [7, 18, 38, 24, 17, 23, 21, 39, 41]}
    assert len(h.roots()) == 9 and h.find_min().key == 7
    assert h.extract_min().key == 7
    assert shape(h) == ["17(24 18(38) 21(23 39(41)))"]
    h.decrease_key(nodes[41], 15)
    assert shape(h) == ["15", "17(24 18(38) 21(23 39*))"]
    h.decrease_key(nodes[39], 16)
    assert shape(h) == ["15", "16", "17(24 18(38) 21*(23))"]
    h.decrease_key(nodes[23], 5)
    assert shape(h) == ["15", "16", "17(24 18(38))", "21", "5"]
    assert h.find_min().key == 5
    assert h.extract_min().key == 5
    assert shape(h) == ["15(21)", "16", "17(24 18(38))"]
    h.delete(nodes[38])
    assert shape(h) == ["15(21)", "16", "17(24 18*)"]
    h.check_invariant()
    assert [h.extract_min().key for _ in range(len(h))] == [15, 16, 17, 18, 21, 24]


def test_edges() -> None:
    h: FibonacciHeap[int, str] = FibonacciHeap()
    with pytest.raises(IndexError):
        h.extract_min()
    with pytest.raises(IndexError):
        h.find_min()
    x = h.insert(3, "a")
    with pytest.raises(ValueError):
        h.decrease_key(x, 4)
    h.decrease_key(x, 3)
    assert h.extract_min().item == "a"
    assert len(h) == 0
    with pytest.raises(ValueError):
        h.decrease_key(x, 1)
    for _ in range(5):
        h.insert(2, "same")
    assert [h.extract_min().key for _ in range(5)] == [2] * 5
    a: FibonacciHeap[int, str] = FibonacciHeap()
    b: FibonacciHeap[int, str] = FibonacciHeap()
    a.union(b)
    b.insert(1, "b")
    a.union(b)
    assert len(a) == 1 and len(b) == 0 and a.find_min().item == "b"


def test_long_cascade() -> None:
    h: FibonacciHeap[int, None] = FibonacciHeap()
    nodes = [h.insert(k) for k in range(1, 2050)]
    h.extract_min()
    h.check_invariant()
    rng = random.Random(5)
    for x in rng.sample(nodes[1:], 1500):
        h.decrease_key(x, x.key - 10000)
        h.check_invariant() if rng.random() < 0.01 else None
    h.check_invariant()
    keys = [h.extract_min().key for _ in range(len(h))]
    assert keys == sorted(keys)


def test_random_against_model() -> None:
    rng = random.Random(1987)
    for _ in range(500):
        h: FibonacciHeap[int, int] = FibonacciHeap()
        other: FibonacciHeap[int, int] = FibonacciHeap()
        live: dict[int, Node[int, int]] = {}
        model: dict[int, int] = {}
        nxt = 0
        for _ in range(rng.randint(0, 60)):
            op = rng.random()
            if op < 0.35:
                k = rng.randint(-50, 50)
                live[nxt] = h.insert(k, nxt)
                model[nxt] = k
                nxt += 1
            elif op < 0.45:
                k = rng.randint(-50, 50)
                live[nxt] = other.insert(k, nxt)
                model[nxt] = k
                nxt += 1
                if rng.random() < 0.3:
                    h.union(other)
            elif op < 0.65:
                if len(h):
                    x = h.extract_min()
                    in_h = [i for i in model if live[i].in_heap or i == x.item]
                    in_h = [i for i in in_h if i == x.item or _in(h, live[i])]
                    assert x.key == min(model[i] for i in in_h)
                    del model[x.item], live[x.item]
                else:
                    with pytest.raises(IndexError):
                        h.extract_min()
            elif op < 0.9:
                ids = [i for i in model if _in(h, live[i])]
                if ids:
                    i = rng.choice(ids)
                    k = model[i] - rng.randint(0, 30)
                    h.decrease_key(live[i], k)
                    model[i] = k
            else:
                ids = [i for i in model if _in(h, live[i])]
                if ids:
                    i = rng.choice(ids)
                    h.delete(live[i])
                    del model[i], live[i]
            h.check_invariant()
            other.check_invariant()
            got = sorted(x.key for x in h)
            assert got == sorted(model[i] for i in model if _in(h, live[i]))
            assert len(h) + len(other) == len(model)


def _in(h: FibonacciHeap[int, int], x: Node[int, int]) -> bool:
    while x.p is not None:
        x = x.p
    return x in h.roots()
