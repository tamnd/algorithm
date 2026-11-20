# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hll-riemann-solver/. The authors are listed in prov/MA9G95.jsonl.

"""HLL approximate Riemann solver for the 1D Euler equations (Harten, Lax and van Leer 1983).

The fan between the slowest speed S_L and the fastest speed S_R is replaced by one
constant state. Two speed estimates are given: the one of Davis (1988) and the one of
Einfeldt (1988), which uses Roe averages (HLLE).
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


def wave_speeds(ql, qr, g=GAMMA, method="einfeldt"):
    """Estimates (S_L, S_R) of the slowest and the fastest signal speed."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    cl, cr = sqrt(g * pl / rl), sqrt(g * pr / rr)
    if method == "davis":
        return min(ul - cl, ur - cr), max(ul + cl, ur + cr)
    wl, wr = sqrt(rl), sqrt(rr)  # Roe averages of u and the enthalpy H = (E + p) / rho
    hl, hr = (ql[2] + pl) / rl, (qr[2] + pr) / rr
    u = (wl * ul + wr * ur) / (wl + wr)
    h = (wl * hl + wr * hr) / (wl + wr)
    c = sqrt((g - 1.0) * (h - 0.5 * u * u))
    return min(ul - cl, u - c), max(ur + cr, u + c)


def hll_flux(ql, qr, g=GAMMA, method="einfeldt"):
    """The HLL flux at the face between the conserved states ql and qr."""
    sl, sr = wave_speeds(ql, qr, g, method)  # @line L1
    fl, fr = euler_flux(ql, g), euler_flux(qr, g)
    if sl >= 0.0:  # @line L2
        return fl
    if sr <= 0.0:  # @line L3
        return fr
    return tuple((sr * a - sl * b + sl * sr * (y - x)) / (sr - sl) for a, b, x, y in zip(fl, fr, ql, qr))  # @line L4


def hll_scalar(ul, ur, f, df):
    """The HLL flux for a scalar law u_t + f(u)_x = 0 with speeds from f' at the two states."""
    sl, sr = min(df(ul), df(ur)), max(df(ul), df(ur))  # @line L1
    if sl >= 0:  # @line L2
        return f(ul)
    if sr <= 0:  # @line L3
        return f(ur)
    return (sr * f(ul) - sl * f(ur) + sl * sr * (ur - ul)) / (sr - sl)  # @line L4


def hll_state(ql, qr, sl, sr, g=GAMMA):
    """The HLL intermediate state U* (the average of the exact fan when the speeds bound it)."""
    fl, fr = euler_flux(ql, g), euler_flux(qr, g)
    return tuple((sr * y - sl * x - (b - a)) / (sr - sl) for a, b, x, y in zip(fl, fr, ql, qr))


def step(cells, dt, dx, flux, periodic=False):
    """One forward Euler step of the conservative scheme. cells is a list of states (tuples or numbers)."""
    ext = ([cells[-1]] + list(cells) + [cells[0]]) if periodic else ([cells[0]] + list(cells) + [cells[-1]])  # @line L5
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]  # @line L6
    lam = dt / dx
    if isinstance(cells[0], tuple):  # @line L7
        return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]
    return [cells[j] - lam * (faces[j + 1] - faces[j]) for j in range(len(cells))]


def solve_euler(cells, dx, t_end, cfl=0.9, g=GAMMA, periodic=False, method="einfeldt"):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux = lambda a, b: hll_flux(a, b, g, method)
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
