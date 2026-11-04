# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-vector/. The authors are listed in prov/E5Q5G6.jsonl.

import random

import pytest

from persistent_vector import PersistentVector


def test_example() -> None:
    # Branching factor M = 4 (bits = 2), as on the page.
    v10: PersistentVector[int] = PersistentVector.from_iterable(range(10), bits=2)
    assert v10._root == ((0, 1, 2, 3), (4, 5, 6, 7)) and v10._tail == (8, 9)
    assert v10.height() == 1 and v10.get(6) == 6
    w = v10.set(6, 60)
    assert w._root[0] is v10._root[0] and w._tail is v10._tail
    assert w.to_list() == [0, 1, 2, 3, 4, 5, 60, 7, 8, 9]
    assert v10.to_list() == list(range(10))
    v = v10
    for x in (10, 11, 12, 13, 14, 15, 16):
        v = v.push(x)
    # 17 items: 4 full leaves in the trie, tail (16,)
    assert len(v._root) == 4 and v._tail == (16,) and v.height() == 1
    v = v.push(17)
    assert v._tail == (16, 17)
    v = v.push(18).push(19).push(20)
    # 21 items: the fifth leaf overflows a root of 4 leaves, so the trie grows.
    assert v.height() == 2 and v._tail == (20,)
    assert v.to_list() == list(range(10)) + list(range(10, 21))
    p = v.pop()
    assert p.height() == 1 and p._tail == (16, 17, 18, 19)
    q = p.pop().pop().pop().pop()
    assert len(q) == 16 and q.height() == 1 and q._tail == (12, 13, 14, 15)
    for x in (v10, w, v, p, q):
        x.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        PersistentVector(0)
    e: PersistentVector[str] = PersistentVector()
    assert len(e) == 0 and e.to_list() == []
    with pytest.raises(IndexError):
        e.pop()
    with pytest.raises(IndexError):
        e.get(0)
    one = e.push("a")
    assert one.get(0) == "a" and one.pop().to_list() == [] and e.to_list() == []
    with pytest.raises(IndexError):
        one.set(1, "b")
    with pytest.raises(IndexError):
        one.get(-1)
    b1: PersistentVector[int] = PersistentVector.from_iterable(range(9), bits=1)
    assert b1.to_list() == list(range(9))
    while len(b1):
        b1.check_invariant()
        b1 = b1.pop()
    e.check_invariant()


def test_deep() -> None:
    n = 200000
    v: PersistentVector[int] = PersistentVector.from_iterable(range(n))
    assert len(v) == n and v.get(n - 1) == n - 1 and v.get(12345) == 12345
    assert v.height() == 3  # 6249 full leaves: more than 32^2, at most 32^3
    u = v
    for i in range(0, n, 1013):
        u = u.set(i, -i)
    assert all(u.get(i) == (-i if i % 1013 == 0 else i) for i in range(0, n, 7))
    assert v.get(1013) == 1013
    while len(u) > 1000:
        u = u.pop()
    assert len(u) == 1000 and u.height() == 1
    u.check_invariant()
    narrow: PersistentVector[int] = PersistentVector.from_iterable(range(5000), bits=1)
    assert narrow.to_list() == list(range(5000))
    narrow.check_invariant()


def test_random_version_tree() -> None:
    rng = random.Random(1979)
    for _ in range(500):
        bits = rng.randint(1, 3)
        versions = [PersistentVector(bits)]
        model: "list[list[int]]" = [[]]
        for _ in range(rng.randint(1, 60)):
            v = rng.randrange(len(versions))
            op = rng.random()
            if op < 0.5:
                x = rng.randint(0, 99)
                versions.append(versions[v].push(x))
                model.append(model[v] + [x])
            elif op < 0.7 and model[v]:
                versions.append(versions[v].pop())
                model.append(model[v][:-1])
            elif op < 0.9 and model[v]:
                i = rng.randrange(len(model[v]))
                x = rng.randint(0, 99)
                versions.append(versions[v].set(i, x))
                m = list(model[v])
                m[i] = x
                model.append(m)
            elif model[v]:
                i = rng.randrange(len(model[v]))
                assert versions[v].get(i) == model[v][i]
        for t, m in zip(versions, model):
            assert t.to_list() == m and len(t) == len(m)
            t.check_invariant()
