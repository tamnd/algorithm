# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parametric-cnc-interpolator/. The authors are listed in prov/QFCNX0.jsonl.

"""A parametric curve interpolator for CNC, after Shpitalni, Koren and Lo.

The tool follows a parametric curve C(u). In each interpolation period tau
it should move the arc length L = V tau along the curve. The interpolator
computes the next parameter by the Taylor expansion of u as a function of
the arc length s:

    du/ds   = 1 / |C'|
    d2u/ds2 = -(C' . C'') / |C'|^4

so the second order step is

    du = L / |C'| - L^2 (C' . C'') / (2 |C'|^4)

and the first order step keeps only the first term. The arc length that
the step really covers differs from L by O(L^3) for the second order step
and by O(L^2) for the first order step.

Curves are given by their derivative functions d1(u) = C'(u) and
d2(u) = C''(u), which return tuples. The speed |C'(u)| is computed with
math.sqrt unless a function `speed` is given. For a Pythagorean hodograph
curve the speed is a polynomial, and with Fractions the whole step is exact.
"""

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def taylor_step(d1, d2, u, L, order=2, speed=None):
    """The parameter increment for the arc length L at the parameter u."""
    a = d1(u)
    sigma = speed(u) if speed is not None else math.sqrt(dot(a, a))
    if sigma == 0:
        raise ValueError("the curve is singular: C'(u) = 0")
    du = L / sigma
    if order == 2:
        b = d2(u)
        du -= L * L * dot(a, b) / (2 * sigma ** 4)
    elif order != 1:
        raise ValueError("order must be 1 or 2")
    return du


def interpolate(d1, d2, u_start, u_end, V, tau, order=2, speed=None):
    """The list of parameters at the ends of the periods, from u_start to u_end."""
    if V <= 0 or tau <= 0:
        raise ValueError("the feed and the period must be positive")
    L = V * tau  # @line L1
    u = u_start  # @line L2
    params = [u]
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    while u < u_end:  # @line L3
        a, b = d1(u), d2(u)  # @line L4
        sigma = speed(u) if speed is not None else math.sqrt(dot(a, a))
        if sigma == 0:
            raise ValueError("the curve is singular: C'(u) = 0")
        du = L / sigma - (L * L * dot(a, b) / (2 * sigma ** 4) if order == 2 else 0)  # @line L5
        if du <= 0:
            raise ValueError("the step is not positive; the period is too long for this curve")
        u = min(u + du, u_end)  # @line L6
        params.append(u)  # @line L7
    return params  # @line L8


def exact_parameters(s, s_inverse, u_start, u_end, V, tau):
    """Reference method: the parameters at arc length steps of exactly V tau,
    from the arc length function s(u) and its inverse."""
    L = V * tau
    s0, s1 = s(u_start), s(u_end)
    params = [u_start]
    k = 1
    while s0 + k * L < s1:
        params.append(s_inverse(s0 + k * L))
        k += 1
    params.append(u_end)
    return params


def feed_errors(params, s, L):
    """The relative error (arc length of the step - L) / L of each full step."""
    out = []
    for a, b in zip(params, params[1:-1]):
        out.append((s(b) - s(a) - L) / L)
    return out
