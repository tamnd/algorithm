# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/richardson-lucy-deconvolution/. The authors are listed in prov/09YP53.jsonl.

"""Richardson-Lucy deconvolution with a circular (periodic) border.

An image is a list of H rows of W nonnegative numbers (int, float or
Fraction); pixel (x, y) is img[y][x] and pixel centers are at integer
coordinates. The point spread function psf is a list of rows with odd
sizes 2b + 1 by 2a + 1, centered at psf[b][a], with nonnegative entries
that sum to 1. The blur model is

    blur(u)(x, y) = sum over (i, j) of psf[j][i] * u(x - (i - a), y - (j - b)),

with indices taken modulo W and H, so every pixel of u spreads exactly its
own value over the blurred image. The observed image d is a sample of
Poisson counts with mean blur(u_true).

Each iteration costs O(W H K) time, where K is the number of entries of
the psf, and O(W H) extra space. A start u0 with a zero pixel keeps that
pixel at zero forever, so the default start is the constant mean of d.
"""

import math
from fractions import Fraction
from typing import List, Optional, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]


def _check_psf(psf: Sequence[Sequence[Num]]) -> None:
    if not psf or not psf[0] or len(psf) % 2 == 0 or len(psf[0]) % 2 == 0:
        raise ValueError("the psf must have odd height and width")
    if any(len(row) != len(psf[0]) for row in psf):
        raise ValueError("the psf must be rectangular")
    if any(v < 0 for row in psf for v in row):
        raise ValueError("the psf must be nonnegative")
    total = sum(v for row in psf for v in row)
    if isinstance(total, float):
        if abs(total - 1.0) > 1e-9:
            raise ValueError("the psf must sum to 1")
    elif total != 1:
        raise ValueError("the psf must sum to 1")


def blur(u: Sequence[Sequence[Num]], psf: Sequence[Sequence[Num]]) -> Image:
    """Circular convolution psf * u. O(W H K)."""
    h, w = len(u), len(u[0])
    bh, bw = len(psf) // 2, len(psf[0]) // 2
    out: Image = []
    for y in range(h):
        row: List[Num] = []
        for x in range(w):
            s: Num = 0
            for j, prow in enumerate(psf):
                for i, p in enumerate(prow):
                    if p:
                        s += p * u[(y - (j - bh)) % h][(x - (i - bw)) % w]
            row.append(s)
        out.append(row)
    return out


def correlate(r: Sequence[Sequence[Num]], psf: Sequence[Sequence[Num]]) -> Image:
    """Circular correlation with psf, the adjoint of blur. O(W H K)."""
    h, w = len(r), len(r[0])
    bh, bw = len(psf) // 2, len(psf[0]) // 2
    out: Image = []
    for y in range(h):
        row: List[Num] = []
        for x in range(w):
            s: Num = 0
            for j, prow in enumerate(psf):
                for i, p in enumerate(prow):
                    if p:
                        s += p * r[(y + (j - bh)) % h][(x + (i - bw)) % w]
            row.append(s)
        out.append(row)
    return out


def poisson_log_likelihood(d: Sequence[Sequence[Num]], b: Sequence[Sequence[Num]]) -> float:
    """sum of d log b - b, the Poisson log likelihood up to a constant; -inf if b = 0 where d > 0."""
    total = 0.0
    for drow, brow in zip(d, b):
        for dv, bv in zip(drow, brow):
            if dv > 0:
                if bv <= 0:
                    return -math.inf
                total += float(dv) * math.log(bv)
            total -= float(bv)
    return total


def richardson_lucy_step(u: Sequence[Sequence[Num]], d: Sequence[Sequence[Num]],
                         psf: Sequence[Sequence[Num]]) -> Image:
    """One multiplicative update u <- u * correlate(d / blur(u)). O(W H K)."""
    b = blur(u, psf)  # @line L3
    r: Image = []
    for drow, brow in zip(d, b):  # @line L4
        row: List[Num] = []
        for dv, bv in zip(drow, brow):
            if dv == 0:
                row.append(0)
            elif bv <= 0:
                raise ValueError("the estimate predicts zero where the data is positive")
            else:
                row.append(dv / bv)
        r.append(row)
    c = correlate(r, psf)  # @line L5
    return [[uv * cv for uv, cv in zip(urow, crow)] for urow, crow in zip(u, c)]  # @line L6


def richardson_lucy(d: Sequence[Sequence[Num]], psf: Sequence[Sequence[Num]], iterations: int,
                    u0: Optional[Sequence[Sequence[Num]]] = None) -> Image:
    """Run the given number of Richardson-Lucy iterations from u0 (default: the constant mean of d).

    Precondition: d is a nonempty rectangular grid of nonnegative numbers, psf is
    as in the module doc string, iterations >= 0, and u0, if given, has the shape
    of d and nonnegative entries. Cost: O(iterations * W H K) time.
    """
    if not d or not d[0] or any(len(row) != len(d[0]) for row in d):
        raise ValueError("d must be a nonempty rectangular grid")
    if any(v < 0 for row in d for v in row):
        raise ValueError("d must be nonnegative")
    if iterations < 0:
        raise ValueError("iterations must be nonnegative")
    _check_psf(psf)
    h, w = len(d), len(d[0])
    if u0 is None:
        total = sum(v for row in d for v in row)
        mean = Fraction(total, w * h) if isinstance(total, (int, Fraction)) else total / (w * h)
        u: Image = [[mean] * w for _ in range(h)]  # @line L1
    else:
        if len(u0) != h or any(len(row) != w for row in u0) or any(v < 0 for row in u0 for v in row):
            raise ValueError("u0 must be a nonnegative grid of the shape of d")
        u = [list(row) for row in u0]
    for _ in range(iterations):  # @line L2
        u = richardson_lucy_step(u, d, psf)
    return u  # @line L7
