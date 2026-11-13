# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unsharp-masking/. The authors are listed in prov/JCQW4C.jsonl.

import random
from fractions import Fraction as F

from unsharp_masking import BORDERS, border_index, combined_kernel, separable_blur, unsharp_mask

BINOMIAL = [F(1, 4), F(1, 2), F(1, 4)]


def direct_2d(image, kernel2d, border):
    """Direct 2D filtering with the given kernel and border rule, O(k^2) per pixel."""
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


def random_kernel(rng, rad):
    half = [F(rng.randint(1, 9)) for _ in range(rad + 1)]
    raw = half[:0:-1] + half
    total = sum(raw)
    return [w / total for w in raw]


def test_step_example() -> None:
    img = [[10, 10, 10, 50, 50, 50]]
    assert separable_blur(img, BINOMIAL, "clamp") == [[10, 10, 20, 40, 50, 50]]
    assert unsharp_mask(img, 1, BINOMIAL, border="clamp") == [[10, 10, 0, 60, 50, 50]]
    assert unsharp_mask(img, 1, BINOMIAL, border="clamp", low=0, high=50) == [[10, 10, 0, 50, 50, 50]]
    assert unsharp_mask(img, 1, BINOMIAL, border="clamp", threshold=11) == img


def test_edges() -> None:
    assert unsharp_mask([], 1, BINOMIAL) == []
    assert unsharp_mask([[5]], 3, BINOMIAL) == [[5]]
    assert unsharp_mask([[F(7)] * 4] * 3, F(5, 2), BINOMIAL, border="mirror") == [[F(7)] * 4] * 3
    img = [[1, 2], [3, 4]]
    assert unsharp_mask(img, 0, BINOMIAL) == img


def test_matches_direct_combined_kernel() -> None:
    rng = random.Random(1951)
    for trial in range(250):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        k = random_kernel(rng, rng.randint(0, 2))
        amount = F(rng.randint(0, 12), rng.randint(1, 4))
        border = BORDERS[trial % 4]
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        got = unsharp_mask(img, amount, k, border=border)
        assert got == direct_2d(img, combined_kernel(k, amount), border)


def test_threshold_against_direct_formula() -> None:
    rng = random.Random(42)
    for _ in range(150):
        h, w = rng.randint(1, 5), rng.randint(1, 5)
        k = random_kernel(rng, 1)
        amount, t = F(rng.randint(1, 6), 2), F(rng.randint(0, 30))
        img = [[rng.randint(0, 100) for _ in range(w)] for _ in range(h)]
        blur = direct_2d(img, [[a * b for b in k] for a in k], "clamp")
        want = [[img[y][x] if abs(img[y][x] - blur[y][x]) < t else img[y][x] + amount * (img[y][x] - blur[y][x])
                 for x in range(w)] for y in range(h)]
        assert unsharp_mask(img, amount, k, border="clamp", threshold=t) == want


def test_float_gaussian_default() -> None:
    rng = random.Random(8)
    img = [[rng.randint(0, 255) for _ in range(7)] for _ in range(6)]
    got = unsharp_mask(img, 1.5, sigma=0.8, border="mirror")
    from unsharp_masking import gaussian_kernel
    k = gaussian_kernel(0.8)
    want = direct_2d(img, combined_kernel(k, 1.5), "mirror")
    assert all(abs(a - b) < 1e-9 for ra, rb in zip(got, want) for a, b in zip(ra, rb))
