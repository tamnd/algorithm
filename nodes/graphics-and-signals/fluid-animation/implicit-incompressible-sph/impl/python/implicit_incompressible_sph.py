# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-incompressible-sph/. The authors are listed in prov/V1STXV.jsonl.
"""Implicit incompressible SPH (IISPH) in 2D.

The pressure p solves the discrete pressure Poisson equation A p = s with

    a^p_i = -sum_j m_j (p_i / rho_i^2 + p_j / rho_j^2) grad W_ij,
    (A p)_i = dt^2 sum_j m_j (a^p_i - a^p_j) . grad W_ij,
    s_i = rho0 - rho^adv_i,
    rho^adv_i = rho_i + dt sum_j m_j (v^adv_i - v^adv_j) . grad W_ij,

so that the predicted density rho^adv_i + (A p)_i equals rho0. The solver is
relaxed Jacobi with omega = 0.5 and the diagonal

    a_ii = -(dt^2 / rho_i^2) (|sum_j m_j grad W_ij|^2 + m_i sum_j m_j |grad W_ij|^2),

with each pressure clamped at 0, in the operator form of the tutorial of
Koschier et al. (2019). Ihmsen et al. (2014) write the same system with the
displacement terms d_ii and d_ij. The solve stops when the mean predicted
compression is below eta rho0 and at least min_iter passes have run.
"""

import math

from sph import density, grad_w, neighbor_pairs

GRAVITY = (0.0, -9.81)


class Neighborhood:
    """The pairs, their gradients and the per-particle gradient sums of one step."""

    def __init__(self, pos, masses, h):
        self.n = len(pos)
        self.pairs = neighbor_pairs(pos, 2.0 * h)
        self.grads = [grad_w((pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]), h) for i, j in self.pairs]
        self.rho = density(pos, masses, h)
        self.m = masses


def pressure_acc(nb, p):
    """a^p_i = -sum_j m_j (p_i / rho_i^2 + p_j / rho_j^2) grad W_ij."""
    ax = [0.0] * nb.n
    ay = [0.0] * nb.n
    rho, m = nb.rho, nb.m
    for (i, j), (gx, gy) in zip(nb.pairs, nb.grads):
        s = p[i] / (rho[i] * rho[i]) + p[j] / (rho[j] * rho[j])
        ax[i] -= m[j] * s * gx
        ay[i] -= m[j] * s * gy
        ax[j] += m[i] * s * gx
        ay[j] += m[i] * s * gy
    return ax, ay


def apply_a(nb, p, dt):
    """(A p)_i = dt^2 sum_j m_j (a^p_i - a^p_j) . grad W_ij."""
    ax, ay = pressure_acc(nb, p)
    out = [0.0] * nb.n
    m = nb.m
    for (i, j), (gx, gy) in zip(nb.pairs, nb.grads):
        d = (ax[i] - ax[j]) * gx + (ay[i] - ay[j]) * gy
        out[i] += m[j] * d
        out[j] += m[i] * d  # grad W_ji = -grad W_ij and a_j - a_i = -(a_i - a_j)
    return [dt * dt * t for t in out]


def diagonal(nb, dt):
    """a_ii = -(dt^2 / rho_i^2) (|sum_j m_j grad W_ij|^2 + m_i sum_j m_j |grad W_ij|^2)."""
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
        sq[i] += m[j] * g2
        sq[j] += m[i] * g2
    return [-(dt * dt) / (nb.rho[i] ** 2) * (sx[i] ** 2 + sy[i] ** 2 + m[i] * sq[i]) for i in range(nb.n)]


def source(nb, vel_adv, dt, rho0):
    """s_i = rho0 - rho^adv_i."""
    rho_adv = list(nb.rho)
    m = nb.m
    for (i, j), (gx, gy) in zip(nb.pairs, nb.grads):
        d = (vel_adv[i][0] - vel_adv[j][0]) * gx + (vel_adv[i][1] - vel_adv[j][1]) * gy
        rho_adv[i] += dt * m[j] * d
        rho_adv[j] += dt * m[i] * d
    return [rho0 - r for r in rho_adv]


def relaxed_jacobi(nb, s, diag, dt, rho0, p0, omega=0.5, eta=0.001, min_iter=2,
                   max_iter=100, clamp=True):
    """Solve A p = s by relaxed Jacobi. Returns (p, iterations, mean error / rho0)."""
    p = list(p0)
    it = 0
    err = float("inf")
    while it < min_iter or (err > eta * rho0 and it < max_iter):  # @line L6
        ap = apply_a(nb, p, dt)  # @line L7
        err = 0.0
        for i in range(nb.n):
            if diag[i] != 0.0:
                p[i] = p[i] + omega * (s[i] - ap[i]) / diag[i]  # @line L8
                if clamp and p[i] < 0.0:
                    p[i] = 0.0
            err += max(ap[i] - s[i], 0.0)  # @line L9
        err /= nb.n
        it += 1
    return p, it, err / rho0


def step(pos, vel, masses, dt, h, rho0, p_prev=None, gravity=GRAVITY,
         eta=0.001, min_iter=2, max_iter=100, box=None):
    """One IISPH step. Returns (pos, vel, p, info) with info = (iterations, error)."""
    nb = Neighborhood(pos, masses, h)  # @line L1
    vel_adv = [(v[0] + dt * gravity[0], v[1] + dt * gravity[1]) for v in vel]  # @line L2
    s = source(nb, vel_adv, dt, rho0)  # @line L3
    diag = diagonal(nb, dt)  # @line L4
    p0 = [0.5 * q for q in p_prev] if p_prev is not None else [0.0] * nb.n  # @line L5
    p, it, err = relaxed_jacobi(nb, s, diag, dt, rho0, p0, 0.5, eta, min_iter, max_iter)
    ax, ay = pressure_acc(nb, p)
    vel = [(vel_adv[i][0] + dt * ax[i], vel_adv[i][1] + dt * ay[i]) for i in range(nb.n)]  # @line L10
    new = [(pos[i][0] + dt * vel[i][0], pos[i][1] + dt * vel[i][1]) for i in range(nb.n)]  # @line L11
    if box is not None:
        x0, y0, x1, y1 = box
        for i in range(nb.n):
            x, y = new[i]
            u, v = vel[i]
            if x < x0 or x > x1:
                x, u = min(max(x, x0), x1), 0.0
            if y < y0 or y > y1:
                y, v = min(max(y, y0), y1), 0.0
            new[i] = (x, y)
            vel[i] = (u, v)
    return new, vel, p, (it, err)


def momentum(vel, masses):
    return (sum(m * v[0] for m, v in zip(masses, vel)), sum(m * v[1] for m, v in zip(masses, vel)))


def angular_momentum(pos, vel, masses):
    return sum(m * (x[0] * v[1] - x[1] * v[0]) for m, x, v in zip(masses, pos, vel))


def mean_compression(pos, masses, h, rho0):
    rho = density(pos, masses, h)
    return sum(max(r - rho0, 0.0) for r in rho) / (rho0 * len(rho))


def speed(v):
    return math.hypot(v[0], v[1])
