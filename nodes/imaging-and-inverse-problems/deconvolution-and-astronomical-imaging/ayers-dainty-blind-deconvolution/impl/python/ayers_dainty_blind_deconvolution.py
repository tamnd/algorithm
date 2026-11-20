# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ayers-dainty-blind-deconvolution/. The authors are listed in prov/MB6VNZ.jsonl.
"""Iterative blind deconvolution in the style of Ayers and Dainty (1988).

Images are lists of rows on a periodic n1 x n2 grid. The data are
y = h * f (+ noise) with the PSF h stored with its center at index (0, 0)
(wrapped around). Both f and h are unknown. The method alternates two
Fourier domain estimates,

    H <- conj(F) C / (|F|^2 + alpha)    (the PSF from the data and the object)
    F <- conj(H) C / (|H|^2 + alpha)    (the object from the data and the PSF)

with C = DFT(y). After each estimate it goes back to the image domain and
applies the constraints there: the object is real, nonnegative and zero
outside an optional support; the PSF is real, nonnegative, zero outside a
known support and sums to 1. Each Fourier estimate is the per frequency
minimizer of |C - A B|^2 + alpha |B|^2, the Wiener-type form of Davey, Lane
and Bates (1989). An optional relaxation beta mixes the new spectrum with
the old one, in the spirit of the averaging step of the original method.
There is no convergence proof.
"""

import cmath
import math


def _roots(n, sign):
    return [cmath.exp(sign * 2j * math.pi * k / n) for k in range(n)]


def _dft1(x, w):
    n = len(x)
    return [sum(x[j] * w[(j * k) % n] for j in range(n)) for k in range(n)]


def _rows_cols(img, sign, scale):
    n1, n2 = len(img), len(img[0])
    w1, w2 = _roots(n1, sign), _roots(n2, sign)
    rows = [_dft1(r, w2) for r in img]
    cols = [_dft1([rows[i][j] for i in range(n1)], w1) for j in range(n2)]
    return [[cols[j][i] * scale for j in range(n2)] for i in range(n1)]


def dft2(img):
    """X[k1][k2] = sum x[j1][j2] exp(-2 pi i (j1 k1 / n1 + j2 k2 / n2)), unnormalized."""
    return _rows_cols(img, -1, 1.0)


def idft2(img):
    """The inverse of dft2, with the factor 1 / (n1 n2)."""
    return _rows_cols(img, 1, 1.0 / (len(img) * len(img[0])))


def conv2(x, h):
    """(h * x)[i1][i2] = sum h[j1][j2] x[(i1 - j1) mod n1][(i2 - j2) mod n2]."""
    n1, n2 = len(x), len(x[0])
    out = [[0.0] * n2 for _ in range(n1)]
    for j1 in range(n1):
        for j2 in range(n2):
            v = h[j1][j2]
            if v == 0:
                continue
            for i1 in range(n1):
                xr, orow = x[(i1 - j1) % n1], out[i1]
                for i2 in range(n2):
                    orow[i2] += v * xr[(i2 - j2) % n2]
    return out


def wiener_update(c, a, alpha):
    """Per frequency minimizer B of |C - A B|^2 + alpha |B|^2, that is conj(A) C / (|A|^2 + alpha).

    With alpha = 0 and A = 0 at a frequency every B fits equally well; 0 is returned there.
    """
    out = []
    for crow, arow in zip(c, a):
        row = []
        for ck, ak in zip(crow, arow):
            den = abs(ak) ** 2 + alpha
            row.append(ak.conjugate() * ck / den if den > 0 else 0j)
        out.append(row)
    return out


def project_object(z, support=None):
    """Real part, negative values set to 0, and zero outside the support if one is given."""
    if support is None:
        return [[max(v.real, 0.0) for v in row] for row in z]
    return [[max(v.real, 0.0) if s else 0.0 for v, s in zip(row, srow)] for row, srow in zip(z, support)]


def project_psf(z, support, fallback):
    """Real part, zero outside the support, negative values set to 0, scaled to sum 1.

    If nothing positive is left, the previous PSF (fallback) is kept.
    """
    h = project_object(z, support)
    total = sum(sum(row) for row in h)
    if total <= 0:
        return [list(row) for row in fallback]
    return [[v / total for v in row] for row in h]


def _mix(old, new, beta):
    return [[(1 - beta) * o + beta * v for o, v in zip(ro, rn)] for ro, rn in zip(old, new)]


def misfit(y, f, h):
    """||y - h * f|| / ||y||."""
    hf = conv2(f, h)
    num = sum((a - b) ** 2 for ra, rb in zip(y, hf) for a, b in zip(ra, rb))
    den = sum(a * a for ra in y for a in ra)
    return math.sqrt(num / den)


def ayers_dainty(y, f0, h0, support=None, obj_support=None, alpha=1e-3, beta=1.0, iters=50, callback=None):
    """Alternate Fourier estimates of the PSF and the object with image domain constraints.

    y: the blurred image. f0, h0: the starting object and PSF.
    support: booleans, True where the PSF may be nonzero (default: everywhere).
    obj_support: booleans, True where the object may be nonzero (default: everywhere).
    alpha >= 0: the Wiener weight (0 gives the inverse filter where it is defined).
    beta in (0, 1]: the weight of the new spectrum in each update.
    callback(k, f, h) is called after each pass. Returns (f, h).
    """
    n1, n2 = len(y), len(y[0])
    if support is None:
        support = [[True] * n2 for _ in range(n1)]
    delta = [[1.0 if (i, j) == (0, 0) else 0.0 for j in range(n2)] for i in range(n1)]
    f = project_object([[complex(v) for v in row] for row in f0], obj_support)  # @line L1
    h = project_psf([[complex(v) for v in row] for row in h0], support, delta)
    c = dft2(y)  # @line L2
    for k in range(iters):  # @line L3
        fh = dft2(f)
        hh = wiener_update(c, fh, alpha)  # @line L4
        if beta != 1.0:
            hh = _mix(dft2(h), hh, beta)
        h = project_psf(idft2(hh), support, h)  # @line L5
        ff = wiener_update(c, dft2(h), alpha)  # @line L6
        if beta != 1.0:
            ff = _mix(fh, ff, beta)
        f = project_object(idft2(ff), obj_support)  # @line L7
        if callback is not None:
            callback(k + 1, f, h)
    return f, h  # @line L8


def shift(x, s1, s2):
    """The image x moved by (s1, s2) on the periodic grid: out[i][j] = x[i - s1][j - s2]."""
    n1, n2 = len(x), len(x[0])
    return [[x[(i - s1) % n1][(j - s2) % n2] for j in range(n2)] for i in range(n1)]
