# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcisph/. The authors are listed in prov/Y0N4QC.jsonl.
"""Predictive-corrective incompressible SPH (PCISPH) in 2D.

The step follows Algorithm 2 of Solenthaler and Pajarola (2009). All particles
have the same mass m. The pressure starts at 0 and is corrected in a loop:
predict the velocities and positions with the current pressure force, predict
the densities, and add delta times the predicted density error to the
pressure. The loop runs at least min_iter times and stops when the largest
predicted compression is below eta * rho0.

delta comes from a prototype particle with a full neighborhood on a square
lattice (Section 2.3 of the paper):

    delta = 1 / (beta (|sum_j grad W_ij|^2 + sum_j |grad W_ij|^2)),
    beta = 2 (dt m / rho0)^2.

The pressure force uses rho0 in place of rho_i and rho_j, as in the
derivation of delta, and the gradients at the start of the step. The neighbor
pairs of the start of the step are reused in the loop (Section 2.4.1).
The page clamps the pressure at 0, so the free surface does not pull.
"""

import math

from sph import grad_w, neighbor_pairs, w_cubic

GRAVITY = (0.0, -9.81)


def prototype_delta(dx, h, m, rho0, dt):
    """delta of the paper for a particle in a full square lattice of spacing dx."""
    k = int(math.ceil(2.0 * h / dx)) + 1
    sx = sy = 0.0
    ss = 0.0
    for a in range(-k, k + 1):
        for b in range(-k, k + 1):
            if a == 0 and b == 0:
                continue
            g = grad_w((-a * dx, -b * dx), h)
            sx += g[0]
            sy += g[1]
            ss += g[0] * g[0] + g[1] * g[1]
    beta = 2.0 * (dt * m / rho0) ** 2
    return 1.0 / (beta * (sx * sx + sy * sy + ss))


def clamp_box(x, y, box):
    if box is None:
        return x, y
    x0, y0, x1, y1 = box
    return min(max(x, x0), x1), min(max(y, y0), y1)


def pressure_accelerations(grads, pairs, p, m, rho0, n):
    """a^p_i = -m sum_j (p_i + p_j) / rho0^2 grad W_ij, pair by pair."""
    ax = [0.0] * n
    ay = [0.0] * n
    c = m / (rho0 * rho0)
    for (i, j), (gx, gy) in zip(pairs, grads):
        s = c * (p[i] + p[j])
        ax[i] -= s * gx
        ay[i] -= s * gy
        ax[j] += s * gx
        ay[j] += s * gy
    return ax, ay


def step(pos, vel, m, dt, h, rho0, delta, gravity=GRAVITY, eta=0.01,
         min_iter=3, max_iter=50, box=None):
    """One PCISPH step. Returns (pos, vel, info) with info = (iterations, error)."""
    n = len(pos)
    pairs = neighbor_pairs(pos, 2.0 * h)  # @line L1
    grads = [grad_w((pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]), h) for i, j in pairs]
    fx = [gravity[0]] * n  # @line L2
    fy = [gravity[1]] * n
    p = [0.0] * n  # @line L3
    apx = [0.0] * n
    apy = [0.0] * n
    w0 = w_cubic(0.0, h)
    it = 0
    err = float("inf")
    xs = pos
    while it < min_iter or (err > eta * rho0 and it < max_iter):  # @line L4
        vs = [(vel[i][0] + dt * (fx[i] + apx[i]), vel[i][1] + dt * (fy[i] + apy[i])) for i in range(n)]  # @line L5
        xs = [clamp_box(pos[i][0] + dt * vs[i][0], pos[i][1] + dt * vs[i][1], box) for i in range(n)]  # @line L6
        rho = [m * w0] * n  # @line L7
        for i, j in pairs:
            w = w_cubic(math.hypot(xs[i][0] - xs[j][0], xs[i][1] - xs[j][1]), h)
            rho[i] += m * w
            rho[j] += m * w
        err = 0.0
        for i in range(n):
            e = rho[i] - rho0  # @line L8
            err = max(err, e)
            p[i] = max(0.0, p[i] + delta * e)  # @line L9
        apx, apy = pressure_accelerations(grads, pairs, p, m, rho0, n)  # @line L10
        it += 1
    vel = [(vel[i][0] + dt * (fx[i] + apx[i]), vel[i][1] + dt * (fy[i] + apy[i])) for i in range(n)]  # @line L11
    new = []
    out_v = []
    for i in range(n):
        x, y = clamp_box(pos[i][0] + dt * vel[i][0], pos[i][1] + dt * vel[i][1], box)  # @line L12
        u, v = vel[i]
        if box is not None:
            if x != pos[i][0] + dt * u:
                u = 0.0
            if y != pos[i][1] + dt * v:
                v = 0.0
        new.append((x, y))
        out_v.append((u, v))
    return new, out_v, (it, max(err, 0.0) / rho0)


def momentum(vel, m):
    return (m * sum(v[0] for v in vel), m * sum(v[1] for v in vel))


def angular_momentum(pos, vel, m):
    return m * sum(x[0] * v[1] - x[1] * v[0] for x, v in zip(pos, vel))
