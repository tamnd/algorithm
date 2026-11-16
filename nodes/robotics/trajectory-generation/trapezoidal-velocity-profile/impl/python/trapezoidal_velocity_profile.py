# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapezoidal-velocity-profile/. The authors are listed in prov/E287FS.jsonl.
"""Trapezoidal velocity profile: rest-to-rest motion of one axis.

trapezoid(D, V, A) returns (Ta, vp, T): the time of the acceleration ramp,
the peak velocity and the total time of the fastest motion over the
distance D > 0 with |velocity| <= V and |acceleration| <= A. When
D < V^2 / A the profile is a triangle and vp < V.

trapezoid_sample(D, Ta, vp, T, t) returns (s, s', s'') at time t.
trapezoid_fixed_time(D, A, T) returns the ramp time of a profile that
covers D in the longer time T, with the same acceleration A. It is used to
make several axes end at the same time.
"""

import math


def trapezoid(D, V, A):
    """Return (Ta, vp, T) of the minimum time rest-to-rest profile."""
    if D <= 0 or V <= 0 or A <= 0:
        raise ValueError("D, V and A must be positive")
    if D * A >= V * V:  # @line L1
        Ta = V / A  # @line L2
        vp = V
        T = D / V + V / A  # @line L3
    else:
        Ta = math.sqrt(D / A)  # @line L4
        vp = A * Ta
        T = 2 * Ta  # @line L5
    return Ta, vp, T  # @line L6


def trapezoid_sample(D, Ta, vp, T, t):
    """Return (s, s', s'') of the profile at time t in [0, T]."""
    A = vp / Ta
    if t <= 0:
        return 0 * D, 0 * D, 0 * D
    if t < Ta:  # @line L7
        return A * t * t / 2, A * t, A
    if t <= T - Ta:  # @line L8
        return vp * (t - Ta / 2), vp, 0 * D
    if t < T:  # @line L9
        r = T - t
        return D - A * r * r / 2, A * r, -A
    return D, 0 * D, 0 * D


def trapezoid_fixed_time(D, A, T):
    """Ramp time Ta of the profile with acceleration A that covers D in exactly T.

    It solves D = A Ta (T - Ta) for the smaller root. A solution exists if and
    only if T >= 2 sqrt(D / A).
    """
    disc = T * T - 4 * D / A
    if disc < 0:
        raise ValueError("T is shorter than the minimum time 2 sqrt(D / A)")
    return (T - math.sqrt(disc)) / 2


def move(q0, q1, V, A):
    """Signed version: a function t -> (q, q', q'') from q0 to q1, and the time T."""
    D = abs(q1 - q0)
    if D == 0:
        return (lambda t: (q0, 0.0, 0.0)), 0.0
    sign = 1 if q1 > q0 else -1
    Ta, vp, T = trapezoid(D, V, A)

    def f(t):
        s, ds, dds = trapezoid_sample(D, Ta, vp, T, t)
        return q0 + sign * s, sign * ds, sign * dds

    return f, T
