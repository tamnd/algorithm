# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hllc-riemann-solver/. The authors are listed in prov/HQEZ7E.jsonl.

"""HLLC approximate Riemann solver for the 1D Euler equations (Toro, Spruce and Speares 1994).

Two middle states, separated by a contact at speed S*, replace the one HLL state.
The outer speeds are the estimates of Einfeldt (1988) with Roe averages.
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


def wave_speeds(ql, qr, g=GAMMA):
    """Einfeldt estimates (S_L, S_R) with the Roe averages of u and H."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    cl, cr = sqrt(g * pl / rl), sqrt(g * pr / rr)
    wl, wr = sqrt(rl), sqrt(rr)
    u = (wl * ul + wr * ur) / (wl + wr)
    h = (wl * (ql[2] + pl) / rl + wr * (qr[2] + pr) / rr) / (wl + wr)
    c = sqrt((g - 1.0) * (h - 0.5 * u * u))
    return min(ul - cl, u - c), max(ur + cr, u + c)


def contact_speed(ql, qr, sl, sr, g=GAMMA):
    """S* from the jump conditions across S_L and S_R with equal middle pressure and velocity."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    return (pr - pl + rl * ul * (sl - ul) - rr * ur * (sr - ur)) / (rl * (sl - ul) - rr * (sr - ur))


def star_state(q, s, ss, g=GAMMA):
    """The middle state U*_K next to the outer wave of speed s = S_K, for the contact speed ss = S*."""
    rho, u, p = cons_to_prim(q, g)
    r = rho * (s - u) / (s - ss)
    return (r, r * ss, r * (q[2] / rho + (ss - u) * (ss + p / (rho * (s - u)))))


def hllc_flux(ql, qr, g=GAMMA):
    """The HLLC flux at the face between the conserved states ql and qr."""
    sl, sr = wave_speeds(ql, qr, g)  # @line L1
    if sl >= 0.0:  # @line L2
        return euler_flux(ql, g)
    if sr <= 0.0:  # @line L3
        return euler_flux(qr, g)
    ss = contact_speed(ql, qr, sl, sr, g)  # @line L4
    if ss >= 0.0:  # @line L5
        q, s = ql, sl
    else:
        q, s = qr, sr
    st = star_state(q, s, ss, g)  # @line L6
    return tuple(f + s * (a - b) for f, a, b in zip(euler_flux(q, g), st, q))  # @line L7


def step(cells, dt, dx, flux, periodic=False):
    """One forward Euler step of the conservative scheme with one ghost cell on each side."""
    ext = ([cells[-1]] + list(cells) + [cells[0]]) if periodic else ([cells[0]] + list(cells) + [cells[-1]])  # @line L8
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]  # @line L9
    lam = dt / dx
    return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]  # @line L10


def solve_euler(cells, dx, t_end, cfl=0.9, g=GAMMA, periodic=False):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux = lambda a, b: hllc_flux(a, b, g)
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
