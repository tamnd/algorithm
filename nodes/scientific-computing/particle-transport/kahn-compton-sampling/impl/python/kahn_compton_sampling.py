# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kahn-compton-sampling/. The authors are listed in prov/7W42N2.jsonl.
"""Kahn's rejection method for the Klein-Nishina distribution.

A photon of energy E scatters off a free electron at rest. Write
alpha = E / (m c^2) and q = alpha / alpha' = E / E', so that the
Compton formula reads q = 1 + alpha (1 - mu), with mu the cosine of the
scattering angle, and q runs over [1, 1 + 2 alpha]. The Klein-Nishina
cross section, as a density in q, is proportional to

    (1 / q^2) (q + 1/q - 1 + mu^2),   mu = 1 - (q - 1) / alpha.

Kahn's method mixes two easy densities in q (uniform, and the density of
(1 + 2 alpha) / (1 + 2 alpha xi)) with weights (1 + 2 alpha) / (9 + 2 alpha)
and 8 / (9 + 2 alpha), and accepts with a factor at most 1 in each branch.
The accepted q has exactly the Klein-Nishina law. The method uses no
square roots, logarithms or tables.
"""

import math


def kahn_sample(alpha: float, rng):
    """Sample one Compton scattering. Returns (alpha_out, mu, tries)."""
    tries = 0
    p1 = (1.0 + 2.0 * alpha) / (9.0 + 2.0 * alpha)
    while True:  # @line L1
        tries += 1
        r1, r2, r3 = rng.random(), rng.random(), rng.random()  # @line L2
        if r1 <= p1:  # @line L3
            q = 1.0 + 2.0 * alpha * r2  # @line L4
            if r3 <= 4.0 * (1.0 / q - 1.0 / (q * q)):  # @line L5
                break
        else:  # @line L6
            q = (1.0 + 2.0 * alpha) / (1.0 + 2.0 * alpha * r2)  # @line L7
            mu = 1.0 - (q - 1.0) / alpha
            if r3 <= 0.5 * (mu * mu + 1.0 / q):  # @line L8
                break
    mu = 1.0 - (q - 1.0) / alpha
    return alpha / q, mu, tries  # @line L9


def klein_nishina_mu_density(alpha: float, mu: float) -> float:
    """Unnormalized Klein-Nishina density in mu: P^2 (P + 1/P - 1 + mu^2), P = E'/E."""
    p = 1.0 / (1.0 + alpha * (1.0 - mu))
    return p * p * (p + 1.0 / p - 1.0 + mu * mu)


def kahn_efficiency(alpha: float, steps: int = 2000) -> float:
    """Exact probability that one try of Kahn's method is accepted (Simpson's rule in q)."""
    k = 4.0 * (1.0 + 2.0 * alpha) / ((9.0 + 2.0 * alpha) * 2.0 * alpha)
    a, b = 1.0, 1.0 + 2.0 * alpha
    h = (b - a) / steps
    total = 0.0
    for i in range(steps + 1):
        q = a + i * h
        mu = 1.0 - (q - 1.0) / alpha
        f = (q + 1.0 / q - 1.0 + mu * mu) / (q * q)
        total += f * (1 if i in (0, steps) else (4 if i % 2 else 2))
    return k * total * h / 3.0


def scattered_energy(energy_kev: float, mu: float, mc2_kev: float = 510.99895) -> float:
    """Compton formula E' = E / (1 + (E / m c^2)(1 - mu))."""
    return energy_kev / (1.0 + energy_kev / mc2_kev * (1.0 - mu))
