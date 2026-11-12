# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temporal-antialiasing/. The authors are listed in prov/Y521G8.jsonl.

"""Temporal antialiasing (TAA): jittered samples accumulated over frames.

Frame t (t = 1, 2, ...) takes one sample per pixel at (i + ox, j + oy), where
(ox, oy) is point t of the Halton sequence in bases 2 and 3. The history image
of the previous frame is fetched at the reprojected pixel center by bilinear
filtering (pixel centers at i + 1/2, clamp to edge), optionally clamped to the
per-channel range of the current 3 x 3 neighborhood, and blended with the new
sample by an exponential moving average with weight alpha.

render(t, x, y) returns the color tuple of frame t at the point (x, y) in pixel
units, y down. motion(t, i, j) returns the screen motion (dx, dy) in pixels of
the surface seen at pixel (i, j) from frame t - 1 to frame t. alpha is a number
or a function of t. Use fractions.Fraction values for exact results.
"""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Tuple, Union

Color = tuple
Image = List[List[Color]]
Num = Union[int, float, Fraction]


def halton(index: int, base: int) -> Fraction:
    """Radical inverse of index >= 0 in the given base, a point of [0, 1)."""
    result, scale = Fraction(0), Fraction(1, base)
    while index > 0:
        index, digit = divmod(index, base)
        result += digit * scale
        scale /= base
    return result


def bilinear(image: Image, x: Num, y: Num) -> Color:
    """Bilinear fetch at the point (x, y) in pixel units, pixel centers at i + 1/2, clamp to edge."""
    h, w = len(image), len(image[0])
    half = Fraction(1, 2) if isinstance(x, (int, Fraction)) and isinstance(y, (int, Fraction)) else 0.5
    gx, gy = x - half, y - half
    i0, j0 = math.floor(gx), math.floor(gy)
    a, b = gx - i0, gy - j0

    def px(i, j):
        return image[min(max(j, 0), h - 1)][min(max(i, 0), w - 1)]

    return tuple(
        (1 - a) * (1 - b) * p + a * (1 - b) * q + (1 - a) * b * r + a * b * s
        for p, q, r, s in zip(px(i0, j0), px(i0 + 1, j0), px(i0, j0 + 1), px(i0 + 1, j0 + 1))
    )


def taa_frame(
    t: int,
    history: Optional[Image],
    render: Callable[[int, Num, Num], Color],
    width: int,
    height: int,
    alpha: Num,
    motion: Optional[Callable[[int, int, int], Tuple[Num, Num]]] = None,
    clamp: bool = True,
    jitter: bool = True,
) -> Image:
    """Render frame t with one jittered sample per pixel and resolve it against the history.

    Precondition: t >= 1, history is the output of frame t - 1 (None for t = 1).
    Cost: W H renders, and Theta(W H) work for the fetch, the clamp and the blend.
    """
    ox, oy = (halton(t, 2), halton(t, 3)) if jitter else (Fraction(1, 2), Fraction(1, 2))  # @line L1
    cur = [[render(t, i + ox, j + oy) for i in range(width)] for j in range(height)]  # @line L2
    out: Image = [[None] * width for _ in range(height)]
    half = Fraction(1, 2)
    for j in range(height):  # @line L3
        for i in range(width):
            if history is None:  # @line L4
                out[j][i] = cur[j][i]
                continue
            dx, dy = motion(t, i, j) if motion else (0, 0)
            qx, qy = i + half - dx, j + half - dy  # @line L5
            hist = bilinear(history, qx, qy)  # @line L6
            if clamp:
                near = [cur[jj][ii] for jj in range(max(0, j - 1), min(height, j + 2)) for ii in range(max(0, i - 1), min(width, i + 2))]
                lo = [min(c[k] for c in near) for k in range(len(hist))]  # @line L7
                hi = [max(c[k] for c in near) for k in range(len(hist))]
                hist = tuple(min(max(v, l), u) for v, l, u in zip(hist, lo, hi))  # @line L8
            out[j][i] = tuple(alpha * x + (1 - alpha) * v for x, v in zip(cur[j][i], hist))  # @line L9
    return out  # @line L10


def temporal_antialiasing(
    render: Callable[[int, Num, Num], Color],
    width: int,
    height: int,
    frames: int,
    alpha: Union[Num, Callable[[int], Num]] = Fraction(1, 10),
    motion: Optional[Callable[[int, int, int], Tuple[Num, Num]]] = None,
    clamp: bool = True,
    jitter: bool = True,
) -> List[Image]:
    """Run TAA for frames 1..frames and return the resolved image of every frame.

    Cost: frames W H renders and Theta(frames W H) other work; one history image of memory.
    """
    outputs: List[Image] = []
    history: Optional[Image] = None
    for t in range(1, frames + 1):
        a = alpha(t) if callable(alpha) else alpha
        history = taa_frame(t, history, render, width, height, a, motion, clamp, jitter)
        outputs.append(history)
    return outputs
