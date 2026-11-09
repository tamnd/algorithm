# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-monotone-point-location/. The authors are listed in prov/VJCF98.jsonl.

import random
from fractions import Fraction

import pytest

from chazelle_monotone_point_location import MonotoneLocator, normalize, orient, top_node

EXAMPLE = {
    "a": (0, 2), "b": (2, 0), "c": (2, 4), "d": (4, 2), "e": (6, 0), "f": (6, 4), "g": (8, 2),
}
EXAMPLE_EDGES = ["ab", "ac", "bd", "cd", "be", "cf", "de", "df", "eg", "fg"]


def reference(segs, q):
    """Linear scan: the answer under the symbolic shear (x, y) -> (x + eps y, y)."""
    segs = [normalize(s) for s in segs]
    for a, b in segs:
        if q == a or q == b:
            return ("vertex", q)
    for i, (a, b) in enumerate(segs):
        if orient(a, b, q) == 0 and a < q < b:
            return ("edge", i)
    above = below = None
    for i, (a, b) in enumerate(segs):
        if not (a < q < b):
            continue
        slope = Fraction(b[1] - a[1], b[0] - a[0])  # a[0] < b[0]: a vertical segment spanning q would contain q
        y = a[1] + slope * (q[0] - a[0])
        if y > q[1]:
            if above is None or (y, -slope) < above[0]:
                above = ((y, -slope), i)
        elif below is None or (y, slope) > below[0]:
            below = ((y, slope), i)
    return ("face", above and above[1], below and below[1])


def in_closed(t, p):
    a, b, c = t
    return orient(a, b, p) >= 0 and orient(b, c, p) >= 0 and orient(c, a, p) >= 0


def insert_point(tris, p):
    for t in tris:
        if p in t:
            return
    for k, t in enumerate(tris):
        if in_closed(t, p):
            a, b, c = t
            sides = [orient(a, b, p), orient(b, c, p), orient(c, a, p)]
            if all(s > 0 for s in sides):
                tris[k : k + 1] = [(a, b, p), (b, c, p), (c, a, p)]
                return
            j = sides.index(0)
            u, w = t[j], t[(j + 1) % 3]
            break
    out = []
    for t in tris:
        if u in t and w in t:
            i = t.index(u)
            if t[(i + 1) % 3] == w:
                x = t[(i + 2) % 3]
                out += [(u, p, x), (p, w, x)]
            else:
                x = t[(i + 1) % 3]
                out += [(u, x, p), (x, w, p)]
        else:
            out.append(t)
    tris[:] = out


def random_regular_graph(rng, g, m, keep):
    """A triangulation of the triangle (0,0), (g,0), (0,g), with random edges deleted while it stays regular."""
    tris = [((0, 0), (g, 0), (0, g))]
    for _ in range(m):
        x = rng.randint(0, g - 1)
        y = rng.randint(0, g - x)
        insert_point(tris, (x, y))
    edges = sorted({normalize((t[k], t[(k + 1) % 3])) for t in tris for k in range(3)})
    verts = sorted({p for e in edges for p in e})
    first, last = verts[0], verts[-1]
    rng.shuffle(edges)
    left = {v: 0 for v in verts}
    right = {v: 0 for v in verts}
    for a, b in edges:
        right[a] += 1
        left[b] += 1
    kept = []
    for a, b in edges:
        if rng.random() > keep and right[a] > 1 and left[b] > 1:
            right[a] -= 1
            left[b] -= 1
            continue
        kept.append((a, b) if rng.random() < 0.5 else (b, a))
    assert all(right[v] > 0 for v in verts if v != last) and all(left[v] > 0 for v in verts if v != first)
    return kept


def chains_of(loc):
    return [[i for i in range(len(loc.segs)) if loc.lo[i] <= j <= loc.hi[i]] for j in range(loc.chains)]


def test_against_linear_scan():
    rng = random.Random(1986)
    for _ in range(80):
        g = rng.randint(2, 9)
        segs = random_regular_graph(rng, g, rng.randint(0, 20), rng.random())
        loc = MonotoneLocator(segs)
        for x in range(-1, g + 2):
            for y in range(-1, g + 2):
                want = reference(segs, (x, y))
                assert loc.locate((x, y)) == want, (segs, (x, y))
                assert loc.locate((x, y), cascade=False) == want


def test_rational_queries():
    rng = random.Random(77)
    for _ in range(20):
        g = rng.randint(3, 8)
        segs = random_regular_graph(rng, g, rng.randint(3, 15), 0.6)
        loc = MonotoneLocator(segs)
        for _ in range(200):
            q = (Fraction(rng.randint(-4, 4 * g + 4), 4), Fraction(rng.randint(-4, 4 * g + 4), 4))
            assert loc.locate(q) == reference(segs, q)


