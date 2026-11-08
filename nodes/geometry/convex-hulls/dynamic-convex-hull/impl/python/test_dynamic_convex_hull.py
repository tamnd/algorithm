# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-convex-hull/. The authors are listed in prov/WCEQ10.jsonl.

from __future__ import annotations

import random

from dynamic_convex_hull import DynamicConvexHull, bridge, chain_points, merge, monotone_chains, orient

Point = tuple[int, int]


def brute_hull(points: set[Point]) -> list[Point]:
    """Hull vertices counterclockwise from the smallest point, by checking every ordered pair.

    (p, q) is a hull edge when every other point is strictly left of pq or strictly inside the
    segment pq. Cost: O(n^3).
    """
    pts = sorted(points)
    if len(pts) <= 1:
        return pts
    nxt: dict[Point, Point] = {}
    for p in pts:
        for q in pts:
            if p == q:
                continue
            ok = True
            for r in pts:
                if r == p or r == q:
                    continue
                d = orient(p, q, r)
                if d < 0:
                    ok = False
                    break
                if d == 0 and not min(p, q) < r < max(p, q):
                    ok = False
                    break
            if ok:
                nxt[p] = q
    start = pts[0]
    out = [start]
    v = nxt[start]
    while v != start:
        out.append(v)
        v = nxt[v]
    return out


def test_example() -> None:
    h = DynamicConvexHull(seed=7)
    steps: list[tuple[str, Point, list[Point]]] = [
        ("+", (0, 0), [(0, 0)]),
        ("+", (6, 0), [(0, 0), (6, 0)]),
        ("+", (3, 4), [(0, 0), (6, 0), (3, 4)]),
        ("+", (3, 1), [(0, 0), (6, 0), (3, 4)]),
        ("+", (0, 4), [(0, 0), (6, 0), (3, 4), (0, 4)]),
        ("+", (7, 3), [(0, 0), (6, 0), (7, 3), (3, 4), (0, 4)]),
        ("-", (3, 4), [(0, 0), (6, 0), (7, 3), (0, 4)]),
        ("-", (0, 0), [(0, 4), (3, 1), (6, 0), (7, 3)]),
        ("-", (3, 1), [(0, 4), (6, 0), (7, 3)]),
    ]
    for op, p, want in steps:
        assert (h.insert(p) if op == "+" else h.delete(p))
        assert h.hull() == want
        h.check_invariant()
    assert len(h) == 3 and (6, 0) in h and (0, 0) not in h


def test_empty_duplicates_and_lines() -> None:
    h = DynamicConvexHull()
    assert h.hull() == [] and len(h) == 0
    assert not h.delete((1, 1))
    assert h.insert((1, 1)) and not h.insert((1, 1))
    assert h.hull() == [(1, 1)]
    for p in [(3, 3), (2, 2), (-1, -1), (0, 0)]:
        h.insert(p)
    h.check_invariant()
    assert h.hull() == [(-1, -1), (3, 3)]
    v = DynamicConvexHull()
    for y in [5, -2, 0, 9, 3]:
        v.insert((4, y))
    assert v.hull() == [(4, -2), (4, 9)]
    v.insert((5, 0))
    assert v.hull() == [(4, -2), (5, 0), (4, 9)]
    v.delete((5, 0))
    v.delete((4, -2))
    assert v.hull() == [(4, 0), (4, 9)]
    v.check_invariant()
    assert h.delete((1, 1)) and not h.delete((1, 1))


def test_bridge_directly() -> None:
    a = DynamicConvexHull()
    b = DynamicConvexHull(seed=1)
    for p in [(0, 0), (1, 3), (2, 4), (3, 3), (4, 1)]:
        a.insert(p)
    for p in [(5, 0), (6, 5), (8, 6), (9, 2)]:
        b.insert(p)
    assert a.root is not None and b.root is not None
    assert bridge(a.root.up, b.root.up, 1) == ((2, 4), (8, 6))
    assert bridge(a.root.low, b.root.low, -1) == ((0, 0), (5, 0))
    assert chain_points(merge(a.root.up, b.root.up, 1)) == [(0, 0), (1, 3), (2, 4), (8, 6), (9, 2)]


def run_ops(rng: random.Random, n_ops: int, span: int, check_every: int) -> None:
    h = DynamicConvexHull(seed=rng.randrange(1 << 30))
    model: set[Point] = set()
    for step in range(n_ops):
        if model and rng.random() < 0.4:
            p = rng.choice(sorted(model)) if rng.random() < 0.9 else (rng.randint(0, span), rng.randint(0, span))
            assert h.delete(p) == (p in model)
            model.discard(p)
        else:
            p = (rng.randint(0, span), rng.randint(0, span))
            assert h.insert(p) == (p not in model)
            model.add(p)
        assert len(h) == len(model)
        assert h.hull() == brute_hull(model)
        if step % check_every == 0:
            h.check_invariant()
    h.check_invariant()


def test_random_small_grid() -> None:
    rng = random.Random(1981)
    for _ in range(700):
        run_ops(rng, rng.randint(1, 25), rng.choice([1, 2, 3, 5, 8, 20]), 4)


def test_random_collinear_heavy() -> None:
    rng = random.Random(1982)
    for _ in range(150):
        h = DynamicConvexHull(seed=rng.randrange(1000))
        model: set[Point] = set()
        dx, dy = rng.choice([(1, 0), (0, 1), (1, 1), (2, -1), (1, 3)])
        for _ in range(20):
            t = rng.randint(-6, 6)
            off = rng.choice([0, 0, 0, 1, -1])
            p = (t * dx - off * dy, t * dy + off * dx)
            if p in model and rng.random() < 0.7:
                h.delete(p)
                model.discard(p)
            else:
                h.insert(p)
                model.add(p)
            assert h.hull() == brute_hull(model)
        h.check_invariant()


def test_random_large() -> None:
    rng = random.Random(1983)
    for _ in range(4):
        h = DynamicConvexHull(seed=rng.randrange(1000))
        model: set[Point] = set()
        for step in range(600):
            if model and rng.random() < 0.45:
                p = rng.choice(sorted(model))
                h.delete(p)
                model.discard(p)
            else:
                p = (rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6))
                h.insert(p)
                model.add(p)
            if step % 25 == 0:
                lower, upper = monotone_chains(sorted(model))
                want = lower + upper[-2:0:-1] if len(model) > 1 else sorted(model)
                assert h.hull() == want
        h.check_invariant()
