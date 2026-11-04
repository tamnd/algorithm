# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brodal-queue/. The authors are listed in prov/CZ84MC.jsonl.

import random

import pytest

from brodal_queue import BrodalQueue, Node


def show(x: Node) -> str:
    s = f"{x.key}/r{x.rank}"
    return s + ("[" + " ".join(show(c) for c in x.children) + "]" if x.children else "")


def shape(q: BrodalQueue) -> str:
    return " ".join(show(t) for t in q.roots)


def test_example() -> None:
    q: BrodalQueue[int, str] = BrodalQueue()
    it = {}
    steps = []
    for v, k in [("a", 6), ("b", 4), ("c", 9), ("d", 2), ("e", 7), ("f", 5), ("g", 8)]:
        it[v] = q.insert(v, k)
        steps.append(shape(q))
    assert steps == [
        "6/r0",
        "4/r0 6/r0",
        "4/r1[6/r0 9/r0]",
        "2/r0 4/r1[6/r0 9/r0]",
        "7/r0 2/r0 4/r1[6/r0 9/r0]",
        "2/r1[7/r0 5/r0] 4/r1[6/r0 9/r0]",
        "2/r2[7/r0 5/r0 4/r1[6/r0 9/r0] 8/r0]",
    ]
    q.check_invariant()
    assert q.find_min() == ("d", 2)
    q.decrease_key(it["e"], 1)
    assert shape(q) == "1/r2[2/r0 5/r0 4/r1[6/r0 9/r0] 8/r0]"
    assert q.find_min() == ("e", 1)
    assert q.delete_min() == ("e", 1)
    assert shape(q) == "8/r0 2/r2[5/r0 4/r1[6/r0 9/r0]]"
    q.check_invariant()
    assert q.delete_min() == ("d", 2)
    assert shape(q) == "4/r2[6/r0 9/r0 5/r1[8/r0]]"
    q.delete(it["c"])
    assert shape(q) == "4/r2[6/r0 5/r1[8/r0]]"
    q.check_invariant()
    assert len(q) == 4


def test_errors() -> None:
    q: BrodalQueue[int, int] = BrodalQueue()
    q.check_invariant()
    with pytest.raises(IndexError):
        q.find_min()
    with pytest.raises(IndexError):
        q.delete_min()
    e = q.insert(1, 10)
    with pytest.raises(ValueError):
        q.decrease_key(e, 11)
    q.delete(e)
    with pytest.raises(KeyError):
        q.delete(e)
    with pytest.raises(KeyError):
        q.decrease_key(e, 1)
    assert len(q) == 0
    q.check_invariant()


def test_meld() -> None:
    a: BrodalQueue[int, int] = BrodalQueue()
    b: BrodalQueue[int, int] = BrodalQueue()
    for k in [9, 4, 7, 1]:
        a.insert(k, k)
    for k in [8, 2, 6]:
        b.insert(k, k)
    a.meld(b)
    a.check_invariant()
    assert len(a) == 7 and len(b) == 0
    assert [a.delete_min()[1] for _ in range(7)] == [1, 2, 4, 6, 7, 8, 9]


def test_roots_stay_few() -> None:
    q: BrodalQueue[int, int] = BrodalQueue()
    for i in range(1000):
        q.insert(i, (i * 7919) % 1000)
        assert len(q.roots) <= (len(q)).bit_length() + 1
    q.check_invariant()
    out = [q.delete_min()[1] for _ in range(1000)]
    assert out == list(range(1000))


def test_random_against_model() -> None:
    rng = random.Random(1996)
    for _ in range(600):
        q: BrodalQueue[int, int] = BrodalQueue()
        model: dict[int, int] = {}
        items = {}
        nxt = 0
        for _ in range(rng.randrange(1, 50)):
            op = rng.randrange(5)
            if op <= 1 or not model:
                k = rng.randrange(40)
                items[nxt] = q.insert(nxt, k)
                model[nxt] = k
                nxt += 1
            elif op == 2:
                v, k = q.delete_min()
                assert k == min(model.values())
                assert model.pop(v) == k
            elif op == 3:
                v = rng.choice(sorted(model))
                k = rng.randrange(model[v] + 1)
                q.decrease_key(items[v], k)
                model[v] = k
            else:
                v = rng.choice(sorted(model))
                q.delete(items[v])
                del model[v]
            q.check_invariant()
            assert len(q) == len(model)
            if model:
                assert q.find_min()[1] == min(model.values())
            for v, it in items.items():
                if v in model:
                    assert it.node is not None and it.node.key == model[v]
