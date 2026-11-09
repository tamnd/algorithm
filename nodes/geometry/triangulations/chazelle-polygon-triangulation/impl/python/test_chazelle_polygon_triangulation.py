# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-polygon-triangulation/. The authors are listed in prov/HPKK4H.jsonl.
import random
from fractions import Fraction

from chazelle_polygon_triangulation import (
    Polygon,
    diagonals,
    faces,
    mountain_chain,
    trapezoids,
    triangulate,
    visibility_map,
)


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def area2(pts):
    n = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))


def proper_cross(a, b, c, d):
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def strictly_inside(poly, q):
    inside = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > q[1]) != (b[1] > q[1]):
            if (orient(a, b, q) > 0) == (b[1] > a[1]):
                inside = not inside
    return inside


def no_three_collinear(pts):
    n = len(pts)
    return all(orient(pts[i], pts[j], pts[k]) != 0
               for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n))


def random_polygon(rng, n, span):
    while True:
        pts = list({(rng.randint(0, span), rng.randint(0, span)) for _ in range(n)})
        if len(pts) < 3 or not no_three_collinear(pts):
            continue
        rng.shuffle(pts)
        changed = True
        while changed:
            changed = False
            m = len(pts)
            for i in range(m):
                for j in range(i + 2, m):
                    if i == 0 and j == m - 1:
                        continue
                    if proper_cross(pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]):
                        pts[i + 1:j + 1] = reversed(pts[i + 1:j + 1])
                        changed = True
        if area2(pts) < 0:
            pts.reverse()
        return pts


def sheared_chords(pts):
    """Independent map for integer input: shear to (x, K y + x), then intersect exactly."""
    K = 2 * max(abs(x) for x, _ in pts) + 1
    q = [(x, K * y + x) for x, y in pts]      # a linear map with determinant K > 0
    n = len(q)
    out = []
    for v in range(n):
        xv, yv = q[v]
        u, w = q[(v - 1) % n], q[(v + 1) % n]
        if (u[1] > yv) != (w[1] > yv):
            want_l, want_r = w[1] > yv, u[1] > yv
        else:
            want_l = want_r = orient(u, q[v], w) < 0
        best_l = best_r = None
        for s in range(n):
            a, b = q[s], q[(s + 1) % n]
            if a[1] == b[1] or not (min(a[1], b[1]) < yv < max(a[1], b[1])):
                continue
            x = Fraction(a[0]) + Fraction(b[0] - a[0]) * Fraction(yv - a[1], b[1] - a[1])
            assert x != xv
            if x < xv and want_l and (best_l is None or x > best_l[0]):
                best_l = (x, s)
            if x > xv and want_r and (best_r is None or x < best_r[0]):
                best_r = (x, s)
        out.append((best_l and best_l[1], best_r and best_r[1]))
    return out


def check_triangulation(pts, tris):
    n = len(pts)
    assert len(tris) == n - 2
    assert sum(orient(pts[a], pts[b], pts[c]) for a, b, c in tris) == area2(pts)
    assert all(orient(pts[a], pts[b], pts[c]) > 0 for a, b, c in tris)
    boundary = {frozenset((i, (i + 1) % n)) for i in range(n)}
    edges = set()
    for a, b, c in tris:
        edges |= {frozenset((a, b)), frozenset((b, c)), frozenset((c, a))}
    assert boundary <= edges and len(edges - boundary) == n - 3
    segs = [tuple(e) for e in edges]
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            u, v = segs[i]
            x, y = segs[j]
            if len({u, v, x, y}) == 4:
                assert not proper_cross(pts[u], pts[v], pts[x], pts[y])
    for e in edges - boundary:
        u, v = tuple(e)
        assert strictly_inside(pts, (Fraction(pts[u][0] + pts[v][0], 2), Fraction(pts[u][1] + pts[v][1], 2)))


def x_at(pts, P, s, y):
    hi, lo = P.seg[s]
    (x1, y1), (x2, y2) = pts[lo], pts[hi]
    return Fraction(x1) + Fraction(x2 - x1) * Fraction(y - y1, y2 - y1)


def trap_area2(pts, P, trap):
    top, bot, left, right = trap
    yt, yb = pts[top][1], pts[bot][1]
    if yt == yb:
        return 0
    wt = x_at(pts, P, right, yt) - x_at(pts, P, left, yt)
    wb = x_at(pts, P, right, yb) - x_at(pts, P, left, yb)
    assert wt >= 0 and wb >= 0
    return (wt + wb) * (yt - yb)


def run(pts, integer=True):
    n = len(pts)
    P = Polygon(pts)
    hit = visibility_map(P)
    if integer:
        assert hit == sheared_chords(pts)
    chords = sum((l is not None) + (r is not None) for l, r in hit)
    traps = trapezoids(P, hit)
    assert len(traps) == chords + 1
    assert sum(trap_area2(pts, P, t) for t in traps) == area2(pts)
    diags = diagonals(P, traps)
    pieces = faces(pts, [(i, (i + 1) % n) for i in range(n)] + sorted(diags))
    assert len(pieces) == len(diags) + 1
    for piece in pieces:
        chain, _ = mountain_chain(pts, piece)      # raises unless the piece is a mountain
        assert all(P.above(chain[i], chain[i + 1]) for i in range(len(chain) - 1))
    tris = triangulate(pts)
    check_triangulation(pts, tris)
    return hit, traps, diags, pieces, tris


def test_example():
    pts = [(0, 0), (6, 0), (6, 4), (4, 4), (3, 1), (2, 4), (0, 4)]
    hit, traps, diags, pieces, tris = run(pts)
    assert hit == [(None, None), (6, None), (None, None), (None, 1), (6, 1), (None, None), (None, 4)]
    assert diags == {(1, 4), (4, 6)}
    assert sorted(sorted(p) for p in pieces) == [[0, 1, 4, 6], [1, 2, 3, 4], [4, 5, 6]]


def test_small_shapes():
    run([(0, 0), (5, 1), (2, 7)])
    run([(3, 0), (6, 1), (8, 3), (7, 6), (4, 8), (1, 7), (0, 4)])
    run([(0, 0), (5, 0), (7, 3), (2, 3)])
    run([(0, 0), (9, 1), (8, 5), (4, 2), (1, 6)])


def test_random_polygons():
    rng = random.Random(1991)
    for _ in range(150):
        run(random_polygon(rng, rng.randint(3, 24), 60))


def test_rotations():
    rng = random.Random(6)
    for _ in range(20):
        pts = random_polygon(rng, rng.randint(5, 16), 40)
        for _ in range(4):
            run(pts)
            pts = [(-y, x) for x, y in pts]


def test_fractions_and_large():
    big = 10 ** 15
    run([(0, 0), (big, 1), (big + 3, big), (big // 2, big // 3), (1, big + 7)])
    run([(Fraction(0), Fraction(0)), (Fraction(7, 2), Fraction(1, 3)), (Fraction(5, 3), Fraction(9, 4)),
         (Fraction(1, 7), Fraction(5, 2))], integer=False)
