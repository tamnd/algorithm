# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-moveout-correction/. The authors are listed in prov/3TP2T7.jsonl.
"""Normal moveout (NMO) correction of the traces of a common-midpoint gather.

A trace is a list of samples d[k] at the two-way times k * dt, k = 0..n-1.
The offset x is in m and the velocity in m/s. The output sample j at the
zero-offset time t0 = j * dt takes the input value at the time
t = sqrt(t0^2 + x^2 / v(t0)^2), found by linear interpolation.
"""

import math


def nmo_time(t0, x, v):
    """The hyperbolic traveltime t = sqrt(t0^2 + x^2 / v^2)."""
    return math.sqrt(t0 * t0 + (x / v) ** 2)


def stretch_factor(t0, x, v):
    """The NMO stretch t / t0 for a constant velocity: an interval dt at time t becomes (t / t0) dt."""
    return nmo_time(t0, x, v) / t0


def interp_linear(trace, dt, t):
    """Linear interpolation of the trace at time t; 0 outside [0, (n - 1) dt]."""
    n = len(trace)
    u = t / dt
    if u < 0.0 or u > n - 1:
        return 0.0
    k = min(int(math.floor(u)), n - 2) if n > 1 else 0
    if n == 1:
        return trace[0] if u == 0.0 else 0.0
    f = u - k
    return (1.0 - f) * trace[k] + f * trace[k + 1]


def _velocity_at(vel, j):
    return vel[j] if isinstance(vel, (list, tuple)) else vel


def nmo_correct(trace, dt, x, vel, stretch_max=None):
    """NMO-correct one trace recorded at offset x.

    vel is a constant or a list with v(t0) for every output sample. If
    stretch_max is given, output samples with (t - t0) / t0 > stretch_max are
    muted (set to 0), and so is t0 = 0 for x != 0. Returns (out, live), where
    live[j] is 1 for a sample that was not muted and 0 otherwise.
    """
    n = len(trace)
    out = [0.0] * n
    live = [0] * n
    for j in range(n):  # @line L1
        t0 = j * dt  # @line L2
        t = nmo_time(t0, x, _velocity_at(vel, j))  # @line L3
        if stretch_max is not None and (t - t0) > stretch_max * t0:  # @line L4
            continue
        out[j] = interp_linear(trace, dt, t)  # @line L5
        live[j] = 1
    return out, live  # @line L6


def nmo_gather(gather, offsets, dt, vel, stretch_max=None):
    """NMO-correct every trace of a gather. Returns the list of corrected traces."""
    return [nmo_correct(tr, dt, x, vel, stretch_max)[0] for tr, x in zip(gather, offsets)]


def one_layer_traveltime(z, x, v):
    """The exact two-way time from a flat reflector at depth z under a constant velocity v.

    The source and the receiver are at the surface, x apart, and the ray
    reflects halfway between them (image-source construction).
    """
    return 2.0 * math.sqrt(z * z + (x / 2.0) ** 2) / v
