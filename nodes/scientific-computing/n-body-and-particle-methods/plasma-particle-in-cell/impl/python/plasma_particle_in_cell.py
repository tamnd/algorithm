# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plasma-particle-in-cell/. The authors are listed in prov/ZFSET4.jsonl.
"""A 1D electrostatic particle-in-cell (PIC) code in the style of ES1.

Normalized units: epsilon_0 = 1, the electrons have charge -1 per unit
density and q/m = -1, and the ions are a fixed uniform background of
density 1. Then the plasma frequency is omega_p = 1 and the Debye length is
lambda_D = v_th, the thermal speed.

The domain is the periodic interval [0, L) with M grid points, dx = L / M.
N simulation particles ("macro-particles") each carry the charge q_p = -L / N
and the mass m_p = L / N, so that their mean density is 1.

Each step: deposit charge with cloud-in-cell weights, solve Gauss's law
dE/dx = rho on the grid, interpolate E to the particles with the same weights,
and push the particles with the leapfrog. Velocities live at half steps.

Cost per step: Theta(N + M) time and Theta(M) extra space.
"""

import math
from typing import Sequence


def deposit(xs: Sequence[float], qp: float, m: int, length: float, background: float = 1.0) -> list[float]:
    """Net charge density on the grid: particle charge by CIC plus the uniform ion background."""
    dx = length / m
    rho = [background] * m
    for x in xs:
        s = x / dx
        j = math.floor(s)
        w = s - j
        rho[j % m] += qp * (1 - w) / dx
        rho[(j + 1) % m] += qp * w / dx
    return rho


def gauss_field(rho: Sequence[float], length: float) -> list[float]:
    """Grid field with E_{j+1/2} - E_{j-1/2} = dx rho_j, zero mean, E_j = (E_{j-1/2} + E_{j+1/2}) / 2.

    This equals -(phi_{j+1} - phi_{j-1}) / (2 dx) for the mean-free solution of
    the 3-point Poisson equation -(phi_{j+1} - 2 phi_j + phi_{j-1}) / dx^2 = rho_j - mean(rho).
    """
    m = len(rho)
    dx = length / m
    mean = sum(rho) / m
    half, acc = [], 0.0
    for r in rho:
        acc += dx * (r - mean)
        half.append(acc)  # half[j] = E_{j+1/2} up to a constant
    shift = sum(half) / m
    half = [e - shift for e in half]
    return [(half[j] + half[j - 1]) / 2 for j in range(m)]


def interpolate(field: Sequence[float], xs: Sequence[float], length: float) -> list[float]:
    m = len(field)
    dx = length / m
    out = []
    for x in xs:
        s = x / dx
        j = math.floor(s)
        w = s - j
        out.append((1 - w) * field[j % m] + w * field[(j + 1) % m])
    return out


def field_energy(e: Sequence[float], length: float) -> float:
    return 0.5 * sum(v * v for v in e) * length / len(e)


def pic_run(
    xs: Sequence[float], vs: Sequence[float], m: int, length: float, h: float, steps: int, qm: float = -1.0
) -> tuple[list[float], list[float], list[float]]:
    """Run the PIC loop from positions x(0) and velocities v(0).

    Returns (x_steps, v_{steps-1/2}, W) where W[n] is the field energy at step n,
    n = 0, ..., steps.
    """
    n = len(xs)
    qp = -length / n  # electrons of mean density 1
    x = [p % length for p in xs]
    rho = deposit(x, qp, m, length)  # @line L1
    e = gauss_field(rho, length)  # @line L2
    ep = interpolate(e, x, length)  # @line L3
    v = [u - 0.5 * h * qm * a for u, a in zip(vs, ep)]  # @line L4
    energies = [field_energy(e, length)]
    for _ in range(steps):  # @line L5
        v = [u + h * qm * a for u, a in zip(v, ep)]  # @line L6
        x = [(p + h * u) % length for p, u in zip(x, v)]  # @line L7
        rho = deposit(x, qp, m, length)  # @line L8
        e = gauss_field(rho, length)  # @line L9
        ep = interpolate(e, x, length)  # @line L10
        energies.append(field_energy(e, length))  # @line L11
    return x, v, energies  # @line L12
