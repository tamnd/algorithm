# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-segment-tree/. The authors are listed in prov/KB52KZ.jsonl.

import random

import pytest

from persistent_segment_tree import PersistentSegmentTree


def test_example() -> None:
    t = PersistentSegmentTree([5, 3, 7, 1])
    assert t.num_nodes() == 7
    assert t.query(0, 0, 4) == 16
    v1 = t.update(0, 2, 10)
    assert t.num_nodes() == 10
    v2 = t.update(0, 0, 0)
    assert t.num_nodes() == 13
    assert t.values(0) == [5, 3, 7, 1]
    assert t.values(v1) == [5, 3, 10, 1]
    assert t.values(v2) == [0, 3, 7, 1]
    assert t.query(v1, 1, 3) == 13
    assert t.query(0, 1, 3) == 10
    assert t.query(v2, 0, 2) == 3
    assert t.query(v1, 0, 4) == 19
    v3 = t.update(v1, 0, 0)
    assert t.values(v3) == [0, 3, 10, 1]
    t.check_invariant()


def test_kth_example() -> None:
    b = [3, 1, 2, 3, 0]
    t = PersistentSegmentTree([0] * 4)
    vs = [0]
    for x in b:
        vs.append(t.add(vs[-1], x, 1))
    # b[1..4) = [1, 2, 3]
    assert [t.kth(vs[1], vs[4], k) for k in (1, 2, 3)] == [1, 2, 3]
    # whole array sorted is [0, 1, 2, 3, 3]
    assert [t.kth(vs[0], vs[5], k) for k in range(1, 6)] == [0, 1, 2, 3, 3]
    # count of values < 3 in b[0..5) is 3
    assert t.query(vs[5], 0, 3) - t.query(vs[0], 0, 3) == 3
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        PersistentSegmentTree([])
    t = PersistentSegmentTree([4])
    assert t.query(0, 0, 1) == 4 and t.query(0, 0, 0) == 0 and t.query(0, 1, 1) == 0
    v = t.update(0, 0, -2)
    assert t.get(v, 0) == -2 and t.get(0, 0) == 4
    assert t.kth(0, t.add(0, 0, 3), 3) == 0
    with pytest.raises(IndexError):
        t.update(0, 1, 0)
    with pytest.raises(IndexError):
        t.query(5, 0, 1)
    with pytest.raises(IndexError):
        t.query(0, 0, 2)
    with pytest.raises(IndexError):
        t.kth(0, 0, 1)
    t.check_invariant()


def test_deep() -> None:
    n = 1 << 17
    t = PersistentSegmentTree([1] * n)
    v = 0
    for i in range(0, n, 997):
        v = t.update(v, i, 0)
    assert t.query(v, 0, n) == n - len(range(0, n, 997))
    assert t.query(0, 0, n) == n
    before = t.num_nodes()
    t.update(v, n - 1, 5)
    assert t.num_nodes() - before == 18  # ceil(lg n) + 1


def test_random_version_tree() -> None:
    rng = random.Random(2718)
    for _ in range(500):
        n = rng.randint(1, 12)
        start = [rng.randint(-5, 5) for _ in range(n)]
        t = PersistentSegmentTree(start)
        model = [list(start)]
        for _ in range(rng.randint(1, 25)):
            v = rng.randrange(len(model))
            op = rng.random()
            if op < 0.5:
                i, x = rng.randrange(n), rng.randint(-5, 5)
                assert t.update(v, i, x) == len(model)
                model.append(list(model[v]))
                model[-1][i] = x
            else:
                l = rng.randint(0, n)
                r = rng.randint(0, n)
                assert t.query(v, l, r) == sum(model[v][l:r])
        for v, arr in enumerate(model):
            assert t.values(v) == arr
        t.check_invariant()


def test_random_kth() -> None:
    rng = random.Random(3141)
    for _ in range(500):
        m = rng.randint(1, 9)
        b = [rng.randrange(m) for _ in range(rng.randint(1, 15))]
        t = PersistentSegmentTree([0] * m)
        vs = [0]
        for x in b:
            vs.append(t.add(vs[-1], x, 1))
        l = rng.randrange(len(b))
        r = rng.randint(l + 1, len(b))
        part = sorted(b[l:r])
        for k in range(1, len(part) + 1):
            assert t.kth(vs[l], vs[r], k) == part[k - 1]
        t.check_invariant()
