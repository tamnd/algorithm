# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topp-reachability-analysis/. The authors are listed in prov/HBHW2D.jsonl.
"""Time-optimal path parameterization by reachability analysis (TOPP-RA).

The path parameter s runs over the grid s_0 < s_1 < ... < s_N. At the grid
point s_i the state is x_i = s'^2 and the control is u_i = s'', held
constant on [s_i, s_(i+1)], so that x_(i+1) = x_i + 2 Delta_i u_i. The
constraints at s_i are rows (a, b, c, lo, hi) that mean

    lo <= a u + b x + c <= hi,

with lo = -inf or hi = +inf allowed. Joint velocity, joint acceleration and
joint torque limits along a path all have this form.

toppra(grid, rows, x_start, x_end) runs the backward pass (controllable
sets K_i, two small LPs per grid point) and the greedy forward pass. Each
LP has two variables (u, x); it is solved exactly by eliminating u
(Fourier-Motzkin), which costs O(m^2) for m rows. The whole algorithm costs
O(N m^2) arithmetic operations and O(N) memory for the sets and the
profile.

Helpers build the rows for one axis with velocity and acceleration limits
and for a planar 2R arm with torque limits along a straight joint path.
"""

import math

INF = math.inf
TOL = 1e-12


def _halfplanes(rows, x_lo=None):
    """Turn rows (a, b, c, lo, hi) into half-planes alpha u + beta x <= gamma."""
    out = []
    for a, b, c, lo, hi in rows:
        if hi < INF:
            out.append((a, b, hi - c))
        if lo > -INF:
            out.append((-a, -b, c - lo))
    out.append((0.0, -1.0, 0.0))  # x >= 0
    return out


def _x_interval(planes):
    """Return the projection [xmin, xmax] of a polygon in (u, x) on the x axis.

    The polygon is the set of alpha u + beta x <= gamma. Eliminating u
    (Fourier-Motzkin) leaves rows c x <= d. Return None if it is empty.
    """
    ups = [p for p in planes if p[0] > 0.0]
    downs = [p for p in planes if p[0] < 0.0]
    rows = [(p[1], p[2]) for p in planes if p[0] == 0.0]
    for ai, bi, gi in ups:
        for aj, bj, gj in downs:
            rows.append((-aj * bi + ai * bj, -aj * gi + ai * gj))
    lo, hi = -INF, INF
    for c, d in rows:
        scale = max(abs(c), abs(d), 1.0)
        if abs(c) <= TOL * scale:
            if d < -TOL * scale:
                return None
        elif c > 0.0:
            hi = min(hi, d / c)
        else:
            lo = max(lo, d / c)
    if lo > hi + TOL * max(1.0, abs(hi)):
        return None
    return (lo + 0.0, max(lo, hi) + 0.0)  # + 0.0 turns -0.0 into 0.0


def one_step_set(rows, delta, k_next):
    """Controllable set K_i: the x with some admissible u that lands in k_next."""
    planes = _halfplanes(rows)
    lo_next, hi_next = k_next
    planes.append((2.0 * delta, 1.0, hi_next))  # x + 2 delta u <= hi_next
    planes.append((-2.0 * delta, -1.0, -lo_next))  # x + 2 delta u >= lo_next
    return _x_interval(planes)


def greedy_control(rows, delta, x, k_next):
    """Largest u with (u, x) admissible and x + 2 delta u in k_next, or None."""
    u_lo = (k_next[0] - x) / (2.0 * delta)
    u_hi = (k_next[1] - x) / (2.0 * delta)
    for a, b, c, lo, hi in rows:
        r = b * x + c
        if a == 0.0:
            if r > hi + TOL * max(1.0, abs(hi)) or r < lo - TOL * max(1.0, abs(lo)):
                return None
            continue
        b1, b2 = (lo - r) / a, (hi - r) / a
        if a < 0.0:
            b1, b2 = b2, b1
        u_lo, u_hi = max(u_lo, b1), min(u_hi, b2)
    if u_lo > u_hi + TOL * max(1.0, abs(u_hi)):
        return None
    return u_hi


