# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-growth-model/. The authors are listed in prov/SN0SST.jsonl.
"""The logistic growth model dN/dt = r N (1 - N / K).

N is the population size (or density), r > 0 is the intrinsic growth rate
per unit of time and K > 0 is the carrying capacity, in the unit of N.
The module gives the closed form solution, a fixed step RK4 integrator,
the time to reach a level, the exact time-h map (a Beverton-Holt map) and
the forward Euler map, which is a logistic map in disguise.
"""

import math


def rate(n: float, r: float, k: float) -> float:
    """The right-hand side r N (1 - N / K)."""
    return r * n * (1.0 - n / k)


def closed_form(n0: float, r: float, k: float, t: float) -> float:
    """N(t) = K N0 / (N0 + (K - N0) e^(-r t)), valid for every N0 >= 0."""
    if n0 == 0.0:
        return 0.0
    return k * n0 / (n0 + (k - n0) * math.exp(-r * t))


def rk4(n0: float, r: float, k: float, dt: float, steps: int) -> float:
    """N after `steps` classical Runge-Kutta steps of size dt from N0."""
    n = n0  # @line L1
    for _ in range(steps):  # @line L2
        k1 = rate(n, r, k)  # @line L3
        k2 = rate(n + dt * k1 / 2.0, r, k)  # @line L4
        k3 = rate(n + dt * k2 / 2.0, r, k)  # @line L5
        k4 = rate(n + dt * k3, r, k)  # @line L6
        n = n + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0  # @line L7
    return n  # @line L8


def time_to_reach(n0: float, n: float, r: float, k: float) -> float:
    """The time at which the solution from N0 reaches N (both on the same side of K)."""
    return math.log(n * (k - n0) / (n0 * (k - n))) / r


def inflection_time(n0: float, r: float, k: float) -> float:
    """The time at which N = K/2, where growth is fastest (needs 0 < N0 < K/2)."""
    return math.log((k - n0) / n0) / r


def exact_step(n: float, r: float, k: float, h: float) -> float:
    """The exact time-h map N -> lambda N / (1 + (lambda - 1) N / K), lambda = e^(r h)."""
    lam = math.exp(r * h)
    return lam * n / (1.0 + (lam - 1.0) * n / k)


def euler_step(n: float, r: float, k: float, h: float) -> float:
    """One forward Euler step N + h r N (1 - N / K)."""
    return n + h * rate(n, r, k)


def harvest_equilibria(r: float, k: float, harvest: float):
    """The equilibria of dN/dt = r N (1 - N/K) - H, as a sorted list (empty if H > r K / 4)."""
    disc = r * r - 4.0 * r * harvest / k
    if disc < 0.0:
        return []
    root = math.sqrt(disc)
    return sorted({k * (r - root) / (2.0 * r), k * (r + root) / (2.0 * r)})
