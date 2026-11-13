# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clahe/. The authors are listed in prov/KNVCNG.jsonl.

import math
import random
from fractions import Fraction

import pytest

from clahe import clahe, clip_histogram, clip_limit, equalization_table

HALF = Fraction(1, 2)


def global_reference(image: list[list[int]], levels: int) -> list[list[int]]:
    """Global equalization by the direct per-pixel formula in exact fractions."""
    flat = [g for row in image for g in row]
    n = len(flat)
    return [
        [math.floor(Fraction((levels - 1) * sum(1 for v in flat if v <= g), n) + HALF) for g in row]
        for row in image
    ]


def tent_weights(pos: int, size: int, count: int) -> list[Fraction]:
    """Weight of each tile along one axis: a hat function of the clamped tile coordinate."""
    u = Fraction(2 * pos + 1, 2 * size) - HALF
    u = min(max(u, Fraction(0)), Fraction(count - 1))
    return [max(Fraction(0), 1 - abs(u - a)) for a in range(count)]


def clahe_reference(image, levels, tiles_x, tiles_y, alpha):
    """CLAHE written out with fractions, tile by tile and pixel by pixel."""
    height, width = len(image), len(image[0])
    tw, th = width // tiles_x, height // tiles_y
    n = tw * th
    beta = n if math.isinf(alpha) else max(1, math.floor(alpha * n / levels))
    maps = {}
    for b in range(tiles_y):
        for a in range(tiles_x):
            vals = [image[y][x] for y in range(b * th, (b + 1) * th) for x in range(a * tw, (a + 1) * tw)]
            hist = [vals.count(k) for k in range(levels)]
            excess = sum(max(v - beta, 0) for v in hist)
            hist = [min(v, beta) + excess // levels for v in hist]
            r = excess % levels
            for m in range(r):
                hist[(m * levels) // r] += 1
            cum = [sum(hist[: k + 1]) for k in range(levels)]
            maps[a, b] = [Fraction((levels - 1) * cum[k], n) for k in range(levels)]
    out = []
    for y in range(height):
        wy = tent_weights(y, th, tiles_y)
        row = []
        for x in range(width):
            wx = tent_weights(x, tw, tiles_x)
            g = image[y][x]
            value = sum(
                wx[a] * wy[b] * math.floor(maps[a, b][g] + HALF)
                for a in range(tiles_x)
                for b in range(tiles_y)
            )
            row.append(math.floor(value + HALF))
        out.append(row)
    return out


def random_image(rng, width, height, levels):
    lo = rng.randrange(levels)
    hi = rng.randint(lo, levels - 1)
    return [[rng.randint(lo, hi) for _ in range(width)] for _ in range(height)]


def test_clip_keeps_total_count() -> None:
    rng = random.Random(9001)
    for _ in range(2000):
        levels = rng.randint(1, 40)
        hist = [rng.choice([0, 0, rng.randint(0, 50)]) for _ in range(levels)]
        limit = rng.randint(1, 60)
        out = clip_histogram(hist, limit)
        assert sum(out) == sum(hist)
        excess = sum(max(v - limit, 0) for v in hist)
        q = excess // levels
        assert all(v <= max(limit, h) + q + 1 for v, h in zip(out, hist))
        assert all(v >= min(h, limit) for v, h in zip(out, hist))
        if excess == 0:
            assert out == hist


def test_one_tile_no_clip_is_global_equalization() -> None:
    rng = random.Random(31)
    for _ in range(300):
        levels = rng.choice([2, 4, 8, 16, 256])
        img = random_image(rng, rng.randint(1, 7), rng.randint(1, 7), levels)
        assert clahe(img, levels, 1, 1, math.inf) == global_reference(img, levels)
        # a clip limit at or above the tile size also leaves the histogram alone
        n = len(img) * len(img[0])
        assert clahe(img, levels, 1, 1, float(levels)) == global_reference(img, levels)
        assert clip_limit(float(levels), n, levels) == n


def test_against_reference() -> None:
    rng = random.Random(2024)
    for _ in range(150):
        levels = rng.choice([4, 8, 16])
        tiles_x, tiles_y = rng.randint(1, 3), rng.randint(1, 3)
        tw, th = rng.randint(1, 4), rng.randint(1, 4)
        img = random_image(rng, tiles_x * tw, tiles_y * th, levels)
        alpha = rng.choice([1.0, 1.5, 2.0, 3.0, math.inf])
        assert clahe(img, levels, tiles_x, tiles_y, alpha) == clahe_reference(img, levels, tiles_x, tiles_y, alpha)


def test_output_range_and_monotone_tables() -> None:
    rng = random.Random(5)
    for _ in range(500):
        levels = rng.choice([4, 16, 256])
        img = random_image(rng, 2 * rng.randint(1, 4), 2 * rng.randint(1, 4), levels)
        out = clahe(img, levels, 2, 2, rng.choice([1.0, 2.0, math.inf]))
        assert all(0 <= v < levels for row in out for v in row)
    # a single table is monotone and ends at L - 1
    for _ in range(500):
        hist = [rng.randint(0, 9) for _ in range(12)]
        if sum(hist) == 0:
            continue
        t = equalization_table(clip_histogram(hist, rng.randint(1, 9)))
        assert all(t[k] <= t[k + 1] for k in range(11)) and t[-1] == 11


def test_constant_image_and_errors() -> None:
    img = [[3] * 4 for _ in range(4)]
    assert clahe(img, 8, 2, 2, math.inf) == [[7] * 4 for _ in range(4)]
    with pytest.raises(ValueError):
        clahe([[1, 2, 3]], 8, 2, 1, 2.0)
    with pytest.raises(ValueError):
        clahe([], 8, 1, 1, 2.0)
