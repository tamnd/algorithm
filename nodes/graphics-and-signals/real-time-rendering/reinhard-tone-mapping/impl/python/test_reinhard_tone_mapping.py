# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reinhard-tone-mapping/. The authors are listed in prov/FX4QEZ.jsonl.

"""Tests of the Reinhard operator against closed forms and brute force.

The global operator is checked on the check values of Equation 3, on the
white point of Equation 4, for monotonicity and for invariance to the
exposure of the input. The separable blur of the local operator is checked
against a direct 2D convolution, and the local operator against the global
one on a constant image and against a direct per-pixel scale search.
"""

import math
import random

from reinhard_tone_mapping import (
    ALPHA1,
    blur,
    compress,
    gaussian_kernel,
    log_average,
    luminance,
    reinhard_global,
    reinhard_local,
    scales,
    tone_map_rgb,
)


def random_image(rng: random.Random, w: int, h: int) -> list[list[float]]:
    """Luminances spread over six orders of magnitude, log uniform."""
    return [[10.0 ** rng.uniform(-3.0, 3.0) for _ in range(w)] for _ in range(h)]


def test_check_values() -> None:
    assert compress(1.0) == 0.5
    assert compress(3.0) == 0.75
    assert compress(0.0) == 0.0


def test_white_point() -> None:
    for white in (0.5, 1.0, 2.0, 7.5, 100.0):
        assert abs(compress(white, white) - 1.0) < 1e-12
    # A large Lwhite gives Equation 3.
    for l in (0.01, 0.5, 2.0, 30.0):
        assert abs(compress(l, 1e9) - compress(l)) < 1e-12


def test_log_average_is_geometric_mean() -> None:
    rng = random.Random(1)
    img = random_image(rng, 8, 8)
    flat = [x for row in img for x in row]
    direct = math.prod(x ** (1.0 / len(flat)) for x in flat)
    assert abs(log_average(img, 0.0) - direct) < 1e-9 * direct


def test_key_maps_log_average() -> None:
    # A constant image c has log average c, so every pixel scales to the key.
    for c in (0.001, 1.0, 250.0):
        out = reinhard_global([[c] * 4 for _ in range(3)], key=0.18, delta=0.0)
        for row in out:
            for v in row:
                assert abs(v - 0.18 / 1.18) < 1e-12


def test_page_example() -> None:
    img = [[0.01, 0.1, 1.0, 10.0, 100.0]]
    simple = reinhard_global(img, delta=0.0)[0]
    white = reinhard_global(img, l_white="max", delta=0.0)[0]
    want_simple = [0.0018, 0.01768, 0.15254, 0.64286, 0.94737]
    want_white = [0.0018, 0.01768, 0.15263, 0.64643, 1.0]
    for got, want in zip(simple, want_simple):
        assert abs(got - want) < 5e-6
    for got, want in zip(white, want_white):
        assert abs(got - want) < 5e-6


def test_monotone_and_range() -> None:
    rng = random.Random(2)
    img = random_image(rng, 16, 16)
    flat = sorted(x for row in img for x in row)
    for l_white in (None, "max", 3.0):
        out = reinhard_global([flat], l_white=l_white)[0]
        assert all(a < b for a, b in zip(out, out[1:]))
        assert out[0] > 0.0
        if l_white is None:
            assert out[-1] < 1.0
        if l_white == "max":
            assert abs(out[-1] - 1.0) < 1e-12


def test_exposure_invariance() -> None:
    # With delta = 0, scaling every input by c > 0 leaves the output unchanged.
    rng = random.Random(3)
    img = random_image(rng, 6, 5)
    base = reinhard_global(img, delta=0.0)
    for c in (1e-3, 0.5, 40.0):
        out = reinhard_global([[c * x for x in row] for row in img], delta=0.0)
        for ra, rb in zip(base, out):
            for a, b in zip(ra, rb):
                assert abs(a - b) < 1e-12


