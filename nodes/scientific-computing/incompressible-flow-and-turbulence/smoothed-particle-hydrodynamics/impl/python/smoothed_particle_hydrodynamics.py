# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smoothed-particle-hydrodynamics/. The authors are listed in prov/9G16QJ.jsonl.

"""Smoothed particle hydrodynamics for the one-dimensional Euler equations of an ideal gas.

Particles carry mass m_i, position x_i, velocity v_i and specific internal energy e_i.
  density   rho_i = sum_j m_j W_ij                   (summation density, self term included)
  pressure  P_i = (gamma - 1) rho_i e_i,  sound speed c_i = sqrt(gamma P_i / rho_i)
  momentum  dv_i/dt = - sum_j m_j A_ij dW_ij/dx_i
  energy    de_i/dt = (1/2) sum_j m_j A_ij (v_i - v_j) dW_ij/dx_i
with A_ij = P_i/rho_i^2 + P_j/rho_j^2 + Pi_ij and the Monaghan artificial viscosity Pi_ij.
W_ij is the cubic spline kernel averaged over h_i and h_j, so dW_ij/dx_i = -dW_ij/dx_j and the
semi-discrete system conserves mass, momentum and total energy exactly. The smoothing lengths
follow h_i = eta m_i / rho_i. Time stepping is kick-drift-kick leapfrog.
"""

import math
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, List, Optional, Sequence, Tuple

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of T/dt


def kernel(r: Any, h: Any) -> Any:
    """The 1D cubic spline kernel W(r, h) with support |r| < 2h and integral 1.

    Exact for Fraction (or int) arguments, float otherwise.
    """
    exact = isinstance(r, (int, Fraction)) and isinstance(h, (int, Fraction))
    one = Fraction(1) if exact else 1.0
    q = abs(r) / (h * one)
    s = 2 * one / (3 * h)
    if q < 1:
        return s * (1 - 3 * q * q / 2 + 3 * q ** 3 / 4)
    if q < 2:
        return s * (2 - q) ** 3 / 4
    return 0 * one


def kernel_gradient(r: float, h: float) -> float:
    """dW/dr for the cubic spline kernel; odd in r."""
    q = abs(r) / h
    s = 2.0 / (3.0 * h * h)
    if q < 1:
        g = -3.0 * q + 2.25 * q * q
    elif q < 2:
        g = -0.75 * (2.0 - q) ** 2
    else:
        return 0.0
    return s * g * (1.0 if r > 0 else -1.0 if r < 0 else 0.0)


@dataclass
class Particles:
    """Particle state; rho and h are recomputed by the density pass."""
    x: List[float]
    v: List[float]
    m: List[float]
    e: List[float]
    h: List[float]
    rho: Optional[List[float]] = None


@dataclass
class SphResult:
    """Final particle state, final time, number of steps and number of pair interactions."""
    p: Particles
    t: float
    steps: int
    pair_evals: int


def step_count(t_end: Any, dt: Any) -> int:
    """The number N of time steps of length at most dt (up to GRID_SLACK) from 0 to t_end."""
    if not dt > 0:
        raise ValueError("the time step dt must be positive")
    if t_end < 0:
        raise ValueError("t_end must not be negative")
    r = t_end / dt
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def neighbour_pairs(x: Sequence[float], h: Sequence[float]) -> List[Tuple[int, int]]:
    """All pairs i < j with |x_i - x_j| < 2 max(h_i, h_j), by sorting and binary search.

    A pair qualifies iff |x_i - x_j| < 2 h_i or |x_i - x_j| < 2 h_j, so it is enough to
    collect, for every i, the particles within 2 h_i of x_i.
    """
    order = sorted(range(len(x)), key=lambda i: x[i])
    xs = [x[i] for i in order]
    found = set()
    for a, i in enumerate(order):
        lo = bisect_left(xs, xs[a] - 2.0 * h[i])
        hi = bisect_right(xs, xs[a] + 2.0 * h[i])
        for b in range(lo, hi):
            j = order[b]
            if j != i and abs(x[i] - x[j]) < 2.0 * h[i]:
                found.add((i, j) if i < j else (j, i))
    return sorted(found)


