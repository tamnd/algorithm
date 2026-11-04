# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-b-tree/. The authors are listed in prov/TMRMPW.jsonl.

import random

import pytest

from kd_b_tree import INF, KdBTree, Page


def shape(u: Page) -> object:
    box = (u.lo, u.hi)
    if u.children is None:
        return (box, sorted(u.points))
    return (box, [shape(c) for c in u.children])


def test_page_example() -> None:
    t = KdBTree(1, 4)
    for p in [(3, 1), (5, 1), (5, 8), (7, 7)]:
        assert t.insert(p)
        t.check_invariant()
    assert t.height() == 1 and len(t.root.children) == 4
    assert t.insert((7, 8))
    t.check_invariant()
    assert not t.insert((7, 8))
    assert t.height() == 2
    assert shape(t.root) == (
        ((-INF, -INF), (INF, INF)),
        [
            (
                ((-INF, -INF), (INF, 8)),
                [
                    (((-INF, -INF), (5, 8)), [(3, 1)]),
                    (((5, -INF), (INF, 7)), [(5, 1)]),
                    (((5, 7), (INF, 8)), [(7, 7)]),
                ],
            ),
            (
                ((-INF, 8), (INF, INF)),
                [
                    (((-INF, 8), (5, INF)), []),
                    (((5, 8), (7, INF)), [(5, 8)]),
                    (((7, 8), (INF, INF)), [(7, 8)]),
                ],
            ),
        ],
    )
    assert sorted(t.range_search((4, 0), (6, 9))) == [(5, 1), (5, 8)]
    assert t.delete((3, 1)) and not t.delete((3, 1))
    t.check_invariant()
    assert len(t) == 4 and t.height() == 2


def test_edges() -> None:
    t = KdBTree(1, 2)
    assert t.range_search((0, 0), (9, 9)) == [] and (1, 1) not in t
    for i in range(64):
        assert t.insert((i, i))
        t.check_invariant()
    assert sorted(t.range_search((10, 10), (12, 12))) == [(10, 10), (11, 11), (12, 12)]
    assert t.height() >= 6
    u = KdBTree(2, 3)
    for i in range(30):
        u.insert((5, i))
    u.check_invariant()
    with pytest.raises(ValueError):
        KdBTree(0, 3)
    with pytest.raises(ValueError):
        KdBTree(2, 1)


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for case in range(600):
        t = KdBTree(rng.randint(1, 4), rng.randint(2, 6))
        live: set = set()
        span = rng.choice([5, 20, 1000])
        for _ in range(rng.randint(1, 60)):
            p = (rng.randrange(span), rng.randrange(span))
            if live and rng.random() < 0.2:
                d = rng.choice(sorted(live))
                assert d in t and t.delete(d)
                live.discard(d)
            assert t.insert(p) == (p not in live)
            live.add(p)
        t.check_invariant()
        assert sorted(t.points()) == sorted(live)
        for _ in range(3):
            x0, x1 = sorted(rng.randrange(-1, span + 1) for _ in range(2))
            y0, y1 = sorted(rng.randrange(-1, span + 1) for _ in range(2))
            want = sorted(q for q in live if x0 <= q[0] <= x1 and y0 <= q[1] <= y1)
            assert sorted(t.range_search((x0, y0), (x1, y1))) == want
