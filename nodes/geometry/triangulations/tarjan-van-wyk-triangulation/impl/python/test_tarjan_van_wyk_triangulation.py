# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-van-wyk-triangulation/. The authors are listed in prov/GNAQSY.jsonl.
import random
from fractions import Fraction

from tarjan_van_wyk_triangulation import (
    Edges,
    diagonals,
    faces,
    key,
    sweep_visibility,
    trapezoids,
    triangulate,
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


def brute_visibility(pts):
    """Nearest edge on each side by comparing every pair of candidates."""
    E = Edges(pts)
    n = len(pts)

    def is_left(a, b):
        # a and b span a common height and do not cross: is a left of b there?
        for q in E.seg[a]:
            if q not in E.seg[b] and E.spans(b, q):
                return E.left_of(b, q)
        for q in E.seg[b]:
            if q not in E.seg[a] and E.spans(a, q):
                return not E.left_of(a, q)
        raise AssertionError("no witness")

    out = []
    for v in range(n):
        want_l, want_r = E.chord_sides(v)
        lefts = [s for s in range(n) if E.spans(s, v) and not E.left_of(s, v)]
        rights = [s for s in range(n) if E.spans(s, v) and E.left_of(s, v)]
        best_l = best_r = None
        for s in lefts:
            if best_l is None or is_left(best_l, s):
                best_l = s
        for s in rights:
            if best_r is None or is_left(s, best_r):
                best_r = s
        out.append((best_l if want_l else None, best_r if want_r else None))
    return out


def x_at(pts, E, s, y):
    hi, lo = E.seg[s]
    (x1, y1), (x2, y2) = pts[lo], pts[hi]
    return Fraction(x1) + Fraction(x2 - x1) * Fraction(y - y1, y2 - y1)


def trap_area2(pts, E, trap):
    top, bot, left, right = trap
    yt, yb = pts[top][1], pts[bot][1]
    if yt == yb:
        return 0
    wt = x_at(pts, E, right, yt) - x_at(pts, E, left, yt)
    wb = x_at(pts, E, right, yb) - x_at(pts, E, left, yb)
    assert wt >= 0 and wb >= 0
    return (wt + wb) * (yt - yb)


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


def run(pts):
    n = len(pts)
    E, hit = sweep_visibility(pts)
    assert hit == brute_visibility(pts)
    chords = sum((l is not None) + (r is not None) for l, r in hit)
    traps = trapezoids(E, hit)
    assert len(traps) == chords + 1
    assert sum(trap_area2(pts, E, t) for t in traps) == area2(pts)
    diags = diagonals(E, traps)
    pieces = faces(pts, [(i, (i + 1) % n) for i in range(n)] + sorted(diags))
    assert len(pieces) == len(diags) + 1
    for piece in pieces:
        m = len(piece)
        peaks = sum(1 for i in range(m)
                    if key(pts[piece[i]]) > key(pts[piece[i - 1]]) and key(pts[piece[i]]) > key(pts[piece[(i + 1) % m]]))
        assert peaks == 1
    tris = triangulate(pts)
    check_triangulation(pts, tris)
    return hit, traps, diags, tris


def test_example():
    pts = [(0, 0), (6, 0), (6, 4), (4, 4), (3, 1), (2, 4), (0, 4)]
    hit, traps, diags, tris = run(pts)
    assert hit[4] == (6, 1)                  # the notch sees edges v6v0 and v1v2
    assert diags == {(1, 4), (4, 6)}
    assert len(traps) == 6


def test_small_shapes():
    run([(0, 0), (5, 1), (2, 7)])
    run([(3, 0), (6, 1), (8, 3), (7, 6), (4, 8), (1, 7), (0, 4)])
    run([(0, 0), (5, 0), (7, 3), (2, 3)])
    run([(0, 0), (9, 1), (8, 5), (4, 2), (1, 6)])


def test_random_polygons():
    rng = random.Random(1988)
    for _ in range(150):
        run(random_polygon(rng, rng.randint(3, 24), 60))


def test_comb_and_spiral_like():
    rng = random.Random(3)
    for k in (3, 7):
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
                break
        run(pts)
        run([(y, -x) for x, y in pts])   # a quarter turn keeps the orientation


def test_fractions_and_large():
    big = 10 ** 15
    run([(0, 0), (big, 1), (big + 3, big), (big // 2, big // 3), (1, big + 7)])
    run([(Fraction(0), Fraction(0)), (Fraction(7, 2), Fraction(1, 3)), (Fraction(5, 3), Fraction(9, 4)),
         (Fraction(1, 7), Fraction(5, 2))])
