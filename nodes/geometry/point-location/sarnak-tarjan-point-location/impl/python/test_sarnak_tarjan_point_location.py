# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sarnak-tarjan-point-location/. The authors are listed in prov/SN1BV9.jsonl.

import random
from fractions import Fraction

from sarnak_tarjan_point_location import PersistentAVL, SarnakTarjanLocator, _h, inorder, normalize, orient, seg_cmp


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


def expected_slab(segs, u, v):
    """The segments spanning (u, v), sorted by y at the middle x, when u and v have distinct x."""
    span = [i for i, (a, b) in enumerate(segs) if a <= u and v <= b]
    if u[0] == v[0]:
        return set(span), None
    xm = Fraction(u[0] + v[0], 2)

    def y_at(i):
        a, b = segs[i]
        return a[1] + Fraction(b[1] - a[1], b[0] - a[0]) * (xm - a[0])

    return set(span), sorted(span, key=y_at)


def test_against_linear_scan():
    rng = random.Random(1986)
    for trial in range(120):
        grid = rng.choice([2, 3, 4, 5])
        segs = random_subdivision(rng, rng.randint(0, 14), grid)
        loc = SarnakTarjanLocator(segs)
        for q in query_points(grid):
            assert loc.locate(q) == reference(segs, q), (segs, q)


def test_versions_are_the_slabs():
    rng = random.Random(42)
    for trial in range(150):
        grid = rng.choice([3, 4, 5, 6])
        segs = random_subdivision(rng, rng.randint(1, 18), grid)
        loc = SarnakTarjanLocator(segs)
        X = loc.X
        assert len(loc.roots) == len(X) - 1
        for i, root in enumerate(loc.roots):
            got = inorder(root)
            span, order = expected_slab(segs, X[i], X[i + 1])
            assert set(got) == span and len(got) == len(span)
            if order is not None:
                assert got == order


def test_avl_balance_and_path_copying():
    rng = random.Random(5)
    segs = [((0, 2 * j), (100, 2 * j + 1)) for j in range(200)]
    tree = PersistentAVL(lambda i, j: seg_cmp(segs[i], segs[j]))
    roots = [None]
    order = list(range(200))
    rng.shuffle(order)
    for i in order:
        roots.append(tree.insert(roots[-1], i))
    for i in order[:100]:
        roots.append(tree.delete(roots[-1], i))
    # every version is intact and balanced
    present: set[int] = set()
    for k, root in enumerate(roots):
        if 1 <= k <= 200:
            present.add(order[k - 1])
        elif k > 200:
            present.discard(order[k - 201])
        assert inorder(root) == sorted(present)
        stack = [root] if root else []
        while stack:
            t = stack.pop()
            assert abs(_h(t.left) - _h(t.right)) <= 1
            stack.extend(c for c in (t.left, t.right) if c)
    # path copying: O(log n) new nodes per update
    assert tree.created <= 300 * 4 * 9


def test_degenerate_cases():
    segs = [((2, 0), (2, 4)), ((3, 2), (6, 2)), ((0, 6), (6, 6))]
    loc = SarnakTarjanLocator(segs)
    assert loc.locate((2, 0)) == ("vertex", (2, 0))
    assert loc.locate((2, 3)) == ("edge", 0)
    assert loc.locate((4, 2)) == ("edge", 1)
    assert loc.locate((2, 5)) == ("face", 2, None)
    assert loc.locate((3, 3)) == ("face", 2, 1)
    assert SarnakTarjanLocator([]).locate((0, 0)) == ("face", None, None)
    # many segments from one vertex, and a fan of vertical and horizontal edges
    fan = [((0, 0), (4, k)) for k in range(-4, 5)] + [((0, 0), (0, 4)), ((0, 0), (-4, 0))]
    loc = SarnakTarjanLocator(fan)
    for q in query_points(3):
        assert loc.locate(q) == reference(fan, q)


def test_space_is_n_log_n():
    # the quadratic family of the slab method needs only O(n log n) nodes here
    for m in (16, 64):
        L = 4 * m + 4
        segs = [((0, 10 + 2 * j), (L, 10 + 2 * j)) for j in range(m)]
        segs += [((4 * k + 1, 0), (4 * k + 2, 0)) for k in range(m)]
        loc = SarnakTarjanLocator(segs)
        n = len(segs)
        assert loc.tree.created <= 4 * n * n.bit_length()
        assert sum(len(inorder(r)) for r in loc.roots) >= m * m


def test_example():
    segs = [((0, 0), (8, 2)), ((4, 6), (8, 2)), ((0, 0), (4, 6)), ((2, 8), (10, 6))]
    loc = SarnakTarjanLocator(segs)
    assert [inorder(r) for r in loc.roots] == [[0, 2], [0, 2, 3], [0, 1, 3], [3]]
    assert [r.seg for r in loc.roots] == [0, 2, 1, 3]
    assert loc.tree.created == 14
    assert loc.locate((4, 7)) == ("face", 3, 1)
    assert loc.locate((5, 3)) == ("face", 1, 0)
    assert loc.locate((6, 7)) == ("edge", 3)
