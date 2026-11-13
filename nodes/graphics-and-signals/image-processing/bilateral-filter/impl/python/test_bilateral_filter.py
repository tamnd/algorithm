# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilateral-filter/. The authors are listed in prov/1PRAE4.jsonl.

import math
import random
from fractions import Fraction as F

from bilateral_filter import bilateral_filter, gaussian_range, gaussian_spatial


def direct(image, radius, ws, wr):
    """The defining formula, one pixel at a time, window cut at the border."""
    h, w = len(image), len(image[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            num = den = 0
            for j in range(max(0, y - radius), min(h, y + radius + 1)):
                for i in range(max(0, x - radius), min(w, x + radius + 1)):
                    wt = ws(i - x, j - y) * wr(image[j][i] - image[y][x])
                    num += wt * image[j][i]
                    den += wt
            row.append(F(num) / den if not isinstance(num, float) else num / den)
        out.append(row)
    return out


def rational_spatial(u, v):
    return F(1, 1 + u * u + v * v)


def rational_range(d):
    return F(100, 100 + d * d)


def close(a, b, tol=1e-9):
    return all(abs(p - q) < tol for ra, rb in zip(a, b) for p, q in zip(ra, rb))


def test_example_row() -> None:
    img = [[10, 12, 10, 50, 48, 50]]
    got = bilateral_filter(img, 1.0, 10.0, radius=1)
    want = [10.7457, 10.9136, 10.7507, 49.2493, 49.0864, 49.2543]
    assert all(abs(a - b) < 1e-4 for a, b in zip(got[0], want))
    blur = bilateral_filter(img, 1.0, 1e9, radius=1)
    assert abs(blur[0][2] - 21.5109) < 1e-4 and abs(blur[0][3] - 38.4891) < 1e-4


def test_edges() -> None:
    assert bilateral_filter([]) == []
    assert bilateral_filter([[7]], 2.0, 5.0) == [[7.0]]
    img = [[F(3)] * 4 for _ in range(3)]
    assert bilateral_filter(img, radius=2, spatial=rational_spatial, rng_weight=rational_range) == img
    rng = random.Random(4)
    img = [[rng.randint(0, 9) for _ in range(5)] for _ in range(4)]
    assert bilateral_filter(img, radius=0, spatial=rational_spatial, rng_weight=rational_range) == img


def test_exact_rational_weights_against_direct() -> None:
    rng = random.Random(1998)
    for _ in range(150):
        h, w, r = rng.randint(1, 5), rng.randint(1, 5), rng.randint(0, 3)
        img = [[rng.randint(0, 60) for _ in range(w)] for _ in range(h)]
        got = bilateral_filter(img, radius=r, spatial=rational_spatial, rng_weight=rational_range)
        assert got == direct(img, r, rational_spatial, rational_range)


def test_gaussian_weights_against_direct() -> None:
    rng = random.Random(839)
    for _ in range(60):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        ss, sr = rng.choice([0.7, 1.0, 1.5]), rng.choice([5.0, 20.0, 80.0])
        r = math.ceil(2 * ss)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        got = bilateral_filter(img, ss, sr)
        assert close(got, direct(img, r, gaussian_spatial(ss), gaussian_range(sr)))


def test_output_stays_in_window_range() -> None:
    rng = random.Random(5)
    for _ in range(60):
        h, w, r = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 2)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        got = bilateral_filter(img, radius=r, spatial=rational_spatial, rng_weight=rational_range)
        for y in range(h):
            for x in range(w):
                win = [img[j][i] for j in range(max(0, y - r), min(h, y + r + 1))
                       for i in range(max(0, x - r), min(w, x + r + 1))]
                assert min(win) <= got[y][x] <= max(win)


def test_large_range_sigma_gives_normalized_gaussian() -> None:
    rng = random.Random(6)
    img = [[rng.randint(0, 255) for _ in range(6)] for _ in range(5)]
    got = bilateral_filter(img, 1.0, 1e12, radius=2)
    want = direct(img, 2, gaussian_spatial(1.0), lambda d: 1.0)
    assert close(got, want, 1e-6)
