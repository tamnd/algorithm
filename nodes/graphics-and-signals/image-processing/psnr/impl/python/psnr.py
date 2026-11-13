# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psnr/. The authors are listed in prov/T7XT8F.jsonl.

"""Mean squared error and peak signal-to-noise ratio of two images.

Images are lists of rows of numbers with the same size. For integer images
the MSE is an exact Fraction. PSNR = 10 log10(peak^2 / MSE) in decibels,
and it is infinite when the images are equal.
"""

import math
from fractions import Fraction


def mse(x: list[list], y: list[list]):
    """Mean of the squared differences. Exact for int or Fraction values."""
    if len(x) != len(y) or any(len(a) != len(b) for a, b in zip(x, y)):
        raise ValueError("the images must have the same size")
    n = sum(len(row) for row in x)
    if n == 0:
        raise ValueError("the images have no pixels")
    total = sum((a - b) ** 2 for ra, rb in zip(x, y) for a, b in zip(ra, rb))
    if isinstance(total, int):
        return Fraction(total, n)
    return total / n


def psnr(x: list[list], y: list[list], peak=255) -> float:
    """PSNR in dB with the given peak value (255 for 8-bit, 1 for values in [0, 1])."""
    e = mse(x, y)
    if e == 0:
        return math.inf
    return 10 * math.log10(peak * peak / e)


def psnr_sequence(frames_x: list, frames_y: list, peak=255) -> tuple[float, float]:
    """Return (mean of per-frame PSNR, PSNR of the mean MSE) for two frame lists.

    The first is never smaller than the second (Jensen's inequality, since
    -log is convex), so a report must say which one it gives.
    """
    errors = [mse(a, b) for a, b in zip(frames_x, frames_y)]
    per_frame = [10 * math.log10(peak * peak / e) for e in errors]
    mean_e = sum(errors) / len(errors)
    return sum(per_frame) / len(per_frame), 10 * math.log10(peak * peak / mean_e)
