# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ausm-scheme/. The authors are listed in prov/H6NW64.jsonl.

"""The AUSM flux of Liou and Steffen (1993) for the 1D Euler equations.

The Euler flux is split into a convective part, u times (rho, rho u, rho H), and a pressure part
(0, p, 0). The convective part is written as M c (rho, rho u, rho H) and upwinded with one
interface Mach number M_L+ + M_R-. The pressure is p_L+ + p_R-. The split polynomials take
exact Fraction input; the full flux uses a square root for the sound speed.
"""

from math import sqrt

GAMMA = 1.4


def mach_split(mach):
    """(M+, M-): van Leer's Mach number split."""
    if abs(mach) <= 1:  # @line L1
        return (mach + 1) ** 2 / 4, -((mach - 1) ** 2) / 4
    return (mach + abs(mach)) / 2, (mach - abs(mach)) / 2


def pressure_split(mach, p):
    """(p+, p-): the pressure split with the weights (M +- 1)^2 (2 -+ M) / 4."""
    if abs(mach) <= 1:  # @line L2
        return p * (mach + 1) ** 2 * (2 - mach) / 4, p * (mach - 1) ** 2 * (2 + mach) / 4
    return (p, 0 * p) if mach > 0 else (0 * p, p)


def prim_to_cons(w, g=GAMMA):
    rho, u, p = w
    return (rho, rho * u, p / (g - 1.0) + 0.5 * rho * u * u)


def cons_to_prim(q, g=GAMMA):
    rho, m, e = q
    u = m / rho
    return (rho, u, (g - 1.0) * (e - 0.5 * m * u))


def euler_flux(q, g=GAMMA):
    rho, m, e = q
    u = m / rho
    p = (g - 1.0) * (e - 0.5 * m * u)
    return (m, m * u + p, u * (e + p))


def _side(q, g):
    """(M, p, c (rho, rho u, rho H)) of one state."""
    rho, u, p = cons_to_prim(q, g)
    c = sqrt(g * p / rho)
    return u / c, p, (rho * c, rho * c * u, c * (q[2] + p))


def ausm_flux(ql, qr, g=GAMMA):
    """The AUSM face flux between the states ql and qr."""
    ml, pl, phil = _side(ql, g)
    mr, pr, phir = _side(qr, g)
    m_half = mach_split(ml)[0] + mach_split(mr)[1]  # @line L3
    p_half = pressure_split(ml, pl)[0] + pressure_split(mr, pr)[1]  # @line L4
    phi = phil if m_half >= 0 else phir  # @line L5
    return (m_half * phi[0], m_half * phi[1] + p_half, m_half * phi[2])  # @line L6


def step(cells, dt, dx, flux=ausm_flux, periodic=False):
    """One first order finite volume step with the face flux flux(U_L, U_R)."""
    ext = ([cells[-1]] + list(cells) + [cells[0]]) if periodic else ([cells[0]] + list(cells) + [cells[-1]])  # @line L7
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]
    lam = dt / dx
    return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]  # @line L8


def solve_euler(cells, dx, t_end, cfl=0.5, flux=ausm_flux, periodic=False, g=GAMMA):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps).

    On Sod's tube the first step gives a negative pressure for cfl above about 0.657.
    """
    t, n = 0.0, 0
    while t < t_end - 1e-14:
        smax = 0.0
        for q in cells:
            rho, u, p = cons_to_prim(q, g)
            smax = max(smax, abs(u) + sqrt(g * p / rho))
        dt = min(cfl * dx / smax, t_end - t)
        cells = step(cells, dt, dx, flux, periodic)
        t += dt
        n += 1
    return cells, n
