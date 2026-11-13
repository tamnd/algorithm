# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sobel-operator/. The authors are listed in prov/JDAK9Z.jsonl.

import random

from sobel_operator import magnitude_squared, sobel

KX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
KY = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]


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
    gx, gy = sobel(image)
    assert gx == [
        [0, 0, 280, 280, 0],
        [0, 70, 280, 210, 0],
        [0, 210, 280, 70, 0],
        [0, 280, 280, 0, 0],
    ]
    assert gy == [[0] * 5, [0, 70, 140, 70, 0], [0, 70, 140, 70, 0], [0] * 5]


def test_against_direct_correlation() -> None:
    rng = random.Random(7)
    for _ in range(200):
        h, w = rng.randint(1, 8), rng.randint(1, 8)
        image = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        gx, gy = sobel(image)
        assert gx == correlate(image, KX)
        assert gy == correlate(image, KY)


def test_affine_image_is_exact() -> None:
    rng = random.Random(11)
    for _ in range(50):
        a, b, c = rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(0, 50)
        image = [[a * x + b * y + c for x in range(7)] for y in range(6)]
        gx, gy = sobel(image)
        for y in range(1, 5):
            for x in range(1, 6):
                assert gx[y][x] == 8 * a
                assert gy[y][x] == 8 * b


def test_box_of_two_by_two_differences() -> None:
    """Sobel gx is the 2x2 box sum of the 2x2 difference, inside the image."""
    rng = random.Random(3)
    image = [[rng.randint(0, 255) for _ in range(9)] for _ in range(8)]
    gx, gy = sobel(image)

    def dx(x, y):
        return image[y][x + 1] + image[y + 1][x + 1] - image[y][x] - image[y + 1][x]

    def dy(x, y):
        return image[y + 1][x] + image[y + 1][x + 1] - image[y][x] - image[y][x + 1]

    for y in range(1, 7):
        for x in range(1, 8):
            assert gx[y][x] == dx(x - 1, y - 1) + dx(x, y - 1) + dx(x - 1, y) + dx(x, y)
            assert gy[y][x] == dy(x - 1, y - 1) + dy(x, y - 1) + dy(x - 1, y) + dy(x, y)


def test_edges_and_magnitude() -> None:
    assert sobel([]) == ([], [])
    assert sobel([[5]]) == ([[0]], [[0]])
    flat = [[42] * 4 for _ in range(3)]
    assert sobel(flat) == ([[0] * 4] * 3, [[0] * 4] * 3)
    assert magnitude_squared([[3, 0]], [[4, -2]]) == [[25, 4]]
