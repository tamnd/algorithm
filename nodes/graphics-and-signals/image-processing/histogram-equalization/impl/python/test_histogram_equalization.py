# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-equalization/. The authors are listed in prov/JQ35J4.jsonl.

import math
import random
from fractions import Fraction

import pytest

from histogram_equalization import equalization_table, histogram_equalization

EXAMPLE = [
    [2, 3, 3, 2],
    [4, 2, 3, 5],
    [3, 3, 4, 3],
    [2, 4, 3, 3],
]


def reference(image: list[list[int]], levels: int) -> list[list[int]]:
    """Direct per-pixel formula in exact fractions: count the pixels at or below the value."""
    flat = [g for row in image for g in row]
    n = len(flat)
    out = []
    for row in image:
        new_row = []
        for g in row:
            c = sum(1 for v in flat if v <= g)
            x = Fraction((levels - 1) * c, n)
            new_row.append(math.floor(x + Fraction(1, 2)))
        out.append(new_row)
    return out


def histogram(image: list[list[int]], levels: int) -> list[int]:
    h = [0] * levels
    for row in image:
        for g in row:
            h[g] += 1
    return h


def random_image(rng: random.Random, levels: int) -> list[list[int]]:
    w, h = rng.randint(1, 7), rng.randint(1, 7)
    lo = rng.randrange(levels)
    hi = rng.randint(lo, levels - 1)
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def test_example() -> None:
    out = histogram_equalization(EXAMPLE, 8)
    assert out == [
        [2, 5, 5, 2],
        [7, 2, 5, 7],
        [5, 5, 7, 5],
        [2, 7, 5, 5],
    ]
    assert equalization_table(histogram(EXAMPLE, 8)) == [0, 0, 2, 5, 7, 7, 7, 7]
    assert histogram(out, 8) == [0, 0, 4, 0, 0, 8, 0, 4]


def test_edges() -> None:
    assert histogram_equalization([[5]], 8) == [[7]]
    assert histogram_equalization([[0, 0], [0, 0]], 8) == [[7, 7], [7, 7]]
    assert histogram_equalization([[0, 1]], 2) == [[1, 1]]
    assert histogram_equalization([[0, 255]], 256) == [[128, 255]]
    with pytest.raises(ValueError):
        histogram_equalization([], 8)
    with pytest.raises(ValueError):
        histogram_equalization([[8]], 8)


def test_random_against_reference() -> None:
    rng = random.Random(4127)
    for _ in range(600):
        levels = rng.choice([2, 3, 4, 8, 16, 256])
        img = random_image(rng, levels)
        assert histogram_equalization(img, levels) == reference(img, levels)


def test_properties() -> None:
    rng = random.Random(77)
    for _ in range(500):
        levels = rng.choice([4, 8, 16, 64])
        img = random_image(rng, levels)
        n = sum(len(r) for r in img)
        hist = histogram(img, levels)
        table = equalization_table(hist)
        # monotone, top level goes to L - 1, values in range
        assert all(table[k] <= table[k + 1] for k in range(levels - 1))
        assert table[-1] == levels - 1
        out = histogram_equalization(img, levels)
        # the number of distinct levels never grows
        assert len({g for r in out for g in r}) <= len({g for r in img for g in r})
        # idempotent
        assert histogram_equalization(out, levels) == out
        # the output cumulative histogram is within one input bin of the uniform one
        hmax = max(hist)
        hout = histogram(out, levels)
        c = 0
        for s in range(levels - 1):
            c += hout[s]
            target = Fraction(2 * s + 1, 2 * (levels - 1))
            assert target - Fraction(hmax, n) <= Fraction(c, n) < target
