# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-relaxation-time-lattice-boltzmann/. The authors are listed in prov/JZ1BG8.jsonl.

"""The multiple-relaxation-time (MRT) lattice Boltzmann method on D2Q9.

Lattice units: grid spacing 1, time step 1, c_s^2 = 1/3. The collision
works on the nine moments m = M f of the populations (the moment basis of
Lallemand and Luo 2000). Moment k relaxes toward its equilibrium with its
own rate s_k:

    m* = m - S (m - m_eq) + (I - S/2) M F,     f* = M^-1 m*,

where F is Guo's force term. The rates of the conserved moments (density
and momentum) do not matter, because m = m_eq for them. The shear rate
s_nu gives the kinematic viscosity nu = (1/s_nu - 1/2)/3. With every rate
equal to 1/tau the scheme is exactly the BGK scheme.

The x direction is periodic. In y the lattice is periodic, or it has two
walls halfway between nodes, at y = -1/2 and y = ny - 1/2 (halfway
bounce-back). Pass Fraction rates, forces and initial data with
exact=True to run in exact rational arithmetic.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List, Optional, Sequence, Tuple

C = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
OPP = [0, 3, 4, 1, 2, 7, 8, 5, 6]
W_EXACT = [Fraction(4, 9)] + [Fraction(1, 9)] * 4 + [Fraction(1, 36)] * 4
W_FLOAT = [float(w) for w in W_EXACT]

# Rows: rho, e, epsilon, j_x, q_x, j_y, q_y, p_xx, p_xy (Lallemand and Luo 2000).
M = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [-4, -1, -1, -1, -1, 2, 2, 2, 2],
    [4, -2, -2, -2, -2, 1, 1, 1, 1],
    [0, 1, 0, -1, 0, 1, -1, -1, 1],
    [0, -2, 0, 2, 0, 1, -1, -1, 1],
    [0, 0, 1, 0, -1, 1, 1, -1, -1],
    [0, 0, -2, 0, 2, 1, 1, -1, -1],
    [0, 1, -1, 1, -1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, -1, 1, -1],
]
# The rows of M are orthogonal: M M^T = diag(NORM2), so M^-1 = M^T diag(1/NORM2).
NORM2 = [9, 36, 36, 6, 12, 6, 12, 4, 4]


@dataclass
class MRTResult:
    """Density and velocity fields indexed [y][x], and the populations f[y * nx + x][i]."""

    rho: List[List[Any]]
    ux: List[List[Any]]
    uy: List[List[Any]]
    steps: int
    f: List[List[Any]]


def nu_of_rate(s_nu: Any) -> Any:
    """Kinematic viscosity of the shear rate: nu = (1/s_nu - 1/2)/3."""
    return (1 / s_nu - Fraction(1, 2)) / 3 if isinstance(s_nu, Fraction) else (1.0 / s_nu - 0.5) / 3.0


def magic_q_rate(s_nu: Any, magic: Any = Fraction(3, 16)) -> Any:
    """The rate s_q that gives (1/s_nu - 1/2)(1/s_q - 1/2) = magic."""
    half = Fraction(1, 2) if isinstance(s_nu, Fraction) else 0.5
    return 1 / (magic / (1 / s_nu - half) + half)


def rates(s_nu: Any, s_q: Any, s_e: Any = None, s_eps: Any = None) -> List[Any]:
    """The diagonal of S in the order of the rows of M. s_e and s_eps default to s_nu."""
    s_e = s_nu if s_e is None else s_e
    s_eps = s_nu if s_eps is None else s_eps
    zero = 0 * s_nu
    return [zero, s_e, s_eps, zero, s_q, zero, s_q, s_nu, s_nu]


def equilibrium(rho: Any, ux: Any, uy: Any, exact: bool = False) -> List[Any]:
    """D2Q9 equilibrium populations, second order in u."""
    w = W_EXACT if exact else W_FLOAT
    usq = ux * ux + uy * uy
    out = []
    for i in range(9):
        cu = C[i][0] * ux + C[i][1] * uy
        out.append(w[i] * rho * (1 + 3 * cu + Fraction(9, 2) * cu * cu - Fraction(3, 2) * usq)
                   if exact else w[i] * rho * (1 + 3 * cu + 4.5 * cu * cu - 1.5 * usq))
    return out


def equilibrium_moments(rho: Any, ux: Any, uy: Any) -> List[Any]:
    """m_eq = M f_eq in closed form."""
    jx, jy = rho * ux, rho * uy
    usq = ux * ux + uy * uy
    return [rho, -2 * rho + 3 * rho * usq, rho - 3 * rho * usq, jx, -jx, jy, -jy,
            rho * (ux * ux - uy * uy), rho * ux * uy]


def guo_force(ux: Any, uy: Any, gx: Any, gy: Any, exact: bool = False) -> List[Any]:
    """Guo's force populations F_i = w_i [3 (c_i - u) + 9 (c_i . u) c_i] . g."""
    w = W_EXACT if exact else W_FLOAT
    out = []
    for i in range(9):
        cx, cy = C[i]
        cu = cx * ux + cy * uy
        out.append(w[i] * ((3 * (cx - ux) + 9 * cu * cx) * gx + (3 * (cy - uy) + 9 * cu * cy) * gy))
    return out


