# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seidel-polygon-triangulation/. The authors are listed in prov/FY0W28.jsonl.
import random
from fractions import Fraction

from seidel_polygon_triangulation import (
    faces,
    key,
    monotone_diagonals,
    seidel_triangulation,
    trapezoidal_decomposition,
)


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def area2(pts):
    n = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))


def proper_cross(a, b, c, d):
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def strictly_inside(poly, q):
    """Even-odd test for a point q not on the boundary."""
    inside = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > q[1]) != (b[1] > q[1]):
            t = orient(a, b, q)
            if (t > 0) == (b[1] > a[1]):
                inside = not inside
    return inside


def no_three_collinear(pts):
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if orient(pts[i], pts[j], pts[k]) == 0:
                    return False
    return True


def random_polygon(rng, n, span):
    while True:
        pts = list({(rng.randint(0, span), rng.randint(0, span)) for _ in range(n)})
        if len(pts) < 3 or not no_three_collinear(pts):
            continue
        rng.shuffle(pts)
        changed = True
        while changed:  # 2-opt untangling ends with a simple polygon
            changed = False
            m = len(pts)
            for i in range(m):
                for j in range(i + 2, m):
                    if i == 0 and j == m - 1:
                        continue
                    a, b = pts[i], pts[i + 1]
                    c, d = pts[j], pts[(j + 1) % m]
                    if proper_cross(a, b, c, d):
                        pts[i + 1:j + 1] = reversed(pts[i + 1:j + 1])
                        changed = True
        if area2(pts) < 0:
            pts.reverse()
        return pts


def check_triangulation(pts, tris):
    n = len(pts)
    assert len(tris) == n - 2
    assert sum(orient(pts[a], pts[b], pts[c]) for a, b, c in tris) == area2(pts)
    assert all(orient(pts[a], pts[b], pts[c]) > 0 for a, b, c in tris)
    boundary = {frozenset((i, (i + 1) % n)) for i in range(n)}
    edges = set()
    for a, b, c in tris:
        edges |= {frozenset((a, b)), frozenset((b, c)), frozenset((c, a))}
    diags = edges - boundary
    assert boundary <= edges
    assert len(diags) == n - 3
    segs = [tuple(e) for e in edges]
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            u, v = segs[i]
            x, y = segs[j]
            if len({u, v, x, y}) == 4:
                assert not proper_cross(pts[u], pts[v], pts[x], pts[y])
    for e in diags:
        u, v = tuple(e)
        mid = (Fraction(pts[u][0] + pts[v][0], 2), Fraction(pts[u][1] + pts[v][1], 2))
        assert strictly_inside(pts, mid)


def x_at(pts, seg, y):
    hi, lo = seg
    (x1, y1), (x2, y2) = pts[lo], pts[hi]
    return Fraction(x1) + Fraction(x2 - x1) * Fraction(y - y1, y2 - y1)


def trapezoid_area2(pts, tz, trap):
    top, bot, left, right = trap
    yt, yb = pts[top][1], pts[bot][1]
    if yt == yb:
        return 0
    wt = x_at(pts, tz.seg[right], yt) - x_at(pts, tz.seg[left], yt)
    wb = x_at(pts, tz.seg[right], yb) - x_at(pts, tz.seg[left], yb)
    assert wt >= 0 and wb >= 0
    return (wt + wb) * (yt - yb)


def check_pieces_monotone(pts, pieces):
    for piece in pieces:
        m = len(piece)
        peaks = sum(1 for i in range(m)
                    if key(pts[piece[i]]) > key(pts[piece[i - 1]]) and key(pts[piece[i]]) > key(pts[piece[(i + 1) % m]]))
        assert peaks == 1


def run(pts, seed=0):
    tz, inside = trapezoidal_decomposition(pts, random.Random(seed))
    assert len(tz.trapezoids()) == 2 * len(pts) + 1
    assert sum(trapezoid_area2(pts, tz, t) for t in inside) == area2(pts)
    diags = monotone_diagonals(tz, inside)
    n = len(pts)
    pieces = faces(pts, [(i, (i + 1) % n) for i in range(n)] + sorted(diags))
    check_pieces_monotone(pts, pieces)
    assert len(pieces) == len(diags) + 1
    tris = seidel_triangulation(pts, seed)
    check_triangulation(pts, tris)
    return tz, inside, tris


def test_example():
    pts = [(0, 0), (6, 0), (6, 4), (4, 4), (3, 1), (2, 4), (0, 4)]
    tz, inside, tris = run(pts)
    assert len(tris) == 5


def test_triangle_and_convex():
    run([(0, 0), (5, 1), (2, 7)])
    run([(3, 0), (6, 1), (8, 3), (7, 6), (4, 8), (1, 7), (0, 4)])


def test_horizontal_edges():
    run([(0, 0), (5, 0), (7, 3), (2, 3)], 3)
    run([(0, 0), (9, 1), (8, 5), (4, 2), (1, 6)], 4)


def test_decomposition_independent_of_order():
    rng = random.Random(7)
    for _ in range(30):
        pts = random_polygon(rng, rng.randint(4, 14), 40)
        base = None
        for seed in range(4):
            tz, inside = trapezoidal_decomposition(pts, random.Random(seed))
            shape = sorted(inside)
            if base is None:
                base = shape
            assert shape == base


def test_random_polygons():
    rng = random.Random(1991)
    for _ in range(150):
        pts = random_polygon(rng, rng.randint(3, 24), 60)
        run(pts, rng.randint(0, 10 ** 6))


def comb(rng, k):
    """A comb with k downward teeth, jittered into general position."""
    while True:
        pts = [(0, 0), (100 * k + rng.randint(1, 9), rng.randint(-9, 9))]
        for i in range(k - 1, -1, -1):
            x = 100 * i
            pts.append((x + 90 + rng.randint(0, 9), 1000 + rng.randint(0, 9)))
            pts.append((x + 60 + rng.randint(0, 9), 200 + rng.randint(0, 99)))
            pts.append((x + 30 + rng.randint(0, 9), 1000 + rng.randint(10, 19)))
        pts.append((rng.randint(-9, -1), 1100 + rng.randint(0, 9)))
        n = len(pts)
        simple = not any(proper_cross(pts[a], pts[(a + 1) % n], pts[b], pts[(b + 1) % n])
                         for a in range(n) for b in range(a + 2, n) if not (a == 0 and b == n - 1))
        if simple and no_three_collinear(pts) and area2(pts) > 0:
            return pts


def test_comb():
    rng = random.Random(5)
    for k in (3, 8):
        pts = comb(rng, k)
        tz, inside, tris = run(pts, k)
        assert len(tris) == len(pts) - 2


def test_fractions_and_large():
    big = 10 ** 15
    run([(0, 0), (big, 1), (big + 3, big), (big // 2, big // 3), (1, big + 7)])
    run([(Fraction(0), Fraction(0)), (Fraction(7, 2), Fraction(1, 3)), (Fraction(5, 3), Fraction(9, 4)),
         (Fraction(1, 7), Fraction(5, 2))])