def test_chains_are_separating_and_complete():
    rng = random.Random(15)
    for _ in range(60):
        g = rng.randint(2, 8)
        segs = random_regular_graph(rng, g, rng.randint(0, 14), rng.random())
        loc = MonotoneLocator(segs)
        verts = {p for s in loc.segs for p in s}
        assert loc.chains == len(segs) - len(verts) + 2  # f + 1 chains, f = E - V + 1 bounded faces
        assert all(w >= 1 for w in loc.weight)
        chains = chains_of(loc)
        for chain in chains:
            path = sorted(loc.segs[i] for i in chain)
            assert path[0][0] == loc.first and path[-1][1] == loc.last
            assert all(path[k][1] == path[k + 1][0] for k in range(len(path) - 1))
        for j in range(len(chains) - 1):
            low = [loc.segs[i] for i in chains[j]]
            high = [loc.segs[i] for i in chains[j + 1]]
            for (a, b) in low:
                for (c, d) in high:
                    for v in (c, d):
                        if a < v < b:
                            assert orient(a, b, v) >= 0
                    for v in (a, b):
                        if c < v < d:
                            assert orient(c, d, v) <= 0


def test_each_edge_stored_once_at_its_top_node():
    rng = random.Random(3)
    for _ in range(30):
        loc = MonotoneLocator(random_regular_graph(rng, rng.randint(3, 10), rng.randint(0, 25), rng.random()))
        assert sum(len(x) for x in loc.L) == len(loc.segs)
        for m, edges in enumerate(loc.L):
            for i in edges:
                assert loc.lo[i] + 1 <= m <= loc.hi[i] + 1
                assert all((k & -k) < (m & -m) for k in range(loc.lo[i] + 1, loc.hi[i] + 2) if k != m)
    assert top_node(3, 5) == 4 and top_node(5, 5) == 5 and top_node(1, 7) == 4 and top_node(9, 12) == 12 and top_node(5, 7) == 6


def test_long_shared_edges_quadratic_chains_linear_storage():
    # a monotone path of p edges, then a stack of s thin faces between (p, 0) and (p + 2, 0)
    for p, s in [(10, 10), (24, 24)]:
        segs = [((i, 0), (i + 1, 0)) for i in range(p)]
        for k in range(1, s + 1):
            segs += [((p, 0), (p + 1, k)), ((p + 1, k), (p + 2, 0))]
        loc = MonotoneLocator(segs)
        entries = sum(loc.hi[i] - loc.lo[i] + 1 for i in range(len(segs)))
        assert loc.chains == s
        assert entries >= p * s
        n = len(segs)
        assert loc.storage() <= 2 * n + 2 * (loc.size + 1)
        for x in range(0, 2 * p + 5):
            for y in range(-1, s + 2):
                q = (Fraction(x, 2), Fraction(y, 1))
                assert loc.locate(q) == reference(segs, q)


def test_query_cost_is_logarithmic():
    rng = random.Random(11)
    segs = random_regular_graph(rng, 40, 250, 0.7)
    loc = MonotoneLocator(segs)
    height = loc.size.bit_length()
    assert loc.storage() <= 2 * len(segs) + 2 * (loc.size + 1)
    for _ in range(400):
        q = (Fraction(rng.randint(-10, 410), 10), Fraction(rng.randint(-10, 410), 10))
        assert loc.locate(q) == reference(segs, q)
        assert loc.steps <= 2 * height


def test_not_regular():
    square = [((0, 0), (4, 0)), ((4, 0), (4, 4)), ((4, 4), (0, 4)), ((0, 4), (0, 0))]
    hole = [((1, 1), (3, 1)), ((3, 1), (2, 3)), ((2, 3), (1, 1))]
    with pytest.raises(ValueError):
        MonotoneLocator(square + hole)
    u_shape = [(0, 0), (6, 0), (6, 2), (2, 2), (2, 4), (6, 4), (6, 6), (0, 6)]
    with pytest.raises(ValueError):
        MonotoneLocator([(u_shape[i], u_shape[(i + 1) % 8]) for i in range(8)])
    closed = [(u_shape[i], u_shape[(i + 1) % 8]) for i in range(8)] + [((0, 0), (2, 2)), ((6, 2), (6, 4))]
    loc = MonotoneLocator(closed)
    assert loc.chains == 4
    assert loc.locate((4, 3)) == ("face", 4, 2)
    with pytest.raises(ValueError):
        MonotoneLocator([])


def test_worked_example():
    segs = [(EXAMPLE[e[0]], EXAMPLE[e[1]]) for e in EXAMPLE_EDGES]
    loc = MonotoneLocator(segs)
    names = {v: k for k, v in EXAMPLE.items()}
    assert loc.chains == 5
    chains = ["".join(sorted({names[p] for i in c for p in loc.segs[i]})) for c in chains_of(loc)]
    assert chains == ["abeg", "abdeg", "acdeg", "acdfg", "acfg"]
    assert {e: loc.weight[k] for k, e in enumerate(EXAMPLE_EDGES)} == {
        "ab": 2, "ac": 3, "bd": 1, "cd": 2, "be": 1, "cf": 1, "de": 2, "df": 1, "eg": 3, "fg": 2,
    }
    assert loc.locate((3, 1)) == ("edge", 2)
    assert loc.locate((3, 2)) == ("face", 3, 2)
    assert loc.locate((4, 2)) == ("vertex", (4, 2))
    assert loc.locate((9, 2)) == ("face", None, None)
    assert loc.locate((5, 5)) == ("face", None, 5)
