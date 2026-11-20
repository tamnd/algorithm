# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-strength-exchange/. The authors are listed in prov/0HQEAM.jsonl.
"""Particle strength exchange (PSE) for the diffusion term nu * Laplacian(omega) in 2D.

Particle p at x_p has volume V_p and vorticity omega_p (circulation V_p omega_p).
The Laplacian is replaced by the integral operator

    L_eps omega(x) = (1 / eps^2) * integral (omega(y) - omega(x)) eta_eps(y - x) dy,

with eta(x) = (4 / pi) exp(-|x|^2), whose second moments are 2, and
eta_eps(x) = eta(x / eps) / eps^2. The integral is a sum over the particles:

    d omega_p / dt = (nu / eps^2) * sum_q V_q (omega_q - omega_p) eta_eps(x_q - x_p).

Each pair adds to p what it takes from q, weighted by the volumes, so the total
circulation sum_p V_p omega_p does not change.

Cost: Theta(P) time per step for P interacting pairs (Theta(N) with a cutoff
and a cell list, Theta(N^2) for all pairs).
"""

import math


def eta(r2: float) -> float:
    """The kernel eta at |x|^2 = r2."""
    return 4 / math.pi * math.exp(-r2)


def exchange_pairs(xs: list[float], ys: list[float], nu: float, eps: float, cutoff: float = 5.0):
    """(p, q, w) for p < q within cutoff * eps, with w = (nu / eps^2) eta_eps(x_p - x_q)."""
    pairs = []
    c2 = (cutoff * eps) ** 2
    for p in range(len(xs)):  # @line L1
        for q in range(p + 1, len(xs)):  # @line L1
            r2 = (xs[p] - xs[q]) ** 2 + (ys[p] - ys[q]) ** 2
            if r2 < c2:  # @line L1
                pairs.append((p, q, nu / eps ** 2 * eta(r2 / eps ** 2) / eps ** 2))  # @line L2
    return pairs


def exchange_rates(omega: list[float], vol: list[float], pairs) -> list[float]:
    """d omega_p / dt for every particle."""
    rate = [0.0] * len(omega)
    for p, q, w in pairs:
        d = w * (omega[q] - omega[p])  # @line L3
        rate[p] += vol[q] * d  # @line L4
        rate[q] -= vol[p] * d  # @line L4
    return rate


def pse_step(omega: list[float], vol: list[float], pairs, h: float) -> list[float]:
    """One explicit Euler step of the exchange."""
    rate = exchange_rates(omega, vol, pairs)
    return [o + h * r for o, r in zip(omega, rate)]  # @line L5


def stable_step(vol: list[float], pairs) -> float:
    """The largest h with h * D_p <= 1, D_p = sum_q V_q w_pq; it keeps the maximum principle."""
    d = [0.0] * len(vol)
    for p, q, w in pairs:
        d[p] += vol[q] * w
        d[q] += vol[p] * w
    return 1 / max(d)


def diffuse(omega: list[float], vol: list[float], pairs, time: float) -> list[float]:
    """Diffuse for the given time with equal Euler steps that satisfy h * D_p <= 1."""
    steps = max(1, math.ceil(time / stable_step(vol, pairs)))
    for _ in range(steps):
        omega = pse_step(omega, vol, pairs, time / steps)
    return omega  # @line L6


def lattice(spacing: float, half_width: float):
    """A square lattice on [-half_width, half_width]^2 with particle volumes spacing^2."""
    k = round(half_width / spacing)
    xs = [i * spacing for i in range(-k, k + 1) for _ in range(-k, k + 1)]
    ys = [j * spacing for _ in range(-k, k + 1) for j in range(-k, k + 1)]
    return xs, ys, [spacing * spacing] * len(xs)
