# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-time-migration/. The authors are listed in prov/Y8PCJ8.jsonl.
"""Reverse-time migration (RTM) of one shot as the exact adjoint of discrete Born modeling.

Conventions (the imaging and inverse problems pages):
- The 2D constant density acoustic wave equation m u_tt - Laplacian u = f with
  m = 1 / v^2 (s^2/m^2), u = 0 for t <= 0. A grid field is a list of rows,
  u[i][j] at depth z = i h and position x = j h.
- The scheme of second order in time and space, for n = 0 .. N - 1:
      u^{n+1} = 2 u^n - u^{n-1} + (dt^2 / m) (L u^n + f^n),  u^0 = u^{-1} = 0,
  with the 5-point Laplacian L and u = 0 outside the grid (Dirichlet edges,
  which reflect; a production code adds an absorbing layer). It is stable for
  v dt / h <= 1 / sqrt(2) (the CFL condition in 2D).
- Receivers record d^n = u^n at the grid points recs, for n = 0 .. N.
- Born modeling: with m = m0 + dm, the first order scattered field solves the
  same scheme with the source s^n = -dm * D2u0^n, where
  D2u0^n = (u0^{n+1} - 2 u0^n + u0^{n-1}) / dt^2 is the second time difference
  of the background field u0.
- RTM: propagate the receiver data backward in time with the transposed
  scheme (the adjoint field lam), and correlate it with D2u0 at zero lag:
      lam^n = R^T r^n + 2 lam^{n+1} + L ((dt^2 / m) lam^{n+1}) - lam^{n+2},
      image = - sum_n D2u0^{n-1} * (dt^2 / m) lam^n.
  This is the exact adjoint of born_modeling, so <B dm, r> = <dm, B^T r>.

Cost: O(N n^2) time per propagation for an n x n grid, and O(N n^2) memory to
store the background field (the main cost of RTM).
"""

import math


def laplacian(u, h):
    """The 5-point Laplacian with u = 0 outside the grid."""
    nz, nx = len(u), len(u[0])
    out = [[0.0] * nx for _ in range(nz)]
    c = 1.0 / (h * h)
    for i in range(nz):
        up = u[i - 1] if i > 0 else None
        dn = u[i + 1] if i < nz - 1 else None
        row = u[i]
        o = out[i]
        for j in range(nx):
            s = -4.0 * row[j]
            if j > 0:
                s += row[j - 1]
            if j < nx - 1:
                s += row[j + 1]
            if up is not None:
                s += up[j]
            if dn is not None:
                s += dn[j]
            o[j] = c * s
    return out


def zeros(nz, nx):
    return [[0.0] * nx for _ in range(nz)]


def propagate(m, src, nsteps, dt, h):
    """Run the scheme with the source field src(n) (a grid, or None for zero).

    Returns the list of the fields u^0 .. u^N and the list of D2u^0 .. D2u^{N-1}.
    """
    nz, nx = len(m), len(m[0])
    prev, cur = zeros(nz, nx), zeros(nz, nx)
    fields, d2 = [cur], []
    for n in range(nsteps):
        lap = laplacian(cur, h)
        f = src(n)
        acc = [[(lap[i][j] + (f[i][j] if f is not None else 0.0)) / m[i][j] for j in range(nx)] for i in range(nz)]
        nxt = [[2.0 * cur[i][j] - prev[i][j] + dt * dt * acc[i][j] for j in range(nx)] for i in range(nz)]
        d2.append(acc)
        fields.append(nxt)
        prev, cur = cur, nxt
    return fields, d2


def point_source(nz, nx, isrc, jsrc, wavelet, h):
    """The source function n -> grid with wavelet[n] / h^2 at one point (a discrete delta)."""
    def src(n):
        g = zeros(nz, nx)
        g[isrc][jsrc] = wavelet[n] / (h * h)
        return g
    return src


def background_field(m, isrc, jsrc, wavelet, dt, h):
    """The source wavefield u0 and its second time differences D2u0."""
    nz, nx = len(m), len(m[0])
    return propagate(m, point_source(nz, nx, isrc, jsrc, wavelet, h), len(wavelet), dt, h)


def born_modeling(dm, m, d2u0, recs, dt, h):
    """Linearized data: the scattered field at the receivers for the perturbation dm.

    Returns a list over n = 0 .. N of lists over the receivers.
    """
    nz, nx = len(m), len(m[0])

    def src(n):
        return [[-dm[i][j] * d2u0[n][i][j] for j in range(nx)] for i in range(nz)]

    fields, _ = propagate(m, src, len(d2u0), dt, h)
    return [[u[i][j] for (i, j) in recs] for u in fields]


def reverse_time_migration(data, m, d2u0, recs, dt, h):
    """The RTM image of one shot: the exact adjoint of born_modeling applied to data.

    data: a list over n = 0 .. N of lists over the receivers.
    """
    nz, nx = len(m), len(m[0])
    nsteps = len(d2u0)  # @line L1
    w = [[dt * dt / m[i][j] for j in range(nx)] for i in range(nz)]
    lam1, lam2 = zeros(nz, nx), zeros(nz, nx)  # @line L2
    image = zeros(nz, nx)
    for n in range(nsteps, 0, -1):  # @line L3
        wl = [[w[i][j] * lam1[i][j] for j in range(nx)] for i in range(nz)]
        lap = laplacian(wl, h)
        lam = [[2.0 * lam1[i][j] + lap[i][j] - lam2[i][j] for j in range(nx)] for i in range(nz)]  # @line L4
        for r, (i, j) in enumerate(recs):
            lam[i][j] += data[n][r]  # @line L5
        g = d2u0[n - 1]
        for i in range(nz):
            for j in range(nx):
                image[i][j] -= g[i][j] * w[i][j] * lam[i][j]  # @line L6
        lam1, lam2 = lam, lam1
    return image  # @line L7


def ricker(t, f0):
    """The Ricker wavelet (1 - 2 a) exp(-a) with a = (pi f0 t)^2, peak frequency f0."""
    a = (math.pi * f0 * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)
