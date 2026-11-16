# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dlt-homography/. The authors are listed in prov/12XVFY.jsonl.
"""Tests of the normalized DLT for homographies."""

import math
import random
from fractions import Fraction

import pytest

from cvla import inv, matvec, mul, norm, sub
from dlt_homography import (apply, canonical, dlt_homography, dlt_rows,
                            dlt_singular_values, inverse, normalizing_similarity,
                            transfer_errors)


def exact_four_point(src, dst):
    """Independent oracle: solve the 8 x 8 linear system with h33 = 1 in
    exact rational arithmetic (Gauss-Jordan elimination)."""
    a = []
    for (x, y), (u, v) in zip(src, dst):
        x, y, u, v = Fraction(x), Fraction(y), Fraction(u), Fraction(v)
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y, u])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y, v])
    a = [[Fraction(c) for c in row] for row in a]
    for c in range(8):
        p = next(r for r in range(c, 8) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        for r in range(8):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    h = [a[i][8] / a[i][i] for i in range(8)] + [Fraction(1)]
    return [h[0:3], h[3:6], h[6:9]]


def random_homography(rng):
    """A homography of pixel images that keeps [0, 640] x [0, 480] in front
    (third coordinate > 0)."""
    return [[1.0 + rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(-50, 50)],
            [rng.uniform(-0.3, 0.3), 1.0 + rng.uniform(-0.3, 0.3), rng.uniform(-50, 50)],
            [rng.uniform(-4e-4, 4e-4), rng.uniform(-4e-4, 4e-4), 1.0]]


def random_points(rng, n):
    return [[rng.uniform(0, 640), rng.uniform(0, 480)] for _ in range(n)]


def rel_dist(a, b):
    return norm(sub(canonical(a), canonical(b)))


def test_square_to_trapezoid():
    src = [(0, 0), (1, 0), (1, 1), (0, 1)]
    dst = [(0, 0), (4, 0), (3, 2), (1, 2)]
    H = dlt_homography(src, dst)
    want = [[4.0, 2.0, 0.0], [0.0, 4.0, 0.0], [0.0, 1.0, 1.0]]
    assert rel_dist(H, want) <= 1e-12
    assert exact_four_point(src, dst) == [[4, 2, 0], [0, 4, 0], [0, 1, 1]]
    u, v = apply(H, (0.5, 0.5))
    assert abs(u - 2.0) <= 1e-12 and abs(v - 4.0 / 3.0) <= 1e-12


def test_rows_vanish_on_the_true_homography():
    rng = random.Random(1)
    for _ in range(50):
        H = random_homography(rng)
        h = [c for row in H for c in row]
        p = random_points(rng, 1)[0]
        y1 = [p[0], p[1], 1.0]
        y2 = matvec(H, y1)
        for row in dlt_rows(y1, y2):
            assert abs(sum(a * b for a, b in zip(row, h))) <= 1e-9 * norm(row) * norm(h)


def test_four_points_against_exact_oracle():
    rng = random.Random(2)
    done = 0
    while done < 40:
        src = [(rng.randint(0, 640), rng.randint(0, 480)) for _ in range(4)]
        dst = [(rng.randint(0, 640), rng.randint(0, 480)) for _ in range(4)]
        if any(Fraction(0) == ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
               for pts in (src, dst) for i, a in enumerate(pts) for j, b in enumerate(pts)
               for k, c in enumerate(pts) if i < j < k):
            continue
        Hx = exact_four_point(src, dst)
        Hf = [[float(c) for c in row] for row in Hx]
        H = dlt_homography(src, dst)
        assert rel_dist(H, Hf) <= 1e-8
        done += 1


def test_exact_recovery_many_points():
    rng = random.Random(3)
    for n in (4, 5, 8, 20, 50):
        for _ in range(4):
            Ht = random_homography(rng)
            x1 = random_points(rng, n)
            x2 = [apply(Ht, p) for p in x1]
            H = dlt_homography(x1, x2)
            assert rel_dist(H, Ht) <= 1e-8
            assert max(transfer_errors(H, x1, x2)) <= 1e-7


def test_plain_dlt_agrees_on_exact_data():
    rng = random.Random(4)
    Ht = random_homography(rng)
    x1 = random_points(rng, 10)
    x2 = [apply(Ht, p) for p in x1]
    assert rel_dist(dlt_homography(x1, x2, normalize=False), Ht) <= 1e-6


def test_normalizing_similarity():
    rng = random.Random(5)
    pts = random_points(rng, 30)
    T = normalizing_similarity(pts)
    q = [matvec(T, [p[0], p[1], 1.0]) for p in pts]
    assert abs(sum(r[0] for r in q)) <= 1e-9 and abs(sum(r[1] for r in q)) <= 1e-9
    mean = sum(math.hypot(r[0], r[1]) for r in q) / len(q)
    assert abs(mean - math.sqrt(2.0)) <= 1e-12
    with pytest.raises(ValueError):
        normalizing_similarity([[3.0, 4.0]] * 5)


def test_covariance_under_similarities():
    """Normalized DLT commutes with similarity changes of both frames."""
    rng = random.Random(6)
    Ht = random_homography(rng)
    x1 = random_points(rng, 30)
    x2 = [[a + rng.gauss(0, 1.0) for a in apply(Ht, p)] for p in x1]
    H = dlt_homography(x1, x2)
    c, s = math.cos(0.7), math.sin(0.7)
    S1 = [[3 * c, -3 * s, 100.0], [3 * s, 3 * c, -40.0], [0.0, 0.0, 1.0]]
    S2 = [[0.5, 0.0, 7.0], [0.0, 0.5, 9.0], [0.0, 0.0, 1.0]]
    y1 = [apply(S1, p) for p in x1]
    y2 = [apply(S2, p) for p in x2]
    G = dlt_homography(y1, y2)
    assert rel_dist(G, mul(mul(S2, H), inv(S1))) <= 1e-9


def test_noise_gives_small_transfer_error():
    rng = random.Random(7)
    sigma = 0.5
    for _ in range(5):
        Ht = random_homography(rng)
        x1 = random_points(rng, 60)
        x2 = [[a + rng.gauss(0, sigma) for a in apply(Ht, p)] for p in x1]
        H = dlt_homography(x1, x2)
        clean = [apply(Ht, p) for p in x1]
        err = transfer_errors(H, x1, clean)
        assert math.sqrt(sum(e * e for e in err) / len(err)) <= sigma


def test_swap_gives_inverse():
    rng = random.Random(8)
    Ht = random_homography(rng)
    x1 = random_points(rng, 12)
    x2 = [apply(Ht, p) for p in x1]
    assert rel_dist(dlt_homography(x2, x1), inverse(dlt_homography(x1, x2))) <= 1e-8


def test_three_collinear_points_lose_rank():
    src = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (0.0, 3.0)]
    dst = [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (1.0, 4.0)]
    s = dlt_singular_values(src, dst)
    assert s[-1] <= 1e-12 * s[0]
    assert s[-2] <= 1e-12 * s[0]
    good = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    s = dlt_singular_values(good, dst)
    assert s[-2] >= 1e-3 * s[0]


def test_bad_input():
    with pytest.raises(ValueError):
        dlt_homography([(0, 0), (1, 0), (0, 1)], [(0, 0), (1, 0), (0, 1)])
    with pytest.raises(ValueError):
        dlt_homography([(0, 0)] * 4, [(0, 0), (1, 0), (0, 1), (1, 1)])
