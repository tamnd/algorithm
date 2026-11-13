# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prewitt-operator/. The authors are listed in prov/CDGEEG.jsonl.

"""The Prewitt operator on a gray image, computed as two separable passes.

An image is a list of H rows, each a list of W integers. Pixel (x, y) is
image[y][x]: x grows to the right and y grows downward. Reads outside the
image use the nearest border pixel (clamp). The outputs are integers:
gx is 6 times an estimate of dI/dx and gy is 6 times an estimate of dI/dy.
"""

Image = list[list[int]]


def _at(image: Image, x: int, y: int) -> int:
    h, w = len(image), len(image[0])
    return image[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]


def prewitt(image: Image) -> tuple[Image, Image]:
    """Return (gx, gy), the Prewitt gradient of image with the clamp border rule."""
    h = len(image)
    if h == 0 or len(image[0]) == 0:
        return [], []
    w = len(image[0])
    # @line L1: sum each column over three rows
    s = [[_at(image, x, y - 1) + image[y][x] + _at(image, x, y + 1) for x in range(w)] for y in range(h)]
    # @line L2: sum each row over three columns
    d = [[_at(image, x - 1, y) + image[y][x] + _at(image, x + 1, y) for x in range(w)] for y in range(h)]
    # @line L3: central difference of s along x
    gx = [[_at(s, x + 1, y) - _at(s, x - 1, y) for x in range(w)] for y in range(h)]
    # @line L4: central difference of d along y
    gy = [[_at(d, x, y + 1) - _at(d, x, y - 1) for x in range(w)] for y in range(h)]
    return gx, gy  # @line L5


def magnitude_squared(gx: Image, gy: Image) -> Image:
    """Return gx^2 + gy^2 at each pixel, an exact integer."""
    return [[a * a + b * b for a, b in zip(rx, ry)] for rx, ry in zip(gx, gy)]
