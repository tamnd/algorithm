# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roe-solver/. The authors are listed in prov/9FFHHH.jsonl.

"""Roe approximate Riemann solver for the 1D Euler equations (Roe 1981), without an entropy fix.

The flux is (F_L + F_R)/2 - (1/2) sum_k |lambda_k| alpha_k r_k, where lambda_k and r_k are the
eigenvalues and eigenvectors of the Jacobian at the Roe average and alpha = R^{-1}(U_R - U_L).
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


def roe_average(ql, qr, g=GAMMA):
    """The Roe averages (u, H, c), weighted by the square roots of the densities."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    wl, wr = sqrt(rl), sqrt(rr)
    u = (wl * ul + wr * ur) / (wl + wr)
    h = (wl * (ql[2] + pl) / rl + wr * (qr[2] + pr) / rr) / (wl + wr)
    return u, h, sqrt((g - 1.0) * (h - 0.5 * u * u))


def roe_waves(ql, qr, g=GAMMA):
    """The eigenvalues, the right eigenvectors and the wave strengths of the Roe matrix."""
    u, h, c = roe_average(ql, qr, g)  # @line L1
    lam = (u - c, u, u + c)  # @line L2
    vecs = ((1.0, u - c, h - u * c), (1.0, u, 0.5 * u * u), (1.0, u + c, h + u * c))
    d0, d1, d2 = (b - a for a, b in zip(ql, qr))  # @line L3
    a2 = (g - 1.0) / (c * c) * (d0 * (h - u * u) + u * d1 - d2)
    a1 = (d0 * (u + c) - d1 - c * a2) / (2.0 * c)
    return lam, vecs, (a1, a2, d0 - a1 - a2)


def roe_flux(ql, qr, g=GAMMA):
    """The Roe flux at the face between the conserved states ql and qr."""
    lam, vecs, alpha = roe_waves(ql, qr, g)
    fl, fr = euler_flux(ql, g), euler_flux(qr, g)
    return tuple(0.5 * (fl[i] + fr[i]) - 0.5 * sum(abs(lam[k]) * alpha[k] * vecs[k][i] for k in range(3)) for i in range(3))  # @line L4


def roe_scalar(ul, ur, f, df):
    """The Roe flux for a scalar law: the speed is the slope of the chord of f."""
    a = (f(ur) - f(ul)) / (ur - ul) if ur != ul else df(ul)  # @line L1
    return (f(ul) + f(ur)) / 2 - abs(a) * (ur - ul) / 2  # @line L4


def step(cells, dt, dx, flux, periodic=False):
    """One forward Euler step of the conservative scheme. cells is a list of states (tuples or numbers)."""
    ext = ([cells[-1]] + list(cells) + [cells[0]]) if periodic else ([cells[0]] + list(cells) + [cells[-1]])  # @line L5
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]  # @line L6
    lam = dt / dx
    if isinstance(cells[0], tuple):  # @line L7
        return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]
    return [cells[j] - lam * (faces[j + 1] - faces[j]) for j in range(len(cells))]


def solve_euler(cells, dx, t_end, cfl=0.9, g=GAMMA, periodic=False):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux = lambda a, b: roe_flux(a, b, g)
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
