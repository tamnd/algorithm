# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-midpoint-stacking/. The authors are listed in prov/RJJQ5H.jsonl.
"""Common-midpoint (CMP) stacking.

A trace is a tuple (s, g, samples): the source and receiver positions along
the line in m, and the samples at two-way times k * dt. The traces are
grouped by midpoint (s + g) / 2, NMO-corrected with the offset |g - s| and
a velocity v(t0), muted where the NMO stretch is too large, and summed. The
sum is divided by the live fold, the number of unmuted traces at each sample.
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


def _nmo(trace, dt, x, vel, stretch_max):
    """NMO correction with a stretch mute. Returns (samples, live flags).

    A sample is not live when it is muted or when its input time falls after
    the end of the record.
    """
    out, live = [0.0] * len(trace), [0] * len(trace)
    tmax = (len(trace) - 1) * dt
    for j in range(len(trace)):
        t0 = j * dt
        v = vel[j] if isinstance(vel, (list, tuple)) else vel
        t = math.sqrt(t0 * t0 + (x / v) ** 2)
        if stretch_max is not None and (t - t0) > stretch_max * t0:
            continue
        if t > tmax * (1.0 + 1e-12):
            continue
        out[j] = _interp(trace, dt, t)
        live[j] = 1
    return out, live


def midpoint_bin(s, g, bin_width, origin=0.0):
    """The index of the midpoint bin of a trace: round(((s + g) / 2 - origin) / bin_width)."""
    return int(round(((s + g) / 2.0 - origin) / bin_width))


def sort_by_midpoint(traces, bin_width, origin=0.0):
    """Group traces into CMP bins: a dict from bin index to a list of (offset, samples)."""
    bins = {}
    for s, g, samples in traces:
        b = midpoint_bin(s, g, bin_width, origin)
        bins.setdefault(b, []).append((abs(g - s), samples))
    return bins


def stack_gather(gather, dt, vel, stretch_max=None):
    """NMO-correct and stack one CMP gather given as a list of (offset, samples).

    Returns (stack, fold), where fold[j] is the number of live traces at
    sample j and stack[j] is their mean (0 where fold[j] = 0).
    """
    n = len(gather[0][1])
    total = [0.0] * n  # @line L3
    fold = [0] * n
    for x, samples in gather:  # @line L4
        c, live = _nmo(samples, dt, x, vel, stretch_max)  # @line L5
        for j in range(n):  # @line L6
            if live[j]:
                total[j] += c[j]
                fold[j] += 1
    stack = [total[j] / fold[j] if fold[j] > 0 else 0.0 for j in range(n)]  # @line L7
    return stack, fold


def cmp_stack(traces, dt, vel, bin_width, origin=0.0, stretch_max=None):
    """Stack a whole line. Returns a dict from bin index to (stack, fold).

    vel is a constant, a list v(t0) used for every bin, or a dict from bin
    index to such a constant or list.
    """
    bins = sort_by_midpoint(traces, bin_width, origin)  # @line L1
    out = {}
    for b in sorted(bins):  # @line L2
        v = vel[b] if isinstance(vel, dict) else vel
        out[b] = stack_gather(bins[b], dt, v, stretch_max)
    return out  # @line L8


def nominal_fold(n_receivers, receiver_spacing, shot_spacing):
    """The full fold n_r dg / (2 ds) of a 2D line with a fixed spread rolled along by ds."""
    return n_receivers * receiver_spacing / (2.0 * shot_spacing)
