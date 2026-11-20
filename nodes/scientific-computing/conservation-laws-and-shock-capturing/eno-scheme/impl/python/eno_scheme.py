# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eno-scheme/. The authors are listed in prov/Z4ZSZ2.jsonl.

"""Finite volume ENO reconstruction of order r (Harten, Engquist, Osher and Chakravarthy 1987)
with the Rusanov flux and the SSP RK3 of Shu and Osher (1988).

In each cell the stencil of r cells grows one cell at a time, to the side where the undivided
difference of the cell averages is smaller in size. The face values are the derivatives of the
Newton interpolant of the primitive function on the r + 1 faces of the stencil. States are numbers
(scalar laws) or tuples (systems, reconstructed componentwise). Fraction data stay exact.
"""

from fractions import Fraction
from functools import lru_cache
from math import sqrt

GAMMA = 1.4


def newton_derivative(values, x):
    """P'(x), where P interpolates values[m] at the nodes m = 0, 1, ..., in Newton form."""
    c = list(values)
    n = len(c)
    for lev in range(1, n):  # divided differences on unit spaced nodes
        for i in range(n - 1, lev - 1, -1):
            c[i] = (c[i] - c[i - 1]) / lev
    total = 0
    for k in range(1, n):  # d/dx of prod_{q<k} (x - q)
        for s in range(k):
            p = c[k]
            for q in range(k):
                if q != s:
                    p *= x - q
            total += p
    return total


@lru_cache(maxsize=None)
def face_weights(r, k):
    """Weights for the stencil of cells i - k, ..., i - k + r - 1: the value at the right face of
    cell i is sum(wr[n] v[i - k + n]) and at the left face sum(wl[n] v[i - k + n])."""
    wr, wl = [], []
    for n in range(r):
        prim = [Fraction(1 if m > n else 0) for m in range(r + 1)]  # primitive of the unit vector e_n
        wr.append(newton_derivative(prim, Fraction(k + 1)))
        wl.append(newton_derivative(prim, Fraction(k)))
    return tuple(wr), tuple(wl)


def _undivided(v, a, l):
    """The l-th undivided difference of v over the cells a, ..., a + l."""
    d = v[a:a + l + 1]
    for _ in range(l):
        d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
    return d[0]


def eno_faces(v, r):
    """For a list v with r ghost cells on each side, return (minus, plus) for the cells r - 1, ...,
    len(v) - r: the reconstructed values at the right face and at the left face of each cell."""
    exact = isinstance(v[0], Fraction) or isinstance(v[0], int)
    minus, plus = [], []
    for i in range(r - 1, len(v) - r + 1):
        left = i  # @line L2
        for l in range(1, r):
            if abs(_undivided(v, left - 1, l)) < abs(_undivided(v, left, l)):  # @line L3
                left -= 1
        wr, wl = face_weights(r, i - left)  # @line L4
        if not exact:
            wr, wl = [float(w) for w in wr], [float(w) for w in wl]
        cells = v[left:left + r]
        minus.append(sum(w * c for w, c in zip(wr, cells)))
        plus.append(sum(w * c for w, c in zip(wl, cells)))
    return minus, plus


def _comp(x, i):
    return x[i] if isinstance(x, tuple) else x


def rate(cells, dx, flux, speed, r=3, periodic=False):
    """dU_j/dt = -(H_{j+1/2} - H_{j-1/2}) / dx with ENO face values and the Rusanov flux."""
    m = len(cells)
    if periodic:  # @line L1
        ext = list(cells[-r:]) + list(cells) + list(cells[:r])
    else:
        ext = [cells[0]] * r + list(cells) + [cells[-1]] * r
    system = isinstance(cells[0], tuple)
    if system:
        parts = [eno_faces([q[c] for q in ext], r) for c in range(len(cells[0]))]
        minus = [tuple(p[0][j] for p in parts) for j in range(m + 2)]
        plus = [tuple(p[1][j] for p in parts) for j in range(m + 2)]
    else:
        minus, plus = eno_faces(ext, r)
    h = []
    for j in range(m + 1):  # face between list entries j and j + 1, that is cells j - 1 and j
        ul, ur = minus[j], plus[j + 1]
        a = max(speed(ul), speed(ur))
        fl, fr = flux(ul), flux(ur)
        if system:
            h.append(tuple((fl[c] + fr[c] - a * (ur[c] - ul[c])) / 2 for c in range(len(ul))))  # @line L5
        else:
            h.append((fl + fr - a * (ur - ul)) / 2)
    if system:
        return [tuple(-(h[j + 1][c] - h[j][c]) / dx for c in range(len(h[0]))) for j in range(m)]  # @line L6
    return [-(h[j + 1] - h[j]) / dx for j in range(m)]


def _axpy(*terms):
    x0 = terms[0][1]
    if isinstance(x0, tuple):
        return tuple(sum(c * x[i] for c, x in terms) for i in range(len(x0)))
    return sum(c * x for c, x in terms)


def step(cells, dt, dx, flux, speed, r=3, periodic=False):
    """One step of the SSP RK3 of Shu and Osher."""
    L = lambda v: rate(v, dx, flux, speed, r, periodic)
    u1 = [_axpy((1, c), (dt, d)) for c, d in zip(cells, L(cells))]  # @line L7
    q = Fraction(1, 4) if isinstance(dt, Fraction) else 0.25
    u2 = [_axpy((1 - q, c), (q, a), (q * dt, d)) for c, a, d in zip(cells, u1, L(u1))]
    t = Fraction(2, 3) if isinstance(dt, Fraction) else 2.0 / 3.0
    return [_axpy((1 - t, c), (t, a), (t * dt, d)) for c, a, d in zip(cells, u2, L(u2))]


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


def solve_euler(cells, dx, t_end, r=3, cfl=0.5, periodic=False, g=GAMMA):
    """March to t_end with dt = cfl dx / max(|u| + c). Returns (cells, number of steps)."""
    t, n = 0.0, 0
    flux, speed = (lambda q: euler_flux(q, g)), (lambda q: euler_speed(q, g))
    while t < t_end - 1e-14:
        dt = min(cfl * dx / max(speed(q) for q in cells), t_end - t)
        cells = step(cells, dt, dx, flux, speed, r, periodic)
        t += dt
        n += 1
    return cells, n
