# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-kpp-equation/. The authors are listed in prov/2NM058.jsonl.
"""The Fisher-KPP equation u_t = D u_xx + r u (1 - u) on [0, L].

The solver is the method of lines with second differences in space and
explicit Euler in time, with mirror (no-flux) ends. It reports where the
front crosses u = 1/2, so that the tests can measure the front speed and
compare it with the minimal speed 2 sqrt(r D), with the speed of the
scheme itself, and with the exact wave of speed 5 / sqrt(6).
"""

import math


def minimal_speed(d: float, r: float) -> float:
    """The minimal front speed 2 sqrt(r D)."""
    return 2.0 * math.sqrt(r * d)


def linear_speed(lam: float, d: float, r: float) -> float:
    """The speed D lam + r / lam of the decay exp(-lam (x - c t)) in the linearized equation."""
    return d * lam + r / lam


def exact_wave(z: float) -> float:
    """The exact wave U(z) = (1 + exp(z / sqrt 6))^-2 for D = r = 1, with speed 5 / sqrt 6."""
    return (1.0 + math.exp(z / math.sqrt(6.0))) ** -2


EXACT_SPEED = 5.0 / math.sqrt(6.0)


def front_position(u, dx: float):
    """The first x where u falls through 1/2, by linear interpolation, or None."""
    for i in range(len(u) - 1):
        if u[i] >= 0.5 > u[i + 1]:
            return (i + (u[i] - 0.5) / (u[i] - u[i + 1])) * dx
    return None


def step(u, mu: float, rdt: float):
    """One explicit step; mu = D dt / dx^2 and rdt = r dt. The ends mirror their neighbours."""
    n = len(u)
    v = [0.0] * n
    for i in range(n):  # @line L3
        left = u[i - 1] if i > 0 else u[1]
        right = u[i + 1] if i < n - 1 else u[n - 2]
        ui = u[i]
        v[i] = ui + mu * (left - 2.0 * ui + right) + rdt * ui * (1.0 - ui)  # @line L4
    return v


def simulate(u0, dx: float, dt: float, t_end: float, d: float = 1.0, r: float = 1.0, marks=()):
    """Run to t_end; return the final grid values and the front position at each time in marks."""
    mu = d * dt / dx ** 2  # @line L1
    rdt = r * dt
    at = {int(round(m / dt)): m for m in marks}
    fronts = {}
    u = list(u0)
    for s in range(1, int(round(t_end / dt)) + 1):  # @line L2
        u = step(u, mu, rdt)  # @line L5
        if s in at:
            fronts[at[s]] = front_position(u, dx)  # @line L6
    return u, fronts  # @line L7


def step_start(length: float, dx: float, x0: float = 10.0):
    """u = 1 for x < x0 and u = 0 after it, on the grid 0, dx, ..., length."""
    n = int(round(length / dx)) + 1
    return [1.0 if i * dx < x0 else 0.0 for i in range(n)]


def wave_start(length: float, dx: float, x0: float = 20.0):
    """The exact wave placed with its centre region near x0."""
    n = int(round(length / dx)) + 1
    return [exact_wave(i * dx - x0) for i in range(n)]


def discrete_linear_speed(dx: float, dt: float, d: float = 1.0, r: float = 1.0) -> float:
    """The spreading speed of the linearized scheme: the minimum over lam of ln(g(lam)) / (dt lam).

    A mode exp(-lam x) grows per step by g = 1 + r dt + 2 mu (cosh(lam dx) - 1).
    """
    mu = d * dt / dx ** 2
    best = math.inf
    for i in range(1, 6001):
        lam = i * 0.001
        g = 1.0 + r * dt + 2.0 * mu * (math.cosh(lam * dx) - 1.0)
        best = min(best, math.log(g) / (dt * lam))
    return best
