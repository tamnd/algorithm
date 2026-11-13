# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roberts-cross-operator/. The authors are listed in prov/W69M2W.jsonl.

import random

from roberts_cross_operator import magnitude_squared, roberts_cross, to_axis_gradient

K1 = [[1, 0], [0, -1]]
K2 = [[0, 1], [-1, 0]]


def correlate2(image, kernel):
    """Direct 2 by 2 correlation anchored at the top left, clamp border, exact integers."""
    h, w = len(image), len(image[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            acc = 0
            for v in range(2):
                for u in range(2):
                    acc += kernel[v][u] * image[min(y + v, h - 1)][min(x + u, w - 1)]
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
    g1, g2 = roberts_cross(image)
    assert g1 == [
        [0, 0, -70, 0, 0],
        [0, -70, -70, 0, 0],
        [0, -70, 0, 0, 0],
        [0, -70, 0, 0, 0],
    ]
    assert g2 == [
        [0, 0, 70, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 70, 0, 0, 0],
        [0, 70, 0, 0, 0],
    ]


def test_against_direct_correlation() -> None:
    rng = random.Random(23)
    for _ in range(300):
        h, w = rng.randint(1, 8), rng.randint(1, 8)
        image = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        g1, g2 = roberts_cross(image)
        assert g1 == correlate2(image, K1)
        assert g2 == correlate2(image, K2)


def test_affine_image_is_exact() -> None:
    rng = random.Random(29)
    for _ in range(50):
        a, b, c = rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(0, 50)
        image = [[a * x + b * y + c for x in range(6)] for y in range(5)]
        g1, g2 = roberts_cross(image)
        gx, gy = to_axis_gradient(g1, g2)
        for y in range(4):
            for x in range(5):
                assert g1[y][x] == -(a + b)
                assert g2[y][x] == a - b
                assert gx[y][x] == 2 * a
                assert gy[y][x] == 2 * b


def test_edges_and_magnitude() -> None:
    assert roberts_cross([]) == ([], [])
    assert roberts_cross([[5]]) == ([[0]], [[0]])
    assert roberts_cross([[1, 4]]) == ([[-3, 0]], [[3, 0]])
    assert magnitude_squared([[3, 0]], [[4, -2]]) == [[25, 4]]
