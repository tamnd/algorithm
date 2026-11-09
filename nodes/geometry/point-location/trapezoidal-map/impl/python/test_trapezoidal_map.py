# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapezoidal-map/. The authors are listed in prov/S5KEK2.jsonl.

import random
from fractions import Fraction

from trapezoidal_map import TrapezoidalMap, build, locate, orient


def normalize(seg):
    a, b = seg
    return (a, b) if a < b else (b, a)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def on_closed(a, b, p):
    return orient(a, b, p) == 0 and min(a, b) <= p <= max(a, b)


def closed_intersect(a, b, c, d):
    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return on_closed(a, b, c) or on_closed(a, b, d) or on_closed(c, d, a) or on_closed(c, d, b)


def compatible(s, t):
    """True if s and t are disjoint or meet only at one shared end point."""
    (a, b), (c, d) = s, t
    shared = {a, b} & {c, d}
    if len(shared) == 2:
        return False
    if len(shared) == 1:
        e = shared.pop()
        f = b if a == e else a
        g = d if c == e else c
        u, w = (f[0] - e[0], f[1] - e[1]), (g[0] - e[0], g[1] - e[1])
        return not (orient(e, f, g) == 0 and dot(u, w) > 0)
    return not closed_intersect(a, b, c, d)


def random_subdivision(rng, n, grid):
    """Up to n non-crossing segments with end points on the even points of a grid."""
    segs = []
    tries = 0
    while len(segs) < n and tries < 40 * n:
        tries += 1
        a = (2 * rng.randint(0, grid), 2 * rng.randint(0, grid))
        b = (2 * rng.randint(0, grid), 2 * rng.randint(0, grid))
        if a == b:
            continue
        s = normalize((a, b))
        if all(compatible(s, t) for t in segs):
            segs.append(s)
    return segs


def reference(segs, q):
    """Linear scan: the answer under the symbolic shear (x, y) -> (x + eps y, y)."""
    segs = [normalize(s) for s in segs]
    for a, b in segs:
        if q == a or q == b:
            return ("vertex", q)
    for i, (a, b) in enumerate(segs):
        if on_closed(a, b, q):
            return ("edge", i)
    above = below = None
    for i, (a, b) in enumerate(segs):
        if not (a < q < b):
            continue
        # here a[0] < b[0]: a vertical segment spanning q would contain q
        y = a[1] + Fraction(b[1] - a[1], b[0] - a[0]) * (q[0] - a[0])
        slope = Fraction(b[1] - a[1], b[0] - a[0])
        if y > q[1]:
            if above is None or (y, -slope) < above[0]:
                above = ((y, -slope), i)
        else:
            if below is None or (y, slope) > below[0]:
                below = ((y, slope), i)
    return ("face", above and above[1], below and below[1])


def query_points(grid):
    return [(x, y) for x in range(-1, 2 * grid + 2) for y in range(-1, 2 * grid + 2)]


def query_points(grid):
    return [(x, y) for x in range(-1, 2 * grid + 2) for y in range(-1, 2 * grid + 2)]


def seg_below(tm, s, t):
    """True if segment s is below segment t on their common open lexicographic range."""
    (a, b), (c, d) = tm.segs[s], tm.segs[t]
    if c >= a:
        o = orient(a, b, c)
        if o == 0:
            o = orient(a, b, d)
        return o > 0
    o = orient(c, d, a)
    if o == 0:
        o = orient(c, d, b)
    return o < 0


