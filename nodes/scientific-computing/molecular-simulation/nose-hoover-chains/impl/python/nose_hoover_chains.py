# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nose-hoover-chains/. The authors are listed in prov/KYF8ST.jsonl.
"""Molecular dynamics with a Nose-Hoover chain thermostat.

The equations of Martyna, Klein and Tuckerman (1992) for N particles in d
dimensions, with a chain of M thermostats of masses Q_1, ..., Q_M, are

    dx_i/dt   = v_i,
    dv_i/dt   = f_i / m_i - xi_1 v_i,
    dxi_1/dt  = G_1 - xi_1 xi_2,         G_1 = (2 K - N_f kT) / Q_1,
    dxi_j/dt  = G_j - xi_j xi_(j+1),     G_j = (Q_(j-1) xi_(j-1)^2 - kT) / Q_j,
    dxi_M/dt  = G_M,
    deta_j/dt = xi_j.

The extended energy

    H' = K + U + sum_j Q_j xi_j^2 / 2 + N_f kT eta_1 + kT (eta_2 + ... + eta_M)

is conserved by the exact flow. With M = 1 the chain is the Nose-Hoover
thermostat.

One step of length h is the symmetric splitting of Martyna, Tuckerman,
Tobias and Klein (1996): a half step of the chain, a velocity Verlet step of
the particles, and a second half step of the chain. In the half step of the
chain, each xi_j gets a quarter step kick by G_j between two scalings by
exp(-xi_(j+1) h / 8), from the end of the chain to its start; then the
velocities are scaled by exp(-xi_1 h / 2) and all eta_j move by xi_j h / 2;
then the kicks are repeated from the start of the chain to its end. Each
piece is the exact flow of a part of the equations, so the step is
time-reversible. One Suzuki-Yoshida stage is used (no multiple time steps
inside the chain).

Cost: one force evaluation and Theta(N d + M) extra work per step.
"""

import math
from typing import Callable

Vec = list[float]
ForceField = Callable[[list[Vec]], tuple[float, list[Vec]]]


def harmonic(k: float) -> ForceField:
    """Independent springs U = k |x_i|^2 / 2 for each particle."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        u = sum(0.5 * k * c * c for p in pos for c in p)
        return u, [[-k * c for c in p] for p in pos]
    return field


def kinetic(v: list[Vec], m: list[float]) -> float:
    """The kinetic energy K = sum_i m_i |v_i|^2 / 2."""
    return sum(0.5 * mi * sum(c * c for c in vi) for vi, mi in zip(v, m))


def chain_masses(nf: int, kT: float, tau: float, length: int) -> list[float]:
    """The masses of Martyna et al. (1992): Q_1 = N_f kT tau^2, Q_j = kT tau^2."""
    return [nf * kT * tau * tau] + [kT * tau * tau] * (length - 1)


def _force(j, xi, q, k, kT, nf):
    """G_j: the thermostat force on link j (0-based)."""
    if j == 0:
        return (2.0 * k - nf * kT) / q[0]
    return (q[j - 1] * xi[j - 1] ** 2 - kT) / q[j]


def _kick(j, xi, q, k, kT, nf, h):
    """A quarter step of link j: scale, kick by G_j, scale."""
    mm = len(xi)
    if j == mm - 1:
        xi[j] += 0.25 * h * _force(j, xi, q, k, kT, nf)  # @line L11
        return
    s = math.exp(-0.125 * h * xi[j + 1])  # @line L12
    xi[j] *= s  # @line L13
    xi[j] += 0.25 * h * _force(j, xi, q, k, kT, nf)  # @line L14
    xi[j] *= s  # @line L15


def _chain_half(v, m, xi, eta, q, h, kT, nf):
    """The exact flows of the chain part for a time h / 2."""
    mm = len(xi)
    k = kinetic(v, m)
    for j in range(mm - 1, -1, -1):  # @line L16
        _kick(j, xi, q, k, kT, nf, h)
    s = math.exp(-0.5 * h * xi[0])  # @line L17
    for vi in v:
        for a in range(len(vi)):
            vi[a] *= s
    k *= s * s
    for j in range(mm):
        eta[j] += 0.5 * h * xi[j]  # @line L18
    for j in range(mm):  # @line L19
        _kick(j, xi, q, k, kT, nf, h)


def extended_energy(x, v, m, u, xi, eta, q, kT, nf) -> float:
    """H' = K + U + sum Q_j xi_j^2 / 2 + N_f kT eta_1 + kT sum_(j >= 2) eta_j."""
    e = kinetic(v, m) + u + sum(0.5 * qj * z * z for qj, z in zip(q, xi))
    return e + nf * kT * eta[0] + kT * sum(eta[1:])


def nose_hoover_chains(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, q: list[float], nf: int,
    xi: list[float] | None = None, eta: list[float] | None = None,
) -> tuple[list[Vec], list[Vec], list[float], list[float], list[float]]:
    """Run steps of Nose-Hoover chain dynamics with masses q (the chain length is len(q)).

    Returns the final positions, velocities, xi and eta, and the extended
    energy H' after each step. The inputs are not changed.
    """
    if h <= 0 or not q or min(q) <= 0 or kT <= 0 or nf <= 0:
        raise ValueError("need h > 0, positive masses q, kT > 0 and nf > 0")
    mm = len(q)
    xi = list(xi) if xi is not None else [0.0] * mm
    eta = list(eta) if eta is not None else [0.0] * mm
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    u, f = forces(x)  # @line L1
    energies = []
    for _ in range(steps):  # @line L2
        _chain_half(v, m, xi, eta, q, h, kT, nf)  # @line L3
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L4
                x[i][a] += h * v[i][a]  # @line L5
        u, f = forces(x)  # @line L6
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L7
        _chain_half(v, m, xi, eta, q, h, kT, nf)  # @line L8
        energies.append(extended_energy(x, v, m, u, xi, eta, q, kT, nf))  # @line L9
    return x, v, xi, eta, energies  # @line L10
