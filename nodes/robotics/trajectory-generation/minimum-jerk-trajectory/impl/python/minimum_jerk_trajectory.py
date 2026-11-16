# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-jerk-trajectory/. The authors are listed in prov/V2PYYM.jsonl.
"""Minimum-jerk trajectory.

min_jerk(x0, xf, T, t) is the motion of Flash and Hogan (1985) from rest at
the point x0 to rest at the point xf in time T. Points are lists of
coordinates; each coordinate follows the same scalar profile, so the path is
the straight segment from x0 to xf.

min_jerk_boundary(...) is the minimizer for general end positions,
velocities and accelerations of one coordinate: a quintic polynomial.
jerk_cost(coeffs, T) is the integral of the squared third derivative.
"""


def min_jerk(x0, xf, T, t):
    """Return (x, x', x'') at time t of the rest-to-rest minimum-jerk motion."""
    if T <= 0:
        raise ValueError("T must be positive")
    tau = t / T  # @line L1
    s = tau ** 3 * (10 - 15 * tau + 6 * tau * tau)  # @line L2
    ds = 30 * tau ** 2 * (1 - tau) ** 2 / T  # @line L3
    dds = 60 * tau * (1 - tau) * (1 - 2 * tau) / (T * T)  # @line L4
    d = [b - a for a, b in zip(x0, xf)]
    return ([a + e * s for a, e in zip(x0, d)], [e * ds for e in d], [e * dds for e in d])  # @line L5


def min_jerk_boundary(p0, v0, c0, p1, v1, c1, T):
    """Coefficients (a0, ..., a5) of the minimum-jerk motion with general end states.

    The minimizer is the unique quintic that meets the six end conditions;
    these are the closed form coefficients of that quintic.
    """
    if T <= 0:
        raise ValueError("T must be positive")
    h = p1 - p0
    a3 = (20 * h - (8 * v1 + 12 * v0) * T - (3 * c0 - c1) * T ** 2) / (2 * T ** 3)  # @line L6
    a4 = (-30 * h + (14 * v1 + 16 * v0) * T + (3 * c0 - 2 * c1) * T ** 2) / (2 * T ** 4)
    a5 = (12 * h - 6 * (v1 + v0) * T + (c1 - c0) * T ** 2) / (2 * T ** 5)
    return (p0, v0, c0 / 2, a3, a4, a5)


def poly_eval(a, t, d=0):
    """Value at t of the d-th derivative of the polynomial with coefficients a."""
    c = list(a)
    for _ in range(d):
        c = [i * c[i] for i in range(1, len(c))] or [0]
    v = 0
    for x in reversed(c):
        v = v * t + x
    return v


def jerk_cost(a, T):
    """Integral over [0, T] of the square of the third derivative of the polynomial a."""
    c = list(a)
    for _ in range(3):
        c = [i * c[i] for i in range(1, len(c))] or [0]
    total = 0
    for i, x in enumerate(c):
        for j, y in enumerate(c):
            total += x * y * T ** (i + j + 1) / (i + j + 1)
    return total
