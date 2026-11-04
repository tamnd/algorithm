# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pr-quadtree/. The authors are listed in prov/D4SJDH.jsonl.

import random

import pytest

from pr_quadtree import Node, PrQuadtree


def shape(u: Node) -> object:
    if u.children is None:
        return sorted(u.points)
    return {o: shape(c) for o, c in enumerate(u.children) if c.count}


def test_page_example() -> None:
    t = PrQuadtree(3, 1)
    for p in [(1, 6), (5, 5), (6, 7), (2, 1), (3, 2)]:
        assert t.insert(p)
        t.check_invariant()
    assert shape(t.root) == {
        0: {1: [(2, 1)], 3: [(3, 2)]},
        2: [(1, 6)],
        3: {0: [(5, 5)], 3: [(6, 7)]},
    }
    assert t.node_count() == 13 and t.height() == 2
    assert sorted(t.range_search((2, 1), (6, 5))) == [(2, 1), (3, 2), (5, 5)]
    assert t.delete((6, 7))
    t.check_invariant()
    assert shape(t.root) == {0: {1: [(2, 1)], 3: [(3, 2)]}, 2: [(1, 6)], 3: [(5, 5)]}
    assert t.node_count() == 9


def test_edges() -> None:
    t = PrQuadtree(0, 1)
    assert t.insert((0, 0)) and not t.insert((0, 0))
    with pytest.raises(ValueError):
        t.insert((0, 1))
    with pytest.raises(ValueError):
        PrQuadtree(2, 0)
    assert t.contains((0, 0)) and t.delete((0, 0)) and not t.delete((0, 0))
    assert len(t) == 0 and t.range_search((0, 0), (0, 0)) == []
    t.check_invariant()


def test_close_points_make_a_chain() -> None:
    t = PrQuadtree(12, 1)
    t.insert((0, 0))
    t.insert((1, 1))
    t.check_invariant()
    assert t.height() == 12 and t.node_count() == 1 + 4 * 12
    t.delete((0, 0))
    assert t.node_count() == 1


def test_order_does_not_matter() -> None:
    rng = random.Random(5)
    pts = list({(rng.randrange(32), rng.randrange(32)) for _ in range(120)})
    a, b = PrQuadtree(5, 2), PrQuadtree(5, 2)
    for p in pts:
        a.insert(p)
    rng.shuffle(pts)
    for p in pts:
        b.insert(p)
    assert shape(a.root) == shape(b.root)


@pytest.mark.parametrize("cap", [1, 3])
def test_random_against_set(cap: int) -> None:
    rng = random.Random(1979 + cap)
    for _ in range(300):
        depth = rng.randrange(0, 5)
        side = 1 << depth
        t = PrQuadtree(depth, cap)
        model: set[tuple[int, int]] = set()
        for _ in range(rng.randrange(1, 40)):
            p = (rng.randrange(side), rng.randrange(side))
            r = rng.random()
            if r < 0.55:
                assert t.insert(p) == (p not in model)
                model.add(p)
            elif r < 0.85:
                assert t.delete(p) == (p in model)
                model.discard(p)
            else:
                assert t.contains(p) == (p in model)
            lo = (rng.randrange(side), rng.randrange(side))
            hi = (lo[0] + rng.randrange(side), lo[1] + rng.randrange(side))
            want = sorted(q for q in model if lo[0] <= q[0] <= hi[0] and lo[1] <= q[1] <= hi[1])
            assert sorted(t.range_search(lo, hi)) == want
        t.check_invariant()
        assert sorted(t.points()) == sorted(model)
