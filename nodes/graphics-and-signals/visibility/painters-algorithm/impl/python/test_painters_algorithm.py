# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/painters-algorithm/. The authors are listed in prov/5FR13Q.jsonl.

import itertools
import random
from fractions import Fraction

from painters_algorithm import painters_algorithm

W, H = 8, 6


def inside(poly, x, y):
    """Independent closed point-in-convex-polygon test by barycentric signs on a fan."""
    a = poly[0]
    for k in range(1, len(poly) - 1):
        b, c = poly[k], poly[k + 1]
        d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if d == 0:
            continue
        l1 = Fraction((b[0] - x) * (c[1] - y) - (b[1] - y) * (c[0] - x), 1) / d
        l2 = Fraction((c[0] - x) * (a[1] - y) - (c[1] - y) * (a[0] - x), 1) / d
        l3 = 1 - l1 - l2
        if l1 >= 0 and l2 >= 0 and l3 >= 0:
            return True
    return False


def zplane(poly, x, y):
    """Depth by solving for the plane z = p x + q y + r with Cramer's rule."""
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = poly[0], poly[1], poly[2]
    det = x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2)
    p = Fraction(z1 * (y2 - y3) - y1 * (z2 - z3) + (z2 * y3 - z3 * y2), det)
    q = Fraction(x1 * (z2 - z3) - z1 * (x2 - x3) + (x2 * z3 - x3 * z2), det)
    r = Fraction(x1 * (y2 * z3 - y3 * z2) - y1 * (x2 * z3 - x3 * z2) + z1 * (x2 * y3 - x3 * y2), det)
    return p * x + q * y + r


def brute(polys, w, h):
    """Per-pixel exact depth test over all polygons. None marks a tie."""
    img = []
    for j in range(h):
        row = []
        for i in range(w):
            x, y = Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2)
            hits = [(zplane(p, x, y), k) for k, p in enumerate(polys) if inside(p, x, y)]
            if not hits:
                row.append(-1)
                continue
            top = max(d for d, _ in hits)
            win = [k for d, k in hits if d == top]
            row.append(win[0] if len(win) == 1 else None)
        img.append(row)
    return img


def agrees(img, ref):
    return all(r is None or r == g for rr, gg in zip(ref, img) for r, g in zip(rr, gg))


def random_triangle(rng, zlo, zhi):
    while True:
        pts = [(rng.randint(-1, W + 1), rng.randint(-1, H + 1)) for _ in range(3)]
        (ax, ay), (bx, by), (cx, cy) = pts
        if (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) != 0:
            return [(x, y, rng.randint(zlo, zhi)) for x, y in pts]


def test_worked_example():
    a = [(0, 0, 1), (6, 0, 1), (6, 4, 1), (0, 4, 1)]
    b = [(3, 1, 3), (8, 1, 3), (5, 6, 3)]
    c = [(1, 2, 5), (5, 2, 5), (1, 6, 5)]
    img = painters_algorithm([a, b, c], W, H)
    rows = ["".join(".ABC"[p + 1] for p in row) for row in reversed(img)]
    assert rows == [".C......", ".CC.BB..", "ACCCBBB.", "ACCCCBB.", "AAABBBBB", "AAAAAA.."]
    assert img == brute([a, b, c], W, H)


def test_overlapping_depth_ranges_fail():
    d = [(0, 0, 0), (8, 0, 8), (8, 6, 8), (0, 6, 0)]
    e = [(5, 1, 5), (7, 1, 5), (7, 3, 5), (5, 3, 5)]
    img = painters_algorithm([d, e], W, H)
    ref = brute([d, e], W, H)
    wrong = [(i, j) for j in range(H) for i in range(W) if img[j][i] != ref[j][i]]
    assert wrong == [(5, 1), (6, 1), (5, 2), (6, 2)]
    # The reverse order is right: a valid order exists, but the sort does not find it.
    assert paint_in_order([d, e], [1, 0]) == ref


def paint_in_order(polys, order):
    img = [[-1] * W for _ in range(H)]
    for k in order:
        for j in range(H):
            for i in range(W):
                if inside(polys[k], Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2)):
                    img[j][i] = k
    return img


def test_cyclic_overlap_has_no_valid_order():
    s1 = [(0, 1, 1), (8, 1, 3), (8, 2, 3), (0, 2, 1)]
    s2 = [(5, 0, 0), (6, 0, 0), (2, 6, 4), (1, 6, 4)]
    s3 = [(1, 0, 4), (2, 0, 4), (7, 6, -2), (6, 6, -2)]
    polys = [s1, s2, s3]
    ref = brute(polys, W, H)
    for perm in itertools.permutations(range(3)):
        assert not agrees(paint_in_order(polys, perm), ref)
    assert not agrees(painters_algorithm(polys, W, H), ref)


def test_edges():
    assert painters_algorithm([], 3, 2) == [[-1, -1, -1], [-1, -1, -1]]
    far = [(20, 20, 0), (30, 20, 0), (20, 30, 0)]
    assert painters_algorithm([far], 3, 2, background=7) == [[7, 7, 7], [7, 7, 7]]
    one = [(0, 0, 0), (3, 0, 0), (0, 3, 0)]
    assert painters_algorithm([one], 3, 2) == [[0, 0, 0], [0, 0, -1]]
    same = [(0, 0, 2), (8, 0, 2), (0, 6, 2)]
    # Equal keys keep the input order, so the later polygon wins.
    assert painters_algorithm([one, same], 3, 2) == [[1, 1, 1], [1, 1, 1]]


def test_layered_scenes_match_brute_force():
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randint(1, 5)
        layers = rng.sample(range(n), n)
        polys = [random_triangle(rng, 10 * layers[k], 10 * layers[k] + 9) for k in range(n)]
        assert agrees(painters_algorithm(polys, W, H), brute(polys, W, H))


def test_errors_need_overlapping_depth_ranges():
    rng = random.Random(6)
    errors = 0
    for _ in range(500):
        polys = [random_triangle(rng, 0, 9) for _ in range(rng.randint(2, 4))]
        img, ref = painters_algorithm(polys, W, H), brute(polys, W, H)
        for j in range(H):
            for i in range(W):
                got, want = img[j][i], ref[j][i]
                if want is None or got == want:
                    continue
                errors += 1
                p, q = polys[got], polys[want]
                # The proof gives min p < max q and min q <= max p.
                assert min(v[2] for v in p) < max(v[2] for v in q)
                assert min(v[2] for v in q) <= max(v[2] for v in p)
    assert errors > 0
