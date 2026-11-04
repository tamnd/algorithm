# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadtree/. The authors are listed in prov/K3B2RT.jsonl.

import random

import pytest

from quadtree import Node, QuadTree


def shape(u: Node) -> object:
    if u.children is None:
        return sorted(u.points)
    return {k: shape(c) for k, c in enumerate(u.children) if c.count}


PAGE = [(2, 3), (12, 2), (9, 6), (5, 12), (14, 13), (11, 7)]


def test_page_example() -> None:
    t = QuadTree(4, 1)
    for p in PAGE:
        assert t.insert(p)
        t.check_invariant()
    assert shape(t.root) == {
        0: [(2, 3)],
        1: {1: [(12, 2)], 2: {2: [(9, 6)], 3: [(11, 7)]}},
        2: [(5, 12)],
        3: [(14, 13)],
    }
    assert t.node_count() == 13 and t.height() == 3
    assert sorted(t.range_search((8, 4), (12, 8))) == [(9, 6), (11, 7)]
    assert t.nearest((10, 10)) == (11, 7)
    assert t.delete((11, 7))
    t.check_invariant()
    assert shape(t.root) == {0: [(2, 3)], 1: {1: [(12, 2)], 2: [(9, 6)]}, 2: [(5, 12)], 3: [(14, 13)]}
    assert t.node_count() == 9


def test_edges() -> None:
    t = QuadTree(0, 1)
    assert t.nearest((0, 0)) is None
    assert t.insert((0, 0)) and not t.insert((0, 0))
    assert t.contains((0, 0)) and len(t) == 1
    with pytest.raises(ValueError):
        t.insert((1, 0))
    with pytest.raises(ValueError):
        QuadTree(-1)
    assert t.delete((0, 0)) and not t.delete((0, 0)) and len(t) == 0
    u = QuadTree(10, 1)
    u.insert((0, 0))
    u.insert((1, 1))
    assert u.height() == 10 and u.node_count() == 41
    assert u.nearest((1023, 1023)) == (1, 1)


def test_order_does_not_matter() -> None:
    rng = random.Random(5)
    pts = list({(rng.randrange(32), rng.randrange(32)) for _ in range(40)})
    a, b = QuadTree(5, 2), QuadTree(5, 2)
    for p in pts:
        a.insert(p)
    rng.shuffle(pts)
    for p in pts:
        b.insert(p)
    assert shape(a.root) == shape(b.root)


def test_random_against_model() -> None:
    rng = random.Random(2024)
    for trial in range(500):
        depth = rng.randint(0, 5)
        side = 1 << depth
        t = QuadTree(depth, rng.randint(1, 3))
        model: set[tuple[int, int]] = set()
        for _ in range(rng.randint(1, 40)):
            p = (rng.randrange(side), rng.randrange(side))
            if rng.random() < 0.6:
                assert t.insert(p) == (p not in model)
                model.add(p)
            else:
                assert t.delete(p) == (p in model)
                model.discard(p)
            t.check_invariant()
        assert sorted(t.points()) == sorted(model)
        lo = (rng.randrange(side), rng.randrange(side))
        hi = (rng.randint(lo[0], side), rng.randint(lo[1], side))
        assert sorted(t.range_search(lo, hi)) == sorted(
            p for p in model if lo[0] <= p[0] <= hi[0] and lo[1] <= p[1] <= hi[1]
        )
        q = (rng.randrange(-2, side + 2), rng.randrange(-2, side + 2))
        got = t.nearest(q)
        if not model:
            assert got is None
        else:
            assert got is not None and got in model
            d = lambda p: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
            assert d(got) == min(d(p) for p in model)
