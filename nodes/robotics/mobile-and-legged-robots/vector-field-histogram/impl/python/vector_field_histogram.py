# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-field-histogram/. The authors are listed in prov/Z398RM.jsonl.

"""The vector field histogram (Borenstein and Koren 1991).

The world is a histogram grid: a dict from a cell (i, j) to a certainty value c >= 0.
Cell (i, j) covers [i*cell, (i+1)*cell) x [j*cell, (j+1)*cell). The robot sits at a
point (x, y). Angles are in degrees, counterclockwise from the +x axis, in [0, 360).

One step:
  1. polar_histogram: each cell of the ws x ws window around the robot adds
     c^2 (a - b d) to the sector of its direction (eqs. 1 to 4 of the paper);
  2. smooth: a triangular moving average over 2l + 1 sectors (eq. 5);
  3. steer: threshold the smoothed histogram, pick the valley of free sectors
     closest to the target, and steer into it (Section 4.2);
  4. speed: slow down for obstacles ahead and for sharp turns (eqs. 8 to 10).
"""

import math


def polar_histogram(grid, x, y, ws=33, n=72, cell=0.1, b=1.0):
    """The polar obstacle density h[0..n-1] of the window around (x, y).

    a is chosen with a - b d_max = 0, where d_max = sqrt(2) (ws - 1) / 2 cells, so the
    farthest cell of the window adds 0. Cells farther than d_max add nothing.
    """
    alpha = 360.0 / n
    half = (ws - 1) // 2
    i0, j0 = math.floor(x / cell), math.floor(y / cell)
    d_max = math.sqrt(2.0) * half * cell
    a = b * d_max
    h = [0.0] * n  # @line L1
    for i in range(i0 - half, i0 + half + 1):
        for j in range(j0 - half, j0 + half + 1):
            c = grid.get((i, j), 0.0)
            if c <= 0.0:
                continue
            dx, dy = (i + 0.5) * cell - x, (j + 0.5) * cell - y  # @line L2
            d = math.hypot(dx, dy)
            if d == 0.0:
                continue
            beta = math.degrees(math.atan2(dy, dx)) % 360.0
            k = int((beta + 1e-9) / alpha) % n
            h[k] += c * c * max(0.0, a - b * d)  # @line L2
    return h


def smooth(h, l=5):
    """Triangular average: weight l + 1 - |j| on sector k + j for |j| <= l, divided by the weight sum."""
    n = len(h)
    total = float((l + 1) * (l + 1))
    return [sum((l + 1 - abs(j)) * h[(k + j) % n] for j in range(-l, l + 1)) / total for k in range(n)]  # @line L3


def circ(a, b, n):
    """Steps from sector a to sector b going counterclockwise."""
    return (b - a) % n


def valleys(free):
    """Maximal runs of free sectors as (start, length), start being the clockwise end."""
    n = len(free)
    if all(free):
        return [(0, n)]
    out = []
    for k in range(n):
        if free[k] and not free[(k - 1) % n]:
            m = 0
            while free[(k + m) % n]:
                m += 1
            out.append((k, m))
    return out


def steer(hs, target_deg, threshold, s_max=18):
    """The steering direction in degrees, or None if every sector is above the threshold."""
    n = len(hs)
    alpha = 360.0 / n
    free = [v < threshold for v in hs]  # @line L4
    kt = int((target_deg % 360.0) / alpha) % n
    if not any(free):  # @line L5
        return None
    if all(free):
        return (kt + 0.5) * alpha
    best = None
    for start, length in valleys(free):  # @line L6
        off = circ(start, kt, n)
        if off < length:
            gap = 0
        else:
            gap = min(circ(kt, start, n), off - (length - 1))
        if best is None or gap < best[0]:
            best = (gap, start, length)
    _, start, length = best
    if length > s_max:  # @line L7
        lo, hi = s_max / 2.0, length - 1 - s_max / 2.0
        off = circ(start, kt, n)
        if off >= length:
            # The target is outside: k_n is the nearer border, k_f = k_n +- s_max.
            off = lo if circ(kt, start, n) <= off - (length - 1) else hi
        theta = start + min(hi, max(lo, off))
    else:
        theta = start + (length - 1) / 2.0  # @line L7
    return ((theta + 0.5) * alpha) % 360.0


def speed(h_c, omega, v_max, h_m, omega_max, v_min):
    """Eqs. 8 to 10: slow down for density h_c ahead and for the turn rate omega."""
    v1 = v_max * (1.0 - min(h_c, h_m) / h_m)  # @line L8
    return v1 * (1.0 - min(abs(omega), omega_max) / omega_max) + v_min  # @line L8


def angle_diff(a, b):
    """The signed difference a - b of two angles in degrees, in (-180, 180]."""
    d = (a - b) % 360.0
    return d - 360.0 if d > 180.0 else d


def run(grid, start, heading, target, threshold, steps=400, dt=0.16, v_max=0.6, omega_max=120.0,
        v_min=0.04, h_m=None, ws=33, cell=0.1, l=5, s_max=18, tol=0.2, record=None):
    """Simulate a point robot that turns at most omega_max deg/s and moves at the VFH speed.

    Returns (x, y, heading, steps, reached).
    """
    x, y = start
    if h_m is None:
        h_m = threshold
    n = 72
    alpha = 360.0 / n
    for k in range(steps):
        if math.hypot(target[0] - x, target[1] - y) < tol:
            return x, y, heading, k, True
        hs = smooth(polar_histogram(grid, x, y, ws, n, cell), l)
        tdeg = math.degrees(math.atan2(target[1] - y, target[0] - x))
        theta = steer(hs, tdeg, threshold, s_max)
        if theta is None:
            return x, y, heading, k, False
        turn = max(-omega_max * dt, min(omega_max * dt, angle_diff(theta, heading)))
        heading = (heading + turn) % 360.0
        h_c = hs[int(heading / alpha) % n]
        v = speed(h_c, turn / dt, v_max, h_m, omega_max, v_min)
        x += v * dt * math.cos(math.radians(heading))
        y += v * dt * math.sin(math.radians(heading))
        if record is not None:
            record(x, y, heading, theta, v)
    return x, y, heading, steps, False
