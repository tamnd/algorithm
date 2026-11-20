# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wisdom-holman-integrator/. The authors are listed in prov/JQMB4C.jsonl.
"""Wisdom-Holman mixed-variable symplectic integrator for planetary systems.

Body 0 is the central star. The state is written in Jacobi coordinates: x'_i
is the position of body i relative to the center of mass of bodies 0..i-1.
The Hamiltonian splits into a sum of Kepler problems, one per planet with
mu_i = G eta_i (eta_i = m_0 + ... + m_i), and an interaction part that depends
on the positions only. A step is kick (h/2), Kepler drift (h), kick (h/2).
The Kepler drift is exact, with the f and g functions of the eccentric
anomaly, for bound orbits. G = 1 unless given.
"""

import math
from typing import Sequence

Vec = Sequence[float]
State = list[list[float]]


def to_jacobi(m: Sequence[float], x: Sequence[Vec]) -> State:
    """Jacobi vectors of positions (or velocities, or accelerations).
    Entry 0 is the center of mass of all bodies."""
    n, dim = len(m), len(x[0])
    out = [[0.0] * dim for _ in range(n)]
    com = list(x[0])
    eta = m[0]
    for i in range(1, n):
        out[i] = [x[i][k] - com[k] for k in range(dim)]
        eta_new = eta + m[i]
        com = [(eta * com[k] + m[i] * x[i][k]) / eta_new for k in range(dim)]
        eta = eta_new
    out[0] = com
    return out


def from_jacobi(m: Sequence[float], xj: Sequence[Vec]) -> State:
    """Inverse of to_jacobi."""
    n, dim = len(m), len(xj[0])
    eta = [0.0] * n
    eta[0] = m[0]
    for i in range(1, n):
        eta[i] = eta[i - 1] + m[i]
    out = [[0.0] * dim for _ in range(n)]
    com = list(xj[0])
    for i in range(n - 1, 0, -1):
        com_prev = [com[k] - m[i] / eta[i] * xj[i][k] for k in range(dim)]
        out[i] = [xj[i][k] + com_prev[k] for k in range(dim)]
        com = com_prev
    out[0] = com
    return out


def accelerations(m: Sequence[float], x: Sequence[Vec], G: float = 1.0) -> State:
    """Newtonian accelerations of all bodies by direct summation."""
    n, dim = len(m), len(x[0])
    a = [[0.0] * dim for _ in range(n)]
    for p in range(n - 1):
        for q in range(p + 1, n):
            d = [x[q][k] - x[p][k] for k in range(dim)]
            r2 = sum(c * c for c in d)
            f = G / (r2 * math.sqrt(r2))
            for k in range(dim):
                a[p][k] += m[q] * f * d[k]
                a[q][k] -= m[p] * f * d[k]
    return a


def kick_accel(m: Sequence[float], xj: Sequence[Vec], G: float = 1.0) -> State:
    """Jacobi accelerations of the interaction Hamiltonian: the full Newtonian
    acceleration in Jacobi form minus the Kepler part -G eta_i x'_i / r'_i^3."""
    n, dim = len(m), len(xj[0])
    aj = to_jacobi(m, accelerations(m, from_jacobi(m, xj), G))  # @line L7
    aj[0] = [0.0] * dim
    eta = m[0]
    for i in range(1, n):
        eta += m[i]
        r = math.sqrt(sum(c * c for c in xj[i]))
        f = G * eta / (r * r * r)
        aj[i] = [aj[i][k] + f * xj[i][k] for k in range(dim)]  # @line L8
    return aj


def kepler_drift(x: Vec, v: Vec, mu: float, dt: float) -> tuple[list[float], list[float]]:
    """Exact Kepler motion for time dt of a bound orbit with x'' = -mu x / |x|^3."""
    dim = len(x)
    r0 = math.sqrt(sum(c * c for c in x))
    v2 = sum(c * c for c in v)
    inv_a = 2.0 / r0 - v2 / mu
    if inv_a <= 0.0:
        raise ValueError("kepler_drift needs a bound orbit")
    a = 1.0 / inv_a
    n = math.sqrt(mu * inv_a ** 3)
    ec = 1.0 - r0 * inv_a
    es = sum(x[k] * v[k] for k in range(dim)) / math.sqrt(mu * a)
    mean = n * dt
    # F(dE) = dE - ec sin dE + es (1 - cos dE) - mean is increasing, with its root in [mean - 2, mean + 2].
    lo, hi = mean - 2.0, mean + 2.0
    de = mean
    for _ in range(100):
        s, c = math.sin(de), math.cos(de)
        fval = de - ec * s + es * (1.0 - c) - mean  # @line L9
        if fval > 0.0:
            hi = de
        else:
            lo = de
        step = fval / (1.0 - ec * c + es * s)
        new = de - step
        if not lo < new < hi:
            new = 0.5 * (lo + hi)
        if abs(new - de) <= 1e-15 * max(1.0, abs(de)):
            de = new
            break
        de = new
    s, c = math.sin(de), math.cos(de)
    r = a * (1.0 - ec * c + es * s)
    f = 1.0 - a / r0 * (1.0 - c)
    g = dt - (de - s) / n
    fdot = -math.sqrt(mu * a) * s / (r * r0)
    gdot = 1.0 - a / r * (1.0 - c)
    x1 = [f * x[k] + g * v[k] for k in range(dim)]  # @line L10
    v1 = [fdot * x[k] + gdot * v[k] for k in range(dim)]
    return x1, v1


def wh_step(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], h: float,
            G: float = 1.0) -> tuple[State, State]:
    """One kick-drift-kick step of size h in Cartesian coordinates."""
    n, dim = len(m), len(x[0])
    xj, vj = to_jacobi(m, x), to_jacobi(m, v)  # @line L1
    aj = kick_accel(m, xj, G)
    vj = [[vj[i][k] + 0.5 * h * aj[i][k] for k in range(dim)] for i in range(n)]  # @line L2
    eta = m[0]
    for i in range(1, n):
        eta += m[i]
        xj[i], vj[i] = kepler_drift(xj[i], vj[i], G * eta, h)  # @line L3
    xj[0] = [xj[0][k] + h * vj[0][k] for k in range(dim)]  # @line L4
    aj = kick_accel(m, xj, G)
    vj = [[vj[i][k] + 0.5 * h * aj[i][k] for k in range(dim)] for i in range(n)]  # @line L5
    return from_jacobi(m, xj), from_jacobi(m, vj)  # @line L6


def integrate(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], h: float, steps: int,
              G: float = 1.0) -> tuple[State, State]:
    x = [list(p) for p in x]
    v = [list(q) for q in v]
    for _ in range(steps):
        x, v = wh_step(m, x, v, h, G)
    return x, v


def energy(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], G: float = 1.0) -> float:
    n = len(m)
    kin = 0.5 * sum(m[i] * sum(c * c for c in v[i]) for i in range(n))
    pot = -sum(G * m[i] * m[q] / math.dist(x[i], x[q]) for i in range(n) for q in range(i + 1, n))
    return kin + pot
