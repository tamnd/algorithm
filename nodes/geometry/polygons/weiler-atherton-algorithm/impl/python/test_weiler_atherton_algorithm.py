# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiler-atherton-algorithm/. The authors are listed in prov/TS2VAV.jsonl.

import math
import random
from fractions import Fraction

import pytest

from weiler_atherton_algorithm import is_simple, weiler_atherton

OPS = {
    "intersection": lambda a, b: a and b,
    "union": lambda a, b: a or b,
    "difference": lambda a, b: a and not b,
}


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def edges_of(poly):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n) if poly[i] != poly[(i + 1) % n]]


def on_boundary(poly, q):
    for a, b in edges_of(poly):
        if orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
    return False


def winding(poly, q):
    """Winding number by signed crossings of the downward vertical ray (q off the boundary)."""
    w = 0
    for a, b in edges_of(poly):
        if a[0] <= q[0] < b[0] and orient(a, b, q) > 0:
            w += 1
        elif b[0] <= q[0] < a[0] and orient(a, b, q) < 0:
            w -= 1
    return w


def twice_area(poly):
    return sum(orient((0, 0), a, b) for a, b in edges_of(poly))


def crossing_xs(e, f):
    (a, b), (c, d) = e, f
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if den == 0:
        return []
    t = Fraction((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0]), den)
    u = Fraction((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0]), den)
    if 0 <= t <= 1 and 0 <= u <= 1:
        return [a[0] + t * (b[0] - a[0])]
    return []


def slab_measure(polys, keep):
    """Exact area of the set of points q with keep(w_1 != 0, ..., w_k != 0), w_j the winding
    number of polys[j]. Inside a vertical slab between consecutive event x values no two edges
    cross, so the cross-section length is linear in x and the midpoint value is exact."""
    groups = [edges_of(p) for p in polys]
    alle = [e for g in groups for e in g]
    xs = {Fraction(p[0]) for e in alle for p in e}
    for i in range(len(alle)):
        for j in range(i + 1, len(alle)):
            xs.update(crossing_xs(alle[i], alle[j]))
    xs = sorted(xs)
    total = Fraction(0)
    for x0, x1 in zip(xs, xs[1:]):
        xm = (x0 + x1) / 2
        hits = []
        for k, g in enumerate(groups):
            for a, b in g:
                if min(a[0], b[0]) < xm < max(a[0], b[0]):
                    y = a[1] + (xm - a[0]) * Fraction(b[1] - a[1]) / (b[0] - a[0])
                    hits.append((y, k, 1 if b[0] > a[0] else -1))
        hits.sort()
        w = [0] * len(groups)
        length = Fraction(0)
        for idx in range(len(hits) - 1):
            y, k, s = hits[idx]
            w[k] += s
            if keep(*(v != 0 for v in w)):
                length += hits[idx + 1][0] - y
        total += (x1 - x0) * length
    return total


def general_position(s, c):
    return not any(on_boundary(c, q) for q in s) and not any(on_boundary(s, q) for q in c)


def star_polygon(rng, size, k):
    pts = list({(rng.randint(0, size), rng.randint(0, size)) for _ in range(k)})
    cx = Fraction(sum(p[0] for p in pts), len(pts)) + Fraction(1, 7)
    cy = Fraction(sum(p[1] for p in pts), len(pts)) + Fraction(1, 11)
    pts.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
    return pts


def check_result(s, c, op, contours, rng, samples=30, size=20):
    keep = OPS[op]
    total = sum(twice_area(cc) for cc in contours)
    assert Fraction(total, 2) == slab_measure([s, c], keep)
    for _ in range(samples):
        q = (Fraction(rng.randint(-2, 4 * size + 2), 4), Fraction(rng.randint(-2, 4 * size + 2), 4))
        if on_boundary(s, q) or on_boundary(c, q):
            continue
        want = 1 if keep(winding(s, q) != 0, winding(c, q) != 0) else 0
        assert sum(winding(cc, q) for cc in contours) == want


