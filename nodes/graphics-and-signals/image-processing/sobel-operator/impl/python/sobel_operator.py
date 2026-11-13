# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sobel-operator/. The authors are listed in prov/JDAK9Z.jsonl.

"""The Sobel operator on a gray image, computed as two separable passes.

An image is a list of H rows, each a list of W integers. Pixel (x, y) is
image[y][x]: x grows to the right and y grows downward. Reads outside the
image use the nearest border pixel (clamp). The outputs are integers:
gx is 8 times an estimate of dI/dx and gy is 8 times an estimate of dI/dy.
"""

Image = list[list[int]]


def _at(image: Image, x: int, y: int) -> int:
    h, w = len(image), len(image[0])
    return image[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]


def sobel(image: Image) -> tuple[Image, Image]:
    """Return (gx, gy), the Sobel gradient of image with the clamp border rule."""
    h = len(image)
    if h == 0 or len(image[0]) == 0:
        return [], []
    w = len(image[0])
    # @line L1: smooth each column with [1, 2, 1]
    s = [[_at(image, x, y - 1) + 2 * image[y][x] + _at(image, x, y + 1) for x in range(w)] for y in range(h)]
    # @line L2: smooth each row with [1, 2, 1]
    d = [[_at(image, x - 1, y) + 2 * image[y][x] + _at(image, x + 1, y) for x in range(w)] for y in range(h)]
    # @line L3: central difference of s along x
    gx = [[_at(s, x + 1, y) - _at(s, x - 1, y) for x in range(w)] for y in range(h)]
    # @line L4: central difference of d along y
    gy = [[_at(d, x, y + 1) - _at(d, x, y - 1) for x in range(w)] for y in range(h)]
    return gx, gy  # @line L5


def magnitude_squared(gx: Image, gy: Image) -> Image:
    """Return gx^2 + gy^2 at each pixel, an exact integer."""
    return [[a * a + b * b for a, b in zip(rx, ry)] for rx, ry in zip(gx, gy)]
