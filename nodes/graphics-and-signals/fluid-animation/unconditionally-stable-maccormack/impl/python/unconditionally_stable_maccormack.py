# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unconditionally-stable-maccormack/. The authors are listed in prov/5R0MXZ.jsonl.

"""The unconditionally stable MacCormack method of Selle et al. (2008) on a 2D MAC grid.

The basic step A is the semi-Lagrangian advection of the shared helper
macgrid.py (an RK2 backtrace and a bilinear sample), and A^R is the same step
with -dt. The method is

    q_hat = A(q),  q_back = A^R(q_hat),  q_new = q_hat + (q - q_back) / 2,

followed by a limiter that keeps q_new in the range of the four values of q
that A mixed at the same point: "revert" (the paper's choice) uses q_hat
there, and "clamp" clamps to the range. A field q has q[a][b] at
((a + ox) dx, (b + oy) dx), as in macgrid.advect.
"""

import math

import macgrid


def semi_lagrangian(g, q, dt, ox=0.5, oy=0.5):
    """One semi-Lagrangian step of q by the velocity of g. A negative dt runs it backward."""
    return macgrid.advect(g, q, dt, ox, oy)


def stencil(q, x, y, dx, ox, oy):
    """The (up to) four values of q that macgrid.sample mixes at (x, y), with the same clamping."""
    na, nb = len(q), len(q[0])
    fx = min(max(x / dx - ox, 0.0), float(na - 1))
    fy = min(max(y / dx - oy, 0.0), float(nb - 1))
    a0 = min(int(math.floor(fx)), na - 2) if na > 1 else 0
    b0 = min(int(math.floor(fy)), nb - 2) if nb > 1 else 0
    a1 = a0 + 1 if na > 1 else a0
    b1 = b0 + 1 if nb > 1 else b0
    return (q[a0][b0], q[a0][b1], q[a1][b0], q[a1][b1])


def stencil_bounds(g, q, dt, ox=0.5, oy=0.5):
    """For each sample point, the min and the max of the values of q at the foot of its backtrace."""
    dx = g.dx
    lo = macgrid.zeros(len(q), len(q[0]))
    hi = macgrid.zeros(len(q), len(q[0]))
    for a in range(len(q)):
        for b in range(len(q[0])):
            xb, yb = macgrid.backtrace(g, (a + ox) * dx, (b + oy) * dx, dt)
            s = stencil(q, xb, yb, dx, ox, oy)  # @line L4
            lo[a][b], hi[a][b] = min(s), max(s)
    return lo, hi


def maccormack(g, q, dt, ox=0.5, oy=0.5, limiter="revert"):
    """One MacCormack step of q by the velocity of g. limiter is "revert", "clamp" or None. Returns a new field."""
    if limiter not in (None, "clamp", "revert"):
        raise ValueError("limiter must be None, 'clamp' or 'revert'")
    na, nb = len(q), len(q[0])
    fwd = semi_lagrangian(g, q, dt, ox, oy)  # @line L1
    back = semi_lagrangian(g, fwd, -dt, ox, oy)  # @line L2
    new = [[fwd[a][b] + 0.5 * (q[a][b] - back[a][b]) for b in range(nb)] for a in range(na)]  # @line L3
    if limiter is None:
        return new
    lo, hi = stencil_bounds(g, q, dt, ox, oy)
    for a in range(na):
        for b in range(nb):
            t = new[a][b]
            if not lo[a][b] <= t <= hi[a][b]:
                new[a][b] = fwd[a][b] if limiter == "revert" else min(max(t, lo[a][b]), hi[a][b])  # @line L5
    return new


def maccormack_velocity(g, dt, limiter="revert"):
    """The MacCormack step applied to u and to v, both moved by the old velocity. Returns (new_u, new_v)."""
    return maccormack(g, g.u, dt, 0.0, 0.5, limiter), maccormack(g, g.v, dt, 0.5, 0.0, limiter)


def constant_velocity(g, uc, vc):
    """Set every face of g to the constant velocity (uc, vc), walls included (for transport tests)."""
    g.u = [[float(uc)] * g.ny for _ in range(g.nx + 1)]
    g.v = [[float(vc)] * (g.ny + 1) for _ in range(g.nx)]


def rotation_velocity(g, omega, cx, cy):
    """Set u = -omega (y - cy) and v = omega (x - cx) at the face centers: a rigid rotation, divergence free on the MAC grid."""
    dx = g.dx
    g.u = [[-omega * ((j + 0.5) * dx - cy) for j in range(g.ny)] for _ in range(g.nx + 1)]
    g.v = [[omega * ((i + 0.5) * dx - cx) for _ in range(g.ny + 1)] for i in range(g.nx)]


def cell_field(g, f):
    """The cell centered field f(x, y)."""
    dx = g.dx
    return [[f((i + 0.5) * dx, (j + 0.5) * dx) for j in range(g.ny)] for i in range(g.nx)]


def max_error(q, r):
    return max(abs(a - b) for c1, c2 in zip(q, r) for a, b in zip(c1, c2))
