# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amanatides-woo-traversal/. The authors are listed in prov/4NS679.jsonl.

import math
import random
from fractions import Fraction as Q

from amanatides_woo_traversal import box_hit, build_grid, cells, clip_to_box, grid_first_hit, traverse

LO = (Q(0), Q(0), Q(0))


def meet_interval(o, d, cell, size, t0, t1, strict=False):
    """Parameter interval where the segment meets the cell, closed or open, in Fraction."""
    lo = tuple(LO[a] + cell[a] * size for a in range(3))
    hi = tuple(lo[a] + size for a in range(3))
    a_lo, a_hi = t0, t1
    for a in range(3):
        if d[a] == 0:
            inside = lo[a] < o[a] < hi[a] if strict else lo[a] <= o[a] <= hi[a]
            if not inside:
                return None
            continue
        ta, tb = (lo[a] - o[a]) / d[a], (hi[a] - o[a]) / d[a]
        if ta > tb:
            ta, tb = tb, ta
        a_lo, a_hi = max(a_lo, ta), min(a_hi, tb)
    if strict:
        return (a_lo, a_hi) if a_lo < a_hi else None
    return (a_lo, a_hi) if a_lo <= a_hi else None


def reference(o, d, size, dims, t0, t1, strict=False):
    """Every cell of the grid that the segment meets, sorted by the entry parameter."""
    out = []
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                iv = meet_interval(o, d, (i, j, k), size, t0, t1, strict)
                if iv is not None:
                    out.append((iv[0], (i, j, k)))
    out.sort()
    return [c for _, c in out]


def generic(o, d, size, dims, t0, t1):
    """True if no two plane crossings coincide and no endpoint lies on a grid plane."""
    ts = []
    for a in range(3):
        for m in range(dims[a] + 1):
            plane = LO[a] + m * size
            if d[a] == 0:
                if o[a] == plane:
                    return False
                continue
            t = (plane - o[a]) / d[a]
            if t == t0 or t == t1:
                return False
            if t0 < t < t1:
                ts.append(t)
    return len(ts) == len(set(ts))


def rand_q(rng, lo, hi, den):
    return Q(rng.randint(lo * den, hi * den), den)


def test_generic_segments_match_exact_enumeration():
    rng = random.Random(31)
    dims, size = (5, 4, 6), Q(1)
    checked = 0
    for _ in range(250):
        o = (rand_q(rng, -1, 6, 97), rand_q(rng, -1, 5, 89), rand_q(rng, -1, 7, 83))
        d = (rand_q(rng, -3, 3, 79), rand_q(rng, -3, 3, 73), rand_q(rng, -3, 3, 71))
        if d == (0, 0, 0):
            continue
        t1 = rand_q(rng, 0, 3, 61)
        if not generic(o, d, size, dims, Q(0), t1):
            continue
        assert cells(o, d, LO, size, dims, Q(0), t1) == reference(o, d, size, dims, Q(0), t1)
        checked += 1
    assert checked > 150


def test_degenerate_segments_stay_between_open_and_closed_sets():
    rng = random.Random(32)
    dims, size = (4, 4, 4), Q(1, 2)
    for _ in range(300):
        o = tuple(Q(rng.randint(-2, 10), 4) for _ in range(3))
        d = tuple(Q(rng.randint(-2, 2), 2) for _ in range(3))
        if d == (0, 0, 0):
            continue
        t1 = Q(rng.randint(0, 8), 2)
        got = cells(o, d, LO, size, dims, Q(0), t1)
        closed = set(reference(o, d, size, dims, Q(0), t1))
        opened = set(reference(o, d, size, dims, Q(0), t1, strict=True))
        assert len(got) == len(set(got))  # each cell at most once
        assert opened <= set(got) <= closed
        for a, b in zip(got, got[1:]):  # consecutive cells share a face
            assert sum(abs(a[i] - b[i]) for i in range(3)) == 1
        if got:
            assert len(got) == 1 + sum(abs(got[-1][i] - got[0][i]) for i in range(3))


def test_entry_parameters_are_ordered_and_exact():
    o, d = (Q(1, 5), Q(3, 10), Q(1, 10)), (Q(1), Q(1, 2), Q(1, 4))
    walk = list(traverse(o, d, LO, Q(1), (4, 4, 4), Q(0), Q(4)))
    assert [c for c, _, _ in walk] == [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0), (3, 2, 1)]
    assert [t for _, t, _ in walk] == [Q(0), Q(4, 5), Q(7, 5), Q(9, 5), Q(14, 5), Q(17, 5), Q(18, 5)]
    for (_, a, b), (_, c, _) in zip(walk, walk[1:]):
        assert a <= b == c


