# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/p3m-method/. The authors are listed in prov/J50KQM.jsonl.
"""Particle-particle particle-mesh (P3M) forces of Hockney and Eastwood, in 2D.

N charges q[i] at positions pos[i] = (x, y) in the periodic unit square
interact by the 2D Coulomb law: the potential of a pair is -q_i q_j log r and
the force on i is q_i q_j (x_i - x_j) / r^2, summed over all periodic images.

The force of a pair is split with a Gaussian of width 1/alpha:

    1/r = exp(-alpha^2 r^2) / r  +  (1 - exp(-alpha^2 r^2)) / r.

The first part is short-range and is summed directly over the pairs closer
than r_c, found with a chaining mesh. The second part is smooth; it is the
field of Gaussian charge clouds, with the Fourier potential
(2 pi / k^2) exp(-k^2 / (4 alpha^2)), and it is computed on an M x M mesh:
charge assignment (CIC or TSC), FFT, multiplication by -i k G(k), inverse
FFT and interpolation with the same weights. G is the optimal influence
function of Hockney and Eastwood, which minimizes the mean square force
error of the mesh part.
"""

import cmath
import math
from typing import Sequence

Point = tuple[float, float]


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT without normalization: sum_g a[g] exp(-+2 pi i n g / len(a))."""
    n = len(a)
    if n == 1:
        return [complex(a[0])]
    even = fft(a[0::2], inverse)
    odd = fft(a[1::2], inverse)
    sign = 1 if inverse else -1
    out = [0j] * n
    for k in range(n // 2):
        w = cmath.exp(sign * 2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + w
        out[k + n // 2] = even[k] - w
    return out


def fft2(grid: list[list[complex]], inverse: bool = False) -> list[list[complex]]:
    """2D FFT of a square grid, rows then columns, without normalization."""
    rows = [fft(r, inverse) for r in grid]
    cols = [fft([rows[i][j] for i in range(len(rows))], inverse) for j in range(len(rows))]
    return [[cols[j][i] for j in range(len(cols))] for i in range(len(rows))]


def weights(x: float, m: int, order: int) -> list[tuple[int, float]]:
    """Mesh points (index mod m) and weights for one coordinate; order 2 is CIC, 3 is TSC."""
    u = x * m
    if order == 2:
        g = math.floor(u)
        t = u - g
        return [(g % m, 1 - t), ((g + 1) % m, t)]
    g = round(u)
    t = u - g
    return [((g - 1) % m, 0.5 * (0.5 - t) ** 2), (g % m, 0.75 - t * t), ((g + 1) % m, 0.5 * (0.5 + t) ** 2)]


def wavenumber(n: int, m: int) -> float:
    """The wave number 2 pi n of the FFT index n, folded to -m/2 .. m/2 - 1."""
    return 2 * math.pi * (n - m if n >= m // 2 else n)


def sinc(x: float) -> float:
    return 1.0 if x == 0 else math.sin(x) / x


def influence(m: int, alpha: float, order: int, kind: str = "optimal", alias: int = 2) -> list[list[float]]:
    """G(k) on the mesh: "optimal" (Hockney-Eastwood), "deconvolved" (phi / U^2) or "plain" (phi)."""
    h = 1.0 / m

    def phi(kx: float, ky: float) -> float:
        k2 = kx * kx + ky * ky
        return 2 * math.pi / k2 * math.exp(-k2 / (4 * alpha * alpha))

    def u2(kx: float, ky: float) -> float:
        return (sinc(kx * h / 2) * sinc(ky * h / 2)) ** (2 * order)

    g = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            kx, ky = wavenumber(i, m), wavenumber(j, m)
            if i == 0 and j == 0:
                continue
            if kind == "plain":
                g[i][j] = phi(kx, ky)
            elif kind == "deconvolved":
                g[i][j] = phi(kx, ky) / u2(kx, ky)
            else:
                num = 0.0
                den = 0.0
                for ax in range(-alias, alias + 1):
                    for ay in range(-alias, alias + 1):
                        qx, qy = kx + 2 * math.pi * m * ax, ky + 2 * math.pi * m * ay
                        w = u2(qx, qy)
                        num += w * (kx * qx + ky * qy) * phi(qx, qy)
                        den += w
                g[i][j] = num / ((kx * kx + ky * ky) * den * den)
    return g


def short_range(q: Sequence[float], pos: Sequence[Point], alpha: float, r_c: float) -> tuple[list[Point], int]:
    """Short-range forces over pairs closer than r_c (minimum image), found with a chaining mesh."""
    n = len(q)
    nc = max(1, int(1 / r_c))
    cells: dict[tuple[int, int], list[int]] = {}
    for i, (x, y) in enumerate(pos):
        cells.setdefault((int(x * nc) % nc, int(y * nc) % nc), []).append(i)
    if nc >= 3:
        offsets = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    else:
        offsets = [(dx, dy) for dx in range(nc) for dy in range(nc)]
    f = [[0.0, 0.0] for _ in range(n)]
    pairs = 0
    for (cx, cy), idx in cells.items():
        for dx, dy in offsets:
            other = cells.get(((cx + dx) % nc, (cy + dy) % nc), ())
            for i in idx:
                for j in other:
                    if i == j:
                        continue
                    rx = pos[i][0] - pos[j][0]
                    ry = pos[i][1] - pos[j][1]
                    rx -= round(rx)
                    ry -= round(ry)
                    r2 = rx * rx + ry * ry
                    if r2 < r_c * r_c:
                        c = q[i] * q[j] * math.exp(-alpha * alpha * r2) / r2
                        f[i][0] += c * rx
                        f[i][1] += c * ry
                        pairs += 1
    return [(a, b) for a, b in f], pairs


def p3m_forces(q: Sequence[float], pos: Sequence[Point], m: int = 32, alpha: float = 12.0, r_c: float = 0.25,
               order: int = 2, kind: str = "optimal"):
    """P3M forces on all charges. m is a power of 2. Returns (forces, stats)."""
    n = len(q)
    w = [(weights(x, m, order), weights(y, m, order)) for x, y in pos]
    rho = [[0j] * m for _ in range(m)]
    for i in range(n):  # @line L1
        for gx, wx in w[i][0]:
            for gy, wy in w[i][1]:
                rho[gx][gy] += q[i] * wx * wy
    rho_k = fft2(rho)  # @line L2
    g = influence(m, alpha, order, kind)
    ex_k = [[0j] * m for _ in range(m)]
    ey_k = [[0j] * m for _ in range(m)]
    for i in range(m):  # @line L3
        for j in range(m):
            kx = 0.0 if i == m // 2 else wavenumber(i, m)
            ky = 0.0 if j == m // 2 else wavenumber(j, m)
            ex_k[i][j] = -1j * kx * g[i][j] * rho_k[i][j]
            ey_k[i][j] = -1j * ky * g[i][j] * rho_k[i][j]
    ex = fft2(ex_k, inverse=True)  # @line L4
    ey = fft2(ey_k, inverse=True)
    forces = []
    for i in range(n):  # @line L5
        fx = fy = 0.0
        for gx, wx in w[i][0]:
            for gy, wy in w[i][1]:
                fx += wx * wy * ex[gx][gy].real
                fy += wx * wy * ey[gx][gy].real
        forces.append([q[i] * fx, q[i] * fy])
    sr, pairs = short_range(q, pos, alpha, r_c)  # @line L6
    out = [(a + c, b + d) for (a, b), (c, d) in zip(forces, sr)]
    return out, {"pairs": pairs, "mesh": m * m}  # @line L7


def ewald_forces(q: Sequence[float], pos: Sequence[Point], alpha: float = 8.0, kmax: int = 14) -> list[Point]:
    """Reference forces by Ewald summation: real space over 3 x 3 images, Fourier space up to |n| <= kmax."""
    n = len(q)
    f = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for ix in (-1, 0, 1):
                for iy in (-1, 0, 1):
                    if i == j and ix == 0 and iy == 0:
                        continue
                    rx = pos[i][0] - pos[j][0] + ix
                    ry = pos[i][1] - pos[j][1] + iy
                    r2 = rx * rx + ry * ry
                    c = q[i] * q[j] * math.exp(-alpha * alpha * r2) / r2
                    f[i][0] += c * rx
                    f[i][1] += c * ry
    for a in range(-kmax, kmax + 1):
        for b in range(-kmax, kmax + 1):
            if a == 0 and b == 0:
                continue
            kx, ky = 2 * math.pi * a, 2 * math.pi * b
            k2 = kx * kx + ky * ky
            coef = 2 * math.pi / k2 * math.exp(-k2 / (4 * alpha * alpha))
            s = sum(qj * cmath.exp(-1j * (kx * x + ky * y)) for qj, (x, y) in zip(q, pos))
            for i, (x, y) in enumerate(pos):
                im = (s * cmath.exp(1j * (kx * x + ky * y))).imag
                f[i][0] += q[i] * coef * kx * im
                f[i][1] += q[i] * coef * ky * im
    return [(a, b) for a, b in f]
