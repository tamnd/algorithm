# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incompressible-sph/. The authors are listed in prov/H0ZQP6.jsonl.
"""Incompressible SPH (ISPH) by a projection step, in a periodic 2D box.

The fluid has the constant density rho0 = 1, so every particle has the volume
V = m / rho0 = L^2 / N. The kernel is the 2D cubic spline with support 2h.

One step of the scheme (a first-order projection, as in Cummins and Rudman 1999):

    v* = v + dt (nu lap v + g)              viscous predictor at the old positions
    x* = x + dt v                           provisional positions
    solve  L phi = D v*                     pressure Poisson equation at x*
    v' = v* - G phi                         projection, the pressure is p = phi / dt
    x' = x + dt (v + v') / 2

The discrete operators, for particles i and their neighbours j within 2h:

    (G phi)_i = sum_j V (phi_i + phi_j) grad_i W_ij       symmetric gradient, conserves momentum
    (D v)_i   = -sum_j V (v_i - v_j) . grad_i W_ij        SPH divergence
    (L phi)_i = sum_j 2 V (phi_i - phi_j) x_ij . grad_i W_ij / (r_ij^2 + eta^2)   compact Laplacian

with eta^2 = 0.01 h^2. L is not D G, so the projection is approximate: D v' is
reduced but not zero. The matrix -L is symmetric positive semidefinite with
constant null vectors, so the right-hand side is made consistent by removing its mean.
The viscous term is the one of Morris, Fox and Zhu (1997) with constant density:

    (nu lap v)_i = sum_j 2 nu V (x_ij . grad_i W_ij) / (r_ij^2 + eta^2) (v_i - v_j)
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from scisparse import cg

Vec = Tuple[float, float]
Pair = Tuple[int, int, float, float, float, float, float]


@dataclass
class ISPHState:
    x: List[float]
    y: List[float]
    u: List[float]
    v: List[float]
    box: float
    h: float


@dataclass
class StepInfo:
    div_before: float  # max |D v*| at x*
    div_after: float  # max |D v'| at x*
    cg_iterations: int


def kernel_2d(r: float, h: float) -> float:
    """Cubic spline W(r, h) in 2D, normalization 10 / (7 pi h^2), support 2h."""
    q = r / h
    s = 10.0 / (7.0 * math.pi * h * h)
    if q < 1.0:
        return s * (1.0 - 1.5 * q * q + 0.75 * q ** 3)
    if q < 2.0:
        return s * 0.25 * (2.0 - q) ** 3
    return 0.0


def kernel_derivative_2d(r: float, h: float) -> float:
    """dW/dr of the 2D cubic spline."""
    q = r / h
    s = 10.0 / (7.0 * math.pi * h ** 3)
    if q < 1.0:
        return s * (-3.0 * q + 2.25 * q * q)
    if q < 2.0:
        return -s * 0.75 * (2.0 - q) ** 2
    return 0.0


def neighbour_pairs(x: Sequence[float], y: Sequence[float], box: float, h: float) -> List[Pair]:
    """All pairs (i, j, dx, dy, dW/dx_i, dW/dy_i, r) with i < j and 0 < r < 2h, minimum image.

    A cell list with cells of side at least 2h; cost O(N k) for k neighbours per
    particle. Requires box >= 6h so that each pair is found once.
    """
    n = len(x)
    nc = int(box // (2.0 * h))
    if nc < 3:
        raise ValueError("the box must be at least 6h wide")
    cell = box / nc
    cells: Dict[Tuple[int, int], List[int]] = {}
    for i in range(n):
        key = (int(x[i] // cell) % nc, int(y[i] // cell) % nc)
        cells.setdefault(key, []).append(i)
    pairs: List[Pair] = []
    cut = 4.0 * h * h
    half = 0.5 * box
    for (cx, cy), members in cells.items():
        near: List[int] = []
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                near.extend(cells.get(((cx + ox) % nc, (cy + oy) % nc), ()))
        for i in members:
            for j in near:
                if j <= i:
                    continue
                dx = x[i] - x[j]
                dy = y[i] - y[j]
                if dx > half:
                    dx -= box
                elif dx < -half:
                    dx += box
                if dy > half:
                    dy -= box
                elif dy < -half:
                    dy += box
                r2 = dx * dx + dy * dy
                if 0.0 < r2 < cut:
                    r = math.sqrt(r2)
                    d = kernel_derivative_2d(r, h) / r
                    pairs.append((i, j, dx, dy, d * dx, d * dy, r))
    pairs.sort()
    return pairs


def density(pairs: Sequence[Pair], n: int, vol: float, h: float) -> List[float]:
    """Summation density rho_i = sum_j V W_ij with rho0 = 1 (self term included)."""
    rho = [vol * kernel_2d(0.0, h)] * n
    for i, j, _, _, _, _, r in pairs:
        w = vol * kernel_2d(r, h)
        rho[i] += w
        rho[j] += w
    return rho


def divergence(pairs: Sequence[Pair], u: Sequence[float], v: Sequence[float], vol: float) -> List[float]:
    """(D v)_i = -sum_j V (v_i - v_j) . grad_i W_ij."""
    out = [0.0] * len(u)
    for i, j, _, _, gx, gy, _ in pairs:
        w = -vol * ((u[i] - u[j]) * gx + (v[i] - v[j]) * gy)
        out[i] += w
        out[j] += w  # (v_j - v_i) . grad_j W_ji is the same number
    return out


def gradient(pairs: Sequence[Pair], phi: Sequence[float], vol: float) -> Tuple[List[float], List[float]]:
    """(G phi)_i = sum_j V (phi_i + phi_j) grad_i W_ij, antisymmetric in each pair."""
    gxo = [0.0] * len(phi)
    gyo = [0.0] * len(phi)
    for i, j, _, _, gx, gy, _ in pairs:
        s = vol * (phi[i] + phi[j])
        gxo[i] += s * gx
        gyo[i] += s * gy
        gxo[j] -= s * gx
        gyo[j] -= s * gy
    return gxo, gyo


def viscous_term(pairs: Sequence[Pair], u: Sequence[float], v: Sequence[float], vol: float,
                 nu: float, h: float) -> Tuple[List[float], List[float]]:
    """Morris, Fox and Zhu viscous acceleration, pairwise antisymmetric."""
    n = len(u)
    au = [0.0] * n
    av = [0.0] * n
    eta2 = 0.01 * h * h
    for i, j, dx, dy, gx, gy, r in pairs:
        c = 2.0 * nu * vol * (dx * gx + dy * gy) / (r * r + eta2)  # c <= 0
        du = c * (u[i] - u[j])
        dv = c * (v[i] - v[j])
        au[i] += du
        av[i] += dv
        au[j] -= du
        av[j] -= dv
    return au, av


def laplacian_matrix(pairs: Sequence[Pair], n: int, vol: float, h: float) -> List[Dict[int, float]]:
    """A = -L for the compact Laplacian; symmetric, diagonally dominant, rows sum to zero."""
    A: List[Dict[int, float]] = [dict() for _ in range(n)]
    eta2 = 0.01 * h * h
    for i, j, dx, dy, gx, gy, r in pairs:
        c = -2.0 * vol * (dx * gx + dy * gy) / (r * r + eta2)  # c >= 0
        A[i][i] = A[i].get(i, 0.0) + c
        A[j][j] = A[j].get(j, 0.0) + c
        A[i][j] = A[i].get(j, 0.0) - c
        A[j][i] = A[j].get(i, 0.0) - c
    return A


def pressure_solve(pairs: Sequence[Pair], u: Sequence[float], v: Sequence[float], vol: float,
                   h: float, tol: float = 1e-12) -> Tuple[List[float], int]:
    """Solve L phi = D v - mean(D v) by CG on -L; returns (phi with mean 0, iterations)."""
    n = len(u)
    div = divergence(pairs, u, v, vol)
    A = laplacian_matrix(pairs, n, vol, h)
    mean = sum(div) / n
    b = [mean - d for d in div]  # -L phi = -(D v - mean), a consistent system
    return cg(A, b, tol=tol)


def project(pairs: Sequence[Pair], u: Sequence[float], v: Sequence[float], vol: float, h: float,
            tol: float = 1e-12) -> Tuple[List[float], List[float], List[float], int]:
    """Return (u', v', phi, CG iterations) with (u', v') = (u, v) - G phi."""
    n = len(u)
    phi, its = pressure_solve(pairs, u, v, vol, h, tol)
    gx, gy = gradient(pairs, phi, vol)
    return [u[i] - gx[i] for i in range(n)], [v[i] - gy[i] for i in range(n)], phi, its


def isph_step(s: ISPHState, dt: float, nu: float = 0.0, g: Vec = (0.0, 0.0),
              tol: float = 1e-12) -> Tuple[ISPHState, StepInfo]:
    """One projection step. Cost O(N k) to build plus O(N k) per CG iteration."""
    n = len(s.x)
    vol = s.box * s.box / n
    pairs = neighbour_pairs(s.x, s.y, s.box, s.h)  # @line L2
    if nu:
        au, av = viscous_term(pairs, s.u, s.v, vol, nu, s.h)
    else:
        au, av = [0.0] * n, [0.0] * n
    us = [s.u[i] + dt * (au[i] + g[0]) for i in range(n)]  # @line L3
    vs = [s.v[i] + dt * (av[i] + g[1]) for i in range(n)]
    xs = [(s.x[i] + dt * s.u[i]) % s.box for i in range(n)]  # @line L4
    ys = [(s.y[i] + dt * s.v[i]) % s.box for i in range(n)]
    pairs = neighbour_pairs(xs, ys, s.box, s.h)
    d0 = divergence(pairs, us, vs, vol)
    phi, its = pressure_solve(pairs, us, vs, vol, s.h, tol)  # @line L5
    gx, gy = gradient(pairs, phi, vol)
    un = [us[i] - gx[i] for i in range(n)]  # @line L6
    vn = [vs[i] - gy[i] for i in range(n)]
    d1 = divergence(pairs, un, vn, vol)
    xn = [(s.x[i] + 0.5 * dt * (s.u[i] + un[i])) % s.box for i in range(n)]  # @line L7
    yn = [(s.y[i] + 0.5 * dt * (s.v[i] + vn[i])) % s.box for i in range(n)]
    info = StepInfo(max(abs(d) for d in d0), max(abs(d) for d in d1), its)
    return ISPHState(xn, yn, un, vn, s.box, s.h), info


def isph(s0: ISPHState, dt: float, steps: int, nu: float = 0.0, g: Vec = (0.0, 0.0),
         tol: float = 1e-12) -> Tuple[ISPHState, List[StepInfo]]:
    """Run `steps` ISPH steps from s0, which is not changed.

    Precondition: dt > 0, steps >= 0, box >= 6h. Cost: steps times one pressure
    solve on N particles with about 20 neighbours each.
    """
    if dt <= 0 or steps < 0:
        raise ValueError("need dt > 0 and steps >= 0")
    s = ISPHState(list(s0.x), list(s0.y), list(s0.u), list(s0.v), s0.box, s0.h)
    infos: List[StepInfo] = []
    for _ in range(steps):  # @line L1
        s, info = isph_step(s, dt, nu, g, tol)
        infos.append(info)
    return s, infos  # @line L8


def lattice(n: int, box: float = 1.0, eta: float = 1.2,
            velocity: Optional[Callable[[float, float], Vec]] = None,
            jitter: float = 0.0, seed: int = 0) -> ISPHState:
    """n x n particles on a square lattice, h = eta * spacing, optional random jitter."""
    rng = random.Random(seed)
    dx = box / n
    x: List[float] = []
    y: List[float] = []
    u: List[float] = []
    v: List[float] = []
    for a in range(n):
        for b in range(n):
            px = ((a + 0.5) * dx + jitter * dx * (rng.random() - 0.5)) % box
            py = ((b + 0.5) * dx + jitter * dx * (rng.random() - 0.5)) % box
            x.append(px)
            y.append(py)
            vx, vy = velocity(px, py) if velocity else (0.0, 0.0)
            u.append(vx)
            v.append(vy)
    return ISPHState(x, y, u, v, box, eta * dx)


def kinetic_energy(s: ISPHState) -> float:
    """(1/2) sum V |v|^2 with V = box^2 / N and rho0 = 1."""
    vol = s.box * s.box / len(s.x)
    return 0.5 * vol * sum(a * a + b * b for a, b in zip(s.u, s.v))


def momentum(s: ISPHState) -> Vec:
    """Total momentum sum V v with rho0 = 1."""
    vol = s.box * s.box / len(s.x)
    return (vol * sum(s.u), vol * sum(s.v))


def taylor_green(x: float, y: float) -> Vec:
    """A divergence-free periodic field on the unit box; KE decays like exp(-16 pi^2 nu t)."""
    k = 2.0 * math.pi
    return (-math.cos(k * x) * math.sin(k * y), math.sin(k * x) * math.cos(k * y))
