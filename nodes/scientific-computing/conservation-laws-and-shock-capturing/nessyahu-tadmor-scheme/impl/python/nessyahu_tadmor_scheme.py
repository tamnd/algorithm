# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nessyahu-tadmor-scheme/. The authors are listed in prov/40T9VJ.jsonl.

"""The second order staggered central scheme of Nessyahu and Tadmor (1990).

One staggered step maps the averages U_j over the cells [x_{j-1/2}, x_{j+1/2}] to the averages
W_{j+1/2} over the staggered cells [x_j, x_{j+1}]:

    W_{j+1/2} = (U_j + U_{j+1}) / 2 + (U'_j - U'_{j+1}) / 8 - lam (F(U_{j+1}^{n+1/2}) - F(U_j^{n+1/2})),

with U_j^{n+1/2} = U_j - (lam / 2) F'_j and lam = dt / dx. U'_j and F'_j are limited differences
of U and of F(U), so no Riemann solver and no Jacobian is needed. The next step maps W back to the
original cells. States are numbers (scalar laws) or tuples (systems). All divisions are by
integers or by dx, so Fraction data stay exact.
"""

from math import sqrt

GAMMA = 1.4


def lin(*terms):
    """The linear combination sum of c * x over (c, x) pairs, for numbers or tuples."""
    x0 = terms[0][1]
    if isinstance(x0, tuple):
        return tuple(sum(c * x[i] for c, x in terms) for i in range(len(x0)))
    return sum(c * x for c, x in terms)


def _div(x, k):
    if isinstance(x, tuple):
        return tuple(a / k for a in x)
    return x / k


def minmod3(a, b, c):
    if a > 0 and b > 0 and c > 0:
        return min(a, b, c)
    if a < 0 and b < 0 and c < 0:
        return max(a, b, c)
    return 0 * a


def slope(left, mid, right, theta):
    """The minmod-theta slope in cell units: minmod(theta dL, (dL + dR) / 2, theta dR)."""
    if isinstance(mid, tuple):
        return tuple(slope(l, m, r, theta) for l, m, r in zip(left, mid, right))
    dl, dr = mid - left, right - mid
    return minmod3(theta * dl, (dl + dr) / 2, theta * dr)


def staggered_step(cells, lam, flux, theta=1.5, periodic=False, shift=0):
    """One staggered step. shift = 0 gives out[j] from cells j and j + 1 (the averages over
    [x_j, x_{j+1}]); shift = 1 gives out[j] from cells j - 1 and j. Outflow boundaries copy the
    end cells into the ghost cells."""
    m = len(cells)
    if periodic:  # @line L1
        ext = [cells[-2], cells[-1]] + list(cells) + [cells[0], cells[1]]
    else:
        ext = [cells[0], cells[0]] + list(cells) + [cells[-1], cells[-1]]
    fx = [flux(q) for q in ext]
    du, mid = {}, {}
    for k in range(1, len(ext) - 1):
        du[k] = slope(ext[k - 1], ext[k], ext[k + 1], theta)  # @line L2
        df = slope(fx[k - 1], fx[k], fx[k + 1], theta)
        mid[k] = lin((1, ext[k]), (-lam / 2, df))  # @line L3
    out = []
    for j in range(m):
        k = j + 2 - shift
        avg = _div(lin((1, ext[k]), (1, ext[k + 1])), 2)
        out.append(lin((1, avg), (1, _div(lin((1, du[k]), (-1, du[k + 1])), 8)), (-lam, flux(mid[k + 1])), (lam, flux(mid[k]))))  # @line L4
    return out


def step(cells, dt, dx, flux, theta=1.5, periodic=False):
    """Two staggered steps of length dt: to the staggered grid and back. Returns cells at t + 2 dt."""
    lam = dt / dx
    w = staggered_step(cells, lam, flux, theta, periodic, 0)  # @line L5
    return staggered_step(w, lam, flux, theta, periodic, 1)


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
    rho, u, p = cons_to_prim(q, g)
    return abs(u) + sqrt(g * p / rho)


def solve_euler(cells, dx, t_end, cfl=0.4, theta=1.5, periodic=False, g=GAMMA):
    """March to t_end in pairs of staggered steps with dt = cfl dx / max(|u| + c).
    Returns (cells, number of staggered steps)."""
    t, n = 0.0, 0
    flux = lambda q: euler_flux(q, g)
    while t < t_end - 1e-14:
        dt = min(cfl * dx / max(euler_speed(q, g) for q in cells), (t_end - t) / 2)
        cells = step(cells, dt, dx, flux, theta, periodic)
        t += 2 * dt
        n += 2
    return cells, n
