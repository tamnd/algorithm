# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kurganov-tadmor-scheme/. The authors are listed in prov/WYYX6A.jsonl.

"""The second order semi-discrete central scheme of Kurganov and Tadmor (2000).

The face flux is H = (F(U+) + F(U-)) / 2 - (a / 2)(U+ - U-), where U- and U+ are the values of a
limited piecewise linear reconstruction on the two sides of the face and a is the largest local
wave speed at the face. The scheme is an ODE system dU_j/dt = -(H_{j+1/2} - H_{j-1/2}) / dx,
integrated here with an SSP Runge-Kutta method. No Riemann solver and no eigenvectors are needed.
States are numbers (scalar laws) or tuples (systems). All halvings divide by integers, so
Fraction data stay exact.
"""

from math import sqrt

GAMMA = 1.4


def lin(*terms):
    """The linear combination sum of c * x over (c, x) pairs, for numbers or tuples."""
    c0, x0 = terms[0]
    if isinstance(x0, tuple):
        return tuple(sum(c * x[i] for c, x in terms) for i in range(len(x0)))
    return sum(c * x for c, x in terms)


def minmod3(a, b, c):
    if a > 0 and b > 0 and c > 0:
        return min(a, b, c)
    if a < 0 and b < 0 and c < 0:
        return max(a, b, c)
    return 0 * a


def slope(left, mid, right, theta):
    """The generalized minmod slope in cell units: minmod(theta dL, (dL + dR) / 2, theta dR)."""
    if isinstance(mid, tuple):
        return tuple(slope(l, m, r, theta) for l, m, r in zip(left, mid, right))
    dl, dr = mid - left, right - mid
    return minmod3(theta * dl, (dl + dr) / 2, theta * dr)


def face_fluxes(cells, flux, speed, theta=1.5, periodic=False):
    """The M + 1 face fluxes H_{j-1/2}, j = 0, ..., M."""
    if periodic:  # @line L1
        ext = [cells[-2], cells[-1]] + list(cells) + [cells[0], cells[1]]
    else:
        ext = [cells[0], cells[0]] + list(cells) + [cells[-1], cells[-1]]
    s = {k: slope(ext[k - 1], ext[k], ext[k + 1], theta) for k in range(1, len(ext) - 1)}  # @line L2
    out = []
    for k in range(1, len(ext) - 2):
        um = lin((1, ext[k]), (1, _div(s[k], 2)))  # @line L3
        up = lin((1, ext[k + 1]), (-1, _div(s[k + 1], 2)))
        a = max(speed(um), speed(up))  # @line L4
        out.append(_div(lin((1, flux(um)), (1, flux(up)), (-a, up), (a, um)), 2))  # @line L5
    return out


def _div(x, k):
    if isinstance(x, tuple):
        return tuple(a / k for a in x)
    return x / k


def rate(cells, dx, flux, speed, theta=1.5, periodic=False):
    """dU_j/dt = -(H_{j+1/2} - H_{j-1/2}) / dx."""
    h = face_fluxes(cells, flux, speed, theta, periodic)
    return [_div(lin((-1, h[j + 1]), (1, h[j])), dx) for j in range(len(cells))]  # @line L6


def step(cells, dt, dx, flux, speed, theta=1.5, periodic=False, method="ssp2"):
    """One step of forward Euler, Heun's SSP RK2 or the SSP RK3 of Shu and Osher."""
    L = lambda v: rate(v, dx, flux, speed, theta, periodic)
    u1 = [lin((1, c), (dt, d)) for c, d in zip(cells, L(cells))]  # @line L7
    if method == "euler":
        return u1
    if method == "ssp2":
        return [_div(lin((1, c), (1, a), (dt, d)), 2) for c, a, d in zip(cells, u1, L(u1))]
    u2 = [_div(lin((3, c), (1, a), (dt, d)), 4) for c, a, d in zip(cells, u1, L(u1))]
    return [_div(lin((1, c), (2, a), (2 * dt, d)), 3) for c, a, d in zip(cells, u2, L(u2))]


# Euler equations with U = (rho, rho u, E).


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


def euler_speed(q, g=GAMMA):
    """The spectral radius |u| + c of the flux Jacobian."""
    rho, u, p = cons_to_prim(q, g)
    return abs(u) + sqrt(g * p / rho)


def solve_euler(cells, dx, t_end, cfl=0.4, theta=1.5, periodic=False, method="ssp2", g=GAMMA):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux, speed = (lambda q: euler_flux(q, g)), (lambda q: euler_speed(q, g))
    while t < t_end - 1e-14:
        dt = min(cfl * dx / max(speed(q) for q in cells), t_end - t)
        cells = step(cells, dt, dx, flux, speed, theta, periodic, method)
        t += dt
        n += 1
    return cells, n
