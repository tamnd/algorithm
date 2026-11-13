# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-of-gaussian/. The authors are listed in prov/P120H7.jsonl.

import math
import random

import pytest

from laplacian_of_gaussian import laplacian_of_gaussian, log_kernels, marr_hildreth, zero_crossings


def kernel_2d(sigma):
    """The closed form ((u^2 + v^2 - c) / s) G(u, v), with c and s fitted to the same two moment conditions."""
    r = max(1, math.ceil(4 * sigma))
    G = [[math.exp(-(u * u + v * v) / (2 * sigma * sigma)) for u in range(-r, r + 1)] for v in range(-r, r + 1)]
    total = sum(map(sum, G))
    G = [[x / total for x in row] for row in G]
    c = sum((u * u + v * v) * G[v + r][u + r] for v in range(-r, r + 1) for u in range(-r, r + 1))
    raw = [[(u * u + v * v - c) * G[v + r][u + r] for u in range(-r, r + 1)] for v in range(-r, r + 1)]
    scale = sum(raw[v + r][u + r] * u * u for v in range(-r, r + 1) for u in range(-r, r + 1)) / 2.0
    return [[x / scale for x in row] for row in raw], r


def direct(image, sigma):
    K, r = kernel_2d(sigma)
    h, w = len(image), len(image[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            out[y][x] = sum(K[v + r][u + r] * image[min(max(y + v, 0), h - 1)][min(max(x + u, 0), w - 1)]
                            for v in range(-r, r + 1) for u in range(-r, r + 1))
    return out


def reference_crossings(lap, t):
    """Per pixel rule: p is marked when some 4-neighbor q crosses zero with it and p wins the pair."""
    h, w = len(lap), len(lap[0])
    out = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            p = lap[y][x]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h:
                    q = lap[yy][xx]
                    first = (dy, dx) > (0, 0)
                    wins = abs(p) < abs(q) or (abs(p) == abs(q) and first)
                    if p * q < 0 and abs(p - q) >= t and wins:
                        out[y][x] = True
            for dx, dy in ((1, 0), (0, 1)):
                if p == 0 and 0 <= x - dx and x + dx < w and 0 <= y - dy and y + dy < h:
                    s, q = lap[y - dy][x - dx], lap[y + dy][x + dx]
                    if s * q < 0 and abs(s - q) >= t:
                        out[y][x] = True
    return out


def test_kernel_moments() -> None:
    g, dxx, r = log_kernels(1.5)
    assert r == 6
    assert math.isclose(sum(g), 1.0)
    assert abs(sum(dxx)) < 1e-12
    assert math.isclose(sum(k * k * dxx[k + r] for k in range(-r, r + 1)), 2.0)


def test_separable_sum_against_direct_2d_correlation() -> None:
    rng = random.Random(67)
    for sigma in (0.7, 1.0, 1.4):
        image = [[rng.randint(0, 255) for _ in range(8)] for _ in range(7)]
        got = laplacian_of_gaussian(image, sigma)
        want = direct(image, sigma)
        for y in range(7):
            for x in range(8):
                assert math.isclose(got[y][x], want[y][x], abs_tol=1e-9)


def test_exact_on_quadratics_and_zero_on_affine_images() -> None:
    n = 30
    quad = [[x * x + y * y for x in range(n)] for y in range(n)]
    affine = [[3 * x - 5 * y + 7 for x in range(n)] for y in range(n)]
    lq = laplacian_of_gaussian(quad, 1.5)
    la = laplacian_of_gaussian(affine, 1.5)
    for y in range(8, n - 8):
        for x in range(8, n - 8):
            assert math.isclose(lq[y][x], 4.0, abs_tol=1e-9)
            assert abs(la[y][x]) < 1e-9


def test_step_between_pixels_gives_one_crossing_per_row() -> None:
    image = [[0] * 8 + [100] * 8 for _ in range(6)]
    mask = marr_hildreth(image, 1.5, 1.0)
    for row in mask:
        assert [x for x in range(16) if row[x]] in ([7], [8])


def test_step_through_a_pixel_center_marks_that_pixel() -> None:
    image = [[0] * 8 + [50] + [100] * 8 for _ in range(6)]
    mask = marr_hildreth(image, 1.5, 1.0)
    for row in mask:
        assert [x for x in range(17) if row[x]] == [8]


def test_disk_gives_a_closed_ring_at_its_radius() -> None:
    n = 33
    image = [[200 if (x - 16) ** 2 + (y - 16) ** 2 <= 64 else 20 for x in range(n)] for y in range(n)]
    mask = marr_hildreth(image, 1.5, 5.0)
    ring = [(x, y) for y in range(n) for x in range(n) if mask[y][x]]
    assert ring
    for x, y in ring:
        assert abs(math.hypot(x - 16, y - 16) - 8.0) <= 1.0
    for y in range(10, 23):
        assert len([x for x in range(n) if mask[y][x]]) == 2


def test_threshold_removes_noise_crossings() -> None:
    rng = random.Random(71)
    image = [[rng.gauss(100, 5) for _ in range(20)] for _ in range(20)]
    assert any(any(r) for r in marr_hildreth(image, 1.5, 0.0))
    assert not any(any(r) for r in marr_hildreth(image, 1.5, 4.0))


def test_zero_crossings_against_per_pixel_rule() -> None:
    rng = random.Random(73)
    for _ in range(300):
        h, w = rng.randint(1, 7), rng.randint(1, 7)
        lap = [[rng.choice((-3, -1, 0, 0, 1, 2, 3)) for _ in range(w)] for _ in range(h)]
        t = rng.choice((0, 1, 2, 4))
        assert zero_crossings(lap, t) == reference_crossings(lap, t)


def test_flat_image_and_errors() -> None:
    assert not any(any(r) for r in marr_hildreth([[9] * 5 for _ in range(4)], 1.0, 0.5))
    assert marr_hildreth([], 1.0, 0.0) == []
    with pytest.raises(ValueError):
        log_kernels(-1.0)
