# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-disturbance-rejection-control/. The authors are listed in prov/1YHBZH.jsonl.

"""Linear active disturbance rejection control for a plant of order two

    y'' = f(t, y, y') + b u,

where f (the total disturbance) is unknown and b is known only roughly, as
b0. Write the plant as y'' = F + b0 u with F = f + (b - b0) u, and estimate
z = (y, y', F) with an observer of the extended state (bandwidth wo):

    z1' = z2 + 3 wo (y - z1),
    z2' = z3 + 3 wo^2 (y - z1) + b0 u,
    z3' = wo^3 (y - z1).

The control cancels the estimate z3 and applies a PD law (bandwidth wc):

    u = (wc^2 (r - z1) - 2 wc z2 - z3) / b0.

If z3 = F exactly, the loop is y'' = wc^2 (r - y) - 2 wc y', with the double
pole -wc. With f = 0 and b = b0 the poles are -wc (twice) and -wo (three times).

control and eso_rhs keep int and Fraction inputs exact.
"""

from fractions import Fraction

__all__ = ["control", "eso_rhs", "observer_gains"]


def _div(a, b):
    if b == 0:
        raise ValueError("b0 must be nonzero")
    if isinstance(a, int) and isinstance(b, int):
        return Fraction(a, b)
    return a / b


def observer_gains(wo):
    """Gains (3 wo, 3 wo^2, wo^3): all three observer poles at -wo."""
    if wo <= 0:
        raise ValueError("wo must be positive")
    return 3 * wo, 3 * wo ** 2, wo ** 3


def control(z, r, wc, b0):
    """Control from the estimate z = (z1, z2, z3) and the reference r."""
    if wc <= 0:
        raise ValueError("wc must be positive")
    u0 = wc ** 2 * (r - z[0]) - 2 * wc * z[1]  # @line L1
    return _div(u0 - z[2], b0)  # @line L2


def eso_rhs(z, y, u, wo, b0):
    """Derivative of the estimate z for the measured output y and input u."""
    b1, b2, b3 = observer_gains(wo)
    e = y - z[0]  # @line L3
    d1 = z[1] + b1 * e  # @line L4
    d2 = z[2] + b2 * e + b0 * u  # @line L5
    d3 = b3 * e  # @line L6
    return [d1, d2, d3]  # @line L7
