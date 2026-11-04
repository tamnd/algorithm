# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pairing-heap/. The authors are listed in prov/G7BE09.jsonl.

import random

import pytest

from pairing_heap import Node, PairingHeap


def shape(v: "Node[int] | None") -> object:
    """The tree as (key, [children]) for comparing with the page."""
    if v is None:
        return None
    kids = []
    c = v.child
    while c is not None:
        kids.append(shape(c))
        c = c.sibling
    return (v.key, kids)


def test_example() -> None:
    h: PairingHeap[int] = PairingHeap()
    for k in [7, 3, 9, 5, 8, 2, 6, 4]:
        h.insert(k)
        h.check_invariant()
    assert shape(h.root) == (2, [(4, []), (6, []), (3, [(8, []), (5, []), (9, []), (7, [])])])
    assert h.delete_min() == 2
    assert shape(h.root) == (3, [(4, [(6, [])]), (8, []), (5, []), (9, []), (7, [])])
    assert h.delete_min() == 3
    assert shape(h.root) == (4, [(5, [(7, []), (9, [])]), (8, []), (6, [])])
    h.check_invariant()


def test_edges() -> None:
    h: PairingHeap[int] = PairingHeap()
    with pytest.raises(IndexError):
        h.delete_min()
    with pytest.raises(IndexError):
        h.find_min()
    x = h.insert(1)
    assert h.delete(x) == 1 and h.is_empty()
    for _ in range(5):
        h.insert(4)
    assert [h.delete_min() for _ in range(5)] == [4] * 5
    y = h.insert(10)
    with pytest.raises(ValueError):
        h.decrease_key(y, 11)


def test_meld() -> None:
    a: PairingHeap[int] = PairingHeap()
    b: PairingHeap[int] = PairingHeap()
    for k in [5, 1, 9]:
        a.insert(k)
    for k in [4, 0, 7]:
        b.insert(k)
    a.meld(b)
    assert len(a) == 6 and b.is_empty()
    a.check_invariant()
    assert [a.delete_min() for _ in range(6)] == [0, 1, 4, 5, 7, 9]


def test_sorted_input_is_long() -> None:
    h: PairingHeap[int] = PairingHeap()
    for k in range(20000):
        h.insert(k)  # one root with 19999 children: no recursion depth problem
    assert [h.delete_min() for _ in range(20000)] == list(range(20000))


def test_random_against_model() -> None:
    rng = random.Random(1986)
    for _ in range(500):
        h: PairingHeap[int] = PairingHeap()
        model: dict[int, int] = {}
        handles: dict[int, Node[int]] = {}
        uid = 0
        for _ in range(rng.randint(1, 60)):
            op = rng.random()
            if op < 0.45 or not model:
                k = rng.randint(-50, 50)
                handles[uid] = h.insert(k)
                model[uid] = k
                uid += 1
            elif op < 0.65:
                got = h.delete_min()
                want = min(model.values())
                assert got == want
                # remove one handle with that key that is no longer in the heap
                live = {id(v) for v in iter_nodes(h)}
                gone = [u for u in model if id(handles[u]) not in live]
                assert len(gone) == 1
                del model[gone[0]]
            elif op < 0.85:
                u = rng.choice(list(model))
                k = model[u] - rng.randint(0, 30)
                h.decrease_key(handles[u], k)
                model[u] = k
            else:
                u = rng.choice(list(model))
                assert h.delete(handles[u]) == model[u]
                del model[u]
            h.check_invariant()
            assert len(h) == len(model)
            assert sorted(h.keys()) == sorted(model.values())
            if model:
                assert h.find_min() == min(model.values())


def iter_nodes(h: PairingHeap[int]) -> list[Node[int]]:
    out = []
    stack = [h.root] if h.root is not None else []
    while stack:
        v = stack.pop()
        out.append(v)
        c = v.child
        while c is not None:
            stack.append(c)
            c = c.sibling
    return out