def brute_blur(img: list[list[float]], width: float) -> list[list[float]]:
    """Direct 2D convolution with the truncated kernel of Equation 5."""
    radius = len(gaussian_kernel(width)) // 2
    h, w = len(img), len(img[0])
    weights = {}
    total = 0.0
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            r2 = dx * dx + dy * dy
            wt = math.exp(-r2 / (width * width)) / (math.pi * width * width)
            weights[(dx, dy)] = wt
            total += wt
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            acc = 0.0
            for (dx, dy), wt in weights.items():
                xx = min(w - 1, max(0, x + dx))
                yy = min(h - 1, max(0, y + dy))
                acc += wt * img[yy][xx]
            out[y][x] = acc / total
    return out


def test_blur_against_direct_convolution() -> None:
    rng = random.Random(4)
    img = random_image(rng, 12, 10)
    for k in range(5):
        width = ALPHA1 * 1.6 ** k
        fast = blur(img, width)
        slow = brute_blur(img, width)
        for ra, rb in zip(fast, slow):
            for a, b in zip(ra, rb):
                assert abs(a - b) < 1e-9 * max(1.0, abs(b))


def test_local_on_constant_image() -> None:
    # Every blur of a constant image is the same constant, so V = 0, the
    # largest scale is chosen, and the result equals the global operator.
    img = [[3.0] * 32 for _ in range(32)]
    out, chosen = reinhard_local(img, return_scales=True)
    glob = reinhard_global(img)
    for y in range(32):
        for x in range(32):
            assert chosen[y][x] == 7
            assert abs(out[y][x] - glob[y][x]) < 1e-12


def direct_local(img, key=0.18, phi=8.0, eps=0.05, r=8, delta=1e-6):
    """The local operator with the scale search written per pixel.

    For each pixel and scale it computes the center and the surround by
    direct 2D convolution, independent of the separable blur.
    """
    lbar = log_average(img, delta)
    lum = [[key * x / lbar for x in row] for row in img]
    blurs = [brute_blur(lum, ALPHA1 * 1.6 ** k) for k in range(r + 1)]
    s = scales(r)
    h, w = len(img), len(img[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            passed = [
                abs((blurs[k][y][x] - blurs[k + 1][y][x]) / (key * 2.0 ** phi / s[k] ** 2 + blurs[k][y][x])) < eps
                for k in range(r)
            ]
            m = 0
            while m + 1 < r and passed[m] and passed[m + 1]:
                m += 1
            out[y][x] = min(1.0, lum[y][x] / (1.0 + blurs[m][y][x]))
    return out


def test_local_against_direct() -> None:
    rng = random.Random(5)
    img = random_image(rng, 10, 9)
    fast = reinhard_local(img, r=4)
    slow = direct_local(img, r=4)
    for ra, rb in zip(fast, slow):
        for a, b in zip(ra, rb):
            assert abs(a - b) < 1e-9


def test_local_step_image() -> None:
    w = 32
    img = [[0.05 if x < 16 else 5.0 for x in range(w)] for _ in range(w)]
    out, chosen = reinhard_local(img, return_scales=True)
    glob = reinhard_global(img)
    # The trace on the page: pixel 19 of row 16 keeps scale 4.
    assert chosen[16][19] == 4
    assert abs(out[16][19] - 0.6491) < 5e-5
    # Next to the step, the dark side gets darker and the bright side
    # brighter than with the global operator: local contrast goes up.
    assert out[16][15] < glob[16][15]
    assert out[16][16] > glob[16][16]
    for row in out:
        for v in row:
            assert 0.0 <= v <= 1.0


def test_local_range_random() -> None:
    rng = random.Random(6)
    img = random_image(rng, 32, 32)
    out, chosen = reinhard_local(img, return_scales=True)
    for ro, rc in zip(out, chosen):
        for v, m in zip(ro, rc):
            assert 0.0 <= v <= 1.0
            assert 0 <= m < 8


def test_rgb_keeps_ratios() -> None:
    rgb = [[(2.0, 1.0, 0.5), (0.1, 0.2, 0.4)]]
    lw = [[luminance(c) for c in row] for row in rgb]
    ld = reinhard_global(lw)
    out = tone_map_rgb(rgb, ld)
    for row_in, row_out, row_ld in zip(rgb, out, ld):
        for c, d, l in zip(row_in, row_out, row_ld):
            assert abs(luminance(d) - l) < 1e-12
            assert abs(d[0] * c[1] - d[1] * c[0]) < 1e-12
