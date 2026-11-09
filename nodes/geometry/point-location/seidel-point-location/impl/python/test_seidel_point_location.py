# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seidel-point-location/. The authors are listed in prov/TGEMGN.jsonl.

import math
import random
from fractions import Fraction

from seidel_point_location import SeidelLocator, dag_size, longest_path, orient


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


def harmonic(n):
    return sum(Fraction(1, i) for i in range(1, n + 1))


def test_against_linear_scan():
    rng = random.Random(1991)
    for trial in range(120):
        grid = rng.choice([2, 3, 4, 5])
        segs = random_subdivision(rng, rng.randint(0, 14), grid)
        loc = SeidelLocator(segs, seed=trial)
        assert len(loc.tm.trapezoids()) == 1 + len(segs) + len({p for s in segs for p in s})
        for q in query_points(grid):
            assert loc.locate(q) == reference(segs, q), (segs, q)


def test_degenerate_cases():
    segs = [((2, 0), (2, 4)), ((3, 2), (6, 2)), ((0, 6), (6, 6)), ((2, 4), (6, 6)), ((2, 4), (6, 2))]
    for seed in range(20):
        loc = SeidelLocator(segs, seed)
        for q in query_points(4):
            assert loc.locate(q) == reference(segs, q)
    assert SeidelLocator([], 0).locate((0, 0)) == ("face", None, None)


def test_expected_bounds_hold_on_average():
    # The proved bounds are 12 H_n nodes on a fixed query path and 12 n + 4 H_n created trapezoids.
    rng = random.Random(7)
    segs = random_subdivision(rng, 60, 14)
    n = len(segs)
    H = harmonic(n)
    queries = [(1, 1), (15, 14), (27, 3), (8, 20)]
    runs = 40
    path_total = {q: 0 for q in queries}
    created_total = 0
    for seed in range(runs):
        loc = SeidelLocator(segs, seed)
        created_total += loc.created()
        for q in queries:
            path_total[q] += loc.find(q)[1]
    assert created_total <= runs * (12 * n + 4 * H)
    for q in queries:
        assert path_total[q] <= runs * 12 * H


def test_rebuild_bounds_every_query():
    rng = random.Random(11)
    segs = random_subdivision(rng, 50, 12)
    n = len(segs)
    bound = math.ceil(6 * math.log(n + 1))
    loc = SeidelLocator(segs, seed=3, max_path=bound)
    assert longest_path(loc.tm.root) <= bound
    for q in query_points(12):
        ans, depth = loc.find(q)
        assert depth <= bound
        assert ans == reference(segs, q)


def test_dag_size_is_linear_on_average():
    rng = random.Random(13)
    for n in (20, 80):
        segs = random_subdivision(rng, n, 2 * n // 5 + 4)
        sizes = [dag_size(SeidelLocator(segs, seed).tm.root) for seed in range(10)]
        # leaves are the created trapezoids, and inner nodes are at most 3 per crossed trapezoid
        assert sum(sizes) / len(sizes) <= 4 * (12 * len(segs) + 4 * float(harmonic(len(segs))))


def test_example_all_orders():
    from itertools import permutations

    from seidel_point_location import TrapezoidalMap

    segs = [((0, 0), (8, 2)), ((4, 6), (8, 2)), ((0, 0), (4, 6)), ((2, 8), (10, 6))]
    created = paths = 0
    lengths = []
    for perm in permutations(range(4)):
        tm = TrapezoidalMap()
        for i in perm:
            tm.insert(segs[i])
        created += tm.created
        depth = tm.find((5, 3))[1]
        paths += depth
        lengths.append(depth)
        assert len(tm.trapezoids()) == 10
    assert Fraction(created, 24) == Fraction(50, 3)
    assert Fraction(paths, 24) == Fraction(17, 3)
    assert (min(lengths), max(lengths)) == (4, 7)
    assert 12 * harmonic(4) == 25 and 12 * 4 + 4 * harmonic(4) == Fraction(169, 3)
