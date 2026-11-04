# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-quadtree/. The authors are listed in prov/C2HX1P.jsonl.

import math
import random
from typing import Optional

from point_quadtree import Node, PointQuadtree

P = [(35, 40), (50, 10), (60, 75), (80, 65), (85, 15), (5, 45), (25, 35), (90, 5)]


def shape(t: Optional[Node]) -> object:
    if t is None:
        return None
    if all(c is None for c in t.child):
        return t.point
    return (t.point, [shape(c) for c in t.child])


def test_page_example() -> None:
    t = PointQuadtree()
    for p in P:
        assert t.insert(p)
    t.check_invariant()
    assert shape(t.root) == (
        (35, 40),
        [(25, 35), ((50, 10), [None, (90, 5), None, (85, 15)]), (5, 45), ((60, 75), [None, (80, 65), None, None])],
    )
    assert t.height() == 3
    assert sorted(t.range_search((20, 30), (70, 80))) == [(25, 35), (35, 40), (60, 75)]
    assert t.delete((50, 10))
    t.check_invariant()
    assert shape(t.root) == (
        (35, 40),
        [(25, 35), ((85, 15), [None, (90, 5), None, None]), (5, 45), ((60, 75), [None, (80, 65), None, None])],
    )
    b = PointQuadtree(P)
    b.check_invariant()
    assert b.root is not None and b.root.point == (60, 75) and b.height() == 3


def test_edges() -> None:
    t = PointQuadtree()
    assert not t.contains((0, 0)) and not t.delete((0, 0))
    assert t.range_search((0, 0), (1, 1)) == []
    assert t.insert((1, 1)) and not t.insert((1, 1))
    assert t.insert((1, 2)) and t.insert((2, 1)) and t.insert((1, 0))
    t.check_invariant()
    assert sorted(t.range_search((1, 1), (1, 1))) == [(1, 1)]
    assert t.delete((1, 1)) and len(t) == 3
    t.check_invariant()
    assert sorted(t.points()) == [(1, 0), (1, 2), (2, 1)]


def test_balanced_build_and_sorted_chain() -> None:
    n = 1000
    pts = [(i, (i * 7919) % n) for i in range(n)]
    t = PointQuadtree(pts)
    t.check_invariant()
    assert t.height() <= math.floor(math.log2(n)) + 1
    c = PointQuadtree()
    for i in range(n):
        c.insert((i, i))
    assert c.height() == n
    assert len(c.range_search((10, 10), (20, 20))) == 11
    assert c.delete((0, 0)) and len(c) == n - 1


def test_random_against_set() -> None:
    rng = random.Random(1974)
    for _ in range(600):
        t = PointQuadtree([(rng.randrange(12), rng.randrange(12)) for _ in range(rng.randrange(0, 15))])
        model = set(t.points())
        for _ in range(rng.randrange(1, 30)):
            p = (rng.randrange(12), rng.randrange(12))
            r = rng.random()
            if r < 0.4:
                assert t.insert(p) == (p not in model)
                model.add(p)
            elif r < 0.7:
                assert t.delete(p) == (p in model)
                model.discard(p)
            else:
                assert t.contains(p) == (p in model)
            lo = (rng.randrange(-1, 12), rng.randrange(-1, 12))
            hi = (lo[0] + rng.randrange(6), lo[1] + rng.randrange(6))
            want = sorted(q for q in model if lo[0] <= q[0] <= hi[0] and lo[1] <= q[1] <= hi[1])
            assert sorted(t.range_search(lo, hi)) == want
        t.check_invariant()
        assert len(t) == len(model)
