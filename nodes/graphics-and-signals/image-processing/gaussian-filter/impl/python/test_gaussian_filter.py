# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-filter/. The authors are listed in prov/T1ZJ15.jsonl.

import math
import random
from fractions import Fraction as F

from gaussian_filter import (BORDERS, border_index, box_cascade_kernel, box_cascade_sigma,
                             box_cascade_sum, gaussian_filter, gaussian_kernel, separable_filter)


def direct_2d(image, kernel2d, border):
    """Direct 2D filtering: sum over all (u, v) of K[v][u] f(x + u, y + v), O(k^2) per pixel."""
    h, w = len(image), len(image[0])
    rad = len(kernel2d) // 2
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            acc = 0
            for v in range(-rad, rad + 1):
                for u in range(-rad, rad + 1):
                    j, i = border_index(y + v, h, border), border_index(x + u, w, border)
                    if i is not None and j is not None:
                        acc += kernel2d[v + rad][u + rad] * image[j][i]
            row.append(acc)
        out.append(row)
    return out


def outer(a, b):
    return [[p * q for q in b] for p in a]


def rational_gaussian(sigma, radius):
    """A Gaussian kernel with each weight rounded to a Fraction, then normalized exactly."""
    raw = [F(math.exp(-u * u / (2 * sigma * sigma))).limit_denominator(10 ** 6)
           for u in range(-radius, radius + 1)]
    total = sum(raw)
    return [w / total for w in raw]


def test_kernel_values() -> None:
    k = gaussian_kernel(1.0)
    assert len(k) == 7
    assert abs(math.fsum(k) - 1) < 1e-15
    assert all(abs(k[i] - k[-1 - i]) < 1e-18 for i in range(7))
    assert abs(k[3] - 0.39905) < 1e-5
    assert abs(k[2] - 0.24203) < 1e-5
    assert abs(k[0] - 0.00443) < 1e-5
    assert len(gaussian_kernel(0.5)) == 5
    assert len(gaussian_kernel(2.0, radius=2)) == 5


def test_edges() -> None:
    assert separable_filter([], [1]) == []
    assert gaussian_filter([[7]], 1.0)[0][0] == 7.0 or abs(gaussian_filter([[7]], 1.0)[0][0] - 7) < 1e-12
    for bad in (0, -1):
        try:
            gaussian_kernel(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("sigma must be positive")
    try:
        separable_filter([[1]], [1, 1])
    except ValueError:
        pass
    else:
        raise AssertionError("an even kernel must be rejected")


def test_constant_image_is_kept() -> None:
    img = [[F(9)] * 5 for _ in range(4)]
    k = rational_gaussian(1.0, 3)
    for b in ("clamp", "mirror", "wrap"):
        assert separable_filter(img, k, b) == img


def test_separable_equals_direct_2d_exactly() -> None:
    rng = random.Random(1986)
    for trial in range(200):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        sigma = rng.choice([0.5, 0.8, 1.0, 1.5])
        rad = rng.randint(0, 3)
        k = rational_gaussian(sigma, rad)
        border = BORDERS[trial % 4]
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        assert separable_filter(img, k, border) == direct_2d(img, outer(k, k), border)


def test_float_gaussian_close_to_direct() -> None:
    rng = random.Random(3)
    img = [[rng.randint(0, 255) for _ in range(9)] for _ in range(8)]
    k = gaussian_kernel(1.2)
    fast = gaussian_filter(img, 1.2, "mirror")
    slow = direct_2d(img, outer(k, k), "mirror")
    assert all(abs(a - b) < 1e-9 for ra, rb in zip(fast, slow) for a, b in zip(ra, rb))


def test_cascade_kernel_and_sigma() -> None:
    assert box_cascade_kernel(1, 1) == [1, 1, 1]
    assert box_cascade_kernel(1, 2) == [1, 2, 3, 2, 1]
    assert box_cascade_kernel(1, 3) == [1, 3, 6, 7, 6, 3, 1]
    for r in range(4):
        for n in range(1, 5):
            k = box_cascade_kernel(r, n)
            assert sum(k) == (2 * r + 1) ** n
            c = len(k) // 2
            var = F(sum(w * (i - c) ** 2 for i, w in enumerate(k)), sum(k))
            assert var == F(n * r * (r + 1), 3)
            assert abs(box_cascade_sigma(r, n) ** 2 - n * r * (r + 1) / 3) < 1e-12


def test_cascade_wrap_equals_direct_2d() -> None:
    rng = random.Random(234)
    for _ in range(80):
        h, w = rng.randint(1, 7), rng.randint(1, 7)
        r, n = rng.randint(0, 2), rng.randint(1, 3)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        k = box_cascade_kernel(r, n)
        assert box_cascade_sum(img, r, n, "wrap") == direct_2d(img, outer(k, k), "wrap")


def test_cascade_clamp_matches_only_in_interior() -> None:
    rng = random.Random(9)
    found_difference = False
    for _ in range(40):
        h, w, r, n = 11, 12, 1, 3
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        k = box_cascade_kernel(r, n)
        fast = box_cascade_sum(img, r, n, "clamp")
        slow = direct_2d(img, outer(k, k), "clamp")
        m = n * r
        for y in range(h):
            for x in range(w):
                if m <= x < w - m and m <= y < h - m:
                    assert fast[y][x] == slow[y][x]
                elif fast[y][x] != slow[y][x]:
                    found_difference = True
    assert found_difference


def test_cascade_approaches_gaussian() -> None:
    errs = []
    for n in (1, 2, 3, 4, 6):
        k = box_cascade_kernel(2, n)
        total, c, s = sum(k), len(k) // 2, box_cascade_sigma(2, n)
        errs.append(max(abs(w / total - math.exp(-(i - c) ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi)))
                        for i, w in enumerate(k)))
    assert all(a > b for a, b in zip(errs, errs[1:]))
