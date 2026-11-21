# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/katsevich-algorithm/. The authors are listed in prov/KKE2E7.jsonl.
"""Katsevich's exact reconstruction for helical cone-beam CT, in the flat-detector form.

Conventions:
- The source is on the helix y(s) = (R cos s, R sin s, H s) with H = P / (2 pi),
  where P is the pitch (the rise per turn).
- e_u(s) = (-sin s, cos s, 0), e_v = (0, 0, 1), e_w(s) = (cos s, sin s, 0).
- A flat detector at the distance D from the source is normal to e_w(s). Its
  point (u, v) is y(s) + u e_u + v e_v - D e_w. The data g[k][r][j] is the line
  integral of f along the ray from y(s_k) through the detector point (u_j, v_r),
  with s_k = s0 + k ds, u_j = (j - (d - 1) / 2) du and v_r = (r - (m - 1) / 2) dv.
- Geometry holds (R, P, D, s0, ds, du, dv).
"""

import math
from collections import namedtuple

Geometry = namedtuple("Geometry", "R P D s0 ds du dv")


def helix_ray(geo, s, u, v):
    """The source y(s) and the unit direction of the ray to the detector point (u, v)."""
    c, sn = math.cos(s), math.sin(s)
    src = (geo.R * c, geo.R * sn, geo.P * s / (2.0 * math.pi))
    w = (-u * sn - geo.D * c, u * c - geo.D * sn, v)
    nn = math.sqrt(u * u + v * v + geo.D * geo.D)
    return src, (w[0] / nn, w[1] / nn, w[2] / nn)


def project(geo, x, s):
    """(u*, v*, depth): the detector point of the ray through x, and depth = R - x . e_w(s)."""
    c, sn = math.cos(s), math.sin(s)
    depth = geo.R - x[0] * c - x[1] * sn
    u = geo.D * (-x[0] * sn + x[1] * c) / depth
    v = geo.D * (x[2] - geo.P * s / (2.0 * math.pi)) / depth
    return u, v, depth


def pi_interval(geo, x):
    """The ends (s_b, s_t) of the PI-line of x: x is on the chord from y(s_b) to y(s_t), s_t - s_b < 2 pi."""
    h = geo.P / (2.0 * math.pi)

    def other_end(sb):
        ax, ay = geo.R * math.cos(sb), geo.R * math.sin(sb)
        dx, dy = x[0] - ax, x[1] - ay
        mu = -2.0 * (ax * dx + ay * dy) / (dx * dx + dy * dy)  # the chord meets the circle again at mu
        st = math.atan2(ay + mu * dy, ax + mu * dx)
        st += 2.0 * math.pi * math.ceil((sb - st) / (2.0 * math.pi))
        if st <= sb:
            st += 2.0 * math.pi
        return st, (1.0 - 1.0 / mu) * h * sb + (1.0 / mu) * h * st - x[2]

    lo, hi = x[2] / h - 2.0 * math.pi, x[2] / h
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if other_end(mid)[1] > 0.0:
            hi = mid
        else:
            lo = mid
    sb = 0.5 * (lo + hi)
    return sb, other_end(sb)[0]


def kappa_v(geo, u, psi):
    """The height of the kappa-line with the angle psi at the column u."""
    c = geo.D * geo.P / (2.0 * math.pi * geo.R)
    if psi == 0.0:
        return c * u / geo.D
    return c * (psi + psi / math.tan(psi) * u / geo.D)


def kappa_psi(geo, u, v):
    """The angle psi in (-pi/2, pi/2) of the kappa-line through (u, v), by bisection, clamped at the ends."""
    lo, hi = -math.pi / 2.0 + 1e-9, math.pi / 2.0 - 1e-9
    if v <= kappa_v(geo, u, lo):
        return lo
    if v >= kappa_v(geo, u, hi):
        return hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if kappa_v(geo, u, mid) < v:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def derivative_view(geo, g, k):
    """g2 of view k: the derivative at a fixed ray direction, times D / sqrt(u^2 + v^2 + D^2)."""
    m, d, dd = len(g[0]), len(g[0][0]), geo.D
    out = []
    for r in range(m):
        v = (r - (m - 1) / 2.0) * geo.dv
        row = []
        for j in range(d):
            u = (j - (d - 1) / 2.0) * geo.du
            gs = (g[k + 1][r][j] - g[k - 1][r][j]) / (2.0 * geo.ds)  # @line L1
            gu = ((g[k][r][j + 1] if j + 1 < d else 0.0) - (g[k][r][j - 1] if j > 0 else 0.0)) / (2.0 * geo.du)
            gv = ((g[k][r + 1][j] if r + 1 < m else 0.0) - (g[k][r - 1][j] if r > 0 else 0.0)) / (2.0 * geo.dv)
            g1 = gs + (u * u + dd * dd) / dd * gu + u * v / dd * gv  # @line L2
            row.append(dd / math.sqrt(u * u + v * v + dd * dd) * g1)  # @line L3
        out.append(row)
    return out


def _height_interp(g2, j, v, dv):
    m = len(g2)
    fr = v / dv + (m - 1) / 2.0
    r0 = math.floor(fr)
    w = fr - r0
    a = g2[r0][j] if 0 <= r0 < m else 0.0
    b = g2[r0 + 1][j] if 0 <= r0 + 1 < m else 0.0
    return (1.0 - w) * a + w * b


def katsevich_point(geo, g2s, x):
    """f(x) = (1 / (2 pi)) integral over the PI-interval of (H g2 along the kappa-line)(u*) / depth ds."""
    sb, st = pi_interval(geo, x)  # @line L4
    k0, k1 = math.floor((sb - geo.s0) / geo.ds), math.ceil((st - geo.s0) / geo.ds)
    vals = {}
    for k in range(k0, k1 + 1):
        g2 = g2s(k)
        d = len(g2[0])
        us, vs, depth = project(geo, x, geo.s0 + k * geo.ds)  # @line L5
        psi = kappa_psi(geo, us, vs)
        line = [_height_interp(g2, j, kappa_v(geo, (j - (d - 1) / 2.0) * geo.du, psi), geo.dv) for j in range(d)]  # @line L6
        fj = us / geo.du + (d - 1) / 2.0
        j0 = math.floor(fj)
        hil = [sum(2.0 / (math.pi * (jj - l)) * line[l] for l in range(d) if (jj - l) % 2) for jj in (j0, j0 + 1)]  # @line L7
        vals[k] = ((j0 + 1 - fj) * hil[0] + (fj - j0) * hil[1]) / depth  # @line L8
    total = 0.0
    for k in range(k0, k1):
        a = geo.s0 + k * geo.ds
        lo, hi = max(a, sb), min(a + geo.ds, st)
        if hi > lo:
            mid = 0.5 * (lo + hi - 2.0 * a) / geo.ds
            total += (hi - lo) * (vals[k] + (vals[k + 1] - vals[k]) * mid)
    return total / (2.0 * math.pi)  # @line L9


def katsevich(geo, g, points):
    """Reconstruct f at each point. The views s_k needed by the PI-intervals and their neighbours must be in g."""
    cache = {}

    def g2s(k):
        if k not in cache:
            cache[k] = derivative_view(geo, g, k)
        return cache[k]

    return [katsevich_point(geo, g2s, x) for x in points]
