# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-status-structure/. The authors are listed in prov/M4V0SH.jsonl.

import random
from fractions import Fraction

import pytest

from sweep_status_structure import Segment, SweepStatus, slope, y_at

A: Segment = ((0, 0), (10, 10))
B: Segment = ((0, 10), (10, 0))
C: Segment = ((1, 5), (3, 5))
D: Segment = ((2, 1), (6, 2))


def test_example() -> None:
    t = SweepStatus()
    t.set_x(0)
    t.insert(A)
    t.insert(B)
    assert t.items == [A, B]
    t.set_x(1)
    t.insert(C)
    assert t.items == [A, C, B]
    assert t.below(C) == A and t.above(C) == B
    t.set_x(2)
    t.insert(D)
    assert t.items == [D, A, C, B]
    assert t.neighbors_of_point(Fraction(3, 2)) == (D, A)
    t.set_x(3)
    t.delete(C)
    assert t.items == [D, A, B]
    t.check_invariant()
    t.set_x(4)
    assert t.neighbors_of_point(5) == (A, B)
    t.set_x(5)
    t.swap(A, B)
    assert t.items == [D, B, A]
    t.check_invariant()
    t.set_x(Fraction(11, 2))
    assert t.items == [D, B, A]
    t.check_invariant()
    t.set_x(6)
    t.delete(D)
    assert t.items == [B, A]
    t.set_x(10)
    t.delete(B)
    t.delete(A)
    assert len(t) == 0


def test_shared_endpoints_and_ties() -> None:
    p, q, r = ((0, 0), (4, 4)), ((0, 0), (4, 0)), ((0, 0), (4, -2))
    t = SweepStatus()
    t.set_x(0)
    for s in (p, q, r):
        t.insert(s)
    assert t.items == [r, q, p]  # same point, ordered by slope
    assert t.neighbors_of_point(0) == (None, None)
    assert t.neighbors_of_point(-1) == (None, r)
    t.set_x(4)
    t.delete(q)  # three segments end at different points
    assert t.items == [r, p]
    s2 = ((4, 4), (6, 0))
    t.delete(p)
    t.insert(s2)
    assert t.items == [r, s2]


def test_errors_and_empty() -> None:
    t = SweepStatus()
    t.set_x(0)
    assert t.neighbors_of_point(0) == (None, None)
    with pytest.raises(KeyError):
        t.delete(A)
    t.insert(A)
    assert t.above(A) is None and t.below(A) is None
    t.insert(B)
    with pytest.raises(ValueError):
        t.swap(A, B)  # they do not meet at x = 0
    big: Segment = ((-(2**62), -(2**62)), (2**62, 2**62 + 1))
    t.insert(big)
    t.check_invariant()


def brute_order(active: list[Segment], x: Fraction) -> list[Segment]:
    return sorted(active, key=lambda s: (y_at(s, x), slope(s)))


def orient(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]) -> int:
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def on_segment(p: tuple[int, int], s: Segment) -> bool:
    a, b = s
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def crossing(s: Segment, t: Segment) -> tuple[Fraction, Fraction] | None:
    """Proper crossing point of s and t, or None."""
    a, b = s
    c, d = t
    if orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0:
        den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
        u = Fraction((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0]), den)
        return (a[0] + u * (b[0] - a[0]), a[1] + u * (b[1] - a[1]))
    return None


def random_set(rng: random.Random, allow_crossings: bool) -> list[Segment]:
    """Segments in general position: no shared endpoint, no endpoint on another segment, no three through one point."""
    segs: list[Segment] = []
    for _ in range(rng.randrange(1, 9)):
        for _attempt in range(20):
            x1, x2 = sorted(rng.sample(range(12), 2))
            s = ((x1, rng.randrange(12)), (x2, rng.randrange(12)))
            ok = True
            for t in segs:
                if any(on_segment(p, t) for p in s) or any(on_segment(p, s) for p in t):
                    ok = False
                elif crossing(s, t) is not None and not allow_crossings:
                    ok = False
            if ok and allow_crossings:
                pts = [crossing(u, v) for i, u in enumerate(segs + [s]) for v in (segs + [s])[i + 1:]]
                pts = [p for p in pts if p is not None]
                ok = len(pts) == len(set(pts))
            if ok:
                segs.append(s)
                break
    return segs


def run_sweep(segs: list[Segment]) -> None:
    crossings = {}
    for i, s in enumerate(segs):
        for t in segs[i + 1:]:
            p = crossing(s, t)
            if p is not None:
                crossings[p] = (s, t)
    xs = sorted({Fraction(s[0][0]) for s in segs} | {Fraction(s[1][0]) for s in segs} | {p[0] for p in crossings})
    t = SweepStatus()
    active: list[Segment] = []
    for j, x in enumerate(xs):
        t.set_x(x)
        for s in segs:
            if s[1][0] == x:
                t.delete(s)
                active.remove(s)
                t.check_invariant()
        for p in sorted(p for p in crossings if p[0] == x):
            s, u = crossings[p]
            lower, upper = (s, u) if slope(s) > slope(u) else (u, s)
            assert t.above(lower) == upper
            t.swap(lower, upper)
            t.check_invariant()
        for s in segs:
            if s[0][0] == x:
                t.insert(s)
                active.append(s)
                t.check_invariant()
        assert t.items == brute_order(active, x)
        for s in active:
            i = t.items.index(s)
            assert t.below(s) == (t.items[i - 1] if i else None)
            assert t.above(s) == (t.items[i + 1] if i + 1 < len(t.items) else None)
        if j + 1 < len(xs):
            mid = (x + xs[j + 1]) / 2
            t.set_x(mid)
            t.check_invariant()
            assert t.items == brute_order(active, mid)
            y = Fraction(random.Random(j).randrange(-2, 26), 2)
            below = [s for s in active if y_at(s, mid) < y]
            above = [s for s in active if y_at(s, mid) > y]
            want_below = max(below, key=lambda s: y_at(s, mid)) if below else None
            want_above = min(above, key=lambda s: y_at(s, mid)) if above else None
            assert t.neighbors_of_point(y) == (want_below, want_above)
    assert len(t) == 0


def test_random_without_crossings() -> None:
    rng = random.Random(4096)
    for _ in range(500):
        run_sweep(random_set(rng, allow_crossings=False))


def test_random_with_crossing_events() -> None:
    rng = random.Random(8191)
    for _ in range(500):
        run_sweep(random_set(rng, allow_crossings=True))
