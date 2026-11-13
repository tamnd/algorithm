# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scharr-operator/. The authors are listed in prov/CBGD3J.jsonl.

import math
import random

from scharr_operator import magnitude_squared, scharr

KX = [[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]]
KY = [[-3, -10, -3], [0, 0, 0], [3, 10, 3]]


def correlate(image, kernel):
    """Direct 2D correlation with the clamp border rule, in exact integers."""
    h, w = len(image), len(image[0])
    r = len(kernel) // 2
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            acc = 0
            for v in range(-r, r + 1):
                for u in range(-r, r + 1):
                    yy = min(max(y + v, 0), h - 1)
                    xx = min(max(x + u, 0), w - 1)
                    acc += kernel[v + r][u + r] * image[yy][xx]
            row.append(acc)
        out.append(row)
    return out


def test_example() -> None:
    image = [
        [10, 10, 10, 80, 80],
        [10, 10, 10, 80, 80],
        [10, 10, 80, 80, 80],
        [10, 10, 80, 80, 80],
    ]
    gx, gy = scharr(image)
    assert gx == [
        [0, 0, 1120, 1120, 0],
        [0, 210, 1120, 910, 0],
        [0, 910, 1120, 210, 0],
        [0, 1120, 1120, 0, 0],
    ]
    assert gy == [[0] * 5, [0, 210, 700, 210, 0], [0, 210, 700, 210, 0], [0] * 5]


def test_against_direct_correlation() -> None:
    rng = random.Random(17)
    for _ in range(200):
        h, w = rng.randint(1, 8), rng.randint(1, 8)
        image = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        gx, gy = scharr(image)
        assert gx == correlate(image, KX)
        assert gy == correlate(image, KY)


def test_affine_image_is_exact() -> None:
    rng = random.Random(19)
    for _ in range(50):
        a, b, c = rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(0, 50)
        image = [[a * x + b * y + c for x in range(7)] for y in range(6)]
        gx, gy = scharr(image)
        for y in range(1, 5):
            for x in range(1, 6):
                assert gx[y][x] == 32 * a
                assert gy[y][x] == 32 * b


def _angle_error(a: int, b: int, r: float) -> float:
    """Largest direction error in degrees of the kernel [a, b, a] x [-1, 0, 1] on plane waves."""
    worst = 0.0
    for k in range(901):
        phi = k * (math.pi / 2) / 900
        wx, wy = r * math.cos(phi), r * math.sin(phi)
        gx = math.sin(wx) * (b + 2 * a * math.cos(wy))
        gy = math.sin(wy) * (b + 2 * a * math.cos(wx))
        worst = max(worst, abs(math.atan2(gy, gx) - phi))
    return math.degrees(worst)


def test_direction_error_smaller_than_sobel_and_prewitt() -> None:
    for r in (math.pi / 8, math.pi / 4, math.pi / 2):
        e_scharr = _angle_error(3, 10, r)
        assert e_scharr < _angle_error(1, 2, r) / 3
        assert e_scharr < _angle_error(1, 1, r) / 3


def test_edges_and_magnitude() -> None:
    assert scharr([]) == ([], [])
    assert scharr([[5]]) == ([[0]], [[0]])
    flat = [[42] * 4 for _ in range(3)]
    assert scharr(flat) == ([[0] * 4] * 3, [[0] * 4] * 3)
    assert magnitude_squared([[3, 0]], [[4, -2]]) == [[25, 4]]
