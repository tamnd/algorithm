# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree/. The authors are listed in prov/AKGCFN.jsonl.

import random

import pytest

from octree import Node, Octree


def shape(u: Node) -> object:
    if u.children is None:
        return sorted(u.points)
    return {o: shape(c) for o, c in enumerate(u.children) if c.count}


def test_page_example() -> None:
    t = Octree(3, 1)
    for p in [(1, 1, 1), (6, 1, 2), (5, 2, 3), (2, 6, 6), (7, 7, 7)]:
        assert t.insert(p)
        t.check_invariant()
    assert shape(t.root) == {
        0: [(1, 1, 1)],
        1: {5: [(6, 1, 2)], 6: [(5, 2, 3)]},
        6: [(2, 6, 6)],
        7: [(7, 7, 7)],
    }
    assert t.node_count() == 17 and t.height() == 2
    assert sorted(t.range_search((4, 0, 0), (7, 3, 3))) == [(5, 2, 3), (6, 1, 2)]
    assert t.delete((5, 2, 3))
    t.check_invariant()
    assert shape(t.root) == {0: [(1, 1, 1)], 1: [(6, 1, 2)], 6: [(2, 6, 6)], 7: [(7, 7, 7)]}
    assert t.node_count() == 9


def test_edges() -> None:
    t = Octree(0, 1)
    assert t.insert((0, 0, 0))
    assert not t.insert((0, 0, 0))
    assert t.contains((0, 0, 0)) and len(t) == 1
    with pytest.raises(ValueError):
        t.insert((1, 0, 0))
    assert t.delete((0, 0, 0)) and not t.delete((0, 0, 0))
    assert len(t) == 0 and t.range_search((0, 0, 0), (0, 0, 0)) == []
    t.check_invariant()


def test_close_points_make_a_chain() -> None:
    t = Octree(10, 1)
    t.insert((0, 0, 0))
    t.insert((1, 1, 1))
    t.check_invariant()
    assert t.height() == 10 and t.node_count() == 1 + 8 * 10
    t.delete((1, 1, 1))
    t.check_invariant()
    assert t.node_count() == 1 and t.height() == 0


def test_shape_does_not_depend_on_order() -> None:
    rng = random.Random(7)
    pts = list({(rng.randrange(16), rng.randrange(16), rng.randrange(16)) for _ in range(60)})
    a, b = Octree(4, 3), Octree(4, 3)
    for p in pts:
        a.insert(p)
    rng.shuffle(pts)
    for p in pts:
        b.insert(p)
    assert shape(a.root) == shape(b.root)


@pytest.mark.parametrize("cap", [1, 2, 4])
def test_random_against_set(cap: int) -> None:
    rng = random.Random(1982 + cap)
    for _ in range(200):
        depth = rng.randrange(0, 5)
        side = 1 << depth
        t = Octree(depth, cap)
        model: set[tuple[int, int, int]] = set()
        for _ in range(rng.randrange(1, 40)):
            p = (rng.randrange(side), rng.randrange(side), rng.randrange(side))
            op = rng.random()
            if op < 0.55:
                assert t.insert(p) == (p not in model)
                model.add(p)
            elif op < 0.85:
                assert t.delete(p) == (p in model)
                model.discard(p)
            else:
                assert t.contains(p) == (p in model)
            lo = tuple(rng.randrange(side) for _ in range(3))
            hi = tuple(c + rng.randrange(side) for c in lo)
            want = sorted(q for q in model if all(lo[i] <= q[i] <= hi[i] for i in range(3)))
            assert sorted(t.range_search(lo, hi)) == want  # type: ignore[arg-type]
        t.check_invariant()
        assert sorted(t.points()) == sorted(model)
