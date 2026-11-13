# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-steinberg-dithering/. The authors are listed in prov/DDE4HS.jsonl.

"""Floyd-Steinberg error diffusion.

The image is a list of rows of values in [0, 1], as int or Fraction. Each
pixel is set to the nearest output level, a value of exactly 1/2 going up for
two levels. The error, the value before the decision minus the level, is
spread to the neighbors that are not yet done with the weights 7/16 (ahead),
3/16 (below and behind), 5/16 (below) and 1/16 (below and ahead). Shares that
fall outside the image are dropped and added up in `lost`. In the serpentine
order, odd rows run from right to left and the weights are mirrored.
"""

from fractions import Fraction

WEIGHTS = ((1, 0, Fraction(7, 16)), (-1, 1, Fraction(3, 16)), (0, 1, Fraction(5, 16)), (1, 1, Fraction(1, 16)))


def nearest_level(v, levels):
    """The nearest level; a tie goes to the higher level."""
    return min(levels, key=lambda q: (abs(v - q), -q))


def floyd_steinberg(image, levels=(0, 1), serpentine=False):
    """Return (output, errors, lost): the levels, the error at each pixel, and the sum dropped at the border."""
    h, w = len(image), len(image[0])
    work = [[Fraction(v) for v in row] for row in image]  # @line L1
    out = [[0] * w for _ in range(h)]
    err = [[0] * w for _ in range(h)]
    lost = Fraction(0)
    for y in range(h):  # @line L2
        step = -1 if serpentine and y % 2 else 1
        for x in range(w)[::step]:  # @line L3
            v = work[y][x]
            q = nearest_level(v, levels)  # @line L4
            out[y][x] = q
            e = v - q  # @line L5
            err[y][x] = e
            for dx, dy, wt in WEIGHTS:  # @line L6
                nx, ny = x + step * dx, y + dy
                if 0 <= nx < w and ny < h:  # @line L7
                    work[ny][nx] += wt * e
                else:
                    lost += wt * e  # @line L8
    return out, err, lost  # @line L9
