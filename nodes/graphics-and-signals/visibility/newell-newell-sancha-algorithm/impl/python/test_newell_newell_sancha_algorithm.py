# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newell-newell-sancha-algorithm/. The authors are listed in prov/GJTAMY.jsonl.

import random
from fractions import Fraction

import pytest

from newell_newell_sancha_algorithm import newell_newell_sancha

W, H = 8, 6


def inside(poly, x, y):
    """Independent closed point-in-convex-polygon test by barycentric signs on a fan."""
    a = poly[0]
    for k in range(1, len(poly) - 1):
        b, c = poly[k], poly[k + 1]
        d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if d == 0:
            continue
        l1 = Fraction((b[0] - x) * (c[1] - y) - (b[1] - y) * (c[0] - x)) / d
        l2 = Fraction((c[0] - x) * (a[1] - y) - (c[1] - y) * (a[0] - x)) / d
        if l1 >= 0 and l2 >= 0 and 1 - l1 - l2 >= 0:
            return True
    return False


def zplane(poly, x, y):
    """Depth by Cramer's rule on the first three vertices."""
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = poly[0], poly[1], poly[2]
    det = Fraction(x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2))
    p = (z1 * (y2 - y3) - y1 * (z2 - z3) + (z2 * y3 - z3 * y2)) / det
    q = (x1 * (z2 - z3) - z1 * (x2 - x3) + (x2 * z3 - x3 * z2)) / det
    r = (x1 * (y2 * z3 - y3 * z2) - y1 * (x2 * z3 - x3 * z2) + z1 * (x2 * y3 - x3 * y2)) / det
    return p * x + q * y + r


def centers(w=W, h=H):
    return [(i, j, Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2)) for j in range(h) for i in range(w)]


def brute(polys, w=W, h=H):
    """Per-pixel exact depth test over all polygons. None marks a tie."""
    img = [[-1] * w for _ in range(h)]
    for i, j, x, y in centers(w, h):
        hits = [(zplane(p, x, y), k) for k, p in enumerate(polys) if inside(p, x, y)]
        if hits:
            top = max(d for d, _ in hits)
            win = [k for d, k in hits if d == top]
            img[j][i] = win[0] if len(win) == 1 else None
    return img


def agrees(img, ref):
    return all(r is None or r == g for rr, gg in zip(ref, img) for r, g in zip(rr, gg))


def area2(poly):
    k = len(poly)
    return abs(sum(poly[i][0] * poly[(i + 1) % k][1] - poly[(i + 1) % k][0] * poly[i][1] for i in range(k)))


def check(polys):
    order, img = newell_newell_sancha(polys, W, H)
    assert agrees(img, brute(polys))
    # The fragments of each polygon cover exactly its area.
    for k, p in enumerate(polys):
        assert sum(area2(v) for o, v in order if o == k) == area2(p)
    # The order is valid at each pixel center: no fragment is nearer than a later one.
    pts = centers()
    for a in range(len(order)):
        for b in range(a + 1, len(order)):
            fa, fb = order[a][1], order[b][1]
            pa, pb = polys[order[a][0]], polys[order[b][0]]
            for _, _, x, y in pts:
                if inside(fa, x, y) and inside(fb, x, y):
                    assert zplane(pa, x, y) <= zplane(pb, x, y)
    return order, img


CYCLE = [
    [(0, 1, 1), (8, 1, 3), (8, 2, 3), (0, 2, 1)],
    [(5, 0, 0), (6, 0, 0), (2, 6, 4), (1, 6, 4)],
    [(1, 0, 4), (2, 0, 4), (7, 6, -2), (6, 6, -2)],
]


def test_cyclic_overlap_is_split():
    order, _ = check(CYCLE)
    assert len(order) > 3


def test_reorders_the_failure_of_the_plain_sort():
    d = [(0, 0, 0), (8, 0, 8), (8, 6, 8), (0, 6, 0)]
    e = [(5, 1, 5), (7, 1, 5), (7, 3, 5), (5, 3, 5)]
    order, _ = check([d, e])
    # No split is necessary: E goes first, then D.
    assert [o for o, _ in order] == [1, 0]


def test_polygons_that_cross():
    a = [(0, 0, 0), (8, 0, 0), (8, 6, 6), (0, 6, 6)]
    b = [(0, 0, 6), (8, 0, 6), (8, 6, 0), (0, 6, 0)]
    order, _ = check([a, b])
    assert len(order) == 3


def test_split_of_the_front_polygon():
    # Here a marked polygon comes back, it does not cross the plane of the
    # front polygon, and the front polygon is split instead (line L8).
    polys = [
        [(0, 3, 5), (3, 3, 5), (4, 8, 10), (1, 8, 10)],
        [(0, 6, 8), (5, 8, 13), (0, 9, 8)],
        [(0, 4, 7), (4, 4, 15), (3, 6, 13), (-1, 6, 5)],
    ]
    check(polys)


def test_edges():
    assert newell_newell_sancha([], 2, 2) == ([], [[-1, -1], [-1, -1]])
    one = [(0, 0, 0), (3, 0, 0), (0, 3, 0)]
    order, img = newell_newell_sancha([one], 3, 2)
    assert [o for o, _ in order] == [0] and img == [[0, 0, 0], [0, 0, -1]]
    check([one, [(0, 0, 0), (3, 0, 0), (0, 3, 0)]])  # coplanar copies
    with pytest.raises(ValueError):
        newell_newell_sancha([[(0, 0, 0), (1, 0, 0), (1, 0, 1)]], 2, 2)


def random_poly(rng):
    while True:
        k = rng.choice((3, 3, 4))
        x0, y0 = rng.randint(-1, W), rng.randint(-1, H)
        pts = [(x0, y0), (x0 + rng.randint(1, 6), y0 + rng.randint(-2, 2)), (x0 + rng.randint(-2, 4), y0 + rng.randint(1, 5))]
        (ax, ay), (bx, by), (cx, cy) = pts
        if (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) == 0:
            continue
        z0, gx, gy = rng.randint(0, 9), rng.randint(-2, 2), rng.randint(-2, 2)
        poly = [(x, y, z0 + gx * (x - x0) + gy * (y - y0)) for x, y in pts]
        if k == 4:
            # Add the fourth corner of the parallelogram, which keeps the polygon convex and planar.
            x, y = bx + cx - ax, by + cy - ay
            poly.insert(2, (x, y, z0 + gx * (x - x0) + gy * (y - y0)))
        return poly


def test_random_scenes_match_brute_force():
    rng = random.Random(11)
    splits = 0
    for _ in range(500):
        polys = [random_poly(rng) for _ in range(rng.randint(2, 4))]
        order, _ = check(polys)
        splits += len(order) - len(polys)
    assert splits > 0
