# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-input-output/. The authors are listed in prov/5WGXT1.jsonl.

"""Fienup's hybrid input-output (HIO) algorithm for phase retrieval.

Images are lists of rows. The data are the Fourier magnitudes A = |DFT2(f)|
of an unknown image f (unnormalized DFT, as in imgkit) and a support mask S.
With positive=True the object is also real and nonnegative, and the
iterates are real. One HIO step is

    g' = P_M g                      (put on the Fourier magnitude)
    g_next(r) = g'(r)               where r is in S (and g'(r) >= 0)
    g_next(r) = g(r) - beta g'(r)   elsewhere.

There is no monotone error and no convergence proof. The value beta = 0.9
is a tuned choice, not a result.
"""

import math

from imgkit import dft2, idft2


def magnitude_projection(g, amp):
    """P_M g: the nearest image to g whose Fourier magnitude is amp."""
    gf = dft2(g)  # @line L3
    for row_g, row_a in zip(gf, amp):  # @line L4
        for j, (v, a) in enumerate(zip(row_g, row_a)):
            r = abs(v)
            row_g[j] = a * v / r if r > 0.0 else complex(a)
    return idft2(gf)  # @line L5


def object_projection(gp, support, positive=False):
    """P_S g': g' on the support (its nonnegative real part if positive), 0 off it."""
    return [[(max(complex(v).real, 0.0) if positive else v) if s else 0.0 for v, s in zip(rv, rs)]
            for rv, rs in zip(gp, support)]


def object_error(gp, support, positive=False):
    """E_0(g') = ||g' - P_S g'||, the part of g' that breaks the object constraint."""
    proj = object_projection(gp, support, positive)
    return math.sqrt(sum(abs(v - p) ** 2 for rv, rp in zip(gp, proj) for v, p in zip(rv, rp)))


def hio_step(g, amp, support, beta=0.9, positive=False):
    """One HIO step. Returns (g_next, g') with g' = P_M g."""
    gp = magnitude_projection(g, amp)
    if positive:
        gp = [[complex(v).real for v in row] for row in gp]
    out = []
    for row_g, row_p, row_s in zip(g, gp, support):  # @line L6
        new_row = []
        for v, p, inside in zip(row_g, row_p, row_s):
            if inside and (not positive or p >= 0.0):  # @line L7
                new_row.append(p)
            else:
                new_row.append(v - beta * p)  # @line L8
        out.append(new_row)
    return out, gp


def hio(amp, support, g0, iters, beta=0.9, positive=False):
    """Run HIO. Returns (estimate, g, errors).

    errors[k] = E_0(g'_k) for k = 0 .. iters - 1, and estimate = P_S(g') of the
    last step, the image that satisfies the object constraint.
    """
    g = [list(row) for row in g0]  # @line L1
    gp = g
    errors = []
    for _ in range(iters):  # @line L2
        g, gp = hio_step(g, amp, support, beta, positive)
        errors.append(object_error(gp, support, positive))
    return object_projection(gp, support, positive), g, errors  # @line L9
