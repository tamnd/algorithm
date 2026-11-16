# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quintic-polynomial-trajectory/. The authors are listed in prov/JZFXGC.jsonl.
"""Quintic polynomial trajectory of one joint.

quintic_coeffs(q0, v0, c0, q1, v1, c1, T) returns (a0, ..., a5) of
q(t) = a0 + a1 t + ... + a5 t^5 on [0, T], with position q, velocity v
and acceleration c given at t = 0 and t = T. The arithmetic is exact
when the inputs are fractions.Fraction values.
"""


def quintic_coeffs(q0, v0, c0, q1, v1, c1, T):
    """Coefficients of the quintic that meets the six end conditions."""
    if T <= 0:
        raise ValueError("T must be positive")
    h = q1 - q0
    a0 = q0  # @line L1
    a1 = v0
    a2 = c0 / 2
    a3 = (20 * h - (8 * v1 + 12 * v0) * T - (3 * c0 - c1) * T ** 2) / (2 * T ** 3)  # @line L2
    a4 = (-30 * h + (14 * v1 + 16 * v0) * T + (3 * c0 - 2 * c1) * T ** 2) / (2 * T ** 4)  # @line L3
    a5 = (12 * h - 6 * (v1 + v0) * T + (c1 - c0) * T ** 2) / (2 * T ** 5)  # @line L4
    return (a0, a1, a2, a3, a4, a5)  # @line L5


def quintic_eval(a, t, order=3):
    """Return the list [q, q', q'', ...] of the first `order` + 1 derivatives at t."""
    out = []
    coeffs = list(a)
    for _ in range(order + 1):  # @line L6
        val = 0
        for c in reversed(coeffs):  # Horner's rule
            val = val * t + c
        out.append(val)
        coeffs = [i * coeffs[i] for i in range(1, len(coeffs))] or [0]
    return out


def rest_to_rest(q0, q1, T, t):
    """The quintic with zero end velocities and accelerations: q0 + (q1 - q0) s(t / T)."""
    tau = t / T
    s = tau ** 3 * (10 - 15 * tau + 6 * tau ** 2)  # @line L7
    return q0 + (q1 - q0) * s