def toppra(grid, rows, x_start=0.0, x_end=0.0):
    """Return (u, x, K) or None if the path cannot be parameterized.

    grid: s_0 < ... < s_N. rows[i]: the constraint rows at s_i (the rows at
    s_N only restrict x_N). u has N entries and x has N + 1 entries. K is
    the list of controllable sets. Cost O(N m^2); memory O(N).
    """
    n = len(grid) - 1
    k = [None] * (n + 1)
    xs_end = _x_interval(_halfplanes(rows[n]))
    if xs_end is None or not (xs_end[0] - TOL <= x_end <= xs_end[1] + TOL):
        return None
    k[n] = (x_end, x_end)  # @line L1
    for i in range(n - 1, -1, -1):  # @line L2
        k[i] = one_step_set(rows[i], grid[i + 1] - grid[i], k[i + 1])  # @line L3
        if k[i] is None:  # @line L4
            return None
    if not (k[0][0] - TOL <= x_start <= k[0][1] + TOL):  # @line L5
        return None
    x = [0.0] * (n + 1)
    u = [0.0] * n
    x[0] = x_start  # @line L6
    for i in range(n):  # @line L7
        delta = grid[i + 1] - grid[i]
        ui = greedy_control(rows[i], delta, x[i], k[i + 1])  # @line L8
        if ui is None:
            return None  # cannot happen in exact arithmetic (Theorem 1)
        u[i] = ui
        x[i + 1] = max(0.0, x[i] + 2.0 * delta * ui)  # @line L9
    x[n] = x_end
    return u, x, k  # @line L10


def traversal_time(grid, x):
    """Time to run the profile when u is constant on each interval.

    On [s_i, s_(i+1)] the speed is sqrt of a linear x, so the time is
    exactly 2 Delta / (sqrt(x_i) + sqrt(x_(i+1))). Infinite if both are 0.
    """
    t = 0.0
    for i in range(len(grid) - 1):
        den = math.sqrt(max(x[i], 0.0)) + math.sqrt(max(x[i + 1], 0.0))
        if den == 0.0:
            return INF
        t += 2.0 * (grid[i + 1] - grid[i]) / den
    return t


def max_violation(rows, u, x):
    """Largest amount by which (u_i, x_i) breaks a row, over all i < N."""
    worst = 0.0
    for i in range(len(u)):
        for a, b, c, lo, hi in rows[i]:
            v = a * u[i] + b * x[i] + c
            worst = max(worst, v - hi, lo - v)
    return worst


# ---------------------------------------------------------------- examples


def uniform_grid(n):
    """n + 1 equally spaced points on [0, 1]."""
    return [i / n for i in range(n + 1)]


def single_axis_rows(grid, dist, vmax, amax):
    """q(s) = dist * s with |q'| <= vmax and |q''| <= amax."""
    rows = []
    for _ in grid:
        r = [(dist, 0.0, 0.0, -amax, amax)]
        if vmax < INF:
            r.append((0.0, dist * dist, 0.0, -INF, vmax * vmax))
        rows.append(r)
    return rows


def arm2r_terms(q, dq):
    """Mass matrix rows times dq and the quadratic velocity term of the 2R arm.

    Links of length 1 with a point mass 1 at each link end, in a horizontal
    plane (no gravity). M = [[3 + 2 c2, 1 + c2], [1 + c2, 1]].
    Return (M dq, C(q, dq) dq).
    """
    c2, s2 = math.cos(q[1]), math.sin(q[1])
    m11, m12, m22 = 3.0 + 2.0 * c2, 1.0 + c2, 1.0
    mdq = [m11 * dq[0] + m12 * dq[1], m12 * dq[0] + m22 * dq[1]]
    cdq = [-s2 * (2.0 * dq[0] * dq[1] + dq[1] * dq[1]), s2 * dq[0] * dq[0]]
    return mdq, cdq


def arm2r_rows(grid, q0, q1, tau_max):
    """Torque rows of the 2R arm along q(s) = q0 + s (q1 - q0).

    tau = M q_s u + (M q_ss + C(q, q_s) q_s) x with q_ss = 0 here.
    """
    dq = [q1[0] - q0[0], q1[1] - q0[1]]
    rows = []
    for s in grid:
        q = [q0[0] + s * dq[0], q0[1] + s * dq[1]]
        a, b = arm2r_terms(q, dq)
        rows.append([(a[j], b[j], 0.0, -tau_max[j], tau_max[j]) for j in range(2)])
    return rows
