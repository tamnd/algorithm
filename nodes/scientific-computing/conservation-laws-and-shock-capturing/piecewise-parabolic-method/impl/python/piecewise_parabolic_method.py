# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piecewise-parabolic-method/. The authors are listed in prov/4Q3HCS.jsonl.

"""The piecewise parabolic method of Colella and Woodward (1984).

Each cell gets a parabola with the cell average as its mean. The face values come from a fourth
order interpolation with limited slopes, and three tests make the parabola monotone in the cell.
For linear advection, advect_step moves the parabolas exactly over one time step (the PPM scheme
for u_t + c u_x = 0 with c > 0). For the Euler equations, solve_euler uses the PPM face values per
conserved component in a method of lines with the HLL flux and SSP RK3; it leaves out the contact
steepening, flattening and characteristic tracing of the full gas dynamics scheme.
Fraction data stay exact.
"""

from math import sqrt

GAMMA = 1.4


def mc_slope(left, mid, right):
    """The monotonized central slope of Colella and Woodward, in cell units."""
    dl, dr = mid - left, right - mid
    if dl * dr <= 0:
        return 0 * dl
    s = min(abs(dl + dr) / 2, 2 * abs(dl), 2 * abs(dr))
    return s if dl > 0 else -s


def constrain(al, a, ar):
    """The three monotonicity tests: returns the new (aL, aR) for a cell with average a."""
    if (ar - a) * (a - al) <= 0:  # @line L4
        return a, a
    d, m = ar - al, a - (al + ar) / 2
    if d * m > d * d / 6:
        return 3 * a - 2 * ar, ar
    if -d * d / 6 > d * m:
        return al, 3 * a - 2 * al
    return al, ar


def ppm_faces(cells, periodic=False):
    """The constrained face values (aL, aR) of every cell, for scalar data."""
    m = len(cells)
    if periodic:  # @line L1
        ext = list(cells[-3:]) + list(cells) + list(cells[:3])
    else:
        ext = [cells[0]] * 3 + list(cells) + [cells[-1]] * 3
    d = [0 * ext[0]] + [mc_slope(ext[k - 1], ext[k], ext[k + 1]) for k in range(1, len(ext) - 1)]  # @line L2
    face = {k: (ext[k] + ext[k + 1]) / 2 - (d[k + 1] - d[k]) / 6 for k in range(1, len(ext) - 2)}  # @line L3
    out = []
    for j in range(m):
        k = j + 3
        out.append(constrain(face[k - 1], ext[k], face[k]))
    return out


def parabola(al, a, ar, xi):
    """The parabola of a cell at the local coordinate xi in [0, 1]."""
    return al + xi * ((ar - al) + 6 * (a - (al + ar) / 2) * (1 - xi))


def right_flux_average(al, a, ar, nu):
    """The average of the parabola over [1 - nu, 1]: the flux through the right face divided by c."""
    return ar - nu / 2 * ((ar - al) - (1 - 2 * nu / 3) * 6 * (a - (al + ar) / 2))  # @line L5


def advect_step(cells, nu, periodic=True):
    """One PPM step for u_t + c u_x = 0, c > 0, with Courant number 0 <= nu <= 1."""
    pf = ppm_faces(cells, periodic)
    flux = [right_flux_average(al, a, ar, nu) for (al, ar), a in zip(pf, cells)]
    inflow = flux[-1] if periodic else cells[0]
    return [a - nu * (flux[j] - (flux[j - 1] if j > 0 else inflow)) for j, a in enumerate(cells)]  # @line L6


# Euler equations with U = (rho, rho u, E), in a method of lines.


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


def hll_flux(ql, qr, g=GAMMA):
    """HLL with the speed estimates of Davis."""
    rl, ul, pl = cons_to_prim(ql, g)
    rr, ur, pr = cons_to_prim(qr, g)
    cl, cr = sqrt(g * pl / rl), sqrt(g * pr / rr)
    sl, sr = min(ul - cl, ur - cr), max(ul + cl, ur + cr)
    fl, fr = euler_flux(ql, g), euler_flux(qr, g)
    if sl >= 0:
        return fl
    if sr <= 0:
        return fr
    return tuple((sr * a - sl * b + sl * sr * (y - x)) / (sr - sl) for a, b, x, y in zip(fl, fr, ql, qr))


def rate(cells, dx, periodic=False, g=GAMMA):
    m = len(cells)
    comps = [ppm_faces([q[c] for q in cells], periodic) for c in range(3)]
    left = [tuple(comps[c][j][0] for c in range(3)) for j in range(m)]
    right = [tuple(comps[c][j][1] for c in range(3)) for j in range(m)]
    if periodic:
        pairs = [(right[j - 1], left[j]) for j in range(m)] + [(right[-1], left[0])]
    else:
        pairs = [(cells[0], left[0])] + [(right[j - 1], left[j]) for j in range(1, m)] + [(right[-1], cells[-1])]
    h = [hll_flux(a, b, g) for a, b in pairs]
    return [tuple(-(h[j + 1][c] - h[j][c]) / dx for c in range(3)) for j in range(m)]


def solve_euler(cells, dx, t_end, cfl=0.5, periodic=False, g=GAMMA):
    """March to t_end with SSP RK3 and dt = cfl dx / max(|u| + c). Returns (cells, steps)."""
    t, n = 0.0, 0

    def speed(q):
        rho, u, p = cons_to_prim(q, g)
        return abs(u) + sqrt(g * p / rho)

    def comb(a, x, b, y, s, z):
        return tuple(a * xi + b * yi + s * zi for xi, yi, zi in zip(x, y, z))

    while t < t_end - 1e-14:
        dt = min(cfl * dx / max(speed(q) for q in cells), t_end - t)
        L1 = rate(cells, dx, periodic, g)
        u1 = [comb(1.0, c, 0.0, c, dt, d) for c, d in zip(cells, L1)]
        L2 = rate(u1, dx, periodic, g)
        u2 = [comb(0.75, c, 0.25, a, 0.25 * dt, d) for c, a, d in zip(cells, u1, L2)]
        L3 = rate(u2, dx, periodic, g)
        cells = [comb(1.0 / 3.0, c, 2.0 / 3.0, a, 2.0 / 3.0 * dt, d) for c, a, d in zip(cells, u2, L3)]
        t += dt
        n += 1
    return cells, n