def check_invariant(tm):
    traps = tm.trapezoids()
    alive = {id(t) for t in traps}
    n, m = len(tm.segs), len(tm.points)
    assert len(traps) == 1 + n + m
    for t in traps:
        lp, rp = t.leftp, t.rightp
        if lp is not None and rp is not None:
            assert lp < rp
        for s in (t.top, t.bottom):
            if s is not None:
                a, b = tm.segs[s]
                assert lp is not None and rp is not None
                assert a <= lp and rp <= b
        if t.top is not None and t.bottom is not None:
            assert seg_below(tm, t.bottom, t.top)
        # left slots
        if lp is None:
            assert t.ul is None and t.ll is None
        else:
            bs = t.bottom is not None and tm.segs[t.bottom][0] == lp
            ts = t.top is not None and tm.segs[t.top][0] == lp
            assert (t.ll is None) == bs and (t.ul is None) == ts
        if rp is None:
            assert t.ur is None and t.lr is None
        else:
            be = t.bottom is not None and tm.segs[t.bottom][1] == rp
            te = t.top is not None and tm.segs[t.top][1] == rp
            assert (t.lr is None) == be and (t.ur is None) == te
        for u in (t.ul, t.ll, t.ur, t.lr):
            assert u is None or id(u) in alive
        if t.ul is not None:
            assert t.ul.rightp == lp and t.ul.top == t.top and t.ul.ur is t
        if t.ll is not None:
            assert t.ll.rightp == lp and t.ll.bottom == t.bottom and t.ll.lr is t
        if t.ur is not None:
            assert t.ur.leftp == rp and t.ur.top == t.top and t.ur.ul is t
        if t.lr is not None:
            assert t.lr.leftp == rp and t.lr.bottom == t.bottom and t.lr.ll is t
    return traps


def in_trap(tm, t, q):
    if t.leftp is not None and not t.leftp < q:
        return False
    if t.rightp is not None and not q < t.rightp:
        return False
    if t.top is not None:
        a, b = tm.segs[t.top]
        if orient(a, b, q) >= 0:
            return False
    if t.bottom is not None:
        a, b = tm.segs[t.bottom]
        if orient(a, b, q) <= 0:
            return False
    return True


def test_against_linear_scan():
    rng = random.Random(1991)
    for trial in range(120):
        grid = rng.choice([2, 3, 4, 5])
        segs = random_subdivision(rng, rng.randint(0, 14), grid)
        tm = build(segs, seed=trial)
        traps = check_invariant(tm)
        for q in query_points(grid):
            ans = locate(tm, q)
            assert ans == reference(segs, q), (segs, q)
            if ans[0] == "face":
                hits = [t for t in traps if in_trap(tm, t, q)]
                assert len(hits) == 1
                assert tm.locate(q) == ("face", hits[0].top, hits[0].bottom)


def test_invariant_after_each_insertion():
    rng = random.Random(6)
    for trial in range(60):
        segs = random_subdivision(rng, rng.randint(1, 16), rng.choice([3, 4, 5]))
        rng.shuffle(segs)
        tm = TrapezoidalMap()
        for s in segs:
            tm.insert(s)
            check_invariant(tm)


def test_degenerate_cases():
    # vertical segments, a star at one vertex, horizontal segments, shared end points
    segs = [((2, 0), (2, 4)), ((3, 2), (6, 2)), ((0, 6), (6, 6)), ((2, 4), (6, 6)), ((2, 4), (6, 2))]
    star = [((4, 4), (4 + dx, 4 + dy)) for dx, dy in [(4, 0), (4, 4), (0, 4), (-4, 4), (-4, 0), (-4, -4), (0, -4), (4, -4), (4, 2)]]
    for case in (segs, star):
        for seed in range(10):
            tm = build(case, seed)
            check_invariant(tm)
            for q in query_points(5):
                assert locate(tm, q) == reference(case, q)
    tm = build([], 0)
    assert locate(tm, (0, 0)) == ("face", None, None)


def test_example():
    segs = [((0, 0), (8, 2)), ((4, 6), (8, 2)), ((0, 0), (4, 6)), ((2, 8), (10, 6))]
    tm = build(segs)  # insertion order s0, s1, s2, s3
    counts = []
    tm2 = TrapezoidalMap()
    for s in segs:
        tm2.insert(s)
        counts.append(len(tm2.trapezoids()))
    assert counts == [4, 6, 7, 10]
    assert len(tm.trapezoids()) == 1 + 4 + 5
    assert locate(tm, (5, 3)) == ("face", 1, 0)
    assert locate(tm, (4, 7)) == ("face", 3, 1)
    assert locate(tm, (6, 7)) == ("edge", 3)
    assert locate(tm, (4, 6)) == ("vertex", (4, 6))


def test_larger_subdivisions():
    rng = random.Random(2008)
    for trial in range(15):
        segs = random_subdivision(rng, 40, 8)
        tm = build(segs, seed=100 + trial)
        check_invariant(tm)
        for q in query_points(8):
            assert locate(tm, q) == reference(segs, q)
