# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roberts-cross-operator/. The authors are listed in prov/W69M2W.jsonl.

"""The Roberts cross operator on a gray image.

An image is a list of H rows, each a list of W integers. Pixel (x, y) is
image[y][x]: x grows to the right and y grows downward. Reads outside the
image use the nearest border pixel (clamp). Output (x, y) belongs to the
point (x + 1/2, y + 1/2) between the four pixels it reads.
"""

Image = list[list[int]]


def roberts_cross(image: Image) -> tuple[Image, Image]:
    """Return (g1, g2): g1 = I(x, y) - I(x+1, y+1) and g2 = I(x+1, y) - I(x, y+1)."""
    h = len(image)
    if h == 0 or len(image[0]) == 0:
        return [], []
    w = len(image[0])
    g1: Image = []
    g2: Image = []
    for y in range(h):  # @line L1
        y1 = min(y + 1, h - 1)
        r1, r2 = [], []
        for x in range(w):  # @line L2
            x1 = min(x + 1, w - 1)
            r1.append(image[y][x] - image[y1][x1])  # @line L3
            r2.append(image[y][x1] - image[y1][x])  # @line L4
        g1.append(r1)
        g2.append(r2)
    return g1, g2  # @line L5


def to_axis_gradient(g1: Image, g2: Image) -> tuple[Image, Image]:
    """Return (2 dI/dx, 2 dI/dy) estimates at the half pixel points: (g2 - g1, -(g1 + g2))."""
    gx = [[b - a for a, b in zip(r1, r2)] for r1, r2 in zip(g1, g2)]
    gy = [[-(a + b) for a, b in zip(r1, r2)] for r1, r2 in zip(g1, g2)]
    return gx, gy


def magnitude_squared(g1: Image, g2: Image) -> Image:
    """Return g1^2 + g2^2 at each pixel, an exact integer."""
    return [[a * a + b * b for a, b in zip(r1, r2)] for r1, r2 in zip(g1, g2)]
