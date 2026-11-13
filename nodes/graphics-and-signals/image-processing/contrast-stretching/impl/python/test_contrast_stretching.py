# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contrast-stretching/. The authors are listed in prov/QDCGWA.jsonl.

import math
import random
from fractions import Fraction

import pytest

from contrast_stretching import contrast_stretching, stretch_ends

HALF = Fraction(1, 2)


def reference(image, levels, p_lo, p_hi):
    """Ends from the sorted pixel values (order statistics), then the exact map per pixel."""
    s = sorted(g for row in image for g in row)
    n = len(s)
    lo = s[math.floor(p_lo * n)]
    hi = s[math.ceil((1 - p_hi) * n) - 1]
    if lo == hi:
        return [row[:] for row in image]
    out = []
    for row in image:
        new_row = []
        for g in row:
            x = Fraction((levels - 1) * (g - lo), hi - lo)
            x = min(max(x, Fraction(0)), Fraction(levels - 1))
            new_row.append(math.floor(x + HALF))
        out.append(new_row)
    return out


def random_image(rng, levels):
    w, h = rng.randint(1, 7), rng.randint(1, 7)
    lo = rng.randrange(levels)
    hi = rng.randint(lo, levels - 1)
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def test_example() -> None:
    img = [[60, 70, 80], [90, 100, 110], [120, 130, 140]]
    assert contrast_stretching(img) == [[0, 32, 64], [96, 128, 159], [191, 223, 255]]
    # clip one pixel at each end: 70 and 130 become the ends
    p = Fraction(1, 9)
    assert contrast_stretching(img, 256, p, p) == [[0, 0, 43], [85, 128, 170], [213, 255, 255]]


def test_edges() -> None:
    assert contrast_stretching([[4, 4], [4, 4]], 8) == [[4, 4], [4, 4]]
    assert contrast_stretching([[3, 5]], 8) == [[0, 7]]
    assert contrast_stretching([[0, 7]], 8) == [[0, 7]]
    with pytest.raises(ValueError):
        contrast_stretching([[1]], 8, Fraction(1, 2), Fraction(1, 2))
    with pytest.raises(ValueError):
        contrast_stretching([[9]], 8)
    with pytest.raises(ValueError):
        contrast_stretching([], 8)


def test_random_against_reference() -> None:
    rng = random.Random(1709)
    for _ in range(800):
        levels = rng.choice([2, 4, 8, 16, 256])
        img = random_image(rng, levels)
        p_lo = Fraction(rng.randint(0, 20), 100)
        p_hi = Fraction(rng.randint(0, 20), 100)
        assert contrast_stretching(img, levels, p_lo, p_hi) == reference(img, levels, p_lo, p_hi)


def test_properties() -> None:
    rng = random.Random(64)
    for _ in range(500):
        levels = rng.choice([8, 16, 256])
        img = random_image(rng, levels)
        n = sum(len(r) for r in img)
        p_lo = Fraction(rng.randint(0, 25), 100)
        p_hi = Fraction(rng.randint(0, 25), 100)
        hist = [0] * levels
        for row in img:
            for g in row:
                hist[g] += 1
        lo, hi = stretch_ends(hist, p_lo, p_hi)
        assert lo <= hi
        # few pixels are clipped at each end
        assert sum(hist[:lo]) <= p_lo * n
        assert sum(hist[hi + 1 :]) <= p_hi * n
        out = contrast_stretching(img, levels, p_lo, p_hi)
        flat_in = [g for r in img for g in r]
        flat_out = [g for r in out for g in r]
        # order is kept, and distinct levels inside [lo, hi] stay distinct when hi - lo <= L - 1
        for a, b in zip(flat_in, flat_out):
            for c, d in zip(flat_in, flat_out):
                if a < c:
                    assert b <= d
                    if lo <= a and c <= hi and lo < hi:
                        assert b < d
        if lo < hi:
            assert min(flat_out) == 0 and max(flat_out) == levels - 1
