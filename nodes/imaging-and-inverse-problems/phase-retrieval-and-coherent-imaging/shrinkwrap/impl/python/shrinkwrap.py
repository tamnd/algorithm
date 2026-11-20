# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shrinkwrap/. The authors are listed in prov/J58G2A.jsonl.

"""Shrinkwrap: phase retrieval with a support that is updated during the run.

Images are lists of rows. The data are the Fourier magnitudes A = |DFT2(f)|
of an unknown image f (unnormalized DFT, as in imgkit). The support is not
given. It starts as the thresholded autocorrelation IDFT2(A^2), which holds
a shifted copy of the support of a nonnegative object. The iteration is HIO.
Every `every` steps the current object estimate is blurred with a Gaussian
of width sigma, and the new support is the set of pixels where the blur is
at least `thresh` times its maximum. Then sigma shrinks by the factor
`decay`, down to sigma_min. The default values (threshold 0.04 for the
autocorrelation, 0.2 for the update, every 20 steps, sigma from 3 to 1.5 by
1 percent) are the ones Marchesini et al. (2003) report; they are tuned,
not derived. There is no convergence proof.
"""

import math

from imgkit import circ_conv2, dft2, idft2


def magnitude_projection(g, amp):
    """P_M g: the nearest image to g whose Fourier magnitude is amp."""
    gf = dft2(g)
    for row_g, row_a in zip(gf, amp):
        for j, (v, a) in enumerate(zip(row_g, row_a)):
            r = abs(v)
            row_g[j] = a * v / r if r > 0.0 else complex(a)
    return idft2(gf)


def object_projection(gp, support):
    """P_S g': the nonnegative real part of g' on the support, 0 off it."""
    return [[max(complex(v).real, 0.0) if s else 0.0 for v, s in zip(rv, rs)]
            for rv, rs in zip(gp, support)]


def object_error(gp, support):
    """E_0(g') = ||g' - P_S g'||."""
    proj = object_projection(gp, support)
    return math.sqrt(sum(abs(v - p) ** 2 for rv, rp in zip(gp, proj) for v, p in zip(rv, rp)))


def hio_step(g, amp, support, beta):
    """One HIO step with nonnegativity. Returns (g_next, g') with g' = Re P_M g."""
    gp = [[complex(v).real for v in row] for row in magnitude_projection(g, amp)]
    out = [[p if s and p >= 0.0 else v - beta * p for v, p, s in zip(rv, rp, rs)]
           for rv, rp, rs in zip(g, gp, support)]
    return out, gp


def autocorrelation(amp):
    """IDFT2(A^2): the periodic autocorrelation c(t) = sum_r f(r + t) conj(f(r))."""
    return idft2([[a * a for a in row] for row in amp])


def threshold_support(img, frac):
    """The pixels where |img| is at least frac times its maximum."""
    top = max(abs(v) for row in img for v in row)
    return [[abs(v) >= frac * top for v in row] for row in img]


def gaussian_kernel(n1, n2, sigma):
    """A periodic Gaussian of width sigma, centered at (0, 0), with sum 1."""
    def w(i, n):
        d = min(i, n - i)
        return math.exp(-d * d / (2.0 * sigma * sigma))
    k = [[w(i, n1) * w(j, n2) for j in range(n2)] for i in range(n1)]
    total = sum(sum(row) for row in k)
    return [[v / total for v in row] for row in k]


def update_support(est, sigma, thresh):
    """Blur |est| with a Gaussian of width sigma and keep the pixels at or above thresh times the maximum."""
    blur = circ_conv2([[abs(v) for v in row] for row in est], gaussian_kernel(len(est), len(est[0]), sigma))
    return threshold_support(blur, thresh)


def shrinkwrap(amp, g0, iters, beta=0.9, every=20, sigma0=3.0, sigma_min=1.5, decay=0.99,
               thresh=0.2, auto_thresh=0.04):
    """Run HIO with shrinkwrap support updates. Returns (estimate, support, errors)."""
    support = threshold_support(autocorrelation(amp), auto_thresh)  # @line L1
    g = [list(row) for row in g0]  # @line L2
    sigma = sigma0
    errors = []
    gp = g
    for k in range(1, iters + 1):  # @line L3
        g, gp = hio_step(g, amp, support, beta)  # @line L4
        errors.append(object_error(gp, support))
        if k % every == 0:  # @line L5
            support = update_support(object_projection(gp, support), sigma, thresh)  # @line L6
            sigma = max(decay * sigma, sigma_min)  # @line L7
    return object_projection(gp, support), support, errors  # @line L8


def distance(a, b):
    """The Euclidean distance between two images."""
    return math.sqrt(sum(abs(u - v) ** 2 for ra, rb in zip(a, b) for u, v in zip(ra, rb)))