U = [(0, 0), (6, 0), (6, 6), (4, 6), (4, 2), (2, 2), (2, 6), (0, 6)]
BAR = [(-1, 4), (7, 4), (7, 5), (-1, 5)]


def test_worked_example() -> None:
    inter = weiler_atherton(U, BAR, "intersection")
    assert sorted(twice_area(c) for c in inter) == [4, 4]
    union = weiler_atherton(U, BAR, "union")
    assert sorted(twice_area(c) for c in union) == [-8, 72]
    diff = weiler_atherton(U, BAR, "difference")
    assert sorted(twice_area(c) for c in diff) == [4, 4, 40]
    rng = random.Random(5)
    for op, res in [("intersection", inter), ("union", union), ("difference", diff)]:
        check_result(U, BAR, op, res, rng, samples=200, size=8)


def test_no_crossings() -> None:
    big = [(0, 0), (10, 0), (10, 10), (0, 10)]
    small = [(2, 2), (3, 2), (3, 3)]
    far = [(20, 20), (21, 20), (21, 21)]
    assert weiler_atherton(small, big) == [small]
    assert weiler_atherton(big, small) == [small]
    assert weiler_atherton(big, far) == []
    assert weiler_atherton(small, big, "union") == [big]
    assert weiler_atherton(big, far, "union") == [big, far]
    assert weiler_atherton(small, big, "difference") == []
    assert weiler_atherton(big, small, "difference") == [big, small[::-1]]
    assert weiler_atherton(big, far, "difference") == [big]


def test_degenerate_inputs_raise() -> None:
    sq = [(0, 0), (4, 0), (4, 4), (0, 4)]
    with pytest.raises(ValueError):
        weiler_atherton(sq, [(4, 0), (8, 0), (8, 4), (4, 4)])  # shared edge
    with pytest.raises(ValueError):
        weiler_atherton(sq, [(2, 0), (6, -2), (6, 2)])  # vertex on an edge
    with pytest.raises(ValueError):
        weiler_atherton(sq, [(4, 4), (8, 4), (8, 8)])  # shared vertex
    with pytest.raises(ValueError):
        weiler_atherton([(0, 0), (2, 2), (2, 0), (0, 2)], sq)  # bowtie
    with pytest.raises(ValueError):
        weiler_atherton(sq, sq, "xor")
    assert not is_simple([(0, 0), (2, 0), (1, 0)])
    assert not is_simple([(0, 0), (4, 0), (4, 4), (2, 0), (0, 4)])


def test_orientation_does_not_matter() -> None:
    rng = random.Random(8)
    for op in OPS:
        res = weiler_atherton(U[::-1], BAR[::-1], op)
        check_result(U, BAR, op, res, rng, samples=100, size=8)


def test_combs() -> None:
    # Two interleaved combs give many crossings and several pieces.
    comb = [(0, 0), (11, 0), (11, 9)]
    for x in range(9, 0, -2):
        comb += [(x, 9), (x, 3), (x - 1, 3), (x - 1, 9)] if x > 1 else []
    comb += [(0, 9)]
    comb = [p for p in comb]
    bar = [(-1, 5), (12, 6), (12, 7), (-1, 8)]
    assert is_simple(comb)
    rng = random.Random(3)
    for op in OPS:
        res = weiler_atherton(comb, bar, op)
        check_result(comb, bar, op, res, rng, samples=200, size=12)


def test_random_star_polygons() -> None:
    rng = random.Random(1977)
    done = 0
    while done < 150:
        s = star_polygon(rng, 20, rng.randint(3, 9))
        c = star_polygon(rng, 20, rng.randint(3, 9))
        if not (is_simple(s) and is_simple(c)):
            continue
        if not general_position(s, c):
            with pytest.raises(ValueError):
                weiler_atherton(s, c)
            continue
        for op in OPS:
            check_result(s, c, op, weiler_atherton(s, c, op), rng)
        done += 1
