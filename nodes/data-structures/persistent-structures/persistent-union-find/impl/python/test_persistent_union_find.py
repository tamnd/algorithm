# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-union-find/. The authors are listed in prov/ZTTVD6.jsonl.

import random

import pytest

from persistent_union_find import PArray, PersistentUnionFind


def test_example() -> None:
    h0 = PersistentUnionFind(4)
    h1 = h0.union(0, 1)
    h2 = h1.union(2, 3)
    h3 = h2.union(1, 3)
    assert h3.find(3) == 0 and h3.find(2) == 0
    assert h3._parent.get(3) == 0  # path compressed: 3 -> 0
    assert h2.find(3) == 2 and h1.find(3) == 3 and h0.find(1) == 1
    h4 = h1.union(1, 2)
    assert h4.sets() == [[0, 1, 2], [3]]
    assert h3.sets() == [[0, 1, 2, 3]]
    assert h2.sets() == [[0, 1], [2, 3]]
    assert h1.sets() == [[0, 1], [2], [3]]
    assert h0.sets() == [[0], [1], [2], [3]]
    for h in (h0, h1, h2, h3, h4):
        h.check_invariant()


def test_edges() -> None:
    e = PersistentUnionFind(0)
    assert e.sets() == []
    with pytest.raises(IndexError):
        e.find(0)
    one = PersistentUnionFind(1)
    assert one.union(0, 0) is one and one.find(0) == 0
    a = PArray([1, 2, 3])
    b = a.set(0, 9)
    assert a.set(1, 2) is a
    assert a.to_list() == [1, 2, 3] and b.to_list() == [9, 2, 3]
    assert a.get(0) == 1 and b.get(0) == 9


def test_deep() -> None:
    n = 100000
    h0 = PersistentUnionFind(n)
    h = h0
    for i in range(n - 1):
        h = h.union(i, i + 1)
    assert h.same(0, n - 1)
    assert not h0.same(0, n - 1)  # reroots through about 2n diffs iteratively
    assert h.find(n - 1) == h.find(0)
    a = PArray([0])
    v = a
    for k in range(200000):
        v = v.set(0, k + 1)
    assert a.get(0) == 0 and v.get(0) == 200000


def test_random_fully_persistent() -> None:
    rng = random.Random(7331)
    for _ in range(500):
        n = rng.randint(1, 8)
        versions = [(PersistentUnionFind(n), list(range(n)))]  # model: label per element
        for _ in range(rng.randint(1, 30)):
            h, lab = rng.choice(versions)
            x, y = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.5:
                h2 = h.union(x, y)
                a, b = lab[x], lab[y]
                lab2 = [a if c == b else c for c in lab]
                versions.append((h2, lab2))
            else:
                assert h.same(x, y) == (lab[x] == lab[y])
        for h, lab in versions:
            for x in range(n):
                for y in range(n):
                    assert h.same(x, y) == (lab[x] == lab[y])
            h.check_invariant()