def density(p: Particles, pairs: List[Tuple[int, int]]) -> List[float]:
    """Summation density with the kernel averaged over h_i and h_j (self term included)."""
    rho = [p.m[i] * kernel(0.0, p.h[i]) for i in range(len(p.x))]
    for i, j in pairs:
        r = p.x[i] - p.x[j]
        w = 0.5 * (kernel(r, p.h[i]) + kernel(r, p.h[j]))
        rho[i] += p.m[j] * w
        rho[j] += p.m[i] * w
    return rho


def accelerations(p: Particles, v: Sequence[float], gamma: float, alpha: float = 1.0, beta: float = 2.0):
    """Density pass, then the momentum and energy right-hand sides; returns (a, de, pair count)."""
    n = len(p.x)
    pairs = neighbour_pairs(p.x, p.h)  # @line L7
    rho = density(p, pairs)  # @line L8
    p.rho = rho
    P = [(gamma - 1.0) * rho[i] * p.e[i] for i in range(n)]
    c = [math.sqrt(max(gamma * P[i] / rho[i], 0.0)) for i in range(n)]
    acc = [0.0] * n
    de = [0.0] * n
    for i, j in pairs:  # @line L9
        r = p.x[i] - p.x[j]
        g = 0.5 * (kernel_gradient(r, p.h[i]) + kernel_gradient(r, p.h[j]))  # dW_ij/dx_i
        vij = v[i] - v[j]
        visc = 0.0
        if vij * r < 0:  # approaching pair: Monaghan artificial viscosity
            hb = 0.5 * (p.h[i] + p.h[j])
            mu = hb * vij * r / (r * r + 0.01 * hb * hb)
            visc = (-alpha * 0.5 * (c[i] + c[j]) * mu + beta * mu * mu) / (0.5 * (rho[i] + rho[j]))
        A = P[i] / rho[i] ** 2 + P[j] / rho[j] ** 2 + visc
        acc[i] -= p.m[j] * A * g
        acc[j] += p.m[i] * A * g
        w = 0.5 * A * vij * g
        de[i] += p.m[j] * w
        de[j] += p.m[i] * w
    return acc, de, len(pairs)  # @line L10


def sph(p0: Particles, t_end: float, dt: float, gamma: float = 1.4, eta: float = 1.2,
        alpha: float = 1.0, beta: float = 2.0, adapt_h: bool = True) -> SphResult:
    """Integrate the SPH system with kick-drift-kick leapfrog from t = 0 to t_end.

    The last step is shortened to land on t_end. The caller chooses dt; a Courant-type
    limit dt <= C h / (c + |v|) with C about 0.3 is needed for stability.
    """
    n = len(p0.x)
    if n == 0:
        raise ValueError("need at least one particle")
    if not (len(p0.v) == len(p0.m) == len(p0.e) == len(p0.h) == n):
        raise ValueError("particle arrays must have equal length")
    if min(p0.m) <= 0 or min(p0.h) <= 0:
        raise ValueError("masses and smoothing lengths must be positive")
    p = Particles(list(p0.x), list(p0.v), list(p0.m), list(p0.e), list(p0.h))
    N = step_count(t_end, dt)  # @line L1
    t, pairs_total = 0.0, 0
    acc, de, k = accelerations(p, p.v, gamma, alpha, beta)  # @line L2
    pairs_total += k
    for s in range(N):
        h = (t_end if s == N - 1 else (s + 1) * dt) - t
        vh = [p.v[i] + 0.5 * h * acc[i] for i in range(n)]  # @line L3
        p.e = [p.e[i] + 0.5 * h * de[i] for i in range(n)]
        p.x = [p.x[i] + h * vh[i] for i in range(n)]  # @line L4
        if adapt_h:
            p.h = [eta * p.m[i] / p.rho[i] for i in range(n)]
        vpred = [vh[i] + 0.5 * h * acc[i] for i in range(n)]
        acc, de, k = accelerations(p, vpred, gamma, alpha, beta)  # @line L5
        pairs_total += k
        p.v = [vh[i] + 0.5 * h * acc[i] for i in range(n)]  # @line L6
        p.e = [p.e[i] + 0.5 * h * de[i] for i in range(n)]
        t += h
    return SphResult(p, t, N, pairs_total)


