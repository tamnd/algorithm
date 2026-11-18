# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moment-shadow-mapping/. The authors are listed in prov/ZPXE0M.jsonl.

"""Moment shadow mapping with four power moments (Peters and Klein 2015).

This is the Hamburger 4MSM lookup of the paper. Depth is in [0, 1] (the
Direct3D clip range), smaller is nearer to the light. A filtered texel holds
b = (b1, b2, b3, b4), the means of z, z^2, z^3 and z^4 over the depths z under
the filter. The lookup computes G, the sharp lower bound on the occluded
fraction (the weight of the depths z < zf), and returns 1 - G, which is an
upper bound on the lit fraction (the weight of the depths z >= zf).
"""

from math import sqrt


def power_moments(depths, weights=None):
    """The filtered moments (b1, b2, b3, b4) of a list of depths."""
    if weights is None:
        weights = [1] * len(depths)
    total = sum(weights)
    return tuple(sum(w * z ** k for z, w in zip(depths, weights)) / total for k in range(1, 5))


def solve_hankel(b, zf):
    """Solve B c = (1, zf, zf^2) for B = [[1, b1, b2], [b1, b2, b3], [b2, b3, b4]]
    by the Cholesky factorization B = L D L^T, as in the paper's shader."""
    b1, b2, b3, b4 = b
    d1 = b2 - b1 * b1
    if d1 <= 0:
        raise ValueError("the moments are not in the interior of the moment space")
    l32 = (b3 - b1 * b2) / d1
    d2 = (b4 - b2 * b2) - l32 * l32 * d1
    if d2 <= 0:
        raise ValueError("the moments are not in the interior of the moment space")
    # Forward substitution with the unit lower triangle L = [[1,0,0],[b1,1,0],[b2,l32,1]].
    y1 = 1
    y2 = zf - b1 * y1
    y3 = zf * zf - b2 * y1 - l32 * y2
    # Divide by D and back substitution with L^T.
    c3 = y3 / d2
    c2 = y2 / d1 - l32 * c3
    c1 = y1 - b1 * c2 - b2 * c3
    return c1, c2, c3


def shadow_intensity(b, zf):
    """G of the paper: the sharp lower bound on the occluded fraction."""
    c1, c2, c3 = solve_hankel(b, zf)  # @line L3
    if c3 == 0:
        raise ZeroDivisionError("c3 = 0: no canonical representation for this depth")
    p, q = c2 / c3, c1 / c3  # @line L4
    disc = sqrt(max(p * p / 4 - q, 0.0))
    z2, z3 = -p / 2 - disc, -p / 2 + disc
    b1, b2 = b[0], b[1]
    if zf <= z2:  # @line L5
        return 0.0
    if zf <= z3:  # @line L6
        return (zf * z3 - b1 * (zf + z3) + b2) / ((z3 - z2) * (zf - z2))
    return 1 - (z2 * z3 - b1 * (z2 + z3) + b2) / ((zf - z2) * (zf - z3))  # @line L7


def msm_lookup(b, z, alpha=0.0, beta=0.0):
    """The lit estimate 1 - G for the receiver depth z.

    alpha is the moment bias (the paper uses 3e-5 for its quantized formats),
    beta the depth bias. Both are tuning.
    """
    bb = tuple((1 - alpha) * x + alpha * 0.5 for x in b)  # @line L1
    zf = z - beta  # @line L2
    g = shadow_intensity(bb, zf)
    return 1 - min(max(g, 0.0), 1.0)  # @line L8


def canonical_nodes(b, zf):
    """The support {zf, z2, z3} of the canonical representation."""
    c1, c2, c3 = solve_hankel(b, zf)
    p, q = c2 / c3, c1 / c3
    disc = sqrt(max(p * p / 4 - q, 0.0))
    return zf, -p / 2 - disc, -p / 2 + disc
