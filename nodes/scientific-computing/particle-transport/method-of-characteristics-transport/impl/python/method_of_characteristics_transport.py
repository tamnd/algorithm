# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/method-of-characteristics-transport/. The authors are listed in prov/J4S5CW.jsonl.
"""The method of characteristics (MOC) for the one-speed transport equation in two dimensions.

The domain is the rectangle [0, width] x [0, height], infinite in z, cut into
nx by ny flat-source regions (cell k = ix + nx * iy). Each cell has
sigma_t > 0, sigma_s and an isotropic source q (particles per cm^3 per s).
The scalar flux is phi = integral of psi over the unit sphere, so the
emission density is Q = (sigma_s phi + q) / (4 pi). All faces are vacuum.

Directions: n_azim azimuthal angles alpha_a = pi (a + 1/2) / n_azim in
(0, pi), each track traced in both directions, times n_polar Gauss-Legendre
polar cosines in (0, 1), counted twice for the symmetry in z. The weights
of all directions sum to 4 pi.

Along a segment of in-plane length l in a cell, the 3D path length is
l / sin(theta) and the exact solution with a flat source is

    psi_out = psi_in exp(-tau) + (Q / sigma_t) (1 - exp(-tau)),  tau = sigma_t l / sin(theta).

The cell flux is phi = 4 pi Q / sigma_t + (sum over segments of w delta sin(theta) (psi_in - psi_out)) / (sigma_t A).
"""

import math


def segment(psi_in, q_over_sigma, tau):
    """Exact outgoing and segment-averaged angular flux for a flat source. Returns (psi_out, psi_avg)."""
    if tau < 1e-10:
        return psi_in - (psi_in - q_over_sigma) * tau, psi_in - (psi_in - q_over_sigma) * tau / 2.0
    decay = 1.0 - math.exp(-tau)
    out = psi_in - (psi_in - q_over_sigma) * decay
    return out, q_over_sigma + (psi_in - out) / tau


def lay_tracks(width, height, nx, ny, n_azim, spacing):
    """Cyclic-free track laydown for vacuum faces.

    Returns a list of tracks (a, delta, segments) where a is the azimuthal
    index, delta the actual track spacing for that angle, and segments a list
    of (cell, length) in the direction (cos alpha, sin alpha)."""
    hx, hy = width / nx, height / ny
    tracks = []
    for a in range(n_azim):
        alpha = math.pi * (a + 0.5) / n_azim
        ca, sa = math.cos(alpha), math.sin(alpha)
        proj = [-x * sa + y * ca for x in (0.0, width) for y in (0.0, height)]
        pmin, pmax = min(proj), max(proj)
        nt = max(1, math.ceil((pmax - pmin) / spacing))
        delta = (pmax - pmin) / nt
        for t in range(nt):
            p = pmin + (t + 0.5) * delta
            x0, y0 = -p * sa, p * ca
            lo, hi = (0.0 - y0) / sa, (height - y0) / sa
            if abs(ca) > 1e-15:
                s1, s2 = (0.0 - x0) / ca, (width - x0) / ca
                lo, hi = max(lo, min(s1, s2)), min(hi, max(s1, s2))
            if hi - lo <= 1e-14:
                continue
            cuts = [lo, hi]
            if abs(ca) > 1e-15:
                for i in range(1, nx):
                    s = (i * hx - x0) / ca
                    if lo < s < hi:
                        cuts.append(s)
            for j in range(1, ny):
                s = (j * hy - y0) / sa
                if lo < s < hi:
                    cuts.append(s)
            cuts.sort()
            segs = []
            for s0, s1 in zip(cuts, cuts[1:]):
                if s1 - s0 <= 1e-14:
                    continue
                sm = (s0 + s1) / 2.0
                ix = min(nx - 1, max(0, int((x0 + sm * ca) / hx)))
                iy = min(ny - 1, max(0, int((y0 + sm * sa) / hy)))
                segs.append((ix + nx * iy, s1 - s0))
            tracks.append((a, delta, segs))
    return tracks


