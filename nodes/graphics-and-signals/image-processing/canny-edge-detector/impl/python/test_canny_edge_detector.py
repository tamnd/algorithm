# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canny-edge-detector/. The authors are listed in prov/XAAHCF.jsonl.

import math
import random

import pytest

from canny_edge_detector import canny, gaussian_kernels, gradient, suppress


def edge_columns(mask, y):
    return [x for x, v in enumerate(mask[y]) if v]


def test_kernels() -> None:
    g, d, r = gaussian_kernels(1.5)
    assert r == 5
    assert math.isclose(sum(g), 1.0)
    assert abs(sum(d)) < 1e-12
    assert math.isclose(sum(k * d[k + r] for k in range(-r, r + 1)), 1.0)


def test_gradient_against_direct_2d_correlation() -> None:
    rng = random.Random(53)
    image = [[rng.randint(0, 255) for _ in range(9)] for _ in range(7)]
    g, d, r = gaussian_kernels(1.0)
    h, w = 7, 9
    gx, gy = gradient(image, 1.0)
    for y in range(h):
        for x in range(w):
            sx = sy = 0.0
            for v in range(-r, r + 1):
                for u in range(-r, r + 1):
                    p = image[min(max(y + v, 0), h - 1)][min(max(x + u, 0), w - 1)]
                    sx += d[u + r] * g[v + r] * p
                    sy += g[u + r] * d[v + r] * p
            assert math.isclose(gx[y][x], sx, abs_tol=1e-9)
            assert math.isclose(gy[y][x], sy, abs_tol=1e-9)


def test_ramp_has_unit_gradient() -> None:
    image = [[3 * x + 2 * y for x in range(20)] for y in range(20)]
    gx, gy = gradient(image, 1.5)
    assert math.isclose(gx[10][10], 3.0) and math.isclose(gy[10][10], 2.0)


def test_vertical_step_single_response_at_the_step() -> None:
    image = [[0] * 8 + [100] * 8 for _ in range(12)]
    mask = canny(image, 1.5, 4.0, 10.0)
    for y in range(1, 11):
        assert edge_columns(mask, y) in ([7], [8])
    assert not any(mask[0]) and not any(mask[11])


def test_noisy_step_single_response_near_the_step() -> None:
    rng = random.Random(59)
    image = [[(0 if x < 10 else 100) + rng.gauss(0, 8) for x in range(20)] for _ in range(16)]
    mask = canny(image, 2.0, 6.0, 12.0)
    for y in range(1, 15):
        cols = edge_columns(mask, y)
        assert len(cols) == 1 and cols[0] in (9, 10)


def test_diagonal_step_through_pixel_centers() -> None:
    """Quantized suppression keeps a second anti-diagonal, because the neighbors along
    (1, 1) skip every other anti-diagonal. The interpolated variant keeps one pixel per row."""
    n = 40
    image = [[100 if x + y > n else (50 if x + y == n else 0) for x in range(n)] for y in range(n)]
    quantized = canny(image, 1.5, 4.0, 10.0)
    interpolated = canny(image, 1.5, 4.0, 10.0, interpolate=True)
    for y in range(8, n - 7):
        cols = edge_columns(quantized, y)
        assert cols == [n - 1 - y, n - y]
        assert edge_columns(interpolated, y) == [n - y]


def test_interpolated_variant_on_steps() -> None:
    image = [[0] * 8 + [100] * 8 for _ in range(12)]
    mask = canny(image, 1.5, 4.0, 10.0, interpolate=True)
    for y in range(1, 11):
        assert edge_columns(mask, y) in ([7], [8])


def test_diagonal_step_between_pixel_centers_gives_a_staircase() -> None:
    """The edge x + y = 39.5 is equally near the lines x + y = 39 and x + y = 40. Those pixels
    are not neighbors along the gradient direction (1, 1), so both survive: two per row."""
    n = 40
    image = [[100 if x + y >= n else 0 for x in range(n)] for y in range(n)]
    mask = canny(image, 1.5, 4.0, 10.0)
    for y in range(8, n - 7):
        assert edge_columns(mask, y) == [n - 1 - y, n - y]


def test_square_boundary() -> None:
    n = 24
    image = [[200 if 6 <= x < 18 and 6 <= y < 18 else 20 for x in range(n)] for y in range(n)]
    mask = canny(image, 1.0, 10.0, 30.0)
    for y in range(n):
        for x in range(n):
            if mask[y][x]:
                near_x = min(abs(x - 5.5), abs(x - 17.5)) <= 1 and 4 <= y <= 19
                near_y = min(abs(y - 5.5), abs(y - 17.5)) <= 1 and 4 <= x <= 19
                assert near_x or near_y
    for y in range(8, 16):
        assert len(edge_columns(mask, y)) == 2


def test_flat_image_and_errors() -> None:
    assert not any(any(r) for r in canny([[7] * 6 for _ in range(5)], 1.0, 1.0, 2.0))
    assert canny([], 1.0, 1.0, 2.0) == []
    with pytest.raises(ValueError):
        canny([[1]], 1.0, 3.0, 2.0)
    with pytest.raises(ValueError):
        gaussian_kernels(0.0)


def test_suppress_matches_direct_rule_on_float_gradients() -> None:
    rng = random.Random(61)
    for _ in range(50):
        gx = [[rng.uniform(-1, 1) for _ in range(6)] for _ in range(6)]
        gy = [[rng.uniform(-1, 1) for _ in range(6)] for _ in range(6)]
        out = suppress(gx, gy)
        steps = ((1, 0), (1, 1), (0, 1), (-1, 1))
        for y in range(1, 5):
            for x in range(1, 5):
                m = lambda xx, yy: gx[yy][xx] ** 2 + gy[yy][xx] ** 2
                k = round((math.degrees(math.atan2(gy[y][x], gx[y][x])) % 180.0) / 45.0) % 4
                dx, dy = steps[k]
                keep = m(x, y) > m(x - dx, y - dy) and m(x, y) >= m(x + dx, y + dy)
                assert (out[y][x] > 0) == keep
