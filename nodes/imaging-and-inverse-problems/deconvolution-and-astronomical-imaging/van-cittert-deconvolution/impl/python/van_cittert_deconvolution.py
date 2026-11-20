# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-cittert-deconvolution/. The authors are listed in prov/3D8AWP.jsonl.
"""Van Cittert deconvolution: x <- x + beta (y - h * x).

Signals are lists and images are lists of rows. The blur is periodic
convolution with the PSF h stored with its center at index 0 (wrapped
around), so a delta PSF gives the identity. Works with float and with
fractions.Fraction values.
"""

from imgkit import circ_conv, circ_conv2, dft, dft2


def _is_image(x):
    return bool(x) and isinstance(x[0], (list, tuple))


def blur(x, h):
    """The periodic convolution h * x of a signal or an image."""
    if _is_image(x):
        return circ_conv2(x, h)
    return circ_conv(x, h)


def mirror(h):
    """The PSF h(-r) on the same periodic grid, so that blur(., mirror(h)) is the adjoint of blur(., h)."""
    if _is_image(h):
        n1, n2 = len(h), len(h[0])
        return [[h[(-i) % n1][(-j) % n2] for j in range(n2)] for i in range(n1)]
    n = len(h)
    return [h[(-j) % n] for j in range(n)]


def blur_adjoint(y, h):
    """The adjoint of x -> h * x for real h: correlation with h."""
    return blur(y, mirror(h))


def _zero_like(y):
    if _is_image(y):
        return [[0 * v for v in row] for row in y]
    return [0 * v for v in y]


def _axpy(x, beta, r):
    if _is_image(x):
        return [[a + beta * b for a, b in zip(ra, rb)] for ra, rb in zip(x, r)]
    return [a + beta * b for a, b in zip(x, r)]


def _sub(a, b):
    if _is_image(a):
        return [[p - q for p, q in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [p - q for p, q in zip(a, b)]


def van_cittert(y, h, beta=1, iters=10, x0=None, callback=None):
    """Run iters steps of x <- x + beta (y - h * x) from x0 (default 0).

    callback(k, x) is called after each step, if given. Returns the last x.
    """
    x = _zero_like(y) if x0 is None else x0  # @line L1
    for k in range(iters):  # @line L2
        r = _sub(y, blur(x, h))  # @line L3
        x = _axpy(x, beta, r)  # @line L4
        if callback is not None:
            callback(k + 1, x)
    return x  # @line L5


def van_cittert_landweber(y, h, beta=1, iters=10, x0=None):
    """The variant x <- x + beta h~ * (y - h * x), which is Landweber for the blur."""
    x = _zero_like(y) if x0 is None else x0
    for _ in range(iters):
        r = _sub(y, blur(x, h))
        x = _axpy(x, beta, blur_adjoint(r, h))
    return x


def otf(h):
    """The discrete OTF H_k = DFT(h)_k of a PSF stored with its center at index 0."""
    if _is_image(h):
        return dft2(h)
    return dft(h)


def filter_factors(h, beta, iters):
    """f_k = 1 - (1 - beta H_k)^iters, the factor of the Van Cittert iterate from x0 = 0."""
    if _is_image(h):
        return [[1 - (1 - beta * v) ** iters for v in row] for row in otf(h)]
    return [1 - (1 - beta * v) ** iters for v in otf(h)]


def converges(h, beta, tol=1e-12):
    """True when |1 - beta H_k| < 1 at every frequency with H_k != 0."""
    hs = otf(h)
    vals = [v for row in hs for v in row] if _is_image(h) else hs
    return all(abs(1 - beta * v) < 1 - tol for v in vals if abs(v) > tol)