def polar_quadrature(n_polar):
    """Gauss-Legendre cosines in (0, 1) and weights that sum to 2 (both hemispheres)."""
    mus, ws = [], []
    for i in range(n_polar):
        x = math.cos(math.pi * (i + 0.75) / (n_polar + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n_polar + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n_polar * (x * p1 - p0) / (x * x - 1.0)
            step = p1 / dp
            x -= step
            if abs(step) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n_polar + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n_polar * (x * p1 - p0) / (x * x - 1.0)
        mus.append((x + 1.0) / 2.0)
        ws.append(2.0 / ((1.0 - x * x) * dp * dp))  # the weight on [-1, 1], twice the mapped weight on (0, 1)
    return mus, ws


def moc_solve(width, height, nx, ny, sigma_t, sigma_s, q, n_azim=8, n_polar=3, spacing=0.05,
              tol=1e-8, max_iter=1000, tracks=None):
    """Source iteration with MOC sweeps. Returns a dict with phi (per cell), leakage, iterations and tracks."""
    ncell = nx * ny
    area = (width / nx) * (height / ny)
    if tracks is None:
        tracks = lay_tracks(width, height, nx, ny, n_azim, spacing)  # @line L1
    mus, ws = polar_quadrature(n_polar)
    sines = [math.sqrt(1.0 - m * m) for m in mus]
    w_azim = math.pi / n_azim
    phi = [0.0] * ncell  # @line L2
    leak = 0.0
    it = 0
    for it in range(1, max_iter + 1):  # @line L3
        qs = [(sigma_s[k] * phi[k] + q[k]) / (4.0 * math.pi) / sigma_t[k] for k in range(ncell)]  # @line L4
        tally = [0.0] * ncell
        leak = 0.0
        for a, delta, segs in tracks:
            for sn, wp in zip(sines, ws):
                wgt = w_azim * wp * delta * sn
                for order in (segs, reversed(segs)):
                    psi = 0.0  # @line L5
                    for k, length in order:
                        dpsi = (psi - qs[k]) * (1.0 - math.exp(-sigma_t[k] * length / sn))  # @line L6
                        tally[k] += wgt * dpsi
                        psi -= dpsi
                    leak += wgt * psi  # @line L7
        new = [4.0 * math.pi * qs[k] + tally[k] / (sigma_t[k] * area) for k in range(ncell)]  # @line L8
        change = max(abs(a - b) for a, b in zip(new, phi))
        phi = new
        if change <= tol * max(abs(v) for v in phi):  # @line L9
            break
    return {"phi": phi, "leakage": leak, "iterations": it, "tracks": tracks}


def expint1(x):
    """E_1(x) for x > 0: series for x <= 1, continued fraction otherwise."""
    if x <= 1.0:
        term, k = 1.0, 1
        total = -0.5772156649015329 - math.log(x)
        while True:
            term *= -x / k
            add = -term / k
            total += add
            if abs(add) < 1e-17 * abs(total):
                break
            k += 1
        return total
    # Lentz continued fraction for E_1
    b = x + 1.0
    c = 1.0 / 1e-300
    d = 1.0 / b
    h = d
    for i in range(1, 300):
        an = -i * i
        b += 2.0
        d = 1.0 / (an * d + b)
        c = b + an / c
        de = c * d
        h *= de
        if abs(de - 1.0) < 1e-16:
            break
    return h * math.exp(-x)


def expint(n, x):
    """E_n(x) for n = 1, 2, 3 and x >= 0 by the recurrence E_(n+1)(x) = (exp(-x) - x E_n(x)) / n."""
    if x == 0.0:
        return math.inf if n == 1 else 1.0 / (n - 1)
    e = expint1(x)
    for k in range(1, n):
        e = (math.exp(-x) - x * e) / k
    return e


def slab_absorber_flux(sigma_t, q, length, a, b):
    """Average over [a, b] of the exact scalar flux (q / (2 sigma_t)) (2 - E2(sigma_t x) - E2(sigma_t (L - x)))
    of a purely absorbing slab with a uniform source and vacuum faces."""
    def int_e2(x0, x1):  # integral of E2(sigma_t x) dx over [x0, x1]
        return (expint(3, sigma_t * x0) - expint(3, sigma_t * x1)) / sigma_t
    total = 2.0 * (b - a) - int_e2(a, b) - int_e2(length - b, length - a)
    return q / (2.0 * sigma_t) * total / (b - a)
