# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-reduction-algorithm/. The authors are listed in prov/HKZC9V.jsonl.

"""Fienup's error reduction algorithm for phase retrieval with a support.

Images are lists of rows. The data are the Fourier magnitudes A = |DFT2(f)|
of an unknown image f (unnormalized DFT, as in imgkit). The object
constraint is a support mask S (a list of rows of booleans), with or without
nonnegativity. Each iteration is a magnitude projection P_M followed by an
object projection P_S. The errors use the unitary DFT, so they are distances
in the object domain (N = n1 n2 is the number of pixels):

    E_F(g)^2 = (1 / N) sum_u (|G_u| - A_u)^2 = ||g - P_M g||^2,
    E_0(g')^2 = ||g' - P_S g'||^2.

E_F does not increase from one iteration to the next.
"""

import math

from imgkit import dft2, idft2


def replace_magnitude(gf, amp):
    """The spectrum with magnitude amp and the phase of gf (phase 0 where gf is 0)."""
    out = []
    for row_g, row_a in zip(gf, amp):
        new_row = []
        for v, a in zip(row_g, row_a):
            r = abs(v)
            new_row.append(a * v / r if r > 0.0 else complex(a))
        out.append(new_row)
    return out


def magnitude_projection(g, amp):
    """P_M g: a nearest image to g whose Fourier magnitude is amp."""
    return idft2(replace_magnitude(dft2(g), amp))


def object_projection(gp, support, positive=False):
    """P_S g': keep g' on the support (its nonnegative real part if positive), 0 off it."""
    out = []
    for row_g, row_s in zip(gp, support):
        new_row = []
        for v, inside in zip(row_g, row_s):
            if not inside:
                new_row.append(0.0)
            elif positive:
                new_row.append(max(complex(v).real, 0.0))
            else:
                new_row.append(v)
        out.append(new_row)
    return out


def fourier_error(g, amp):
    """E_F(g) = ||g - P_M g||, computed in the Fourier domain."""
    gf = dft2(g)
    n = len(gf) * len(gf[0])
    s = sum((abs(v) - a) ** 2 for row_g, row_a in zip(gf, amp) for v, a in zip(row_g, row_a))
    return math.sqrt(s / n)


def object_error(gp, support, positive=False):
    """E_0(g') = ||g' - P_S g'||."""
    proj = object_projection(gp, support, positive)
    return math.sqrt(sum(abs(v - p) ** 2 for rv, rp in zip(gp, proj) for v, p in zip(rv, rp)))


def error_reduction(amp, support, g0, iters, positive=False):
    """Run error reduction. Returns (g, errors) with errors[k] = E_F(g_k), k = 0 .. iters."""
    g = object_projection(g0, support, positive)  # @line L1
    errors = []
    n = len(amp) * len(amp[0])
    for _ in range(iters):  # @line L2
        gf = dft2(g)  # @line L3
        errors.append(math.sqrt(sum((abs(v) - a) ** 2 for rg, ra in zip(gf, amp) for v, a in zip(rg, ra)) / n))
        gpf = replace_magnitude(gf, amp)  # @line L4
        gp = idft2(gpf)  # @line L5
        g = object_projection(gp, support, positive)  # @line L6
    errors.append(fourier_error(g, amp))
    return g, errors  # @line L7
