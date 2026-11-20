# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flux-vector-splitting/. The authors are listed in prov/6X7CE5.jsonl.

"""Flux vector splitting for the 1D Euler equations: Steger-Warming (1981) and van Leer (1982).

The flux is written as F(U) = F+(U) + F-(U), where F+ has only nonnegative and F- only
nonpositive wave speeds. The face flux is F+(U_L) + F-(U_R): each part is taken from the
side it comes from.
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


def steger_warming(q, g=GAMMA):
    """Return (F+, F-) of Steger and Warming: the eigenvalues split by sign."""
    rho, u, p = cons_to_prim(q, g)
    c = sqrt(g * p / rho)
    h = (q[2] + p) / rho
    lam = (u - c, u, u + c)  # @line L1
    vecs = ((1.0, u - c, h - u * c), (1.0, u, 0.5 * u * u), (1.0, u + c, h + u * c))
    weights = (rho / (2.0 * g), rho * (g - 1.0) / g, rho / (2.0 * g))  # U = sum of weights[k] vecs[k]
    parts = []
    for sign in (1.0, -1.0):
        lp = [0.5 * (x + sign * abs(x)) for x in lam]
        parts.append(tuple(sum(lp[k] * weights[k] * vecs[k][i] for k in range(3)) for i in range(3)))  # @line L2
    return parts[0], parts[1]


def van_leer(q, g=GAMMA):
    """Return (F+, F-) of van Leer: polynomials in the Mach number, smooth at M = -1 and M = 1."""
    rho, u, p = cons_to_prim(q, g)
    c = sqrt(g * p / rho)
    mach = u / c
    if mach >= 1.0:  # @line L3
        return euler_flux(q, g), (0.0, 0.0, 0.0)
    if mach <= -1.0:
        return (0.0, 0.0, 0.0), euler_flux(q, g)
    parts = []
    for sign in (1.0, -1.0):
        mass = sign * 0.25 * rho * c * (mach + sign) ** 2  # @line L4
        a = (g - 1.0) * u + sign * 2.0 * c
        parts.append((mass, mass * a / g, mass * a * a / (2.0 * (g * g - 1.0))))  # @line L5
    return parts[0], parts[1]


def fvs_flux(ql, qr, split=van_leer, g=GAMMA):
    """The face flux F+(U_L) + F-(U_R)."""
    fp, _ = split(ql, g)
    _, fm = split(qr, g)
    return tuple(a + b for a, b in zip(fp, fm))  # @line L6


def fvs_scalar(ul, ur, fplus, fminus):
    """The same idea for a scalar law f = f+ + f- with f+ nondecreasing and f- nonincreasing."""
    return fplus(ul) + fminus(ur)


def step(cells, dt, dx, flux, periodic=False):
    """One forward Euler step of the conservative scheme with one ghost cell on each side."""
    ext = ([cells[-1]] + list(cells) + [cells[0]]) if periodic else ([cells[0]] + list(cells) + [cells[-1]])  # @line L7
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]  # @line L8
    lam = dt / dx
    if isinstance(cells[0], tuple):
        return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]  # @line L9
    return [cells[j] - lam * (faces[j + 1] - faces[j]) for j in range(len(cells))]


def solve_euler(cells, dx, t_end, cfl=0.9, g=GAMMA, periodic=False, split=van_leer):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux = lambda a, b: fvs_flux(a, b, split, g)
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
