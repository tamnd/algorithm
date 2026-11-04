# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree/. The authors are listed in prov/39PCSM.jsonl.

import math
import random

from kd_tree import KdTree, Node


def shape(t: "Node | None") -> object:
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.point
    return (shape(t.left), t.point, shape(t.right))


P = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]


def test_page_example() -> None:
    t = KdTree(2, P)
    t.check_invariant()
    assert shape(t.root) == (((2, 3), (5, 4), (4, 7)), (7, 2), ((8, 1), (9, 6), None))
    assert sorted(t.range_search((3, 1), (8, 5))) == [(5, 4), (7, 2), (8, 1)]
    assert t.nearest((9, 2)) == (8, 1)
    t.insert((6, 3))
    t.check_invariant()
    assert shape(t.root) == (((None, (2, 3), (6, 3)), (5, 4), (4, 7)), (7, 2), ((8, 1), (9, 6), None))
    assert t.delete((7, 2))
    t.check_invariant()
    assert shape(t.root) == (((None, (2, 3), (6, 3)), (5, 4), (4, 7)), (8, 1), (9, 6))
    assert t.delete((5, 4))
    t.check_invariant()
    assert shape(t.root) == (((None, (2, 3), (6, 3)), (4, 7), None), (8, 1), (9, 6))


def test_edges() -> None:
    t = KdTree(3)
    assert t.nearest((0, 0, 0)) is None
    assert t.range_search((0, 0, 0), (1, 1, 1)) == []
    assert not t.delete((1, 2, 3))
    t.insert((1, 2, 3))
    assert t.contains((1, 2, 3)) and t.nearest((5, 5, 5)) == (1, 2, 3)
    assert t.delete((1, 2, 3)) and t.root is None
    # duplicates and equal coordinates
    d = KdTree(2, [(1, 1)] * 5 + [(1, 2), (2, 1)])
    d.check_invariant()
    assert len(d.range_search((1, 1), (1, 1))) == 5
    for _ in range(5):
        assert d.delete((1, 1))
        d.check_invariant()
    assert not d.contains((1, 1))
    # one dimension
    one = KdTree(1, [(x,) for x in [5, 3, 8, 1, 4]])
    one.check_invariant()
    assert sorted(one.range_search((2,), (5,))) == [(3,), (4,), (5,)]


def test_balanced_build_height() -> None:
    rng = random.Random(3)
    for n in [1, 2, 3, 7, 8, 100, 1000]:
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        t = KdTree(2, pts)
        t.check_invariant()
        assert t.height() == math.floor(math.log2(n)) + 1


def test_sorted_insertions_make_a_path() -> None:
    t = KdTree(2)
    for i in range(200):
        t.insert((i, i))
    t.check_invariant()
    assert t.height() == 200  # pitfall: no rebalancing on insertion


def test_random_operations_against_list() -> None:
    rng = random.Random(1975)
    for trial in range(60):
        k = rng.randint(1, 3)
        model = [tuple(float(rng.randint(0, 6)) for _ in range(k)) for _ in range(rng.randint(0, 20))]
        t = KdTree(k, model)
        t.check_invariant()
        for _ in range(40):
            op = rng.random()
            if op < 0.3:
                p = tuple(float(rng.randint(0, 6)) for _ in range(k))
                t.insert(p)
                model.append(p)
            elif op < 0.5:
                p = tuple(float(rng.randint(0, 6)) for _ in range(k))
                ok = t.delete(p)
                assert ok == (p in model)
                if ok:
                    model.remove(p)
            elif op < 0.8:
                lo = [float(rng.randint(-1, 7)) for _ in range(k)]
                hi = [lo[i] + rng.randint(0, 4) for i in range(k)]
                want = sorted(p for p in model if all(lo[i] <= p[i] <= hi[i] for i in range(k)))
                assert sorted(t.range_search(lo, hi)) == want
            else:
                q = [rng.uniform(-1, 7) for _ in range(k)]
                got = t.nearest(q)
                if not model:
                    assert got is None
                else:
                    best = min(math.dist(q, p) for p in model)
                    assert got is not None and abs(math.dist(q, got) - best) < 1e-9
            t.check_invariant()
            assert sorted(t.points()) == sorted(model)