def to_moments(f: Sequence[Any]) -> List[Any]:
    """m = M f, written out row by row."""
    f0, f1, f2, f3, f4, f5, f6, f7, f8 = f
    axes = f1 + f2 + f3 + f4
    diag = f5 + f6 + f7 + f8
    dx = f5 - f6 - f7 + f8
    dy = f5 + f6 - f7 - f8
    return [f0 + axes + diag, -4 * f0 - axes + 2 * diag, 4 * f0 - 2 * axes + diag,
            f1 - f3 + dx, 2 * (f3 - f1) + dx, f2 - f4 + dy, 2 * (f4 - f2) + dy,
            f1 - f2 + f3 - f4, f5 - f6 + f7 - f8]


def from_moments(m: Sequence[Any]) -> List[Any]:
    """f = M^-1 m = M^T diag(1/NORM2) m, written out column by column."""
    r, e, ep, jx, qx, jy, qy, pxx, pxy = (m[k] / NORM2[k] for k in range(9))
    a = r - e - 2 * ep
    d = r + 2 * e + ep
    return [r - 4 * e + 4 * ep,
            a + jx - 2 * qx + pxx, a + jy - 2 * qy - pxx,
            a - jx + 2 * qx + pxx, a - jy + 2 * qy - pxx,
            d + jx + qx + jy + qy + pxy, d - jx - qx + jy + qy - pxy,
            d - jx - qx - jy - qy + pxy, d + jx + qx - jy - qy - pxy]


def macros(f: Sequence[Any], gx: Any, gy: Any, half: Any) -> Tuple[Any, Any, Any]:
    """Density and velocity with the half force shift: u = (sum c_i f_i + g/2)/rho."""
    rho = sum(f)
    jx = sum(C[i][0] * f[i] for i in range(9))
    jy = sum(C[i][1] * f[i] for i in range(9))
    return rho, (jx + half * gx) / rho, (jy + half * gy) / rho


def collide(f: Sequence[Any], s: Sequence[Any], gx: Any = 0, gy: Any = 0,
            exact: bool = False) -> List[Any]:
    """One MRT collision at one node: lines L3 to L6."""
    half = Fraction(1, 2) if exact else 0.5
    rho, ux, uy = macros(f, gx, gy, half)                                     # @line L3
    m = to_moments(f)                                                         # @line L4
    meq = equilibrium_moments(rho, ux, uy)
    if gx or gy:
        mf = to_moments(guo_force(ux, uy, gx, gy, exact))
    else:
        mf = [0] * 9
    ms = [m[k] - s[k] * (m[k] - meq[k]) + (1 - half * s[k]) * mf[k]          # @line L5
          for k in range(9)]
    return from_moments(ms)                                                   # @line L6


def mrt_d2q9(nx: int, ny: int, s: Sequence[Any], steps: int,
             init: Callable[[int, int], Tuple[Any, Any, Any]],
             gx: Any = 0, gy: Any = 0, walls: bool = False, exact: bool = False,
             f0: Optional[List[List[Any]]] = None) -> MRTResult:
    """Run the MRT lattice Boltzmann method on an nx by ny lattice.

    s is the diagonal of S (see rates). init(x, y) returns (rho, ux, uy);
    the populations start at equilibrium unless f0 is given. Precondition:
    0 < s_k < 2 for the nonconserved moments, nx >= 1, ny >= 2 with walls.
    Cost: Theta(steps * nx * ny) node updates, each a constant number of
    operations (two 9 by 9 products with the fixed matrix M).
    """
    half = Fraction(1, 2) if exact else 0.5
    n = nx * ny
    if f0 is not None:
        f = [list(p) for p in f0]
    else:
        f = []
        for y in range(ny):                                                   # @line L1
            for x in range(nx):
                rho, ux, uy = init(x, y)
                f.append(equilibrium(rho, ux, uy, exact))
    for _ in range(steps):                                                    # @line L2
        post = [collide(f[k], s, gx, gy, exact) for k in range(n)]
        new = [[0] * 9 for _ in range(n)]
        for y in range(ny):                                                   # @line L7
            for x in range(nx):
                p = post[x + nx * y]
                for i in range(9):
                    xt = (x + C[i][0]) % nx
                    yt = y + C[i][1]
                    if walls and (yt < 0 or yt >= ny):
                        new[x + nx * y][OPP[i]] = p[i]
                        continue
                    new[xt + nx * (yt % ny)][i] = p[i]
        f = new
    rho_g, ux_g, uy_g = [], [], []
    for y in range(ny):                                                       # @line L8
        rr, uu, vv = [], [], []
        for x in range(nx):
            r, u, v = macros(f[x + nx * y], gx, gy, half)
            rr.append(r)
            uu.append(u)
            vv.append(v)
        rho_g.append(rr)
        ux_g.append(uu)
        uy_g.append(vv)
    return MRTResult(rho_g, ux_g, uy_g, steps, f)
