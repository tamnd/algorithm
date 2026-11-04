# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bsp-tree/. The authors are listed in prov/MSZB1N.jsonl.

import random
from fractions import Fraction as F
from typing import Optional

import pytest

from bsp_tree import BspTree, Node, Point, Segment, side


def fmt(s: Segment) -> str:
    return "(%s,%s)-(%s,%s)" % (s[0][0], s[0][1], s[1][0], s[1][1])


def shape(t: Optional[Node]) -> object:
    if t is None:
        return None
    return ([fmt(s) for s in t.on], shape(t.front), shape(t.back))


A = ((0, 0), (4, 0))
B = ((2, -2), (2, 2))
C = ((5, -1), (5, 3))
D = ((-1, 3), (3, 4))


def test_page_example() -> None:
    t = BspTree([A, B, C, D])
    t.check_invariant()
    assert shape(t.root) == (
        ["(0,0)-(4,0)"],
        (["(2,0)-(2,2)"], (["(-1,3)-(2,15/4)"], None, None),
         (["(5,0)-(5,3)"], (["(2,15/4)-(3,4)"], None, None), None)),
        (["(2,-2)-(2,0)"], None, (["(5,-1)-(5,0)"], None, None)),
    )
    assert t.size() == 7 and t.height() == 4
    assert [fmt(s) for s in t.back_to_front((3, -3))] == [
        "(-1,3)-(2,15/4)", "(2,0)-(2,2)", "(5,0)-(5,3)", "(2,15/4)-(3,4)",
        "(0,0)-(4,0)", "(2,-2)-(2,0)", "(5,-1)-(5,0)",
    ]


def test_edges() -> None:
    t = BspTree([])
    assert t.root is None and t.back_to_front((0, 0)) == []
    with pytest.raises(ValueError):
        BspTree([((1, 1), (1, 1))])
    t.insert(((0, 0), (1, 0)))
    t.insert(((2, 0), (3, 0)))  # on the same line
    t.check_invariant()
    assert t.size() == 2 and t.height() == 1
    assert len(t.back_to_front((5, 0))) == 2


def test_chain_is_deep_but_iterative() -> None:
    n = 200
    segs = [((0, i), (1, i)) for i in range(n)]
    t = BspTree(segs)
    assert t.height() == n and t.size() == n
    order = t.back_to_front((F(1, 2), -1))
    assert [s[0][1] for s in order] == list(range(n - 1, -1, -1))


def _cross(o: Point, a: Point, b: Point) -> F:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _proper(p: Point, q: Point, r: Point, s: Point) -> bool:
    """Whether segments pq and rs meet at a point interior to both."""
    d1, d2 = _cross(p, q, r), _cross(p, q, s)
    d3, d4 = _cross(r, s, p), _cross(r, s, q)
    return d1 * d2 < 0 and d3 * d4 < 0


def _touch(p: Point, q: Point, r: Point, s: Point) -> bool:
    """Whether closed segments pq and rs meet."""
    def on(a: Point, b: Point, c: Point) -> bool:
        return (_cross(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
                and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))
    d1, d2 = _cross(p, q, r), _cross(p, q, s)
    d3, d4 = _cross(r, s, p), _cross(r, s, q)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return on(p, q, r) or on(p, q, s) or on(r, s, p) or on(r, s, q)


def _random_scene(rng: random.Random, n: int) -> list[Segment]:
    segs: list[Segment] = []
    while len(segs) < n:
        p = (F(rng.randrange(21)), F(rng.randrange(21)))
        q = (F(rng.randrange(21)), F(rng.randrange(21)))
        if p == q or any(_touch(p, q, a, b) for a, b in segs):
            continue
        segs.append((p, q))
    return segs


def _param(s: Segment, p: Point) -> F:
    (ax, ay), (bx, by) = s
    return (p[0] - ax) / (bx - ax) if bx != ax else (p[1] - ay) / (by - ay)


def test_random_against_oracle() -> None:
    rng = random.Random(1980)
    for case in range(500):
        segs = _random_scene(rng, rng.randrange(1, 9))
        t = BspTree(segs, seed=case if case % 2 else None)
        t.check_invariant()
        frags = t.fragments()
        # The fragments of each segment tile it exactly.
        for s in segs:
            parts = []
            for f in frags:
                if side(s, f[0]) == 0 and side(s, f[1]) == 0:
                    a, b = sorted((_param(s, f[0]), _param(s, f[1])))
                    if a >= 0 and b <= 1:
                        parts.append((a, b))
            parts.sort()
            assert parts[0][0] == 0 and parts[-1][1] == 1
            assert all(parts[i][1] == parts[i + 1][0] for i in range(len(parts) - 1))
        # Painter's order: no earlier fragment hides a point of a later one.
        v = (F(rng.randrange(-5, 26)), F(rng.randrange(-5, 26)))
        order = t.back_to_front(v)
        assert sorted(map(fmt, order)) == sorted(map(fmt, frags))
        for i in range(len(order)):
            for j in range(i + 1, len(order)):
                p, q = order[j]
                for w in (F(1, 4), F(1, 2), F(3, 4)):
                    y = (p[0] + w * (q[0] - p[0]), p[1] + w * (q[1] - p[1]))
                    assert not _proper(v, y, order[i][0], order[i][1])
