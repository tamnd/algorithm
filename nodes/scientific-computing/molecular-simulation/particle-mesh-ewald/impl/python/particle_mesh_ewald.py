# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-mesh-ewald/. The authors are listed in prov/QV4418.jsonl.
"""Particle mesh Ewald (PME) with Lagrange interpolation: the reciprocal part of the Ewald sum on a grid.

This is the method of Darden, York and Pedersen (1993). Units are Gaussian
(the energy of two charges is q_i q_j / r). The box is a cube of side L with a
grid of K points per side, K a power of two. Each charge is spread to the 2p
nearest grid points in each direction with the weights of piecewise Lagrange
interpolation of order 2p, so exp(i k . r_j) is replaced by its interpolant.
The structure factor is then one 3D FFT of the charge grid, and

    E_rec = (2 pi / V) sum over m != 0 of exp(-k^2 / (4 alpha^2)) / k^2 |S(m)|^2,

with k = 2 pi m / L for |m_a| <= K / 2. The forces come from the reciprocal
electric field, computed on the grid by multiplying by i k in Fourier space
(three more FFTs), and interpolated back to the charges with the same weights.
Because the same weights spread the charges and pick up the field, the
reciprocal forces sum to zero up to rounding, but they are not exactly
minus the gradient of the interpolated energy.

Cost: Theta(N p^3) for spreading and interpolation, Theta(K^3 log K) for the
four FFTs. Memory Theta(K^3). The real-space and self parts of the Ewald sum
are not computed here: see the ewald-summation page.
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
            col = fft([g[i] for i in idx])
            for i, v in zip(idx, col):
                g[i] = v
    for y in range(k):
        for z in range(k):
            idx = [(x * k + y) * k + z for x in range(k)]
            col = fft([g[i] for i in idx])
            for i, v in zip(idx, col):
                g[i] = v
    return g


def lagrange_weights(u: float, p: int) -> tuple[int, list[float]]:
    """Weights of the 2p grid points floor(u) - p + 1, ..., floor(u) + p for Lagrange interpolation at u."""
    first = math.floor(u) - p + 1
    xs = [first + j for j in range(2 * p)]
    w = []
    for j, xj in enumerate(xs):
        c = 1.0
        for l, xl in enumerate(xs):
            if l != j:
                c *= (u - xl) / (xj - xl)
        w.append(c)
    return first, w


def pme_reciprocal(
    q: list[float], pos: list[Vec], box: float, alpha: float, kgrid: int, p: int,
) -> tuple[float, list[Vec]]:
    """Reciprocal Ewald energy and forces by PME with Lagrange interpolation of order 2p."""
    n, k = len(q), kgrid
    vol = box ** 3
    # line L1: scaled coordinates and the interpolation weights of each charge
    stencils = []
    for r in pos:  # @line L1
        stencils.append([lagrange_weights((r[a] / box) * k % k, p) for a in range(3)])
    grid = [0j] * (k * k * k)
    for i in range(n):  # @line L2
        (fx, wx), (fy, wy), (fz, wz) = stencils[i]
        for a, wa in enumerate(wx):
            gx = (fx + a) % k
            for b, wb in enumerate(wy):
                gy = (fy + b) % k
                for c, wc in enumerate(wz):
                    grid[(gx * k + gy) * k + (fz + c) % k] += q[i] * wa * wb * wc
    # line L3: S(m) = sum_g Q(g) exp(+2 pi i m.g / K) is the conjugate of the forward FFT
    sk = [v.conjugate() for v in fft3(grid, k)]  # @line L3
    energy = 0.0
    tpl = 2.0 * math.pi / box
    ak = [[0j] * (k * k * k) for _ in range(3)]
    for mx in range(k):  # @line L4
        kx = tpl * (mx if mx <= k // 2 else mx - k)
        for my in range(k):
            ky = tpl * (my if my <= k // 2 else my - k)
            for mz in range(k):
                if mx == 0 and my == 0 and mz == 0:
                    continue
                kz = tpl * (mz if mz <= k // 2 else mz - k)
                k2 = kx * kx + ky * ky + kz * kz
                g = math.exp(-k2 / (4.0 * alpha * alpha)) / k2
                idx = (mx * k + my) * k + mz
                s = sk[idx]
                energy += (2.0 * math.pi / vol) * g * (s.real * s.real + s.imag * s.imag)  # @line L5
                # i k derivative; the Nyquist component of each direction has no sign, so it is dropped
                for d, kd, md in ((0, kx, mx), (1, ky, my), (2, kz, mz)):
                    if 2 * md != k:
                        ak[d][idx] = kd * g * s
    # line L6: field on the grid, E_d(g) = -(4 pi / V) Im sum_m k_d G(m) S(m) exp(-2 pi i m.g / K)
    field = [[-(4.0 * math.pi / vol) * v.imag for v in fft3(ak[d], k)] for d in range(3)]  # @line L6
    forces = []
    for i in range(n):  # @line L7
        (fx, wx), (fy, wy), (fz, wz) = stencils[i]
        f = [0.0, 0.0, 0.0]
        for a, wa in enumerate(wx):
            gx = (fx + a) % k
            for b, wb in enumerate(wy):
                gy = (fy + b) % k
                for c, wc in enumerate(wz):
                    idx = (gx * k + gy) * k + (fz + c) % k
                    w = q[i] * wa * wb * wc
                    for d in range(3):
                        f[d] += w * field[d][idx]
        forces.append(f)
    return energy, forces  # @line L8
