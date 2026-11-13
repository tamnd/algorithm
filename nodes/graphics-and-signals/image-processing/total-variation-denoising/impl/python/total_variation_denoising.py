# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-variation-denoising/. The authors are listed in prov/BVXMK0.jsonl.

"""Total variation denoising (the ROF model) by Chambolle's projection algorithm (2004).

An image is a list of H rows of W real numbers; pixel (x, y) is f[y][x].
The discrete gradient uses forward differences and is 0 at the last
column (for the x part) and the last row (for the y part), which is a
Neumann border rule. The isotropic total variation is

    TV(u) = sum over pixels of sqrt(ux^2 + uy^2),

and the denoised image is the unique minimizer of the strongly convex energy

    E(u) = 1/2 * sum (u - f)^2 + lam * TV(u).

The algorithm works on a dual field p (two numbers per pixel) with
|p| <= 1 at every pixel and returns u = f - lam * div p, where
div = -grad^T. The duality gap E(u) - D(p) bounds E(u) - min E from
above, and |u - u*|^2 <= 2 * gap.

Each iteration costs O(W H) time; the extra space is O(W H).
"""

import math
from fractions import Fraction
from typing import List, Optional, Sequence, Tuple, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]
Field = Tuple[Image, Image]


def grad(u: Sequence[Sequence[Num]]) -> Field:
    """Forward differences, 0 at the last column (x part) and the last row (y part)."""
    h, w = len(u), len(u[0])
    gx = [[(u[y][x + 1] - u[y][x]) if x < w - 1 else 0 for x in range(w)] for y in range(h)]
    gy = [[(u[y + 1][x] - u[y][x]) if y < h - 1 else 0 for x in range(w)] for y in range(h)]
    return gx, gy


def div(px: Sequence[Sequence[Num]], py: Sequence[Sequence[Num]]) -> Image:
    """The discrete divergence, defined so that sum(div(p) * u) = -sum(p . grad(u))."""
    h, w = len(px), len(px[0])
    out: Image = []
    for y in range(h):
        row: List[Num] = []
        for x in range(w):
            a = (px[y][x] if x < w - 1 else 0) - (px[y][x - 1] if x > 0 else 0)
            b = (py[y][x] if y < h - 1 else 0) - (py[y - 1][x] if y > 0 else 0)
            row.append(a + b)
        out.append(row)
    return out


def total_variation(u: Sequence[Sequence[Num]]) -> float:
    """The isotropic total variation, sum of |grad u| over the pixels."""
    gx, gy = grad(u)
    return sum(math.hypot(a, b) for ra, rb in zip(gx, gy) for a, b in zip(ra, rb))


def rof_energy(u: Sequence[Sequence[Num]], f: Sequence[Sequence[Num]], lam: float) -> float:
    """E(u) = 1/2 |u - f|^2 + lam TV(u)."""
    fid = sum((a - b) ** 2 for ra, rb in zip(u, f) for a, b in zip(ra, rb))
    return 0.5 * float(fid) + lam * total_variation(u)


def dual_energy(px: Sequence[Sequence[Num]], py: Sequence[Sequence[Num]],
                f: Sequence[Sequence[Num]], lam: float) -> float:
    """D(p) = 1/2 (|f|^2 - |f - lam div p|^2), a lower bound on min E when |p| <= 1."""
    d = div(px, py)
    ff = sum(a * a for r in f for a in r)
    rr = sum((a - lam * b) ** 2 for ra, rb in zip(f, d) for a, b in zip(ra, rb))
    return 0.5 * float(ff - rr)


def tv_denoise_dual(f: Sequence[Sequence[Num]], lam: float, iterations: int = 1000,
                    tau: float = 0.125, tol: Optional[float] = None) -> Tuple[Image, Image, Image]:
    """Chambolle's iteration. Returns (u, px, py).

    Precondition: f is a nonempty rectangular grid, lam > 0, 0 < tau <= 1/8.
    Stops after the given number of iterations, or earlier when tol is given
    and the duality gap is at most tol (the gap is checked every 10 steps).
    Cost: O(W H) per iteration.
    """
    if not f or not f[0] or any(len(r) != len(f[0]) for r in f):
        raise ValueError("f must be a nonempty rectangular grid")
    if lam <= 0:
        raise ValueError("lam must be positive")
    if not 0 < tau <= 0.125:
        raise ValueError("tau must satisfy 0 < tau <= 1/8")
    h, w = len(f), len(f[0])
    px: Image = [[0.0] * w for _ in range(h)]  # @line L1
    py: Image = [[0.0] * w for _ in range(h)]
    for it in range(iterations):  # @line L2
        d = div(px, py)
        v = [[d[y][x] - f[y][x] / lam for x in range(w)] for y in range(h)]  # @line L3
        gx, gy = grad(v)  # @line L4
        for y in range(h):  # @line L5
            for x in range(w):
                a, b = gx[y][x], gy[y][x]
                den = 1.0 + tau * math.hypot(a, b)
                px[y][x] = (px[y][x] + tau * a) / den
                py[y][x] = (py[y][x] + tau * b) / den
        if tol is not None and it % 10 == 9:
            u = _primal(f, px, py, lam)
            if rof_energy(u, f, lam) - dual_energy(px, py, f, lam) <= tol:
                break
    return _primal(f, px, py, lam), px, py  # @line L6


def _primal(f: Sequence[Sequence[Num]], px: Image, py: Image, lam: float) -> Image:
    d = div(px, py)
    return [[f[y][x] - lam * d[y][x] for x in range(len(f[0]))] for y in range(len(f))]


def tv_denoise(f: Sequence[Sequence[Num]], lam: float, iterations: int = 1000,
               tau: float = 0.125, tol: Optional[float] = None) -> Image:
    """The ROF denoised image, approximately argmin 1/2 |u - f|^2 + lam TV(u)."""
    return tv_denoise_dual(f, lam, iterations, tau, tol)[0]
