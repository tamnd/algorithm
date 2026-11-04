# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binomial-heap/. The authors are listed in prov/A5XZ80.jsonl.

import random

import pytest

from binomial_heap import BinomialHeap, BNode, Entry


def tree(x: BNode[int, None]) -> str:
    s = str(x.entry.key)
    kids = " ".join(tree(c) for c in reversed(x.children))
    return s + ("(" + kids + ")" if kids else "")


def shape(h: BinomialHeap[int, None]) -> str:
    return " | ".join(tree(r) for r in reversed(h.roots))


def test_example() -> None:
    h: BinomialHeap[int, None] = BinomialHeap()
    e: dict[int, Entry[int, None]] = {}
    steps = []
    for k in [12, 7, 25, 15, 28, 33, 41]:
        e[k] = h.insert(k)
        steps.append(shape(h))
        h.check_invariant()
    assert steps == [
        "12",
        "7(12)",
        "25 | 7(12)",
        "7(15(25) 12)",
        "28 | 7(15(25) 12)",
        "28(33) | 7(15(25) 12)",
        "41 | 28(33) | 7(15(25) 12)",
    ]
    assert h.find_min().key == 7
    assert h.extract_min().key == 7
    assert shape(h) == "12(41) | 15(28(33) 25)"
    h.decrease_key(e[41], 3)
    assert shape(h) == "3(12) | 15(28(33) 25)"
    g: BinomialHeap[int, None] = BinomialHeap()
    g.insert(9)
    g.insert(30)
    h.union(g)
    assert shape(h) == "3(15(28(33) 25) 9(30) 12)"
    assert len(g) == 0 and len(h) == 8
    h.delete(e[28])
    assert shape(h) == "12 | 9(30) | 3(15(33) 25)"
    h.check_invariant()
    assert [h.extract_min().key for _ in range(len(h))] == [3, 9, 12, 15, 25, 30, 33]


def test_edges() -> None:
    h: BinomialHeap[int, str] = BinomialHeap()
    with pytest.raises(IndexError):
        h.extract_min()
    with pytest.raises(IndexError):
        h.find_min()
    a = h.insert(5, "a")
    with pytest.raises(ValueError):
        h.decrease_key(a, 6)
    assert h.extract_min().item == "a"
    with pytest.raises(ValueError):
        h.decrease_key(a, 1)
    with pytest.raises(ValueError):
        h.delete(a)
    for _ in range(9):
        h.insert(4, "x")
    h.check_invariant()
    assert [r.degree for r in h.roots] == [3, 0]
    assert [h.extract_min().key for _ in range(9)] == [4] * 9


def test_insert_shape_is_binary() -> None:
    h: BinomialHeap[int, None] = BinomialHeap()
    for n in range(1, 300):
        h.insert(-n)
        degs = {r.degree for r in h.roots}
        assert degs == {i for i in range(n.bit_length()) if n >> i & 1}


def test_random_against_model() -> None:
    rng = random.Random(1978)
    for _ in range(600):
        h: BinomialHeap[int, int] = BinomialHeap()
        live: dict[int, Entry[int, int]] = {}
        nxt = 0
        for _ in range(rng.randint(0, 50)):
            op = rng.random()
            if op < 0.35:
                live[nxt] = h.insert(rng.randint(-40, 40), nxt)
                nxt += 1
            elif op < 0.45:
                g: BinomialHeap[int, int] = BinomialHeap()
                for _ in range(rng.randint(0, 6)):
                    live[nxt] = g.insert(rng.randint(-40, 40), nxt)
                    nxt += 1
                h.union(g)
            elif op < 0.65:
                if live:
                    m = min(x.key for x in live.values())
                    x = h.extract_min()
                    assert x.key == m
                    del live[x.item]
                else:
                    with pytest.raises(IndexError):
                        h.extract_min()
            elif op < 0.85:
                if live:
                    i = rng.choice(list(live))
                    h.decrease_key(live[i], live[i].key - rng.randint(0, 20))
            else:
                if live:
                    i = rng.choice(list(live))
                    h.delete(live.pop(i))
            h.check_invariant()
            assert len(h) == len(live)
            if live:
                assert h.find_min().key == min(x.key for x in live.values())
