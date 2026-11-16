# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shi-tomasi-corner-detector/. The authors are listed in prov/K93XA7.jsonl.

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction

from shi_tomasi_corner_detector import (
    compare_roots,
    shi_tomasi_corners,
    shi_tomasi_response,
    structure_tensor,
)

getcontext().prec = 60


def pix(img, u, v):
    h, w = len(img), len(img[0])
    return img[min(max(v, 0), h - 1)][min(max(u, 0), w - 1)]


def oracle_lambda(img):
    """Direct 2D window sums and the eigenvalue in 60-digit decimals."""
    h, w = len(img), len(img[0])
    gx = [[pix(img, u + 1, v) - pix(img, u - 1, v) for u in range(w)] for v in range(h)]
    gy = [[pix(img, u, v + 1) - pix(img, u, v - 1) for u in range(w)] for v in range(h)]
    wt = [1, 2, 1]
    lam = {}
    for v in range(h):
        for u in range(w):
            a = b = c = 0
            for j in range(-1, 2):
                for i in range(-1, 2):
                    x = pix(gx, u + i, v + j)
                    y = pix(gy, u + i, v + j)
                    k = wt[i + 1] * wt[j + 1]
                    a += k * x * x
                    b += k * y * y
                    c += k * x * y
            disc = Decimal((a - b) ** 2 + 4 * c * c).sqrt()
            lam[(u, v)] = (Decimal(a + b) - disc) / 2
    return lam


def oracle_corners(img, q, d, n):
    h, w = len(img), len(img[0])
    lam = oracle_lambda(img)
    top = max(lam.values())
    qd = Decimal(q.numerator) / Decimal(q.denominator)
    cands = []
    for (u, v), x in lam.items():
        if not x > qd * top:
            continue
        if all(lam[(u + du, v + dv)] <= x for du in (-1, 0, 1) for dv in (-1, 0, 1)
               if (u + du, v + dv) in lam):
            cands.append((-x, v, u))
    cands.sort()
    kept = []
    for _, v, u in cands:
        if n is not None and len(kept) == n:
            break
        if all(math.hypot(u - x, v - y) >= d for x, y in kept):
            kept.append((u, v))
    return kept


def square(n, lo, hi, val=9):
    return [[val if (lo <= u <= hi and lo <= v <= hi) else 0 for u in range(n)] for v in range(n)]


def test_worked_example_single_corner():
    img = [[9 if (u >= 4 and v >= 4) else 0 for u in range(8)] for v in range(8)]
    a, b, c = structure_tensor(img)
    assert (a[4][4], b[4][4], c[4][4]) == (729, 729, 324)
    lam = shi_tomasi_response(img)
    assert lam[4][4] == 405.0 and lam[3][3] == 162.0
    assert (a[4][6], b[4][6], c[4][6]) == (0, 972, 0) and lam[4][6] == 0.0
    assert shi_tomasi_corners(img) == [(4, 4)]


def test_worked_example_square_and_selection():
    img = square(12, 3, 8)
    assert shi_tomasi_corners(img) == [(3, 3), (8, 3), (3, 8), (8, 8)]
    assert shi_tomasi_corners(img, min_distance=3) == [(3, 3), (8, 3), (3, 8), (8, 8)]
    assert shi_tomasi_corners(img, min_distance=3, max_corners=2) == [(3, 3), (8, 3)]
    # (8, 3) and (3, 8) are 5 away from (3, 3); (8, 8) is 5 sqrt(2), about 7.07, away.
    assert shi_tomasi_corners(img, min_distance=6) == [(3, 3), (8, 8)]


def test_flat_image_and_quality_one():
    assert shi_tomasi_corners([[5] * 6 for _ in range(6)]) == []
    assert shi_tomasi_corners(square(12, 3, 8), quality=1) == []
    assert shi_tomasi_corners([[3]]) == []


def test_compare_roots_against_decimals():
    rng = random.Random(5)
    for _ in range(3000):
        p1, p2 = rng.randint(-30, 30), rng.randint(-30, 30)
        n1, n2 = rng.choice([rng.randint(0, 900), rng.randint(0, 30) ** 2]), rng.randint(0, 900)
        x = Decimal(p1) - Decimal(n1).sqrt()
        y = Decimal(p2) - Decimal(n2).sqrt()
        want = (x > y) - (x < y)
        assert compare_roots(p1, n1, p2, n2) == want
    assert compare_roots(5, 4, 4, 1) == 0 and compare_roots(3, 2, 3, 2) == 0


def test_eigenvalue_identities():
    rng = random.Random(17)
    for _ in range(40):
        img = [[rng.randint(0, 9) for _ in range(6)] for _ in range(6)]
        a, b, c = structure_tensor(img)
        lam = shi_tomasi_response(img)
        for v in range(6):
            for u in range(6):
                x, aa, bb, cc = lam[v][u], a[v][u], b[v][u], c[v][u]
                scale = 1 + (aa + bb) ** 2
                assert x >= -1e-9
                assert abs(x * (aa + bb - x) - (aa * bb - cc * cc)) <= 1e-9 * scale
                # Rayleigh: no unit direction gives a smaller quadratic form.
                for k in range(12):
                    t = math.pi * k / 12
                    e, f = math.cos(t), math.sin(t)
                    assert aa * e * e + 2 * cc * e * f + bb * f * f >= x - 1e-9 * scale


def test_random_against_oracle():
    rng = random.Random(1994)
    for _ in range(600):
        w, h = rng.randint(3, 7), rng.randint(3, 7)
        img = [[rng.randint(0, 3) for _ in range(w)] for _ in range(h)]
        q = rng.choice([Fraction(0), Fraction(1, 10), Fraction(1, 2), Fraction(9, 10)])
        d = rng.choice([0, 1, 2, 3])
        n = rng.choice([None, 1, 3])
        assert shi_tomasi_corners(img, q, d, n) == oracle_corners(img, q, d, n)


def test_rotation_by_90_degrees():
    rng = random.Random(23)
    for _ in range(30):
        img = [[rng.randint(0, 20) for _ in range(7)] for _ in range(5)]
        h, w = 5, 7
        rot = [[img[h - 1 - j][i] for j in range(h)] for i in range(w)]  # rot[i][j] = img[h-1-j][i]
        la, lb = shi_tomasi_response(img), shi_tomasi_response(rot)
        for v in range(h):
            for u in range(w):
                # img pixel (u, v) goes to rot pixel (h - 1 - v, u).
                assert abs(la[v][u] - lb[u][h - 1 - v]) < 1e-9


def test_offset_and_gain():
    rng = random.Random(29)
    for _ in range(30):
        img = [[rng.randint(0, 20) for _ in range(7)] for _ in range(7)]
        base = shi_tomasi_corners(img, Fraction(1, 5), 2)
        assert shi_tomasi_corners([[x + 50 for x in r] for r in img], Fraction(1, 5), 2) == base
        assert shi_tomasi_corners([[3 * x for x in r] for r in img], Fraction(1, 5), 2) == base
