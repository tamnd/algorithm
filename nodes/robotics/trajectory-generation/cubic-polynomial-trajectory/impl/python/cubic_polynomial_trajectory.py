# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cubic-polynomial-trajectory/. The authors are listed in prov/HEFVQT.jsonl.
"""Cubic polynomial trajectory of one joint.

cubic_coeffs(q0, v0, q1, v1, T) returns (a0, a1, a2, a3) of
q(t) = a0 + a1 t + a2 t^2 + a3 t^3 on [0, T], with q(0) = q0, q'(0) = v0,
q(T) = q1 and q'(T) = v1. The arithmetic is exact when the inputs are
fractions.Fraction values, and it works with float values too.

cubic_via(points, velocities, times) joins one cubic per interval, so
that the trajectory passes through each point with the given velocity.
"""


def cubic_coeffs(q0, v0, q1, v1, T):
    """Coefficients of the cubic that meets the four end conditions."""
    if T <= 0:
        raise ValueError("T must be positive")
    h = q1 - q0
    a0 = q0  # @line L1
    a1 = v0  # @line L2
    a2 = (3 * h - (2 * v0 + v1) * T) / (T * T)  # @line L3
    a3 = (-2 * h + (v0 + v1) * T) / (T * T * T)  # @line L4
    return (a0, a1, a2, a3)  # @line L5


def cubic_eval(a, t):
    """Return (q, q', q'') of the cubic with coefficients a at time t."""
    a0, a1, a2, a3 = a
    q = a0 + t * (a1 + t * (a2 + t * a3))  # @line L6
    dq = a1 + t * (2 * a2 + 3 * a3 * t)  # @line L7
    ddq = 2 * a2 + 6 * a3 * t  # @line L8
    return q, dq, ddq  # @line L9


def cubic_via(points, velocities, times):
    """One cubic per interval [times[k], times[k+1]].

    Returns a list of (t_start, coefficients) in local time t - t_start.
    The velocity at each point is given, so the result has a continuous
    velocity. Its acceleration jumps at the via points in general.
    """
    if not (len(points) == len(velocities) == len(times)) or len(points) < 2:
        raise ValueError("need at least two points, with one velocity and one time each")
    out = []
    for k in range(len(points) - 1):
        T = times[k + 1] - times[k]
        out.append((times[k], cubic_coeffs(points[k], velocities[k], points[k + 1], velocities[k + 1], T)))
    return out


def via_eval(segments, t):
    """Evaluate a via point trajectory from cubic_via at time t."""
    idx = 0
    for k, (t0, _) in enumerate(segments):
        if t >= t0:
            idx = k
    t0, a = segments[idx]
    return cubic_eval(a, t - t0)
