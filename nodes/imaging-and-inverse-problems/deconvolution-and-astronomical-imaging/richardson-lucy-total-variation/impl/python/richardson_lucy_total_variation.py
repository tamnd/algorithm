# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/richardson-lucy-total-variation/. The authors are listed in prov/DC5KCE.jsonl.
"""Richardson-Lucy with total variation regularization (RLTV), after Dey et al. (2006).

Images are lists of rows. The blur is periodic 2D convolution with a PSF h of
the image size, stored with its center at (0, 0), h >= 0 and sum h = 1. The
update is

    x <- x / (1 - lam div(grad x / |grad x|_eps)) * (h~ * (y / (h * x)))

with forward differences for grad, the negative adjoint (backward
differences) for div, a periodic border and |g|_eps = sqrt(g1^2 + g2^2 + eps^2).
"""

import math

from imgkit import circ_conv2


def mirror(h):
    """The PSF h(-r) on the same periodic grid."""
    n1, n2 = len(h), len(h[0])
    return [[h[(-i) % n1][(-j) % n2] for j in range(n2)] for i in range(n1)]


def grad(x):
    """Forward differences with a periodic border: (x[i+1][j] - x[i][j], x[i][j+1] - x[i][j])."""
    n1, n2 = len(x), len(x[0])
    g1 = [[x[(i + 1) % n1][j] - x[i][j] for j in range(n2)] for i in range(n1)]
    g2 = [[x[i][(j + 1) % n2] - x[i][j] for j in range(n2)] for i in range(n1)]
    return g1, g2


def div(p1, p2):
    """Backward differences, the negative adjoint of grad: <grad x, p> = -<x, div p>."""
    n1, n2 = len(p1), len(p1[0])
    return [[p1[i][j] - p1[(i - 1) % n1][j] + p2[i][j] - p2[i][(j - 1) % n2] for j in range(n2)] for i in range(n1)]


def tv_curvature(x, eps):
    """div(grad x / |grad x|_eps). Every entry lies in [-4, 4]."""
    g1, g2 = grad(x)
    n1, n2 = len(x), len(x[0])
    p1 = [[0.0] * n2 for _ in range(n1)]
    p2 = [[0.0] * n2 for _ in range(n1)]
    for i in range(n1):
        for j in range(n2):
            m = math.sqrt(g1[i][j] ** 2 + g2[i][j] ** 2 + eps * eps)
            p1[i][j] = g1[i][j] / m
            p2[i][j] = g2[i][j] / m
    return div(p1, p2)


def tv(x, eps):
    """The smoothed total variation sum sqrt(g1^2 + g2^2 + eps^2)."""
    g1, g2 = grad(x)
    return sum(math.sqrt(a * a + b * b + eps * eps) for ra, rb in zip(g1, g2) for a, b in zip(ra, rb))


def neg_log_likelihood(x, y, h):
    """sum (h * x - y log(h * x)), the Poisson negative log-likelihood up to a constant."""
    b = circ_conv2(x, h)
    total = 0.0
    for rb, ry in zip(b, y):
        for bi, yi in zip(rb, ry):
            total += bi - (yi * math.log(bi) if yi > 0 else 0.0)
    return total


def objective(x, y, h, lam, eps):
    """The functional that RLTV is built from: the Poisson term plus lam times TV."""
    return neg_log_likelihood(x, y, h) + lam * tv(x, eps)


def rl_correction(x, y, h, ht=None):
    """c = h~ * (y / (h * x)), the Richardson-Lucy correction factor."""
    if ht is None:
        ht = mirror(h)
    b = circ_conv2(x, h)
    r = [[(yi / bi if yi > 0 else 0.0) for bi, yi in zip(rb, ry)] for rb, ry in zip(b, y)]
    return circ_conv2(r, ht)


def rltv(y, h, lam, iters, x0=None, eps=1e-3, callback=None):
    """Run iters RLTV steps from x0 (default: the constant mean of y). lam = 0 gives Richardson-Lucy."""
    n1, n2 = len(y), len(y[0])
    if x0 is None:
        mean = sum(map(sum, y)) / (n1 * n2)
        x0 = [[mean] * n2 for _ in range(n1)]
    ht = mirror(h)
    x = [list(row) for row in x0]  # @line L1
    for k in range(iters):  # @line L2
        c = rl_correction(x, y, h, ht)  # @line L3
        kappa = tv_curvature(x, eps)  # @line L4
        new = []
        for i in range(n1):
            row = []
            for j in range(n2):
                d = 1.0 - lam * kappa[i][j]  # @line L5
                if d <= 0.0:
                    raise ValueError("1 - lam div(grad x / |grad x|) <= 0; lower lam")
                row.append(x[i][j] * c[i][j] / d)  # @line L6
            new.append(row)
        x = new
        if callback is not None:
            callback(k + 1, x)
    return x  # @line L7
