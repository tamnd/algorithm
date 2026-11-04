# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/catenable-deque/. The authors are listed in prov/776W85.jsonl.

import math
import random

import pytest

from catenable_deque import CatenableDeque


def test_example() -> None:
    a = CatenableDeque.from_iterable([1, 2, 3, 4, 5])
    b = CatenableDeque.from_iterable([6, 7, 8, 9, 10])
    a.check_invariant()
    assert a.depth() == 1 and b.depth() == 1
    c = a + b
    c.check_invariant()
    assert c.to_list() == list(range(1, 11))
    assert c.depth() == 1
    assert c._q.f == (1, 2, 3) and c._q.r == (9, 10)
    assert c._q.m.d == ((4, 5), (6, 7, 8))
    assert c.head() == 1 and c.last() == 10
    t = c.tail().tail().tail()
    t.check_invariant()
    assert t.to_list() == list(range(4, 11))
    assert a.to_list() == [1, 2, 3, 4, 5]
    assert (c + c).to_list() == list(range(1, 11)) * 2


def test_empty() -> None:
    q: CatenableDeque[int] = CatenableDeque()
    q.check_invariant()
    assert len(q) == 0 and q.is_empty() and q.to_list() == []
    for op in (q.head, q.last, q.tail, q.init):
        with pytest.raises(IndexError):
            op()
    assert (q + q).to_list() == []
    one = q.cons(7)
    assert (one + q).to_list() == [7] and (q + one).to_list() == [7]


def test_ends() -> None:
    q = CatenableDeque.from_iterable(range(200))
    out = []
    while not q.is_empty():
        out.append(q.head())
        q = q.tail()
        q.check_invariant()
    assert out == list(range(200))
    q = CatenableDeque.from_iterable(range(200))
    out = []
    while not q.is_empty():
        out.append(q.last())
        q = q.init()
        q.check_invariant()
    assert out == list(range(199, -1, -1))


def test_depth_bound() -> None:
    q: CatenableDeque[int] = CatenableDeque()
    for k in range(1, 3000):
        q = q.cons(k) if k % 3 else q.snoc(k)
        if k % 97 == 0 and len(q) < 20000:
            q = q + q
        assert q.depth() <= max(0, math.log2(len(q)))
    q.check_invariant()


def test_random_persistent() -> None:
    rng = random.Random(776)
    versions: list[tuple[CatenableDeque[int], list[int]]] = [(CatenableDeque(), [])]
    checks = 0
    for step in range(3000):
        q, ref = rng.choice(versions)
        op = rng.randrange(7)
        if op == 0:
            x = rng.randrange(1000)
            q, ref = q.cons(x), [x] + ref
        elif op == 1:
            x = rng.randrange(1000)
            q, ref = q.snoc(x), ref + [x]
        elif op in (2, 3):
            q2, ref2 = rng.choice(versions)
            if len(ref) + len(ref2) > 400:
                continue
            q, ref = q + q2, ref + ref2
        elif op == 4 and ref:
            assert q.head() == ref[0]
            q, ref = q.tail(), ref[1:]
        elif op == 5 and ref:
            assert q.last() == ref[-1]
            q, ref = q.init(), ref[:-1]
        else:
            continue
        q.check_invariant()
        assert len(q) == len(ref)
        assert q.to_list() == ref
        checks += 1
        versions.append((q, ref))
    for q, ref in versions:
        assert q.to_list() == ref
        checks += 1
    assert checks >= 500