def totals(p: Particles) -> Tuple[float, float, float]:
    """(mass, momentum, total energy) = (sum m, sum m v, sum m (v^2/2 + e))."""
    return (sum(p.m), sum(m * v for m, v in zip(p.m, p.v)),
            sum(m * (0.5 * v * v + e) for m, v, e in zip(p.m, p.v, p.e)))


def shock_tube(n_left: int, left=(1.0, 0.0, 1.0), right=(0.125, 0.0, 0.1), x_min: float = -0.75,
               x_max: float = 0.75, gamma: float = 1.4, eta: float = 1.2) -> Particles:
    """Equal-mass particles for a Riemann problem at x = 0; states are (rho, v, P)."""
    rl, vl, pl = left
    rr, vr, pr = right
    dl = -x_min / n_left
    m = rl * dl
    dr = m / rr
    xl = [x_min + (i + 0.5) * dl for i in range(n_left)]
    n_right = int(round(x_max / dr))
    xr = [(i + 0.5) * dr for i in range(n_right)]
    x = xl + xr
    v = [vl] * n_left + [vr] * n_right
    e = [pl / ((gamma - 1) * rl)] * n_left + [pr / ((gamma - 1) * rr)] * n_right
    h = [eta * dl] * n_left + [eta * dr] * n_right
    return Particles(x, v, [m] * len(x), e, h)


def riemann_exact(left, right, gamma: float, xi: float) -> Tuple[float, float, float]:
    """Exact solution (rho, v, P) of the Euler Riemann problem at x/t = xi (no vacuum)."""
    rl, vl, pl = left
    rr, vr, pr = right
    cl, cr = math.sqrt(gamma * pl / rl), math.sqrt(gamma * pr / rr)

    def fk(p, rk, pk, ck):
        if p > pk:
            A, B = 2 / ((gamma + 1) * rk), (gamma - 1) / (gamma + 1) * pk
            q = math.sqrt(A / (p + B))
            return (p - pk) * q, q * (1 - (p - pk) / (2 * (p + B)))
        r = (p / pk) ** ((gamma - 1) / (2 * gamma))
        return 2 * ck / (gamma - 1) * (r - 1), (p / pk) ** (-(gamma + 1) / (2 * gamma)) / (rk * ck)

    p = max(1e-12, 0.5 * (pl + pr))
    for _ in range(100):
        f1, d1 = fk(p, rl, pl, cl)
        f2, d2 = fk(p, rr, pr, cr)
        step = (f1 + f2 + vr - vl) / (d1 + d2)
        p_new = max(1e-12, p - step)
        if abs(p_new - p) < 1e-14 * p:
            p = p_new
            break
        p = p_new
    f1, _ = fk(p, rl, pl, cl)
    f2, _ = fk(p, rr, pr, cr)
    u = 0.5 * (vl + vr) + 0.5 * (f2 - f1)
    g1, g2 = (gamma - 1) / (gamma + 1), (gamma - 1) / (2 * gamma)
    if xi <= u:  # left of the contact
        if p > pl:
            s = vl - cl * math.sqrt((gamma + 1) / (2 * gamma) * p / pl + g2)
            return (rl, vl, pl) if xi < s else (rl * (p / pl + g1) / (g1 * p / pl + 1), u, p)
        cs = cl * (p / pl) ** g2
        if xi < vl - cl:
            return rl, vl, pl
        if xi > u - cs:
            return rl * (p / pl) ** (1 / gamma), u, p
        vf = 2 / (gamma + 1) * (cl + (gamma - 1) / 2 * vl + xi)
        cf = vf - xi
        return rl * (cf / cl) ** (2 / (gamma - 1)), vf, pl * (cf / cl) ** (2 * gamma / (gamma - 1))
    if p > pr:
        s = vr + cr * math.sqrt((gamma + 1) / (2 * gamma) * p / pr + g2)
        return (rr, vr, pr) if xi > s else (rr * (p / pr + g1) / (g1 * p / pr + 1), u, p)
    cs = cr * (p / pr) ** g2
    if xi > vr + cr:
        return rr, vr, pr
    if xi < u + cs:
        return rr * (p / pr) ** (1 / gamma), u, p
    vf = 2 / (gamma + 1) * (-cr + (gamma - 1) / 2 * vr + xi)
    cf = xi - vf
    return rr * (cf / cr) ** (2 / (gamma - 1)), vf, pr * (cf / cr) ** (2 * gamma / (gamma - 1))
