# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-to-parallel-rebinning/. The authors are listed in prov/D52MD2.jsonl.
"""Fan-to-parallel rebinning, followed by parallel-beam filtered back-projection.

Conventions:
- omega(t) = (cos t, sin t) and omega_perp(t) = (-sin t, cos t). The Radon
  transform is R f(theta, s) = integral f(s omega(theta) + t omega_perp(theta)) dt.
- The source at angle beta is S(beta) = D omega_perp(beta). The ray at the fan
  angle gamma is the line with theta = beta + gamma and s = D sin gamma, so the
  fan data is g(beta, gamma) = R f(beta + gamma, D sin gamma).
- Fan data: a full scan, beta_k = 2 pi k / a for k = 0 .. a - 1, and either an
  equiangular detector, gamma_j = (j - (d - 1) / 2) alpha, or a flat virtual
  detector through the center, t_j = (j - (d - 1) / 2) tau_f, with the fan angle
  atan(t_j / D).
- Parallel data: theta_k = k pi / a_p for k = 0 .. a_p - 1 and
  s_j = (j - (d_p - 1) / 2) tau for j = 0 .. d_p - 1.
- The output image is n x n on [-1, 1]^2, pixel (i, j) centered at
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n.
"""

import math


def fan_coordinates(theta, s, dist):
    """(beta, gamma) of the line (theta, s): gamma = asin(s / D), beta = theta - gamma mod 2 pi."""
    gamma = math.asin(s / dist)
    return (theta - gamma) % (2.0 * math.pi), gamma


def bilinear(g, u, v):
    """Interpolate g[k][j] at the fractional indices (u, v): periodic in k, zero outside in j."""
    a, d = len(g), len(g[0])
    k0 = math.floor(u)
    wu = u - k0
    j0 = math.floor(v)
    wv = v - j0
    val = 0.0
    for dk, fu in ((0, 1.0 - wu), (1, wu)):
        if fu == 0.0:
            continue
        row = g[(k0 + dk) % a]
        for dj, fv in ((0, 1.0 - wv), (1, wv)):
            j = j0 + dj
            if fv != 0.0 and 0 <= j < d:
                val += fu * fv * row[j]
    return val


def rebin(g, dist, alpha, a_p, d_p, tau, detector="equiangular", average=False):
    """Parallel sinogram P[k][j] ~ R f(theta_k, s_j) from full-scan fan data g.

    alpha is the angle step of an equiangular detector, or the spacing tau_f of
    a flat detector. With average=True each parallel sample is the mean of its
    two copies in the full scan, (theta, s) and (theta + pi, -s).
    """
    a, d = len(g), len(g[0])  # @line L1
    dbeta = 2.0 * math.pi / a
    c0 = (d - 1) / 2.0

    def sample(theta, s):
        beta, gamma = fan_coordinates(theta, s, dist)  # @line L6
        if detector == "equiangular":
            v = gamma / alpha + c0  # @line L7
        else:
            v = dist * math.tan(gamma) / alpha + c0
        return bilinear(g, beta / dbeta, v)  # @line L8

    out = []
    for k in range(a_p):  # @line L2
        theta = k * math.pi / a_p  # @line L3
        row = []
        for j in range(d_p):  # @line L4
            s = (j - (d_p - 1) / 2.0) * tau  # @line L5
            val = sample(theta, s)
            if average:
                val = 0.5 * (val + sample(theta + math.pi, -s))
            row.append(val)
        out.append(row)
    return out  # @line L9


def ram_lak_kernel(d, tau):
    """h(m tau), m = -(d - 1) .. d - 1, of the ramp filter band-limited to 1 / (2 tau)."""
    out = []
    for m in range(-(d - 1), d):
        if m == 0:
            out.append(1.0 / (4.0 * tau * tau))
        elif m % 2 == 0:
            out.append(0.0)
        else:
            out.append(-1.0 / (m * m * math.pi * math.pi * tau * tau))
    return out


def parallel_fbp(sino, tau, n):
    """Parallel-beam FBP on [0, pi) with the Ram-Lak kernel and a direct convolution."""
    a, d = len(sino), len(sino[0])
    h = ram_lak_kernel(d, tau)
    c0 = (d - 1) / 2.0
    qs = [[tau * sum(h[j - l + d - 1] * p[l] for l in range(d)) for j in range(d)] for p in sino]
    xs = [-1.0 + (2 * j + 1) / n for j in range(n)]
    ys = [1.0 - (2 * i + 1) / n for i in range(n)]
    img = [[0.0] * n for _ in range(n)]
    for k, q in enumerate(qs):
        c, s = math.cos(k * math.pi / a), math.sin(k * math.pi / a)
        for i, y in enumerate(ys):
            row = img[i]
            for j, x in enumerate(xs):
                u = (x * c + y * s) / tau + c0
                b = math.floor(u)
                w = u - b
                if 0 <= b < d:
                    row[j] += (1.0 - w) * q[b]
                if 0 <= b + 1 < d:
                    row[j] += w * q[b + 1]
    return [[math.pi / a * v for v in row] for row in img]


def rebin_and_reconstruct(g, dist, alpha, a_p, d_p, tau, n, detector="equiangular", average=False):
    """Rebin the fan data, then reconstruct with parallel-beam FBP."""
    return parallel_fbp(rebin(g, dist, alpha, a_p, d_p, tau, detector, average), tau, n)
