# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rusanov-flux/. The authors are listed in prov/PDKD22.jsonl.

"""Rusanov (local Lax-Friedrichs) flux for scalar laws and the 1D Euler equations.

F(U_L, U_R) = (F(U_L) + F(U_R)) / 2 - (s / 2) (U_R - U_L), with s the largest
local wave speed. The first order finite volume update uses outflow ghost cells
(one on each side, filled by copy) or a periodic grid.
"""

from math import sqrt

GAMMA = 1.4


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


def max_speed(q, g=GAMMA):
    rho, u, p = cons_to_prim(q, g)
    return abs(u) + sqrt(g * p / rho)


def rusanov_euler(ql, qr, g=GAMMA):
    """The Rusanov flux of the Euler equations between conserved states ql and qr."""
    s = max(max_speed(ql, g), max_speed(qr, g))  # @line L1
    fl, fr = euler_flux(ql, g), euler_flux(qr, g)
    return tuple(0.5 * (a + b) - 0.5 * s * (y - x) for a, b, x, y in zip(fl, fr, ql, qr))  # @line L2


def rusanov_scalar(ul, ur, f, df):
    """The Rusanov flux of u_t + f(u)_x = 0; df is f'. For convex f the endpoint speeds bound |f'|."""
    s = max(abs(df(ul)), abs(df(ur)))  # @line L1
    return 0.5 * (f(ul) + f(ur)) - 0.5 * s * (ur - ul)  # @line L2


def step(cells, dt, dx, flux, periodic=False):
    """One forward Euler step of the conservative scheme. cells is a list of states (tuples or floats)."""
    if periodic:  # @line L3
        ext = [cells[-1]] + list(cells) + [cells[0]]
    else:
        ext = [cells[0]] + list(cells) + [cells[-1]]
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]  # @line L4
    lam = dt / dx
    if isinstance(cells[0], tuple):  # @line L5
        return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]
    return [cells[j] - lam * (faces[j + 1] - faces[j]) for j in range(len(cells))]


def solve_euler(cells, dx, t_end, cfl=0.9, g=GAMMA, periodic=False):
    """March the Euler equations to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux = lambda a, b: rusanov_euler(a, b, g)
    while t < t_end - 1e-14:
        smax = max(max_speed(q, g) for q in cells)
        dt = min(cfl * dx / smax, t_end - t)
        cells = step(cells, dt, dx, flux, periodic)
        t += dt
        n += 1
    return cells, n
