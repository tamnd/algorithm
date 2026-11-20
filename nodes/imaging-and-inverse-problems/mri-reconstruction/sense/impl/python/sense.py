# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sense/. The authors are listed in prov/7VT2V0.jsonl.

"""SENSE reconstruction for Cartesian undersampling (Pruessmann, Weiger, Scheidegger and Boesiger 1999).

Conventions: an image is a list of n rows, img[i][j]. The k-space of coil k
is y_k = F_u (s_k x) with the unitary 2D DFT F_u = F / n, in DFT order. The
scan keeps the rows kappa = 0, R, 2R, ... of the phase encoding axis (the first
index) and skips the others, with n a multiple of R. The other k-space rows of
the input are never read.

Folding: with m = n / R, the inverse DFT of size m x n of the kept rows gives
a_k(i, j) = sum_p s_k(i + p m, j) x(i + p m, j) / n, so n times it is the
folded image, the sum of the R pixels that fall on the same place. At each
folded pixel, SENSE solves the c x R weighted least squares problem
min (a - E v)^H Psi^(-1) (a - E v) with E[k][p] = s_k(i + p m, j).

Noise: if the k-space noise of the coils has the covariance Psi at each
sample, the folded noise has the covariance R Psi, and the noise covariance
of the unfolded pixels is R (E^H Psi^(-1) E)^(-1).
"""

import math
from typing import Optional, Sequence

from imgkit import dft2, idft2
from imgla import cholesky, solve

Image = list[list[complex]]


def unitary_dft2(img: Sequence[Sequence[complex]]) -> Image:
    """F_u x = F x / n for an n x n image."""
    n = len(img)
    return [[v / n for v in row] for row in dft2(img)]


def unitary_idft2(ksp: Sequence[Sequence[complex]]) -> Image:
    """F_u^H y = n idft2(y) for an n x n array."""
    n = len(ksp)
    return [[v * n for v in row] for row in idft2(ksp)]


def sense_mask(n: int, r: int) -> list[bool]:
    """True for the kept phase encoding rows kappa = 0, R, 2R, ..."""
    return [kappa % r == 0 for kappa in range(n)]


def encode(x: Image, maps: Sequence[Image], r: int) -> list[Image]:
    """The forward model: y_k = M F_u (s_k x), with the skipped rows set to 0."""
    keep = sense_mask(len(x), r)
    out = []
    for s in maps:
        ksp = unitary_dft2([[sv * xv for sv, xv in zip(srow, xrow)] for srow, xrow in zip(s, x)])
        out.append([row if keep[kappa] else [0j] * len(row) for kappa, row in enumerate(ksp)])
    return out


def encode_adjoint(y: Sequence[Image], maps: Sequence[Image], r: int) -> Image:
    """The adjoint: x = sum_k conj(s_k) F_u^H (M y_k)."""
    n = len(maps[0])
    keep = sense_mask(n, r)
    out = [[0j] * n for _ in range(n)]
    for s, yk in zip(maps, y):
        img = unitary_idft2([list(row) if keep[kappa] else [0j] * n for kappa, row in enumerate(yk)])
        for i in range(n):
            for j in range(n):
                out[i][j] += s[i][j].conjugate() * img[i][j]
    return out


def folded_images(y: Sequence[Image], r: int) -> list[Image]:
    """n times the inverse DFT of size (n/R) x n of the kept rows of each coil."""
    n = len(y[0])
    out = []
    for yk in y:
        sub = [list(yk[kappa]) for kappa in range(0, n, r)]
        out.append([[v * n for v in row] for row in idft2(sub)])
    return out


def _whitener(psi: Optional[Sequence[Sequence[complex]]], c: int):
    """A function v -> L^(-1) v with Psi = L L^H, or the identity when psi is None."""
    if psi is None:
        return lambda v: list(v)
    low = cholesky(psi)

    def apply(v):
        z = [0j] * c
        for i in range(c):
            z[i] = (v[i] - sum(low[i][k] * z[k] for k in range(i))) / low[i][i]
        return z

    return apply


def sense(
    y: Sequence[Image],
    maps: Sequence[Image],
    r: int,
    psi: Optional[Sequence[Sequence[complex]]] = None,
    lam: float = 0.0,
) -> Image:
    """Unfold the image from the kept rows of y (one n x n array per coil).

    psi is the c x c coil noise covariance (None for the identity). lam >= 0
    adds lam ||v||^2 to each small problem (Tikhonov); lam = 0 is plain SENSE
    and needs R <= c and a full column rank E at every folded pixel.
    """
    c = len(maps)
    n = len(maps[0])
    if n % r != 0:
        raise ValueError("n must be a multiple of R")
    if r > c and lam == 0.0:
        raise ValueError("SENSE needs R <= c")
    m = n // r  # @line L1
    a = folded_images(y, r)  # @line L2
    white = _whitener(psi, c)  # @line L3
    x = [[0j] * n for _ in range(n)]
    for i in range(m):  # @line L4
        for j in range(n):
            e = [[maps[k][i + p * m][j] for p in range(r)] for k in range(c)]  # @line L5
            cols = [white([e[k][p] for k in range(c)]) for p in range(r)]  # @line L6
            b = white([a[k][i][j] for k in range(c)])
            gram = [[sum(cols[p][k].conjugate() * cols[q][k] for k in range(c)) for q in range(r)] for p in range(r)]  # @line L7
            for p in range(r):
                gram[p][p] += lam
            rhs = [sum(cols[p][k].conjugate() * b[k] for k in range(c)) for p in range(r)]
            v = solve(gram, rhs)
            for p in range(r):  # @line L8
                x[i + p * m][j] = v[p]
    return x  # @line L9


def g_factor(
    maps: Sequence[Image],
    r: int,
    psi: Optional[Sequence[Sequence[complex]]] = None,
) -> list[list[float]]:
    """The g-factor map: g = sqrt([(E^H Psi^-1 E)^-1]_pp [E^H Psi^-1 E]_pp) at pixel i + p m."""
    c = len(maps)
    n = len(maps[0])
    m = n // r
    white = _whitener(psi, c)
    g = [[0.0] * n for _ in range(n)]
    eye_r = [[1.0 if p == q else 0.0 for q in range(r)] for p in range(r)]
    for i in range(m):
        for j in range(n):
            cols = [white([maps[k][i + p * m][j] for k in range(c)]) for p in range(r)]
            gram = [[sum(cols[p][k].conjugate() * cols[q][k] for k in range(c)) for q in range(r)] for p in range(r)]
            inv = solve(gram, eye_r)
            for p in range(r):
                g[i + p * m][j] = math.sqrt(max(0.0, (inv[p][p] * gram[p][p]).real))
    return g
