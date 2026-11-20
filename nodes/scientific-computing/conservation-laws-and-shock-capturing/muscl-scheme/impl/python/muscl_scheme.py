# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muscl-scheme/. The authors are listed in prov/7J4C0V.jsonl.

"""MUSCL-Hancock scheme (van Leer 1979; Toro 2009, Chapter 14) for scalar laws and the 1D Euler equations.

Each cell gets a limited linear slope. The two boundary values of the cell are moved by half a time
step with the flux difference across the cell, and a Riemann solver gives the face flux from the
values on the two sides of the face. The reconstruction is done on the conserved variables.
"""

from math import sqrt

GAMMA = 1.4


def minmod(a, b):
    if a * b <= 0:
        return 0 * a
    return a if abs(a) < abs(b) else b


def van_leer(a, b):
    if a * b <= 0:
        return 0 * a
    return 2 * a * b / (a + b)


def mc(a, b):
    """The monotonized central limiter: minmod(2a, (a + b) / 2, 2b)."""
    if a * b <= 0:
        return 0 * a
    c = (a + b) / 2
    s = 1 if a > 0 else -1
    return s * min(2 * abs(a), abs(c), 2 * abs(b))


LIMITERS = {"minmod": minmod, "vanleer": van_leer, "mc": mc}


def _pad(cells, periodic):
    if periodic:
        return [cells[-2], cells[-1]] + list(cells) + [cells[0], cells[1]]
    return [cells[0], cells[0]] + list(cells) + [cells[-1], cells[-1]]


def _comb(x, y, s):
    """x + s y for numbers or tuples."""
    if isinstance(x, tuple):
        return tuple(a + s * b for a, b in zip(x, y))
    return x + s * y


def _diff(x, y):
    return _comb(x, y, -1)


def _slope(left, mid, right, lim):
    if isinstance(mid, tuple):
        return tuple(lim(m - l, r - m) for l, m, r in zip(left, mid, right))
    return lim(mid - left, right - mid)


def step(cells, dt, dx, flux, riemann, limiter="minmod", periodic=False):
    """One MUSCL-Hancock step. flux(U) is the physical flux, riemann(UL, UR) the face flux."""
    lim = LIMITERS[limiter]
    ext = _pad(cells, periodic)  # @line L1
    half = dt / (2 * dx)
    lo, hi = [], []
    for k in range(1, len(ext) - 1):
        d = _halve(_slope(ext[k - 1], ext[k], ext[k + 1], lim))  # @line L2
        um, up = _comb(ext[k], d, -1), _comb(ext[k], d, 1)  # @line L3
        df = _diff(flux(up), flux(um))
        lo.append(_comb(um, df, -half))  # @line L4
        hi.append(_comb(up, df, -half))
    faces = [riemann(hi[k], lo[k + 1]) for k in range(len(cells) + 1)]  # @line L5
    lam = dt / dx
    return [_comb(cells[j], _diff(faces[j + 1], faces[j]), -lam) for j in range(len(cells))]  # @line L6


def _halve(d):
    """Half of a slope; exact for Fraction data."""
    if isinstance(d, tuple):
        return tuple(x / 2 for x in d)
    return d / 2


# Scalar laws.


def upwind_flux(a):
    """The exact Riemann flux of u_t + a u_x = 0."""
    return lambda ul, ur: a * ul if a >= 0 else a * ur


def burgers_godunov(ul, ur):
    """The exact Riemann (Godunov) flux of Burgers' equation u_t + (u^2 / 2)_x = 0."""
    if ul <= ur:
        if ul > 0:
            return ul * ul / 2
        if ur < 0:
            return ur * ur / 2
        return 0 * ul
    return max(ul * ul, ur * ur) / 2


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


def hllc_flux(ql, qr, g=GAMMA):
    """HLLC flux (Toro, Spruce and Speares 1994) with the speed estimates of Davis."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    cl, cr = sqrt(g * pl / rl), sqrt(g * pr / rr)
    sl, sr = min(ul - cl, ur - cr), max(ul + cl, ur + cr)
    if sl >= 0.0:
        return euler_flux(ql, g)
    if sr <= 0.0:
        return euler_flux(qr, g)
    ss = (pr - pl + rl * ul * (sl - ul) - rr * ur * (sr - ur)) / (rl * (sl - ul) - rr * (sr - ur))
    q, s, rho, u, p = (ql, sl, rl, ul, pl) if ss >= 0.0 else (qr, sr, rr, ur, pr)
    k = rho * (s - u) / (s - ss)
    star = (k, k * ss, k * (q[2] / rho + (ss - u) * (ss + p / (rho * (s - u)))))
    f = euler_flux(q, g)
    return tuple(a + s * (b - c) for a, b, c in zip(f, star, q))


def max_speed(cells, g=GAMMA):
    smax = 0.0
    for q in cells:
        rho, u, p = cons_to_prim(q, g)
        smax = max(smax, abs(u) + sqrt(g * p / rho))
    return smax


def solve_euler(cells, dx, t_end, cfl=0.8, limiter="minmod", periodic=False, g=GAMMA):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux, riemann = (lambda q: euler_flux(q, g)), (lambda a, b: hllc_flux(a, b, g))
    while t < t_end - 1e-14:
        dt = min(cfl * dx / max_speed(cells, g), t_end - t)
        cells = step(cells, dt, dx, flux, riemann, limiter, periodic)
        t += dt
        n += 1
    return cells, n