def test_ties_follow_the_paper():
    # Through a lattice corner in 2D (z constant): t_max x = t_max y, so the y axis steps first.
    got = cells((Q(1, 2), Q(1, 2), Q(1, 2)), (Q(1), Q(1), Q(0)), LO, Q(1), (3, 3, 1), Q(0), Q(2))
    assert got[:3] == [(0, 0, 0), (0, 1, 0), (1, 1, 0)]


def test_start_outside_the_grid():
    o, d = (Q(-2), Q(1, 2), Q(1, 2)), (Q(1), Q(0), Q(0))
    assert cells(o, d, LO, Q(1), (3, 1, 1)) == [(0, 0, 0), (1, 0, 0), (2, 0, 0)]
    assert cells(o, (Q(-1), Q(0), Q(0)), LO, Q(1), (3, 1, 1)) == []


def random_boxes(rng, k):
    boxes = []
    for _ in range(k):
        lo = tuple(rand_q(rng, 0, 5, 4) for _ in range(3))  # boxes stay inside the 8^3 grid
        ext = tuple(rand_q(rng, 0, 3, 4) for _ in range(3))
        boxes.append((lo, tuple(lo[a] + ext[a] for a in range(3))))
    return boxes


def test_closest_hit_through_grid_equals_linear_scan():
    rng = random.Random(33)
    dims, size = (8, 8, 8), Q(1)
    for _ in range(80):
        boxes = random_boxes(rng, 12)
        grid = build_grid(boxes, LO, size, dims)
        o = (rand_q(rng, -2, 10, 7), rand_q(rng, -2, 10, 7), Q(-1))
        tgt = (rand_q(rng, 0, 8, 5), rand_q(rng, 0, 8, 5), Q(9))
        d = tuple(tgt[a] - o[a] for a in range(3))
        hits = [(box_hit(o, d, b, Q(0), Q(1)), i) for i, b in enumerate(boxes)]
        hits = [h for h in hits if h[0] is not None]
        expect = min(hits) if hits else None
        got = grid_first_hit(grid, boxes, o, d, LO, size, dims, Q(0), Q(1))
        assert (got and got[0]) == (expect and expect[0])


def test_without_the_cell_check_a_long_object_wins_wrongly():
    # Box A spans cells 0 to 3 along x but is hit only at x = 3 (it starts low and rises in z);
    # box B sits in cell 1 and is hit first.
    boxes = [((Q(0), Q(0), Q(0)), (Q(4), Q(1), Q(1, 4))), ((Q(1), Q(0), Q(0)), (Q(2), Q(1), Q(1)))]
    dims, size = (4, 1, 1), Q(1)
    grid = build_grid(boxes, LO, size, dims)
    o, d = (Q(0), Q(1, 2), Q(1)), (Q(4), Q(0), Q(-1))  # z falls from 1 to 0 over x in [0, 4]
    good = grid_first_hit(grid, boxes, o, d, LO, size, dims, Q(0), Q(1))
    bad = grid_first_hit(grid, boxes, o, d, LO, size, dims, Q(0), Q(1), check_cell=False)
    assert good == (Q(1, 4), 1)
    assert bad[1] == 0 and bad[0] > good[0]


def test_float_walk_matches_exact_walk_on_generic_rays():
    rng = random.Random(34)
    dims = (16, 16, 16)
    same = 0
    for _ in range(100):
        o = (rand_q(rng, 0, 16, 101), rand_q(rng, 0, 16, 103), Q(-1))
        d = (rand_q(rng, -1, 1, 107), rand_q(rng, -1, 1, 109), Q(1))
        if not generic(o, d, Q(1), dims, Q(0), Q(40)):
            continue
        exact = cells(o, d, LO, Q(1), dims, Q(0), Q(40))
        fl = cells(tuple(map(float, o)), tuple(map(float, d)), (0.0, 0.0, 0.0), 1.0, dims, 0.0, 40.0)
        same += exact == fl
    assert same > 50


def test_clip_parallel_ray_outside_is_empty():
    assert clip_to_box((Q(0), Q(2), Q(0)), (Q(1), Q(0), Q(0)), LO, (Q(1), Q(1), Q(1)), Q(0), math.inf) is None
