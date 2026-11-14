# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volumetric-mesh-repair/. The authors are listed in prov/5S30QB.jsonl.

import random
from fractions import Fraction
from itertools import product

from volumetric_mesh_repair import crossed_edges, make_grid, odd_cells, repair

EPS = Fraction(1, 10 ** 4)  # a concrete stand-in for the symbolic eps; small against all coordinates


# ---- brute force ----


def perturbed(g, i, j):
    x, y = g.point(i, j)
    return (x + EPS, y + EPS * EPS)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_cross(a, b, p, q):
    """Exact proper crossing test of two segments in general position."""
    return (orient(a, b, p) > 0) != (orient(a, b, q) > 0) and (orient(p, q, a) > 0) != (orient(p, q, b) > 0)


def even_odd(point, segments):
    """Brute-force parity of a ray to the right against all segments (half-open rule in y)."""
    x, y = point
    c = 0
    for p, q in segments:
        if (p[1] > y) != (q[1] > y):
            xc = p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1])
            if xc > x:
                c += 1
    return c % 2 == 1


def all_grid_edges(g):
    for j in range(g.ny + 1):
        for i in range(g.nx):
            yield ("h", i, j), (i, j), (i + 1, j)
    for j in range(g.ny):
        for i in range(g.nx + 1):
            yield ("v", i, j), (i, j), (i, j + 1)


def random_chain(rng, k, r):
    pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(k)]
    return [(pts[t], pts[(t + 1) % k]) for t in range(k)]


def check_contour(res):
    """Each output vertex has one segment in and one out, so the output is a set of closed curves."""
    ins, outs = {}, {}
    for a, b in res.segments:
        assert a != b
        outs[a] = outs.get(a, 0) + 1
        ins[b] = ins.get(b, 0) + 1
    assert ins == outs and set(ins.values()) <= {1}


# ---- tests ----


def test_scan_conversion_against_brute_force():
    rng = random.Random(2004)
    for _ in range(150):
        segs = [((rng.randint(-6, 6), rng.randint(-6, 6)), (rng.randint(-6, 6), rng.randint(-6, 6)))
                for _ in range(rng.randint(1, 4))]
        h = Fraction(rng.randint(1, 3), rng.randint(1, 2))
        g = make_grid(segs, h)
        for p, q in segs:
            got = set(crossed_edges(g, p, q))
            want = {e for e, a, b in all_grid_edges(g)
                    if p != q and segments_cross(perturbed(g, *a), perturbed(g, *b), p, q)}
            assert got == want


def test_closed_input_gives_even_odd_signs():
    rng = random.Random(1)
    for _ in range(80):
        segs = []
        for _ in range(rng.randint(1, 3)):
            segs += random_chain(rng, rng.randint(3, 6), 7)
        h = Fraction(rng.randint(1, 4), 2)
        res = repair(segs, h)
        assert res.odd_cells == [] and res.toggled == []
        for (i, j), side in res.inside.items():
            assert side == even_odd(perturbed(res.grid, i, j), segs)
        check_contour(res)


def test_contour_bounds_exactly_the_inside_points():
    rng = random.Random(5)
    for _ in range(60):
        segs = [s for s in random_chain(rng, rng.randint(3, 7), 6) if rng.random() < 0.8]  # with gaps
        res = repair(segs, 1)
        check_contour(res)
        for (i, j), side in res.inside.items():
            # an unperturbed grid point never lies on the output, which joins edge midpoints
            assert side == even_odd(res.grid.point(i, j), res.segments)


def test_patching_makes_every_cell_even_and_signs_consistent():
    rng = random.Random(77)
    for _ in range(120):
        segs = [((rng.randint(-5, 5), rng.randint(-5, 5)), (rng.randint(-5, 5), rng.randint(-5, 5)))
                for _ in range(rng.randint(1, 6))]
        res = repair(segs, Fraction(rng.randint(1, 2)))
        g = res.grid
        assert len(res.odd_cells) % 2 == 0
        assert odd_cells(g, res.marked) == []
        for e, a, b in all_grid_edges(g):
            assert (res.inside[a] != res.inside[b]) == (e in res.marked)
        assert not any(res.inside[(i, j)] for i in (0, g.nx) for j in range(g.ny + 1))
        check_contour(res)


def test_signs_are_unique_up_to_complement():
    """Brute force over all sign vectors of a small grid: only the result and its complement fit."""
    rng = random.Random(9)
    for _ in range(12):
        segs = [((rng.randint(1, 3), rng.randint(1, 3)), (rng.randint(1, 3), rng.randint(1, 3)))
                for _ in range(rng.randint(1, 3))]
        res = repair(segs, 1)
        g = res.grid
        verts = [(i, j) for j in range(g.ny + 1) for i in range(g.nx + 1)]
        if len(verts) > 16:
            continue
        edges = list(all_grid_edges(g))
        fits = []
        for bits in product((False, True), repeat=len(verts)):
            s = dict(zip(verts, bits))
            if all((s[a] != s[b]) == (e in res.marked) for e, a, b in edges):
                fits.append(s)
        assert len(fits) == 2
        assert res.inside in fits
        assert {v: not x for v, x in res.inside.items()} in fits


def test_page_example_square_with_a_gap():
    # three sides of the square [1, 4] x [1, 4]; the top side is missing
    segs = [((1, 1), (4, 1)), ((4, 1), (4, 4)), ((1, 4), (1, 1))]
    res = repair(segs, 1)
    g = res.grid
    assert (g.x0, g.y0, g.nx, g.ny) == (0, 0, 5, 5)
    assert res.odd_cells == [(0, 3), (3, 3)]  # the cells that hold the two free ends (1, 4) and (4, 4)
    assert res.toggled == [("v", 3, 3), ("v", 2, 3), ("v", 1, 3)]
    assert len(res.marked) == 12
    inside = sorted(v for v, s in res.inside.items() if s)
    assert inside == sorted((i, j) for i in range(1, 4) for j in range(1, 4))
    assert len(res.segments) == 12
    check_contour(res)


def test_duplicate_and_dangling_segments():
    sq = [((0, 0), (3, 0)), ((3, 0), (3, 3)), ((3, 3), (0, 3)), ((0, 3), (0, 0))]
    a = repair(sq, 1)
    b = repair(sq + [((0, 0), (3, 0))] * 2 + [((1, 1), (2, 2))] * 2, 1)  # doubled copies cancel
    assert a.inside == b.inside and a.segments == b.segments
    c = repair(sq + [((3, 1), (5, 1))], 1)  # a dangling piece outside the square
    assert len(c.odd_cells) == 2 and odd_cells(c.grid, c.marked) == []
    check_contour(c)
