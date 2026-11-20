# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semblance-velocity-analysis/. The authors are listed in prov/8B18AH.jsonl.
"""Semblance velocity analysis of a common-midpoint gather.

The gather is a list of N traces with offsets x_i, sampled at k * dt. For a
zero-offset time index j and a trial velocity v, the samples a_i(k) are read
along the hyperbola t = sqrt((k dt)^2 + x_i^2 / v^2) for k in a window
j - W .. j + W, and the semblance is

    S = sum_k (sum_i a_i(k))^2 / (N sum_k sum_i a_i(k)^2),

a number between 0 and 1 (0 when the window holds no energy).
"""

import math


def _interp(trace, dt, t):
    n = len(trace)
    u = t / dt
    if n < 2 or u < 0.0 or u > n - 1:
        return 0.0
    k = min(int(math.floor(u)), n - 2)
    f = u - k
    return (1.0 - f) * trace[k] + f * trace[k + 1]


def semblance_of_window(rows):
    """S for a window given as rows a[k][i] (time k, trace i)."""
    num = 0.0
    den = 0.0
    n = 0
    for row in rows:
        n = len(row)
        s = sum(row)
        num += s * s
        den += sum(a * a for a in row)
    if den == 0.0:
        return 0.0
    return num / (n * den)


def semblance(gather, offsets, dt, j, v, half_window):
    """The semblance at zero-offset index j and velocity v, window j - W .. j + W."""
    num = 0.0  # @line L3
    den = 0.0
    for k in range(j - half_window, j + half_window + 1):  # @line L4
        t0 = k * dt
        a = [_interp(tr, dt, math.sqrt(t0 * t0 + (x / v) ** 2)) if k >= 0 else 0.0
             for tr, x in zip(gather, offsets)]  # @line L5
        s = sum(a)  # @line L6
        num += s * s
        den += sum(ai * ai for ai in a)
    if den == 0.0:  # @line L7
        return 0.0
    return num / (len(gather) * den)


def velocity_spectrum(gather, offsets, dt, velocities, half_window, times=None):
    """S[j][m] for every zero-offset index j in times (default all) and velocities[m]."""
    n = len(gather[0])
    idx = range(n) if times is None else times
    spec = []
    for j in idx:  # @line L1
        spec.append([semblance(gather, offsets, dt, j, v, half_window) for v in velocities])  # @line L2
    return spec  # @line L8


def pick_velocity(row, velocities):
    """The trial velocity with the largest semblance in one row of the spectrum."""
    m = max(range(len(row)), key=lambda i: row[i])
    return velocities[m]
