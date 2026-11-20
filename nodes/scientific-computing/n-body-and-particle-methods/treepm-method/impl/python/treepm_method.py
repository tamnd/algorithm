# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treepm-method/. The authors are listed in prov/BKG2W0.jsonl.
"""TreePM gravity in the periodic unit square, in 2D.

N masses m[i] > 0 at positions pos[i] = (x, y) attract by the 2D law: the
potential of a pair is m_i m_j log r and the force on i is
-m_i m_j (x_i - x_j) / r^2, summed over all periodic images.

The potential is split in Fourier space with a Gaussian filter of scale r_s:

    phi_long(k) = phi(k) exp(-k^2 r_s^2),   phi(k) = 2 pi / k^2,

so the short-range pair force is the Newtonian force times
exp(-r^2 / (4 r_s^2)). The long-range part is computed on an M x M mesh
(TSC assignment, deconvolution, FFT, ik differentiation, interpolation).
The short-range part is computed with a Barnes-Hut quadtree: a node of
side s at distance d from the particle is used as one point mass if
s < theta d, and nodes farther than r_cut = cut * r_s are skipped.
"""

import cmath
import math
from typing import Optional, Sequence

Point = tuple[float, float]


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT without normalization."""
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
    rows = [fft(r, inverse) for r in grid]
    cols = [fft([rows[i][j] for i in range(len(rows))], inverse) for j in range(len(rows))]
    return [[cols[j][i] for j in range(len(cols))] for i in range(len(rows))]


def tsc(x: float, m: int) -> list[tuple[int, float]]:
    """Triangular shaped cloud weights for one coordinate."""
    u = x * m
    g = round(u)
    t = u - g
    return [((g - 1) % m, 0.5 * (0.5 - t) ** 2), (g % m, 0.75 - t * t), ((g + 1) % m, 0.5 * (0.5 + t) ** 2)]


def pm_forces(mass: Sequence[float], pos: Sequence[Point], m: int, r_s: float) -> list[list[float]]:
    """Long-range forces on the mesh with the filter exp(-k^2 r_s^2)."""
    w = [(tsc(x, m), tsc(y, m)) for x, y in pos]
    rho = [[0j] * m for _ in range(m)]
    for i, mi in enumerate(mass):
        for gx, wx in w[i][0]:
            for gy, wy in w[i][1]:
                rho[gx][gy] += mi * wx * wy
    rho_k = fft2(rho)
    h = 1.0 / m

    def sinc(z: float) -> float:
        return 1.0 if z == 0 else math.sin(z) / z

    ex_k = [[0j] * m for _ in range(m)]
    ey_k = [[0j] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if i == 0 and j == 0:
                continue
            kx = 2 * math.pi * (i - m if i >= m // 2 else i)
            ky = 2 * math.pi * (j - m if j >= m // 2 else j)
            k2 = kx * kx + ky * ky
            u2 = (sinc(kx * h / 2) * sinc(ky * h / 2)) ** 6
            g = 2 * math.pi / k2 * math.exp(-k2 * r_s * r_s) / u2
            dx = 0.0 if i == m // 2 else kx
            dy = 0.0 if j == m // 2 else ky
            ex_k[i][j] = 1j * dx * g * rho_k[i][j]
            ey_k[i][j] = 1j * dy * g * rho_k[i][j]
    ex = fft2(ex_k, inverse=True)
    ey = fft2(ey_k, inverse=True)
    out = []
    for i, mi in enumerate(mass):
        fx = fy = 0.0
        for gx, wx in w[i][0]:
            for gy, wy in w[i][1]:
                fx += wx * wy * ex[gx][gy].real
                fy += wx * wy * ey[gx][gy].real
        out.append([mi * fx, mi * fy])
    return out


class Node:
    """A square of the quadtree: center, side, total mass, center of mass, and children or a bucket."""

    __slots__ = ("cx", "cy", "size", "mass", "mx", "my", "children", "idx")

    def __init__(self, cx: float, cy: float, size: float):
        self.cx, self.cy, self.size = cx, cy, size
        self.mass = self.mx = self.my = 0.0
        self.children: list["Node"] = []
        self.idx: list[int] = []


def build_tree(mass: Sequence[float], pos: Sequence[Point], leaf_size: int = 4) -> Node:
    """Quadtree of the unit square; leaves hold at most leaf_size particles (or are at depth 40)."""

    def build(idx: list[int], cx: float, cy: float, size: float, depth: int) -> Node:
        node = Node(cx, cy, size)
        node.mass = sum(mass[i] for i in idx)
        node.mx = sum(mass[i] * pos[i][0] for i in idx) / node.mass
        node.my = sum(mass[i] * pos[i][1] for i in idx) / node.mass
        if len(idx) <= leaf_size or depth >= 40:
            node.idx = idx
            return node
        quads: list[list[int]] = [[], [], [], []]
        for i in idx:
            quads[(pos[i][0] >= cx) * 2 + (pos[i][1] >= cy)].append(i)
        q = size / 4
        for k, sub in enumerate(quads):
            if sub:
                node.children.append(build(sub, cx + (q if k >= 2 else -q), cy + (q if k % 2 else -q), size / 2, depth + 1))
        return node

    return build(list(range(len(mass))), 0.5, 0.5, 1.0, 0)


def wrap(d: float) -> float:
    return d - round(d)


def tree_short_range(mass: Sequence[float], pos: Sequence[Point], root: Node, r_s: float, theta: float,
                     cut: float = 6.0) -> tuple[list[list[float]], int]:
    """Short-range forces by a tree walk for each particle. Returns (forces, interactions)."""
    r_cut = cut * r_s
    a = 1.0 / (4 * r_s * r_s)
    out = []
    count = 0
    for i, (xi, yi) in enumerate(pos):  # @line L3
        fx = fy = 0.0
        stack = [root]
        while stack:
            node = stack.pop()
            bx = max(0.0, abs(wrap(xi - node.cx)) - node.size / 2)
            by = max(0.0, abs(wrap(yi - node.cy)) - node.size / 2)
            if bx * bx + by * by >= r_cut * r_cut:  # @line L4
                continue
            if not node.children:  # @line L5
                for j in node.idx:
                    if j == i:
                        continue
                    dx, dy = wrap(xi - pos[j][0]), wrap(yi - pos[j][1])
                    r2 = dx * dx + dy * dy
                    if r2 < r_cut * r_cut:
                        c = -mass[i] * mass[j] * math.exp(-a * r2) / r2
                        fx += c * dx
                        fy += c * dy
                        count += 1
                continue
            dx, dy = wrap(xi - node.mx), wrap(yi - node.my)
            r2 = dx * dx + dy * dy
            if node.size * node.size < theta * theta * r2:  # @line L6
                c = -mass[i] * node.mass * math.exp(-a * r2) / r2
                fx += c * dx
                fy += c * dy
                count += 1
            else:
                stack.extend(node.children)
        out.append([fx, fy])
    return out, count


def treepm_forces(mass: Sequence[float], pos: Sequence[Point], m: int = 32, r_s: Optional[float] = None,
                  theta: float = 0.5, cut: float = 6.0, leaf_size: int = 4):
    """TreePM forces. r_s defaults to 1.25 mesh cells. Returns (forces, stats).

    The cutoff cut * r_s must be at most 1/2, so that the minimum image is the only image in range.
    """
    if r_s is None:
        r_s = 1.25 / m
    if cut * r_s > 0.5:
        raise ValueError("cut * r_s must be at most 1/2")
    if not mass:
        return [], {"interactions": 0}
    long = pm_forces(mass, pos, m, r_s)  # @line L1
    root = build_tree(mass, pos, leaf_size)  # @line L2
    short, count = tree_short_range(mass, pos, root, r_s, theta, cut)
    out = [(a[0] + b[0], a[1] + b[1]) for a, b in zip(long, short)]  # @line L7
    return out, {"interactions": count}


def ewald_forces(mass: Sequence[float], pos: Sequence[Point], alpha: float = 8.0, kmax: int = 14) -> list[Point]:
    """Reference forces by Ewald summation: real space over 3 x 3 images, Fourier space up to |n| <= kmax."""
    n = len(mass)
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
                    c = -mass[i] * mass[j] * math.exp(-alpha * alpha * r2) / r2
                    f[i][0] += c * rx
                    f[i][1] += c * ry
    for a in range(-kmax, kmax + 1):
        for b in range(-kmax, kmax + 1):
            if a == 0 and b == 0:
                continue
            kx, ky = 2 * math.pi * a, 2 * math.pi * b
            k2 = kx * kx + ky * ky
            coef = 2 * math.pi / k2 * math.exp(-k2 / (4 * alpha * alpha))
            s = sum(mj * cmath.exp(-1j * (kx * x + ky * y)) for mj, (x, y) in zip(mass, pos))
            for i, (x, y) in enumerate(pos):
                im = (s * cmath.exp(1j * (kx * x + ky * y))).imag
                f[i][0] -= mass[i] * coef * kx * im
                f[i][1] -= mass[i] * coef * ky * im
    return [(a, b) for a, b in f]
