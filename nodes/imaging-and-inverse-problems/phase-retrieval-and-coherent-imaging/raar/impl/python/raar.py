# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raar/. The authors are listed in prov/MJJXEG.jsonl.

"""Luke's relaxed averaged alternating reflections (RAAR).

For two nearest point maps P_S and P_M and the reflections R = 2 P - I,

    V(x) = (beta / 2) (R_S R_M x + x) + (1 - beta) P_M x,   0 < beta <= 1.

At beta = 1 this is the Douglas-Rachford map. Images are lists of rows. The
phase retrieval version uses P_M, which puts the Fourier magnitude
A = |DFT2(f)| on an image (unnormalized DFT, as in imgkit), and P_S, which
keeps the image on the support S (the nonnegative real part with
positive=True) and sets zero off it. The estimate is P_M x.

For two closed convex sets that meet, V is firmly nonexpansive, its fixed
points are the points of the intersection (for 0 < beta < 1), and the
iterates converge to one of them. For phase retrieval the magnitude set is
not convex, and there is no convergence proof.
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


def support_projection(support, positive=False):
    """The map P_S for a support mask, as a function of an image."""
    def proj(g):
        return [[(max(complex(v).real, 0.0) if positive else v) if s else 0.0 for v, s in zip(rv, rs)]
                for rv, rs in zip(g, support)]
    return proj


def raar_step(x, proj_s, proj_m, beta):
    """One RAAR step for the nearest point maps proj_s and proj_m."""
    p = proj_m(x)  # @line L3
    r = [[2 * u - v for u, v in zip(rp, rx)] for rp, rx in zip(p, x)]  # @line L4
    q = proj_s(r)  # @line L5
    return [[0.5 * beta * (2 * a - b + v) + (1 - beta) * u
             for a, b, v, u in zip(rq, rr, rx, rp)]
            for rq, rr, rx, rp in zip(q, r, x, p)]  # @line L6


def raar_generic(proj_s, proj_m, x0, iters, beta):
    """Run RAAR for any two nearest point maps. Returns the list of iterates x_0 .. x_iters."""
    x = [list(row) for row in x0]  # @line L1
    path = [x]
    for _ in range(iters):  # @line L2
        x = raar_step(x, proj_s, proj_m, beta)
        path.append(x)
    return path


def raar(amp, support, x0, iters, beta=0.9, positive=False):
    """RAAR for phase retrieval. Returns (estimate, x) with estimate = P_M x."""
    proj_s = support_projection(support, positive)
    proj_m = lambda g: magnitude_projection(g, amp)  # noqa: E731
    x = raar_generic(proj_s, proj_m, x0, iters, beta)[-1]
    return proj_m(x), x  # @line L7


def distance(a, b):
    """The Euclidean distance between two images."""
    return math.sqrt(sum(abs(u - v) ** 2 for ra, rb in zip(a, b) for u, v in zip(ra, rb)))
