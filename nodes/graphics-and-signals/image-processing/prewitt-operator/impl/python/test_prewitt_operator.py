# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prewitt-operator/. The authors are listed in prov/CDGEEG.jsonl.

import random

from prewitt_operator import magnitude_squared, prewitt

KX = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
KY = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]


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
    gx, gy = prewitt(image)
    assert gx == [
        [0, 0, 210, 210, 0],
        [0, 70, 210, 140, 0],
        [0, 140, 210, 70, 0],
        [0, 210, 210, 0, 0],
    ]
    assert gy == [[0] * 5, [0, 70, 70, 70, 0], [0, 70, 70, 70, 0], [0] * 5]


def test_against_direct_correlation() -> None:
    rng = random.Random(5)
    for _ in range(200):
        h, w = rng.randint(1, 8), rng.randint(1, 8)
        image = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        gx, gy = prewitt(image)
        assert gx == correlate(image, KX)
        assert gy == correlate(image, KY)


def test_affine_image_is_exact() -> None:
    rng = random.Random(13)
    for _ in range(50):
        a, b, c = rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(0, 50)
        image = [[a * x + b * y + c for x in range(7)] for y in range(6)]
        gx, gy = prewitt(image)
        for y in range(1, 5):
            for x in range(1, 6):
                assert gx[y][x] == 6 * a
                assert gy[y][x] == 6 * b


def test_quadratic_term_does_not_bias_gx() -> None:
    """For I = x^2 the central difference is exact at each inner pixel: 6 * 2x."""
    image = [[x * x for x in range(8)] for _ in range(5)]
    gx, _ = prewitt(image)
    for y in range(1, 4):
        for x in range(1, 7):
            assert gx[y][x] == 6 * 2 * x


def test_edges_and_magnitude() -> None:
    assert prewitt([]) == ([], [])
    assert prewitt([[5]]) == ([[0]], [[0]])
    flat = [[42] * 4 for _ in range(3)]
    assert prewitt(flat) == ([[0] * 4] * 3, [[0] * 4] * 3)
    assert magnitude_squared([[3, 0]], [[4, -2]]) == [[25, 4]]
