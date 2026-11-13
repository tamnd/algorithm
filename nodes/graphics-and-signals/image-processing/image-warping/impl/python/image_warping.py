# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-warping/. The authors are listed in prov/V5CTT9.jsonl.

"""Warp a gray image by inverse mapping, and show the holes of forward mapping.

An image is a list of H rows of W numbers, with the center of pixel (x, y)
at the integer point (x, y). A warp is given by its inverse map: a function
that takes an output point (u, v) to the input point (x, y) it comes from.
Inverse mapping visits every output pixel once, so no output pixel is left
empty, and it reads the input between pixel centers by interpolation.

Points outside the square spanned by the input pixel centers, 0 <= x <= W-1
and 0 <= y <= H-1, get the fill value. Coordinates may be Fractions, and
then the bilinear result is exact.

Cost: O(W' H') map evaluations and interpolations for a W' x H' output.
"""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Tuple

Point = Tuple[float, float]
Map = Callable[[float, float], Point]


def sample_nearest(img: Sequence[Sequence], x, y, fill=0):
    """Value of the nearest pixel center, ties rounded up, or fill outside the image."""
    h, w = len(img), len(img[0])
    if not (0 <= x <= w - 1 and 0 <= y <= h - 1):
        return fill
    i = math.floor(x + Fraction(1, 2)) if isinstance(x, Fraction) else math.floor(x + 0.5)
    j = math.floor(y + Fraction(1, 2)) if isinstance(y, Fraction) else math.floor(y + 0.5)
    return img[j][i]


def sample_bilinear(img: Sequence[Sequence], x, y, fill=0):
    """Bilinear interpolation of the four pixel centers around (x, y), or fill outside the image."""
    h, w = len(img), len(img[0])
    if not (0 <= x <= w - 1 and 0 <= y <= h - 1):
        return fill
    i = min(math.floor(x), w - 2) if w > 1 else 0
    j = min(math.floor(y), h - 2) if h > 1 else 0
    fx, fy = x - i, y - j
    i1, j1 = min(i + 1, w - 1), min(j + 1, h - 1)
    top = (1 - fx) * img[j][i] + fx * img[j][i1]
    bottom = (1 - fx) * img[j1][i] + fx * img[j1][i1]
    return (1 - fy) * top + fy * bottom


def inverse_warp(img: Sequence[Sequence], out_w: int, out_h: int, inv: Map,
                 method: str = "linear", fill=0) -> list:
    """Output pixel (u, v) gets the input sampled at inv(u, v)."""
    if not img or not img[0]:
        raise ValueError("the image is empty")
    sample = {"linear": sample_bilinear, "nearest": sample_nearest}[method]
    out = []
    for v in range(out_h):
        row = []
        for u in range(out_w):
            x, y = inv(u, v)
            row.append(sample(img, x, y, fill))
        out.append(row)
    return out


def forward_warp(img: Sequence[Sequence], out_w: int, out_h: int, fwd: Map,
                 fill=0) -> Tuple[list, List[List[bool]]]:
    """Send each input pixel to the output pixel nearest to fwd(x, y); later pixels overwrite.

    Returns the output and a mask that is True where no input pixel landed."""
    out = [[fill] * out_w for _ in range(out_h)]
    hit = [[False] * out_w for _ in range(out_h)]
    for y, row in enumerate(img):
        for x, val in enumerate(row):
            u, v = fwd(x, y)
            i, j = math.floor(u + 0.5), math.floor(v + 0.5)
            if 0 <= i < out_w and 0 <= j < out_h:
                out[j][i] = val
                hit[j][i] = True
    return out, [[not b for b in r] for r in hit]


def affine(a, b, c, d, e, f) -> Map:
    """The map (x, y) -> (a x + b y + c, d x + e y + f)."""
    return lambda x, y: (a * x + b * y + c, d * x + e * y + f)


def invert_affine(a, b, c, d, e, f) -> Map:
    """The inverse of affine(a, b, c, d, e, f); the matrix [[a, b], [d, e]] must be invertible."""
    det = a * e - b * d
    if det == 0:
        raise ValueError("the affine map is not invertible")
    ia, ib, id_, ie = e / det, -b / det, -d / det, a / det
    return affine(ia, ib, -(ia * c + ib * f), id_, ie, -(id_ * c + ie * f))


def homography(h: Sequence[Sequence[float]]) -> Map:
    """The projective map given by a 3 x 3 matrix, (x, y) -> ((h0 . p) / (h2 . p), (h1 . p) / (h2 . p))."""
    def m(x, y):
        z = h[2][0] * x + h[2][1] * y + h[2][2]
        return ((h[0][0] * x + h[0][1] * y + h[0][2]) / z, (h[1][0] * x + h[1][1] * y + h[1][2]) / z)
    return m


def rotation_about(cx, cy, angle: float) -> Tuple[float, ...]:
    """Coefficients (a, b, c, d, e, f) of the rotation by angle radians about (cx, cy)."""
    co, si = math.cos(angle), math.sin(angle)
    return (co, -si, cx - co * cx + si * cy, si, co, cy - si * cx - co * cy)
