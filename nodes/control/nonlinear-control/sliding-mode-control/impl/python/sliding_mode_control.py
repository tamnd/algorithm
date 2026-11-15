# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-mode-control/. The authors are listed in prov/WP3VZ0.jsonl.

"""Sliding mode control of a system in controllable canonical form

    x_i' = x_(i+1),   i = 1, ..., n - 1,
    x_n' = f(x) + b(x) u + d(t, x),

with a known nominal model f_hat of f, a known b(x) != 0 and an unknown
term delta = f - f_hat + d with |delta| <= D. The sliding variable is

    s = c_1 x_1 + ... + c_(n-1) x_(n-1) + x_n,

and the control is

    u = (-f_hat(x) - sum_(i < n) c_i x_(i+1) - k sigma(s)) / b(x),

with sigma(s) = sgn(s), or sat(s / phi) for a boundary layer of width
phi > 0. Along the system s' = delta - k sigma(s), so k >= D + eta gives
s s' <= -eta |s| when sigma = sgn.

The input values may be int, Fraction or float. With exact data and exact
f_hat and b, the value of u is exact (the division by b uses Fraction when
both sides are int).
"""

from fractions import Fraction

__all__ = ["sgn", "sat", "sliding_variable", "smc"]


def sgn(s):
    """Return -1, 0 or 1."""
    return (s > 0) - (s < 0)


def sat(z):
    """Return z clipped to [-1, 1]."""
    if z > 1:
        return 1
    if z < -1:
        return -1
    return z


def _div(p, q):
    if isinstance(p, int) and isinstance(q, int):
        return Fraction(p, q)
    return p / q


def sliding_variable(c, x):
    """s = c_1 x_1 + ... + c_(n-1) x_(n-1) + x_n, for len(c) = len(x) - 1."""
    n = len(x)
    if len(c) != n - 1:
        raise ValueError("c must have len(x) - 1 entries")
    return sum(c[i] * x[i] for i in range(n - 1)) + x[n - 1]


def smc(x, c, f_hat, b, k, phi=0):
    """Return (u, s) for the state x.

    c: the n - 1 coefficients of the sliding surface; the polynomial
       c_1 + c_2 l + ... + c_(n-1) l^(n-2) + l^(n-1) must be Hurwitz.
    f_hat(x): the nominal drift of the last state.
    b(x): the input gain of the last state, never zero.
    k: the switching gain, k >= D + eta with eta > 0.
    phi: 0 for the discontinuous law, or the width of the boundary layer.
    """
    n = len(x)
    if k <= 0:
        raise ValueError("k must be positive")
    if phi < 0:
        raise ValueError("phi must be zero or positive")
    s = sliding_variable(c, x)  # @line L1
    bx = b(x)
    if bx == 0:
        raise ZeroDivisionError("b(x) = 0")
    v = -f_hat(x) - sum(c[i] * x[i + 1] for i in range(n - 1))  # @line L2
    if phi > 0:  # @line L3
        sigma = sat(_div(s, phi))  # @line L3
    else:
        sigma = sgn(s)  # @line L4
    u = _div(v - k * sigma, bx)  # @line L5
    return u, s  # @line L6
