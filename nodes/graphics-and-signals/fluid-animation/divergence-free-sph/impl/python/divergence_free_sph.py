# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divergence-free-sph/. The authors are listed in prov/9VJ2XT.jsonl.
"""Divergence-free SPH (DFSPH) in 2D, after Bender and Koschier (2015).

Each step runs two solvers that share the factor

    alpha_i = rho_i / (|sum_j m_j grad W_ij|^2 + sum_j |m_j grad W_ij|^2).

The density solver uses kappa_i = (rho*_i - rho0) alpha_i / dt^2 with the
predicted density rho*_i = rho_i + dt sum_j m_j (v_i - v_j) . grad W_ij. The
divergence solver uses kappa_i = (D rho_i / Dt) alpha_i / dt. Both apply

    v_i <- v_i - dt sum_j m_j (kappa_i / rho_i + kappa_j / rho_j) grad W_ij.

This file counts only compression (rho* > rho0, D rho / Dt > 0) and has no
warm start; both are choices of this file.
"""

import math

from sph import density, grad_w, neighbor_pairs

GRAVITY = (0.0, -9.81)
ALPHA_EPS = 1e-6


class Neighborhood:
    """The pairs, their gradients, the densities and the factors alpha_i."""

    def __init__(self, pos, masses, h):
        self.n = len(pos)
        self.pairs = neighbor_pairs(pos, 2.0 * h)
        self.grads = [grad_w((pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]), h) for i, j in self.pairs]
        self.rho = density(pos, masses, h)
        self.m = masses
        self.alpha = alpha_factors(self)


def alpha_factors(nb):
    """alpha_i = rho_i / (|sum_j m_j grad W_ij|^2 + sum_j |m_j grad W_ij|^2), denominator at least 1e-6."""
    sx = [0.0] * nb.n
    sy = [0.0] * nb.n
    sq = [0.0] * nb.n
    m = nb.m
    for (i, j), (gx, gy) in zip(nb.pairs, nb.grads):
        sx[i] += m[j] * gx
        sy[i] += m[j] * gy
        sx[j] -= m[i] * gx
        sy[j] -= m[i] * gy
        g2 = gx * gx + gy * gy
        sq[i] += m[j] * m[j] * g2
        sq[j] += m[i] * m[i] * g2
    return [nb.rho[i] / max(sx[i] ** 2 + sy[i] ** 2 + sq[i], ALPHA_EPS) for i in range(nb.n)]


def density_rate(nb, vel):
    """D rho_i / Dt = sum_j m_j (v_i - v_j) . grad W_ij."""
    out = [0.0] * nb.n
    m = nb.m
    for (i, j), (gx, gy) in zip(nb.pairs, nb.grads):
        d = (vel[i][0] - vel[j][0]) * gx + (vel[i][1] - vel[j][1]) * gy
        out[i] += m[j] * d
        out[j] += m[i] * d
    return out


def apply_kappa(nb, vel, kappa, dt):
    """v_i <- v_i - dt sum_j m_j (kappa_i / rho_i + kappa_j / rho_j) grad W_ij."""
    vx = [v[0] for v in vel]
    vy = [v[1] for v in vel]
    rho, m = nb.rho, nb.m
    for (i, j), (gx, gy) in zip(nb.pairs, nb.grads):
        s = kappa[i] / rho[i] + kappa[j] / rho[j]
        vx[i] -= dt * m[j] * s * gx
        vy[i] -= dt * m[j] * s * gy
        vx[j] += dt * m[i] * s * gx
        vy[j] += dt * m[i] * s * gy
    return list(zip(vx, vy))


def density_solver(nb, vel, dt, rho0, eta=0.001, min_iter=2, max_iter=100):
    """Make the predicted density at most rho0 on average. Returns (vel, iterations, mean error / rho0)."""
    it = 0
    err = float("inf")
    while it < min_iter or (err > eta * rho0 and it < max_iter):  # @line L3
        rate = density_rate(nb, vel)
        e = [max(nb.rho[i] + dt * rate[i] - rho0, 0.0) for i in range(nb.n)]  # @line L4
        err = sum(e) / nb.n
        kappa = [e[i] * nb.alpha[i] / (dt * dt) for i in range(nb.n)]  # @line L5
        vel = apply_kappa(nb, vel, kappa, dt)  # @line L6
        it += 1
    return vel, it, err / rho0


def divergence_solver(nb, vel, dt, rho0, eta_v=0.001, min_iter=1, max_iter=100):
    """Make the positive density rate small. Returns (vel, iterations, mean dt rate / rho0)."""
    it = 0
    err = float("inf")
    while it < min_iter or (err > eta_v * rho0 and it < max_iter):  # @line L9
        rate = [max(r, 0.0) for r in density_rate(nb, vel)]  # @line L10
        err = dt * sum(rate) / nb.n
        kappa = [rate[i] * nb.alpha[i] / dt for i in range(nb.n)]  # @line L11
        vel = apply_kappa(nb, vel, kappa, dt)  # @line L12
        it += 1
    return vel, it, err / rho0


def clamp_box(pos, vel, box):
    x0, y0, x1, y1 = box
    out_p, out_v = [], []
    for (x, y), (u, v) in zip(pos, vel):
        if x < x0 or x > x1:
            x, u = min(max(x, x0), x1), 0.0
        if y < y0 or y > y1:
            y, v = min(max(y, y0), y1), 0.0
        out_p.append((x, y))
        out_v.append((u, v))
    return out_p, out_v


def step(pos, vel, masses, dt, h, rho0, gravity=GRAVITY, eta=0.001, eta_v=0.001,
         max_iter=100, box=None):
    """One DFSPH step. Returns (pos, vel, (density iterations, density error, divergence iterations, divergence error))."""
    nb = Neighborhood(pos, masses, h)  # @line L1
    vel = [(v[0] + dt * gravity[0], v[1] + dt * gravity[1]) for v in vel]  # @line L2
    vel, it_d, err_d = density_solver(nb, vel, dt, rho0, eta, 2, max_iter)
    pos = [(pos[i][0] + dt * vel[i][0], pos[i][1] + dt * vel[i][1]) for i in range(nb.n)]  # @line L7
    if box is not None:
        pos, vel = clamp_box(pos, vel, box)
    nb = Neighborhood(pos, masses, h)  # @line L8
    vel, it_v, err_v = divergence_solver(nb, vel, dt, rho0, eta_v, 1, max_iter)
    return pos, vel, (it_d, err_d, it_v, err_v)  # @line L13


def cfl_step(dx, v_max, lam=0.4, dt_max=0.005):
    """dt = min(lam dx / v_max, dt_max)."""
    if v_max <= 0.0:
        return dt_max
    return min(lam * dx / v_max, dt_max)


def momentum(vel, masses):
    return (sum(m * v[0] for m, v in zip(masses, vel)), sum(m * v[1] for m, v in zip(masses, vel)))


def angular_momentum(pos, vel, masses):
    return sum(m * (x[0] * v[1] - x[1] * v[0]) for m, x, v in zip(masses, pos, vel))


def mean_compression(pos, masses, h, rho0):
    rho = density(pos, masses, h)
    return sum(max(r - rho0, 0.0) for r in rho) / (rho0 * len(rho))


def max_speed(vel):
    return max((math.hypot(v[0], v[1]) for v in vel), default=0.0)
