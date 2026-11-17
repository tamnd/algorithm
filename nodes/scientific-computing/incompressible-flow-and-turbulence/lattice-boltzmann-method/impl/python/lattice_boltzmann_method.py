# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-boltzmann-method/. The authors are listed in prov/ANY3EP.jsonl.

"""The lattice Boltzmann method (BGK collision) on the D2Q9 and D1Q3 lattices.

Lattice units: grid spacing 1, time step 1, sound speed c_s^2 = 1/3.
D2Q9 approximates the weakly compressible Navier-Stokes equations with
kinematic viscosity nu = (tau - 1/2)/3; D1Q3 with a zero-velocity
equilibrium approximates the diffusion equation with D = (tau - 1/2)/3.

Each step is a local collision followed by streaming to the neighbours.
The x direction is periodic; in y the domain is periodic or bounded by
two walls halfway between nodes (bounce-back), at y = -1/2 and ny - 1/2.
A constant body force (gx, gy) enters by Guo's forcing scheme.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List, Sequence, Tuple

C = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
OPP = [0, 3, 4, 1, 2, 7, 8, 5, 6]
W_EXACT = [Fraction(4, 9)] + [Fraction(1, 9)] * 4 + [Fraction(1, 36)] * 4


@dataclass
class LBMResult:
    """Density and velocity fields indexed [y][x], and the populations."""

    rho: List[List[Any]]
    ux: List[List[Any]]
    uy: List[List[Any]]
    steps: int
    f: List[List[Any]]


def _consts(exact: bool):
    if exact:
        return W_EXACT, Fraction(3), Fraction(9, 2), Fraction(3, 2), Fraction(1, 2)
    return [float(w) for w in W_EXACT], 3.0, 4.5, 1.5, 0.5


def equilibrium(rho: Any, ux: Any, uy: Any, exact: bool = False) -> List[Any]:
    """D2Q9 equilibrium w_i rho (1 + 3 c.u + 9/2 (c.u)^2 - 3/2 |u|^2)."""
    w, three, nine_half, three_half, _ = _consts(exact)
    usq = ux * ux + uy * uy
    out = []
    for i, (cx, cy) in enumerate(C):
        cu = cx * ux + cy * uy
        out.append(w[i] * rho * (1 + three * cu + nine_half * cu * cu - three_half * usq))
    return out


def moments(fs: Sequence[Any], gx: Any = 0, gy: Any = 0, half: Any = 0.5) -> Tuple[Any, Any, Any]:
    """Density and velocity (with the half force shift) of one node."""
    rho = sum(fs)
    jx = sum(C[i][0] * fs[i] for i in range(9)) + half * gx
    jy = sum(C[i][1] * fs[i] for i in range(9)) + half * gy
    return rho, jx / rho, jy / rho


def lbm_d2q9(nx: int, ny: int, tau: Any, steps: int,
             init: Callable[[int, int], Tuple[Any, Any, Any]] = None,
             force: Tuple[Any, Any] = (0, 0), walls: bool = False) -> LBMResult:
    """Run `steps` BGK steps on an nx by ny D2Q9 lattice.

    init(x, y) gives (rho, ux, uy) for the starting equilibrium (default
    (1, 0, 0)).  Pass Fractions for tau, init values and force to run in
    exact arithmetic.
    """
    if nx < 1 or ny < 1:
        raise ValueError("the lattice needs at least one node")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    if not tau > Fraction(1, 2):
        raise ValueError("tau must exceed 1/2 (viscosity (tau - 1/2)/3 > 0)")
    if walls and ny < 2:
        raise ValueError("a channel needs ny >= 2")
    exact = isinstance(tau, Fraction)
    w, three, nine_half, _, half = _consts(exact)
    gx, gy = force
    omega = 1 / tau
    fpref = 1 - half * omega                    # Guo forcing prefactor 1 - 1/(2 tau)
    if init is None:
        init = lambda x, y: (1, 0, 0)
    n = nx * ny
    f = [[0] * n for _ in range(9)]
    for y in range(ny):                                          # @line L1
        for x in range(nx):
            r, u, v = init(x, y)
            eq = equilibrium(r, u, v, exact)
            for i in range(9):
                f[i][y * nx + x] = eq[i]
    for _ in range(steps):                                       # @line L2
        post = [[0] * n for _ in range(9)]
        for k in range(n):
            fs = [f[i][k] for i in range(9)]
            rho, ux, uy = moments(fs, gx, gy, half)              # @line L3
            eq = equilibrium(rho, ux, uy, exact)
            for i in range(9):                                   # @line L4
                cx, cy = C[i]
                cu = cx * ux + cy * uy
                src = 0
                if gx or gy:
                    src = fpref * w[i] * (three * ((cx - ux) * gx + (cy - uy) * gy)
                                          + 2 * nine_half * cu * (cx * gx + cy * gy))
                post[i][k] = fs[i] - omega * (fs[i] - eq[i]) + src
        nf = [[0] * n for _ in range(9)]
        for y in range(ny):                                      # @line L5
            for x in range(nx):
                k = y * nx + x
                for i in range(9):
                    cx, cy = C[i]
                    yt = y + cy
                    if walls and (yt < 0 or yt >= ny):           # @line L6
                        nf[OPP[i]][k] = post[i][k]
                        continue
                    nf[i][(yt % ny) * nx + (x + cx) % nx] = post[i][k]
        f = nf
    rho_f = [[0] * nx for _ in range(ny)]
    ux_f = [[0] * nx for _ in range(ny)]
    uy_f = [[0] * nx for _ in range(ny)]
    for y in range(ny):                                          # @line L7
        for x in range(nx):
            r, u, v = moments([f[i][y * nx + x] for i in range(9)], gx, gy, half)
            rho_f[y][x], ux_f[y][x], uy_f[y][x] = r, u, v
    return LBMResult(rho_f, ux_f, uy_f, steps, f)


def lbm_d1q3_diffusion(rho0: Sequence[Any], tau: Any, steps: int) -> List[Any]:
    """D1Q3 BGK for the periodic diffusion equation, D = (tau - 1/2)/3.

    Velocities 0, +1, -1 with weights 2/3, 1/6, 1/6; equilibrium w_i rho.
    With tau = 1 one step is the FTCS scheme with mu = 1/6.
    """
    if not tau > Fraction(1, 2):
        raise ValueError("tau must exceed 1/2")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    n = len(rho0)
    if n == 0:
        return []
    exact = isinstance(tau, Fraction)
    w = [Fraction(2, 3), Fraction(1, 6), Fraction(1, 6)]
    if not exact:
        w = [float(x) for x in w]
    omega = 1 / tau
    f = [[w[i] * r for r in rho0] for i in range(3)]
    for _ in range(steps):
        rho = [f[0][j] + f[1][j] + f[2][j] for j in range(n)]
        post = [[f[i][j] - omega * (f[i][j] - w[i] * rho[j]) for j in range(n)] for i in range(3)]
        f = [post[0],
             [post[1][(j - 1) % n] for j in range(n)],
             [post[2][(j + 1) % n] for j in range(n)]]
    return [f[0][j] + f[1][j] + f[2][j] for j in range(n)]
