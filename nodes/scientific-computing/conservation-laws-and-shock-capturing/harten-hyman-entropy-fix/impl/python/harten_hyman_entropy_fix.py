# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harten-hyman-entropy-fix/. The authors are listed in prov/QYXKT4.jsonl.

"""The Roe flux for the 1D Euler equations with the Harten-Hyman entropy fix (Harten and Hyman 1983).

At a transonic wave, where the speed is negative on the left of the wave and positive on its
right, the wave is split into two parts that move at the two side speeds. In the flux this
replaces |lambda| by (1 - beta) lambda_r - beta lambda_l with beta = (lambda_r - lambda) / (lambda_r - lambda_l).
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


def roe_waves(ql, qr, g=GAMMA):
    """Eigenvalues, right eigenvectors and wave strengths of the Roe matrix."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    wl, wr = sqrt(rl), sqrt(rr)
    u = (wl * ul + wr * ur) / (wl + wr)
    h = (wl * (ql[2] + pl) / rl + wr * (qr[2] + pr) / rr) / (wl + wr)
    c = sqrt((g - 1.0) * (h - 0.5 * u * u))
    lam = (u - c, u, u + c)
    vecs = ((1.0, u - c, h - u * c), (1.0, u, 0.5 * u * u), (1.0, u + c, h + u * c))
    d0, d1, d2 = (b - a for a, b in zip(ql, qr))
    a2 = (g - 1.0) / (c * c) * (d0 * (h - u * u) + u * d1 - d2)
    a1 = (d0 * (u + c) - d1 - c * a2) / (2.0 * c)
    return lam, vecs, (a1, a2, d0 - a1 - a2)


def fixed_speed(lam, lam_l, lam_r):
    """The Harten-Hyman value that replaces |lam| for a wave with side speeds lam_l and lam_r."""
    if lam_l < 0 < lam_r:  # @line L3
        beta = (lam_r - lam) / (lam_r - lam_l)
        return (1 - beta) * lam_r - beta * lam_l
    return abs(lam)  # @line L4


def side_speeds(ql, qr, lam, vecs, alpha, g=GAMMA):
    """Speeds of the acoustic waves 1 and 3 on both sides, from the states of the linear solution."""
    q1 = tuple(a + alpha[0] * r for a, r in zip(ql, vecs[0]))  # between waves 1 and 2
    q2 = tuple(b - alpha[2] * r for b, r in zip(qr, vecs[2]))  # between waves 2 and 3

    def speeds(q):
        rho, u, p = cons_to_prim(q, g)
        c = sqrt(g * max(p, 0.0) / rho)
        return u - c, u + c

    return (speeds(ql)[0], speeds(q1)[0]), (speeds(q2)[1], speeds(qr)[1])


def roe_flux(ql, qr, g=GAMMA, fix=True):
    """The Roe flux, with the Harten-Hyman fix on the two acoustic waves when fix is True."""
    lam, vecs, alpha = roe_waves(ql, qr, g)  # @line L1
    mod = [abs(x) for x in lam]
    if fix:
        (l1, r1), (l3, r3) = side_speeds(ql, qr, lam, vecs, alpha, g)  # @line L2
        mod[0] = fixed_speed(lam[0], l1, r1)
        mod[2] = fixed_speed(lam[2], l3, r3)
    fl, fr = euler_flux(ql, g), euler_flux(qr, g)
    return tuple(0.5 * (fl[i] + fr[i]) - 0.5 * sum(mod[k] * alpha[k] * vecs[k][i] for k in range(3)) for i in range(3))  # @line L5


def roe_scalar(ul, ur, f, df, fix=True):
    """The Murman-Roe flux for a scalar convex law, with the fix when fix is True."""
    a = (f(ur) - f(ul)) / (ur - ul) if ur != ul else df(ul)  # @line L1
    s = fixed_speed(a, df(ul), df(ur)) if fix else abs(a)  # @line L2
    return (f(ul) + f(ur)) / 2 - s * (ur - ul) / 2  # @line L5


def step(cells, dt, dx, flux):
    """One forward Euler step with one outflow ghost cell on each side."""
    ext = [cells[0]] + list(cells) + [cells[-1]]
    faces = [flux(ext[j], ext[j + 1]) for j in range(len(ext) - 1)]
    lam = dt / dx
    if isinstance(cells[0], tuple):
        return [tuple(q - lam * (b - a) for q, a, b in zip(cells[j], faces[j], faces[j + 1])) for j in range(len(cells))]
    return [cells[j] - lam * (faces[j + 1] - faces[j]) for j in range(len(cells))]


def solve_euler(cells, dx, t_end, cfl=0.9, g=GAMMA, fix=True):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux = lambda a, b: roe_flux(a, b, g, fix)
    while t < t_end - 1e-14:
        smax = 0.0
        for q in cells:
            rho, u, p = cons_to_prim(q, g)
            smax = max(smax, abs(u) + sqrt(g * p / rho))
        dt = min(cfl * dx / smax, t_end - t)
        cells = step(cells, dt, dx, flux)
        t += dt
        n += 1
    return cells, n
