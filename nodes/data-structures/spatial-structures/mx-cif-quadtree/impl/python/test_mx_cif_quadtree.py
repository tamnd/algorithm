# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mx-cif-quadtree/. The authors are listed in prov/RHN2XW.jsonl.

import random

import pytest

from mx_cif_quadtree import MxCifQuadtree, Node, intersects


def shape(u: Node) -> object:
    kids = {o: shape(c) for o, c in enumerate(u.children) if c is not None}
    return (sorted(u.rects), kids)


def smallest_cell(depth: int, r: tuple[int, int, int, int]) -> tuple[int, int, int]:
    """Oracle: the smallest aligned cell that holds r, by trying sizes from small to large."""
    for k in range(depth + 1):
        s = 1 << k
        x, y = (r[0] // s) * s, (r[1] // s) * s
        if r[2] <= x + s and r[3] <= y + s:
            return x, y, s
    raise AssertionError


def test_page_example() -> None:
    t = MxCifQuadtree(3)
    A, B, C, D, E = (1, 2, 7, 5), (5, 5, 7, 7), (0, 0, 1, 1), (1, 6, 3, 8), (4, 0, 8, 4)
    for r in [A, B, C, D, E]:
        assert t.insert(r)
        t.check_invariant()
    assert not t.insert(A)
    assert shape(t.root) == (
        [A],
        {
            0: ([], {0: ([], {0: ([C], {})})}),
            1: ([E], {}),
            2: ([D], {}),
            3: ([B], {}),
        },
    )
    assert t.node_count() == 7
    assert sorted(t.window((5, 1, 6, 6))) == sorted([A, B, E])
    assert t.stab((2, 7)) == [D]
    assert sorted(t.stab((5, 3))) == sorted([A, E])
    assert t.delete(C) and not t.delete(C)
    t.check_invariant()
    assert t.node_count() == 4


def test_edges() -> None:
    t = MxCifQuadtree(0)
    assert t.insert((0, 0, 1, 1)) and t.node_count() == 1
    assert t.stab((0, 0)) == [(0, 0, 1, 1)]
    assert t.delete((0, 0, 1, 1)) and len(t) == 0
    with pytest.raises(ValueError):
        t.insert((0, 0, 0, 1))
    with pytest.raises(ValueError):
        t.insert((0, 0, 2, 1))
    with pytest.raises(ValueError):
        MxCifQuadtree(-1)
    u = MxCifQuadtree(10)
    assert u.insert((0, 0, 1, 1)) and u.node_count() == 11
    assert u.insert((511, 0, 513, 1)) and u.root.rects == [(511, 0, 513, 1)]
    assert not u.delete((5, 5, 6, 6))
    assert u.delete((0, 0, 1, 1)) and u.node_count() == 1


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for case in range(600):
        depth = rng.randint(0, 5)
        side = 1 << depth
        t = MxCifQuadtree(depth)
        live: set[tuple[int, int, int, int]] = set()
        for _ in range(rng.randint(1, 40)):
            x1, x2 = sorted(rng.sample(range(side + 1), 2))
            y1, y2 = sorted(rng.sample(range(side + 1), 2))
            if rng.random() < 0.5:
                w = rng.randint(1, max(1, side // 4))
                h = rng.randint(1, max(1, side // 4))
                x1, y1 = rng.randrange(side - w + 1), rng.randrange(side - h + 1)
                x2, y2 = x1 + w, y1 + h
            r = (x1, y1, x2, y2)
            if live and rng.random() < 0.3:
                d = rng.choice(sorted(live))
                assert t.delete(d)
                live.discard(d)
            assert t.insert(r) == (r not in live)
            live.add(r)
        t.check_invariant()
        assert sorted(t.rects()) == sorted(live)
        stack = [t.root]
        while stack:
            u = stack.pop()
            for r in u.rects:
                assert smallest_cell(depth, r) == (u.x, u.y, u.size)
            stack.extend(c for c in u.children if c is not None)
        u2 = MxCifQuadtree(depth)
        for r in rng.sample(sorted(live), len(live)):
            u2.insert(r)
        assert shape(u2.root) == shape(t.root)
        x1, x2 = sorted(rng.sample(range(side + 1), 2))
        y1, y2 = sorted(rng.sample(range(side + 1), 2))
        q = (x1, y1, x2, y2)
        assert sorted(t.window(q)) == sorted(r for r in live if intersects(r, q))
        p = (rng.randrange(side), rng.randrange(side))
        want = [r for r in live if r[0] <= p[0] < r[2] and r[1] <= p[1] < r[3]]
        assert sorted(t.stab(p)) == sorted(want)
