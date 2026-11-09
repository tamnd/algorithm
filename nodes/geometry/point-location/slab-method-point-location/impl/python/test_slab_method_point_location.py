# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slab-method-point-location/. The authors are listed in prov/T6VRZV.jsonl.

import random
from fractions import Fraction

from slab_method_point_location import SlabLocator, build_dcel, normalize, orient


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


def test_against_linear_scan():
    rng = random.Random(20240601)
    for trial in range(120):
        grid = rng.choice([2, 3, 4, 5])
        segs = random_subdivision(rng, rng.randint(0, 14), grid)
        loc = SlabLocator(segs)
        for q in query_points(grid):
            assert loc.locate(q) == reference(segs, q), (segs, q)


def test_degenerate_cases():
    # a vertical segment, a horizontal one, and queries with the x of a vertex
    segs = [((2, 0), (2, 4)), ((3, 2), (6, 2)), ((0, 6), (6, 6))]
    loc = SlabLocator(segs)
    assert loc.locate((2, 0)) == ("vertex", (2, 0))
    assert loc.locate((2, 3)) == ("edge", 0)
    assert loc.locate((4, 2)) == ("edge", 1)
    # same x as the vertical segment, above it: under the shear q is right of (2, 4),
    # so the downward ray misses the vertical segment
    assert loc.locate((2, 5)) == ("face", 2, None)
    # below it: under the shear q is left of (2, 0)
    assert loc.locate((2, -1)) == ("face", 2, None)
    # same x as the vertex (3, 2), below and above it
    assert loc.locate((3, 1)) == ("face", 2, None)
    assert loc.locate((3, 3)) == ("face", 2, 1)
    for q in query_points(3):
        assert loc.locate(q) == reference(segs, q)


def test_small_inputs():
    assert SlabLocator([]).locate((0, 0)) == ("face", None, None)
    loc = SlabLocator([((0, 0), (4, 0))])
    assert loc.locate((2, 1)) == ("face", None, 0)
    assert loc.locate((2, -1)) == ("face", 0, None)
    assert loc.locate((5, 0)) == ("face", None, None)


def test_quadratic_storage():
    # m long horizontal segments and m short segments below them, at distinct x
    for m in (4, 8, 16):
        L = 4 * m + 4
        long_segs = [((0, 10 + 2 * j), (L, 10 + 2 * j)) for j in range(m)]
        short = [((4 * k + 1, 0), (4 * k + 2, 0)) for k in range(m)]
        loc = SlabLocator(long_segs + short)
        assert loc.storage() >= m * m


def faces_from_answer(dcel, ans):
    above, below = ans[1], ans[2]
    f_above = dcel["face"][2 * above + 1] if above is not None else None
    f_below = dcel["face"][2 * below] if below is not None else None
    return f_above, f_below


def components(segs):
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in segs:
        parent.setdefault(a, a)
        parent.setdefault(b, b)
        parent[find(a)] = find(b)
    return len({find(v) for v in parent})


def test_dcel_invariants_and_faces():
    rng = random.Random(77)
    for trial in range(120):
        grid = rng.choice([2, 3, 4])
        segs = random_subdivision(rng, rng.randint(1, 12), grid)
        d = build_dcel(segs)
        tw, nx, pv, org, fc = d["twin"], d["next"], d["prev"], d["origin"], d["face"]
        for h in range(len(tw)):
            assert tw[tw[h]] == h and tw[h] != h
            assert org[nx[h]] == org[tw[h]]
            assert pv[nx[h]] == h and nx[pv[h]] == h
            assert fc[nx[h]] == fc[h]
        V, E, F, C = len(d["vertices"]), len(segs), d["faces"], components(segs)
        assert V - E + F == 1 + C
        loc = SlabLocator(segs)
        pts = query_points(grid)
        label = {}
        for q in pts:
            ans = loc.locate(q)
            if ans[0] != "face":
                continue
            fa, fb = faces_from_answer(d, ans)
            if fa is not None and fb is not None:
                assert fa == fb
            label[q] = fa if fa is not None else (fb if fb is not None else 0)
        # two points joined by an open segment that meets no segment lie in one face
        faces = list(label)
        for _ in range(300):
            p, q = rng.choice(faces), rng.choice(faces)
            if p == q:
                continue
            if all(not closed_intersect(p, q, a, b) for a, b in segs):
                assert label[p] == label[q]


def test_example():
    segs = [((0, 0), (8, 2)), ((4, 6), (8, 2)), ((0, 0), (4, 6)), ((2, 8), (10, 6))]
    loc = SlabLocator(segs)
    assert loc.X == [(0, 0), (2, 8), (4, 6), (8, 2), (10, 6)]
    assert loc.slabs == [[0, 2], [0, 2, 3], [0, 1, 3], [3]]
    assert loc.storage() == 9
    assert orient((4, 6), (8, 2), (5, 3)) == -8 and orient((0, 0), (8, 2), (5, 3)) == 14
    assert loc.locate((5, 3)) == ("face", 1, 0)
    assert loc.locate((4, 6)) == ("vertex", (4, 6))
    assert loc.locate((6, 7)) == ("edge", 3)
    assert loc.locate((4, 7)) == ("face", 3, 1)
    assert loc.locate((1, 5)) == ("face", None, 2)
    assert loc.locate((9, 4)) == ("face", 3, None)
