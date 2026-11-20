# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-deconvolution/. The authors are listed in prov/03GAAZ.jsonl.
"""Nearest neighbor deconvolution of a widefield focal series, after Agard (1984).

A stack is a list of planes y[0..nz-1], each an image (a list of rows). The
imaging model is y_j = sum_k h_{j-k} * x_k, with * the periodic 2D convolution
and h_d the 2D PSF of a source d planes away; planes outside the stack are
empty. Nearest neighbor deconvolution keeps only the two neighbors, and uses
the observed neighbors in place of the unknown ones:

    x_j = y_j - c (h_{+1} * y_{j-1} + h_{-1} * y_{j+1}),

optionally followed by a 2D Wiener filter with the in-focus PSF h_0 and by
clipping at zero.
"""

from imgkit import circ_conv2, dft2, idft2, new_image


def blur_stack(x, psfs):
    """y_j = sum_k psfs[j - k] * x_k over the offsets present in the dict psfs, zero outside the stack."""
    nz = len(x)
    n1, n2 = len(x[0]), len(x[0][0])
    out = []
    for j in range(nz):
        acc = new_image(n1, n2, 0)
        for d, h in psfs.items():
            k = j - d
            if 0 <= k < nz:
                b = circ_conv2(x[k], h)
                acc = [[p + q for p, q in zip(ra, rb)] for ra, rb in zip(acc, b)]
        out.append(acc)
    return out


def wiener_2d(img, h0, alpha):
    """The 2D filter conj(H0) Y / (|H0|^2 + alpha), real part. alpha = 0 is the plain inverse."""
    hf = dft2(h0)
    yf = dft2(img)
    xf = [[hk.conjugate() * yk / (abs(hk) ** 2 + alpha) for hk, yk in zip(rh, ry)] for rh, ry in zip(hf, yf)]
    return [[v.real for v in row] for row in idft2(xf)]


def nearest_neighbor(y, h_prev, h_next, c, h0=None, alpha=0.0, clip=False):
    """Nearest neighbor deconvolution of the stack y.

    h_prev is the PSF h_{+1} that carries plane j - 1 into plane j, h_next the
    PSF h_{-1} that carries plane j + 1 into plane j, and c the subtraction
    constant. With h0 given, each plane is then filtered by wiener_2d(., h0,
    alpha). With clip, negative values are set to 0.
    """
    nz = len(y)
    n1, n2 = len(y[0]), len(y[0][0])
    out = []
    for j in range(nz):  # @line L1
        b = new_image(n1, n2, 0)  # @line L2
        if j > 0:
            b = circ_conv2(y[j - 1], h_prev)  # @line L3
        if j < nz - 1:
            t = circ_conv2(y[j + 1], h_next)  # @line L4
            b = [[p + q for p, q in zip(ra, rb)] for ra, rb in zip(b, t)]
        xj = [[yv - c * bv for yv, bv in zip(ry, rb)] for ry, rb in zip(y[j], b)]  # @line L5
        if h0 is not None:
            xj = wiener_2d(xj, h0, alpha)  # @line L6
        if clip:
            xj = [[max(v, 0) for v in row] for row in xj]  # @line L7
        out.append(xj)
    return out  # @line L8
