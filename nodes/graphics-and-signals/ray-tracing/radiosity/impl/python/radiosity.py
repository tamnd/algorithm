# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radiosity/. The authors are listed in prov/E000CC.jsonl.

"""Radiosity for diffuse patches (Goral, Torrance, Greenberg and Battaile 1984).

The radiosity B_i of patch i solves B_i = E_i + rho_i sum_j F_ij B_j, where F_ij is the
form factor from patch i to patch j. The code computes the form factors of planar
patches with the exact point-to-polygon formula, integrated over patch i with
Gauss-Legendre quadrature, and solves the system by Gauss-Seidel iteration. It also has
Jacobi iteration, progressive refinement (Cohen, Chen, Wallace and Greenberg 1988) and an
exact Gaussian elimination that works with Fraction values.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

Vec = tuple[float, float, float]


def _sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a: Vec) -> float:
    return math.sqrt(_dot(a, a))


@dataclass
class Patch:
    """A planar convex quadrilateral v0, v0 + e1, v0 + e1 + e2, v0 + e2 with a unit normal n."""

    v0: Vec
    e1: Vec
    e2: Vec
    normal: Vec

    @property
    def vertices(self) -> list[Vec]:
        a = self.v0
        b = tuple(a[k] + self.e1[k] for k in range(3))
        c = tuple(b[k] + self.e2[k] for k in range(3))
        d = tuple(a[k] + self.e2[k] for k in range(3))
        return [a, b, c, d]

    @property
    def area(self) -> float:
        return _norm(_cross(self.e1, self.e2))

    def point(self, u: float, v: float) -> Vec:
        return tuple(self.v0[k] + u * self.e1[k] + v * self.e2[k] for k in range(3))


def point_to_polygon(p: Vec, n: Vec, polygon: Sequence[Vec]) -> float:
    """The form factor from a differential area at p with normal n to a polygon (Lambert's formula).

    F = (1 / 2 pi) |sum_k gamma_k n . (a_k x a_k+1) / |a_k x a_k+1||, where a_k = v_k - p and
    gamma_k is the angle between a_k and a_k+1. The polygon must lie in front of p.
    """
    total = 0.0
    k = len(polygon)
    for i in range(k):
        a = _sub(polygon[i], p)
        b = _sub(polygon[(i + 1) % k], p)
        c = _cross(a, b)
        cn = _norm(c)
        if cn == 0.0:
            continue
        gamma = math.atan2(cn, _dot(a, b))
        total += gamma * _dot(n, c) / cn
    return abs(total) / (2.0 * math.pi)


def gauss_legendre(n: int) -> tuple[list[float], list[float]]:
    """Nodes and weights of n-point Gauss-Legendre quadrature on [0, 1]."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(0.5 * (1.0 - x))
        ws.append(1.0 / ((1.0 - x * x) * dp * dp))
    return xs, ws


def form_factor(pi: Patch, pj: Patch, order: int = 8) -> float:
    """F_ij = (1 / A_i) integral over A_i of the point-to-polygon factor to patch j.

    Patches in the same plane get 0. This assumes no other patch blocks the view, as in a
    convex room.
    """
    if abs(_dot(pi.normal, pj.normal) - 1.0) < 1e-12 and abs(_dot(pi.normal, _sub(pj.v0, pi.v0))) < 1e-12:
        return 0.0
    xs, ws = gauss_legendre(order)
    verts = pj.vertices
    s = 0.0
    for u, wu in zip(xs, ws):
        for v, wv in zip(xs, ws):
            s += wu * wv * point_to_polygon(pi.point(u, v), pi.normal, verts)
    return s


def form_factor_matrix(patches: Sequence[Patch], order: int = 8) -> list[list[float]]:
    return [[form_factor(a, b, order) for b in patches] for a in patches]


def cube_room(n: int) -> list[Patch]:
    """The six inner faces of the unit cube, each split into n x n square patches, normals inward."""
    patches = []
    h = 1.0 / n
    for axis in range(3):
        b, c = (axis + 1) % 3, (axis + 2) % 3
        for side in (0.0, 1.0):
            normal = [0.0, 0.0, 0.0]
            normal[axis] = 1.0 if side == 0.0 else -1.0
            for i in range(n):
                for j in range(n):
                    v0 = [0.0, 0.0, 0.0]
                    v0[axis], v0[b], v0[c] = side, i * h, j * h
                    e1 = [0.0, 0.0, 0.0]
                    e1[b] = h
                    e2 = [0.0, 0.0, 0.0]
                    e2[c] = h
                    patches.append(Patch(tuple(v0), tuple(e1), tuple(e2), tuple(normal)))
    return patches


def sphere_zone_form_factors(cuts: Sequence[Fraction]) -> tuple[list[Fraction], list[list[Fraction]]]:
    """Zones of the inside of the unit sphere between the heights cuts[0] < cuts[1] < ... .

    Inside a sphere, the form factor from any point to a region is the area of the region
    divided by 4 pi, so F_ij = (z_j+1 - z_j) / 2 for every i, and A_i = 2 pi (z_i+1 - z_i).
    The function returns the areas divided by 2 pi, and the exact form factors.
    """
    dz = [cuts[k + 1] - cuts[k] for k in range(len(cuts) - 1)]
    return dz, [[d / 2 for d in dz] for _ in dz]


def gauss_seidel(emission: Sequence, reflectance: Sequence, F: Sequence[Sequence], tol: float = 1e-12, max_iter: int = 10000):
    """Solve B = E + rho F B by Gauss-Seidel iteration. Return B and the number of sweeps."""
    n = len(emission)
    B = list(emission)  # @line L2
    for sweep in range(1, max_iter + 1):  # @line L3
        delta = 0.0  # @line L4
        for i in range(n):  # @line L5
            b = emission[i] + reflectance[i] * sum(F[i][j] * B[j] for j in range(n))  # @line L6
            delta = max(delta, abs(b - B[i]))  # @line L7
            B[i] = b
        if delta < tol:  # @line L8
            return B, sweep  # @line L9
    return B, max_iter


def radiosity(patches: Sequence[Patch], emission: Sequence[float], reflectance: Sequence[float], tol: float = 1e-12, order: int = 8):
    """The full method: form factors, then Gauss-Seidel. Return B, F and the number of sweeps."""
    F = form_factor_matrix(patches, order)  # @line L1
    B, sweeps = gauss_seidel(emission, reflectance, F, tol)
    return B, F, sweeps


def jacobi(emission: Sequence, reflectance: Sequence, F: Sequence[Sequence], tol: float = 1e-12, max_iter: int = 10000):
    """Solve B = E + rho F B by Jacobi iteration. Return B and the number of sweeps."""
    n = len(emission)
    B = list(emission)
    for sweep in range(1, max_iter + 1):
        new = [emission[i] + reflectance[i] * sum(F[i][j] * B[j] for j in range(n)) for i in range(n)]
        delta = max(abs(new[i] - B[i]) for i in range(n))
        B = new
        if delta < tol:
            return B, sweep
    return B, max_iter


def progressive_refinement(emission: Sequence, reflectance: Sequence, F: Sequence[Sequence], areas: Sequence, tol: float = 1e-12, max_steps: int = 100000):
    """Progressive refinement radiosity by shooting.

    Each step picks the patch with the most unshot power A_i dB_i and shoots it: every patch j
    gets rho_j F_ji dB_i = rho_j F_ij (A_i / A_j) dB_i, which also becomes unshot. Return B and the
    number of shooting steps. Stop when the largest unshot power is below tol.
    """
    n = len(emission)
    B = list(emission)
    dB = list(emission)
    for step in range(1, max_steps + 1):
        i = max(range(n), key=lambda k: dB[k] * areas[k])
        if dB[i] * areas[i] < tol:
            return B, step - 1
        shot = dB[i]
        dB[i] = 0 * shot
        for j in range(n):
            add = reflectance[j] * F[i][j] * areas[i] / areas[j] * shot
            B[j] += add
            dB[j] += add
    return B, max_steps


def exact_solve(emission: Sequence, reflectance: Sequence, F: Sequence[Sequence]) -> list:
    """Solve (I - rho F) B = E by Gaussian elimination. With Fraction input the answer is exact.

    No pivoting is needed because the matrix is strictly diagonally dominant by rows when
    every rho_i < 1 and every row sum of F is at most 1.
    """
    n = len(emission)
    A = [[(1 if i == j else 0) - reflectance[i] * F[i][j] for j in range(n)] + [emission[i]] for i in range(n)]
    for k in range(n):
        for i in range(k + 1, n):
            m = A[i][k] / A[k][k]
            for j in range(k, n + 1):
                A[i][j] -= m * A[k][j]
    B = [0] * n
    for i in range(n - 1, -1, -1):
        s = A[i][n] - sum(A[i][j] * B[j] for j in range(i + 1, n))
        B[i] = s / A[i][i]
    return B
