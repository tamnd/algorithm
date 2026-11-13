# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-local-means/. The authors are listed in prov/S75JEX.jsonl.

import math
import random
from fractions import Fraction as F

from non_local_means import non_local_means


def direct(image, search, patch, weight):
    """The defining formula, pixel by pixel: each patch distance summed term by term."""
    h, w = len(image), len(image[0])

    def at(y, x):
        return image[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]

    area = (2 * patch + 1) ** 2
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            num = den = 0
            for qy in range(max(0, y - search), min(h, y + search + 1)):
                for qx in range(max(0, x - search), min(w, x + search + 1)):
                    total = sum((at(y + b, x + a) - at(qy + b, qx + a)) ** 2
                                for b in range(-patch, patch + 1) for a in range(-patch, patch + 1))
                    wq = weight(F(total, area))
                    num += wq * image[qy][qx]
                    den += wq
            row.append(num / den)
        out.append(row)
    return out


def rational(d):
    return F(1) / (1 + d / 100)


def close(a, b, tol=1e-9):
    return all(abs(p - q) < tol for ra, rb in zip(a, b) for p, q in zip(ra, rb))


def test_example_row() -> None:
    img = [[10, 12, 10, 50, 48, 50]]
    got = non_local_means(img, h=10.0, search=2, patch=1)
    want = [10.98268, 11.01222, 10.19651, 49.80349, 48.98778, 49.01732]
    assert all(abs(a - b) < 1e-5 for a, b in zip(got[0], want))


def test_edges() -> None:
    assert non_local_means([]) == []
    assert non_local_means([[7]]) == [[7.0]]
    rng = random.Random(1)
    img = [[rng.randint(0, 9) for _ in range(4)] for _ in range(3)]
    assert non_local_means(img, search=0, patch=2, weight=rational) == img
    const = [[5] * 4 for _ in range(3)]
    assert non_local_means(const, search=2, patch=1, weight=rational) == const


def test_exact_rational_weight_against_direct() -> None:
    rng = random.Random(2005)
    for _ in range(80):
        h, w = rng.randint(1, 5), rng.randint(1, 5)
        s, f = rng.randint(0, 2), rng.randint(0, 2)
        img = [[rng.randint(0, 40) for _ in range(w)] for _ in range(h)]
        assert non_local_means(img, search=s, patch=f, weight=rational) == direct(img, s, f, rational)


def test_exp_weight_against_direct() -> None:
    rng = random.Random(490)
    for _ in range(40):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        s, f, hh = rng.randint(1, 2), rng.randint(0, 2), rng.choice([5.0, 15.0, 40.0])
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        got = non_local_means(img, h=hh, search=s, patch=f)
        assert close(got, direct(img, s, f, lambda d: math.exp(-d / (hh * hh))))


def test_output_is_a_convex_combination() -> None:
    rng = random.Random(9)
    for _ in range(40):
        h, w, s = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 2)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        got = non_local_means(img, search=s, patch=1, weight=rational)
        for y in range(h):
            for x in range(w):
                win = [img[j][i] for j in range(max(0, y - s), min(h, y + s + 1))
                       for i in range(max(0, x - s), min(w, x + s + 1))]
                assert min(win) <= got[y][x] <= max(win)
