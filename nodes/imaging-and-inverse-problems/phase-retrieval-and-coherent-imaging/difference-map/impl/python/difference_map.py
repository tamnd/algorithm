# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-map/. The authors are listed in prov/CRHCPN.jsonl.

"""Elser's difference map for phase retrieval with a support.

Images are lists of rows. P_M puts the Fourier magnitude A = |DFT2(f)| on an
image (unnormalized DFT, as in imgkit). P_S is the object projection: zero
off the support S, and with positive=True the nonnegative real part on S.
With the estimates

    f_S(x) = (1 + gamma_S) P_S(x) - gamma_S x,
    f_M(x) = (1 + gamma_M) P_M(x) - gamma_M x,

one step is x <- x + beta (P_S(f_M(x)) - P_M(f_S(x))). Elser's choice is
gamma_S = -1 / beta and gamma_M = 1 / beta. The choice gamma_S = -1 and
gamma_M = 1 / beta gives Fienup's HIO with feedback beta (support only).
At a fixed point, P_M(f_S(x)) = P_S(f_M(x)) is a solution.
"""

import math

from imgkit import dft2, idft2


def magnitude_projection(g, amp):
    """P_M g: the nearest image to g whose Fourier magnitude is amp."""
    gf = dft2(g)
    for row_g, row_a in zip(gf, amp):
        for j, (v, a) in enumerate(zip(row_g, row_a)):
            r = abs(v)
            row_g[j] = a * v / r if r > 0.0 else complex(a)
    return idft2(gf)


def object_projection(g, support, positive=False):
    """P_S g: g on the support (its nonnegative real part if positive), 0 off it."""
    return [[(max(complex(v).real, 0.0) if positive else v) if s else 0.0 for v, s in zip(rv, rs)]
            for rv, rs in zip(g, support)]


def combine(a, x, ca, cx):
    """The image ca a + cx x."""
    return [[ca * u + cx * v for u, v in zip(ra, rx)] for ra, rx in zip(a, x)]


def dm_step(x, amp, support, beta, gamma_s, gamma_m, positive=False):
    """One difference map step. Returns (x_next, estimate) with estimate = P_M(f_S(x))."""
    f_s = combine(object_projection(x, support, positive), x, 1 + gamma_s, -gamma_s)  # @line L3
    f_m = combine(magnitude_projection(x, amp), x, 1 + gamma_m, -gamma_m)  # @line L4
    p_m = magnitude_projection(f_s, amp)
    p_s = object_projection(f_m, support, positive)
    x_next = [[v + beta * (s - m) for v, s, m in zip(rv, rs, rm)]
              for rv, rs, rm in zip(x, p_s, p_m)]  # @line L5
    return x_next, p_m


def difference_map(amp, support, x0, iters, beta=0.9, gamma_s=None, gamma_m=None, positive=False):
    """Run the difference map. Returns (estimate, x, gaps).

    gaps[k] = ||x_{k+1} - x_k|| / |beta| = ||P_S(f_M) - P_M(f_S)||, which is zero
    exactly at a fixed point. The defaults are Elser's gamma_S = -1 / beta and
    gamma_M = 1 / beta.
    """
    if gamma_s is None:
        gamma_s = -1.0 / beta
    if gamma_m is None:
        gamma_m = 1.0 / beta
    x = [list(row) for row in x0]  # @line L1
    estimate = x
    gaps = []
    for _ in range(iters):  # @line L2
        x_next, estimate = dm_step(x, amp, support, beta, gamma_s, gamma_m, positive)
        gaps.append(math.sqrt(sum(abs(a - b) ** 2 for ra, rb in zip(x_next, x) for a, b in zip(ra, rb)))
                    / abs(beta))
        x = x_next
    return estimate, x, gaps  # @line L6
