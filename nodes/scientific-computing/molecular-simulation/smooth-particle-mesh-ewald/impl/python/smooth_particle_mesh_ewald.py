# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-particle-mesh-ewald/. The authors are listed in prov/WR206R.jsonl.
"""Smooth particle mesh Ewald (SPME): the reciprocal Ewald sum with cardinal B-splines.

This is the method of Essmann, Perera, Berkowitz, Darden, Lee and Pedersen
(1995). Units are Gaussian (the energy of two charges is q_i q_j / r). The box
is a cube of side L with K grid points per side, K a power of two. With the
scaled coordinate u = K x / L, each charge is spread to n grid points in each
direction with the cardinal B-spline weights M_n(u - g). Then

    S(m) ~ b(m_1) b(m_2) b(m_3) F(Q)(m),
    E_rec = (1/2) sum over m != 0 of C(m) B(m) |F(Q)(m)|^2,
    C(m) = (4 pi / V) exp(-k^2 / (4 alpha^2)) / k^2,  B(m) = |b(m_1) b(m_2) b(m_3)|^2,

with F(Q)(m) = sum_g Q(g) exp(2 pi i m.g / K) and k = 2 pi m / L. The energy is
E_rec = (1/2) sum_g Q(g) phi(g), with phi the convolution of Q with the
inverse transform of C B. The forces are the exact gradient of this
approximate energy: F_i = -sum_g (dQ(g) / dr_i) phi(g), and dM_n / du =
M_(n-1)(u) - M_(n-1)(u - 1).

Cost: Theta(N n^3) for spreading and forces, Theta(K^3 log K) for two FFTs.
Memory Theta(K^3). The forces conserve the approximate energy but their sum
is not exactly zero.
"""

import cmath
import math

Vec = list[float]


def fft(a: list[complex]) -> list[complex]:
    """Radix-2 FFT, X_m = sum_g a_g exp(-2 pi i m g / n), for len(a) a power of two."""
    n = len(a)
    if n == 1:
        return list(a)
    even, odd = fft(a[0::2]), fft(a[1::2])
    out = [0j] * n
    for m in range(n // 2):
        t = cmath.exp(-2j * math.pi * m / n) * odd[m]
        out[m] = even[m] + t
        out[m + n // 2] = even[m] - t
    return out


def fft3(grid: list[complex], k: int) -> list[complex]:
    """3D FFT of a K^3 grid stored flat with index (x K + y) K + z."""
    g = list(grid)
    for x in range(k):
        for y in range(k):
            base = (x * k + y) * k
            g[base:base + k] = fft(g[base:base + k])
    for x in range(k):
        for z in range(k):
            idx = [(x * k + y) * k + z for y in range(k)]
            for i, v in zip(idx, fft([g[i] for i in idx])):
                g[i] = v
    for y in range(k):
        for z in range(k):
            idx = [(x * k + y) * k + z for x in range(k)]
            for i, v in zip(idx, fft([g[i] for i in idx])):
                g[i] = v
    return g


def bspline(w: float, n: int) -> tuple[list[float], list[float]]:
    """Values M_n(w + j) and derivatives M_n'(w + j) for j = 0, ..., n - 1, with 0 <= w < 1 and n >= 3."""
    m = [w, 1.0 - w]  # M_2(w), M_2(w + 1)
    deriv = []
    for order in range(3, n + 1):
        if order == n:
            # M_n'(x) = M_(n-1)(x) - M_(n-1)(x - 1)
            deriv = [(m[j] if j < len(m) else 0.0) - (m[j - 1] if j >= 1 else 0.0) for j in range(n)]
        new = []
        for j in range(order):
            x = w + j
            a = m[j] if j < len(m) else 0.0
            b = m[j - 1] if j >= 1 else 0.0
            new.append((x * a + (order - x) * b) / (order - 1))
        m = new
    return m, deriv


def bspline_moduli(k: int, n: int) -> list[float]:
    """|b(m)|^2 for m = 0, ..., K - 1; set to 0 where the denominator vanishes (odd n, 2m = K)."""
    at_int, _ = bspline(0.0, n)  # M_n(j) for j = 0, ..., n - 1
    out = []
    for m in range(k):
        den = sum(at_int[j + 1] * cmath.exp(2j * math.pi * m * j / k) for j in range(n - 1))
        out.append(0.0 if abs(den) < 1e-10 else 1.0 / (abs(den) ** 2))
    return out


def spme_reciprocal(
    q: list[float], pos: list[Vec], box: float, alpha: float, kgrid: int, n: int,
) -> tuple[float, list[Vec]]:
    """Reciprocal Ewald energy and forces by smooth PME with B-splines of order n (degree n - 1)."""
    k, npart = kgrid, len(q)
    vol = box ** 3
    stencils = []
    for r in pos:  # @line L1
        st = []
        for a in range(3):
            u = (r[a] / box) * k % k
            fl = math.floor(u)
            vals, ders = bspline(u - fl, n)
            # grid point fl - j has weight M_n(u - fl + j)
            st.append(([(fl - j) % k for j in range(n)], vals, ders))
        stencils.append(st)
    grid = [0j] * (k * k * k)
    for i in range(npart):  # @line L2
        (gx, mx, _), (gy, my, _), (gz, mz, _) = stencils[i]
        for a in range(n):
            for b in range(n):
                base = (gx[a] * k + gy[b]) * k
                wab = q[i] * mx[a] * my[b]
                for c in range(n):
                    grid[base + gz[c]] += wab * mz[c]
    fq = [v.conjugate() for v in fft3(grid, k)]  # @line L3: F(Q)(m)
    bmod = bspline_moduli(k, n)
    tpl = 2.0 * math.pi / box
    energy = 0.0
    prod = [0j] * (k * k * k)
    for ix in range(k):  # @line L4
        kx = tpl * (ix if ix <= k // 2 else ix - k)
        for iy in range(k):
            ky = tpl * (iy if iy <= k // 2 else iy - k)
            for iz in range(k):
                if ix == 0 and iy == 0 and iz == 0:
                    continue
                kz = tpl * (iz if iz <= k // 2 else iz - k)
                k2 = kx * kx + ky * ky + kz * kz
                cb = (4.0 * math.pi / vol) * math.exp(-k2 / (4.0 * alpha * alpha)) / k2 * bmod[ix] * bmod[iy] * bmod[iz]
                idx = (ix * k + iy) * k + iz
                s = fq[idx]
                energy += 0.5 * cb * (s.real * s.real + s.imag * s.imag)  # @line L5
                prod[idx] = cb * s
    # line L6: phi(g) = sum_m C B F(Q)(m) exp(-2 pi i m.g / K), the convolution of theta_rec with Q
    phi = [v.real for v in fft3(prod, k)]  # @line L6
    forces = []
    scale = k / box
    for i in range(npart):  # @line L7
        (gx, mx, dx), (gy, my, dy), (gz, mz, dz) = stencils[i]
        f = [0.0, 0.0, 0.0]
        for a in range(n):
            for b in range(n):
                base = (gx[a] * k + gy[b]) * k
                for c in range(n):
                    p = phi[base + gz[c]]
                    f[0] -= dx[a] * my[b] * mz[c] * p
                    f[1] -= mx[a] * dy[b] * mz[c] * p
                    f[2] -= mx[a] * my[b] * dz[c] * p
        forces.append([q[i] * scale * x for x in f])  # @line L8
    return energy, forces
