# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-random-access-list/. The authors are listed in prov/00WGSN.jsonl.

import random

import pytest

from binary_random_access_list import BinaryRandomAccessList


def build(items: list[int]) -> BinaryRandomAccessList[int]:
    r: BinaryRandomAccessList[int] = BinaryRandomAccessList()
    for x in reversed(items):
        r = r.cons(x)
    return r


def test_example() -> None:
    r: BinaryRandomAccessList[int] = BinaryRandomAccessList()
    digits = []
    for x in [10, 20, 30, 40, 50, 60]:
        r = r.cons(x)
        r.check_invariant()
        digits.append(r.digits())
    assert digits == [[1], [0, 1], [1, 1], [0, 0, 1], [1, 0, 1], [0, 1, 1]]
    assert r.to_list() == [60, 50, 40, 30, 20, 10]
    assert r.lookup(3) == 30
    u = r.update(3, 99)
    assert u.to_list() == [60, 50, 40, 99, 20, 10]
    assert r.to_list() == [60, 50, 40, 30, 20, 10]
    t = r.tail()
    assert t.digits() == [1, 0, 1] and t.to_list() == [50, 40, 30, 20, 10]
    assert t.tail().digits() == [0, 0, 1]


def test_edges() -> None:
    e: BinaryRandomAccessList[int] = BinaryRandomAccessList()
    assert e.is_empty() and len(e) == 0
    for f in (e.head, e.tail, lambda: e.lookup(0), lambda: e.update(0, 1)):
        with pytest.raises(IndexError):
            f()
    one = e.cons(7)
    assert one.head() == 7 and one.tail().is_empty() and one.tail().digits() == []
    with pytest.raises(IndexError):
        one.lookup(1)
    with pytest.raises(IndexError):
        one.lookup(-1)
    p = build(list(range(16)))
    assert p.digits() == [0, 0, 0, 0, 1]
    assert [p.lookup(i) for i in range(16)] == list(range(16))


def test_random_against_list() -> None:
    rng = random.Random(77)
    for _ in range(500):
        versions = [(BinaryRandomAccessList(), [])]
        for _ in range(rng.randrange(1, 40)):
            r, m = versions[rng.randrange(len(versions))]
            op = rng.random()
            if m and op < 0.25:
                assert r.head() == m[0]
                r2, m2 = r.tail(), m[1:]
            elif m and op < 0.5:
                i = rng.randrange(len(m))
                y = rng.randrange(1000)
                assert r.lookup(i) == m[i]
                r2, m2 = r.update(i, y), m[:i] + [y] + m[i + 1:]
            else:
                x = rng.randrange(1000)
                r2, m2 = r.cons(x), [x] + m
            r2.check_invariant()
            assert len(r2) == len(m2)
            versions.append((r2, m2))
        for r, m in versions:
            assert r.to_list() == m
            assert r.digits() == [int(b) for b in reversed(bin(len(m))[2:])] if m else r.digits() == []
