# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cg-sense/. The authors are listed in prov/CCN5EK.jsonl.

"""CG-SENSE: iterative SENSE for any k-space trajectory (Pruessmann, Weiger, Boernert and Boesiger 2001).

The model is y = E x + e with the encoding operator E x = (M F (s_k x))_k for
coils k = 1..c: multiply by the coil map, transform, keep the samples. The
method runs the conjugate gradient method (Hestenes and Stiefel 1952) on the
normal equations

    E^H D E x = E^H D y,

where D is a positive diagonal weight on the samples (the density
compensation; D = 1 gives the plain least squares solution). E is given as
two functions, so the same code works for a Cartesian mask (with the FFT)
and for a non-Cartesian trajectory (here with a direct nonuniform DFT).

Images are flat row-major lists of n^2 complex numbers. Data are flat lists:
coil 0 first, then coil 1, and so on.
"""

import cmath
import math
from typing import Callable, Optional, Sequence

from imgkit import dft2, idft2

Vector = list[complex]
Operator = Callable[[Sequence[complex]], Vector]


def _dot(u: Sequence[complex], v: Sequence[complex]) -> complex:
    return sum(a.conjugate() * b for a, b in zip(u, v))


def cartesian_ops(maps: Sequence[Sequence[Sequence[complex]]], mask: Sequence[Sequence[bool]]):
    """E and E^H for a Cartesian sampling mask (n x n booleans) with the unitary DFT F / n."""
    n = len(mask)
    where = [(i, j) for i in range(n) for j in range(n) if mask[i][j]]

    def apply_e(x: Sequence[complex]) -> Vector:
        out = []
        for s in maps:
            img = [[s[i][j] * x[i * n + j] for j in range(n)] for i in range(n)]
            ksp = dft2(img)
            out.extend(ksp[i][j] / n for i, j in where)
        return out

    def apply_eh(y: Sequence[complex]) -> Vector:
        out = [0j] * (n * n)
        per = len(where)
        for k, s in enumerate(maps):
            ksp = [[0j] * n for _ in range(n)]
            for t, (i, j) in enumerate(where):
                ksp[i][j] = y[k * per + t]
            img = idft2(ksp)
            for i in range(n):
                for j in range(n):
                    out[i * n + j] += s[i][j].conjugate() * img[i][j] * n
        return out

    return apply_e, apply_eh


def nudft_ops(maps: Sequence[Sequence[Sequence[complex]]], points: Sequence[tuple[float, float]]):
    """E and E^H for k-space points (kx, ky) in cycles per field of view, by direct sums.

    Pixel (i, j) sits at (j - n/2, i - n/2) in pixel units, and the sample at
    (kx, ky) of coil k is (1/n) sum s_k x exp(-2 pi i (kx (j - n/2) + ky (i - n/2)) / n).
    This is the nonuniform DFT; a fast code would use a nonuniform FFT instead.
    """
    n = len(maps[0])
    h = n / 2.0
    phase = [
        [cmath.exp(-2j * math.pi * (kx * (j - h) + ky * (i - h)) / n) / n for i in range(n) for j in range(n)]
        for kx, ky in points
    ]

    def apply_e(x: Sequence[complex]) -> Vector:
        out = []
        for s in maps:
            sx = [s[i][j] * x[i * n + j] for i in range(n) for j in range(n)]
            out.extend(sum(a * b for a, b in zip(row, sx)) for row in phase)
        return out

    def apply_eh(y: Sequence[complex]) -> Vector:
        out = [0j] * (n * n)
        m = len(points)
        for k, s in enumerate(maps):
            acc = [0j] * (n * n)
            for t, row in enumerate(phase):
                yt = y[k * m + t]
                if yt != 0:
                    for q in range(n * n):
                        acc[q] += row[q].conjugate() * yt
            for i in range(n):
                for j in range(n):
                    out[i * n + j] += s[i][j].conjugate() * acc[i * n + j]
        return out

    return apply_e, apply_eh


def cg_sense(
    y: Sequence[complex],
    apply_e: Operator,
    apply_eh: Operator,
    size: int,
    iters: int,
    weights: Optional[Sequence[float]] = None,
    tol: float = 0.0,
    callback: Optional[Callable[[int, Vector], None]] = None,
) -> Vector:
    """Solve E^H D E x = E^H D y by CG from x = 0 with at most iters steps.

    size is the number of pixels, weights the diagonal of D (None for D = 1).
    The loop stops early when ||r|| <= tol ||b||. callback(t, x) sees each iterate.
    """
    def weigh(v):
        return list(v) if weights is None else [w * a for w, a in zip(weights, v)]

    def normal(v):
        return apply_eh(weigh(apply_e(v)))

    b = apply_eh(weigh(y))  # @line L1
    x = [0j] * size  # @line L2
    r = list(b)
    p = list(r)
    rr = _dot(r, r).real
    bnorm = math.sqrt(_dot(b, b).real)
    for t in range(iters):  # @line L3
        if rr == 0.0 or math.sqrt(rr) <= tol * bnorm:  # @line L4
            break
        q = normal(p)  # @line L5
        alpha = rr / _dot(p, q).real  # @line L6
        x = [xi + alpha * pi for xi, pi in zip(x, p)]  # @line L7
        r = [ri - alpha * qi for ri, qi in zip(r, q)]  # @line L8
        rr_new = _dot(r, r).real
        p = [ri + (rr_new / rr) * pi for ri, pi in zip(r, p)]  # @line L9
        rr = rr_new
        if callback is not None:
            callback(t + 1, x)
    return x  # @line L10


def radial_points(spokes: int, samples: int) -> list[tuple[float, float]]:
    """A radial trajectory: spokes through the center at angles pi s / spokes, samples at r = t - (samples - 1) / 2."""
    pts = []
    for s in range(spokes):
        th = math.pi * s / spokes
        for t in range(samples):
            r = t - (samples - 1) / 2.0
            pts.append((r * math.cos(th), r * math.sin(th)))
    return pts


def radial_density(points: Sequence[tuple[float, float]]) -> list[float]:
    """A simple density compensation for a radial trajectory: the distance |k| to the center."""
    return [math.hypot(kx, ky) for kx, ky in points]
