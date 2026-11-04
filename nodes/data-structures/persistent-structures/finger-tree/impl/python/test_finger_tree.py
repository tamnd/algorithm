# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finger-tree/. The authors are listed in prov/BJ50ZK.jsonl.

import random

import pytest

from finger_tree import FingerTree


def test_example() -> None:
    t: FingerTree[int] = FingerTree()
    shapes = []
    for x in range(1, 10):
        t = t.snoc(x)
        t.check_invariant()
        shapes.append(t.depth())
    assert t.to_list() == list(range(1, 10))
    assert shapes == [0, 1, 1, 1, 1, 1, 1, 1, 2]
    assert t.lookup(4) == 5
    left, right = t.split_at(4)
    assert left.to_list() == [1, 2, 3, 4]
    assert right.to_list() == [5, 6, 7, 8, 9]
    both = right.append(left)
    both.check_invariant()
    assert both.to_list() == [5, 6, 7, 8, 9, 1, 2, 3, 4]
    assert t.to_list() == list(range(1, 10))


def test_empty() -> None:
    t: FingerTree[int] = FingerTree()
    t.check_invariant()
    assert len(t) == 0 and t.viewl() is None and t.viewr() is None
    with pytest.raises(IndexError):
        t.head()
    with pytest.raises(IndexError):
        t.last()
    with pytest.raises(IndexError):
        t.lookup(0)
    a, b = t.split_at(0)
    assert a.to_list() == [] and b.to_list() == []


def test_ends() -> None:
    t = FingerTree.from_iterable(list(range(100)))
    out = []
    while True:
        v = t.viewl()
        if v is None:
            break
        x, t = v
        t.check_invariant()
        out.append(x)
    assert out == list(range(100))
    t = FingerTree.from_iterable(list(range(100)))
    out = []
    while len(t):
        t, x = t.viewr()  # type: ignore[misc]
        t.check_invariant()
        out.append(x)
    assert out == list(range(99, -1, -1))


def test_depth_is_logarithmic() -> None:
    t: FingerTree[int] = FingerTree()
    for x in range(5000):
        t = t.cons(x)
    t.check_invariant()
    assert 2 ** (t.depth() - 1) <= len(t)


def test_all_splits_and_appends_small() -> None:
    for n in range(0, 40):
        t = FingerTree.from_iterable(list(range(n)))
        for i in range(-1, n + 2):
            a, b = t.split_at(i)
            a.check_invariant()
            b.check_invariant()
            k = min(max(i, 0), n)
            assert a.to_list() == list(range(k))
            assert b.to_list() == list(range(k, n))
            c = a.append(b)
            c.check_invariant()
            assert c.to_list() == list(range(n))
        for i in range(n):
            assert t.lookup(i) == i


def test_random_against_lists() -> None:
    rng = random.Random(20261104)
    versions: list[tuple[FingerTree[int], list[int]]] = [(FingerTree(), [])]
    checks = 0
    for _ in range(3000):
        t, ref = rng.choice(versions)
        op = rng.randrange(7)
        if op == 0:
            x = rng.randrange(1000)
            nt, nref = t.cons(x), [x] + ref
        elif op == 1:
            x = rng.randrange(1000)
            nt, nref = t.snoc(x), ref + [x]
        elif op == 2:
            v = t.viewl()
            if v is None:
                assert ref == []
                continue
            assert v[0] == ref[0]
            nt, nref = v[1], ref[1:]
        elif op == 3:
            w = t.viewr()
            if w is None:
                assert ref == []
                continue
            assert w[1] == ref[-1]
            nt, nref = w[0], ref[:-1]
        elif op == 4:
            u, uref = rng.choice(versions)
            nt, nref = t.append(u), ref + uref
        elif op == 5:
            i = rng.randrange(len(ref) + 1)
            a, b = t.split_at(i)
            a.check_invariant()
            b.check_invariant()
            assert a.to_list() == ref[:i] and b.to_list() == ref[i:]
            nt, nref = (a, ref[:i]) if rng.random() < 0.5 else (b, ref[i:])
        else:
            if ref:
                i = rng.randrange(len(ref))
                assert t.lookup(i) == ref[i]
            continue
        nt.check_invariant()
        assert len(nt) == len(nref)
        assert nt.to_list() == nref
        checks += 1
        if len(nref) < 3000:
            versions.append((nt, nref))
    for t, ref in versions:
        assert t.to_list() == ref
    assert checks >= 500
