# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-independent-fast-multipole-method/. The authors are listed in prov/RS9RNM.jsonl.
"""Kernel-independent fast multipole method of Ying, Biros and Zorin, in 2D on a uniform tree.

Charges q[i] sit at points z[i] (complex numbers) of the unit square. The
output is u_j = sum over i != j of q_i K(z_j, z_i) for a kernel K that is
given as a function. The method never expands K. It only evaluates it.

Each box B of half-width h has P points on four circles about its center:

    upward equivalent  radius 1.5 h    (holds the density sigma_up)
    upward check       radius 2.5 h
    downward check     radius 1.5 h
    downward equivalent radius 2.5 h   (holds the density sigma_down)

The upward equivalent density is fitted so that its potential on the upward
check circle equals the potential of the charges of B; then it gives the
far field of B. The downward equivalent density is fitted so that its
potential on the downward check circle equals the potential of all far
charges; then it gives the far field inside B. Each fit is a small linear
solve; the P by P matrices are inverted once per level.

The kernel must be the fundamental solution of an elliptic equation for the
fits to be unique (here the default is log|x - y|), and it must depend on
x - y only, because the matrices are computed once per level and offset.
For the log kernel the circles must not have radius 1; the tree starts at
level 2, where every radius is at most 2.5 / 8.
"""

import math
from typing import Callable, Optional, Sequence

from scimat import inv, matmul, matvec, transpose

Kernel = Callable[[complex, complex], float]


def log_kernel(x: complex, y: complex) -> float:
    """K(x, y) = log|x - y|, the 2D Laplace kernel."""
    return math.log(abs(x - y))


def circle(center: complex, radius: float, n: int) -> list[complex]:
    return [center + radius * complex(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]


def kernel_matrix(kernel: Kernel, xs: Sequence[complex], ys: Sequence[complex]) -> list[list[float]]:
    """Matrix [K(x_i, y_j)]."""
    return [[kernel(x, y) for y in ys] for x in xs]


def fit_matrix(a: list[list[float]], alpha: float = 0.0) -> list[list[float]]:
    """The matrix that maps check potentials to an equivalent density.

    With alpha = 0 it is the inverse of the square matrix a. With alpha > 0
    it is the regularized pseudoinverse (A^T A + lambda I)^-1 A^T, with
    lambda = alpha times the mean of diag(A^T A); these normal equations
    square the condition number of A and lose digits for many points.
    """
    if alpha == 0.0:
        return inv(a)
    at = transpose(a)
    g = matmul(at, a)
    lam = alpha * sum(g[i][i] for i in range(len(g))) / len(g)
    for i in range(len(g)):
        g[i][i] += lam
    return matmul(inv(g), at)


def box_center(ix: int, iy: int, level: int) -> complex:
    h = 1.0 / (1 << level)
    return complex((ix + 0.5) * h, (iy + 0.5) * h)


def interaction_list(ix: int, iy: int, level: int) -> list[tuple[int, int]]:
    """Children of the near neighbours of the parent that are not near neighbours of the box (the V list)."""
    m = 1 << level
    px, py = ix // 2, iy // 2
    out = []
    for nx in range(2 * (px - 1), 2 * (px + 2)):
        for ny in range(2 * (py - 1), 2 * (py + 2)):
            if 0 <= nx < m and 0 <= ny < m and max(abs(nx - ix), abs(ny - iy)) > 1:
                out.append((nx, ny))
    return out


class Operators:
    """The matrices of one level, for boxes of side w = 2^-level, centered at 0."""

    def __init__(self, kernel: Kernel, level: int, n: int, alpha: float = 0.0):
        w = 1.0 / (1 << level)
        h = w / 2
        self.ue = circle(0j, 1.5 * h, n)
        self.uc = circle(0j, 2.5 * h, n)
        self.dc = circle(0j, 1.5 * h, n)
        self.de = circle(0j, 2.5 * h, n)
        self.uc2ue = fit_matrix(kernel_matrix(kernel, self.uc, self.ue), alpha)
        self.dc2de = fit_matrix(kernel_matrix(kernel, self.dc, self.de), alpha)
        self.m2l = {}
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if max(abs(dx), abs(dy)) > 1:
                    off = complex(dx * w, dy * w)
                    self.m2l[(dx, dy)] = kernel_matrix(kernel, self.dc, [y + off for y in self.ue])
        self.w = w


def child_matrices(kernel: Kernel, parent: Operators, child: Operators):
    """K from the child upward equivalent points to the parent upward check points,
    and K from the parent downward equivalent points to the child downward check points,
    for the four child positions."""
    up, down = {}, {}
    for a in (0, 1):
        for b in (0, 1):
            off = complex((a - 0.5) * child.w, (b - 0.5) * child.w)
            up[(a, b)] = kernel_matrix(kernel, parent.uc, [y + off for y in child.ue])
            down[(a, b)] = kernel_matrix(kernel, [x + off for x in child.dc], parent.de)
    return up, down


def _addv(acc: list[float], v: Sequence[float]) -> None:
    for k in range(len(acc)):
        acc[k] += v[k]


def kifmm(q: Sequence[float], z: Sequence[complex], kernel: Kernel = log_kernel, n_points: int = 16,
          levels: Optional[int] = None, s: int = 8, alpha: float = 0.0):
    """Potentials u_j = sum_{i != j} q_i K(z_j, z_i), with n_points points on each circle.

    levels is the leaf level L (at least 2); alpha is passed to fit_matrix.
    Returns (u, stats), where stats counts the ordered pairs of the near
    field ("p2p") and the M2L products of the V lists ("m2l").
    """
    n = len(z)
    if levels is None:
        levels = max(2, math.ceil(math.log(n / s, 4))) if n > s else 2
    L = levels
    ops = {l: Operators(kernel, l, n_points, alpha) for l in range(2, L + 1)}
    kids = {l: child_matrices(kernel, ops[l], ops[l + 1]) for l in range(2, L)}
    m = 1 << L
    leaf: dict[tuple[int, int], list[int]] = {}
    for i, zi in enumerate(z):
        key = (min(int(zi.real * m), m - 1), min(int(zi.imag * m), m - 1))
        leaf.setdefault(key, []).append(i)
    up: list[dict] = [dict() for _ in range(L + 1)]
    for key, idx in leaf.items():  # @line L1
        c = box_center(*key, L)
        check = [sum(q[i] * kernel(x + c, z[i]) for i in idx) for x in ops[L].uc]
        up[L][key] = matvec(ops[L].uc2ue, check)
    for l in range(L - 1, 1, -1):  # @line L2
        checks: dict = {}
        for (cx, cy), sig in up[l + 1].items():
            key = (cx // 2, cy // 2)
            acc = checks.setdefault(key, [0.0] * n_points)
            _addv(acc, matvec(kids[l][0][(cx % 2, cy % 2)], sig))
        for key, check in checks.items():
            up[l][key] = matvec(ops[l].uc2ue, check)
    down: list[dict] = [dict() for _ in range(L + 1)]
    n_m2l = 0
    for l in range(2, L + 1):
        mm = 1 << l
        checks = {}
        for tx in range(mm):
            for ty in range(mm):
                if l == L and (tx, ty) not in leaf:
                    continue
                acc = [0.0] * n_points
                used = False
                for src in interaction_list(tx, ty, l):  # @line L3
                    sig = up[l].get(src)
                    if sig is not None:
                        _addv(acc, matvec(ops[l].m2l[(src[0] - tx, src[1] - ty)], sig))
                        n_m2l += 1
                        used = True
                if l > 2:
                    par = down[l - 1].get((tx // 2, ty // 2))
                    if par is not None:  # @line L4
                        _addv(acc, matvec(kids[l - 1][1][(tx % 2, ty % 2)], par))
                        used = True
                if used:
                    checks[(tx, ty)] = acc
        for key, check in checks.items():  # @line L5
            down[l][key] = matvec(ops[l].dc2de, check)
    u = [0.0] * n
    n_p2p = 0
    for key, idx in leaf.items():
        c = box_center(*key, L)
        sig = down[L].get(key)
        if sig is not None:
            de = [y + c for y in ops[L].de]
            for j in idx:  # @line L6
                u[j] += sum(sk * kernel(z[j], y) for sk, y in zip(sig, de))
        ix, iy = key
        for nx in range(ix - 1, ix + 2):  # @line L7
            for ny in range(iy - 1, iy + 2):
                for i in leaf.get((nx, ny), ()):
                    for j in idx:
                        if i != j:
                            u[j] += q[i] * kernel(z[j], z[i])
                            n_p2p += 1
    return u, {"p2p": n_p2p, "m2l": n_m2l}


def direct(q: Sequence[float], z: Sequence[complex], kernel: Kernel = log_kernel) -> list[float]:
    """Direct summation over all ordered pairs: the reference."""
    n = len(z)
    return [sum(q[i] * kernel(z[j], z[i]) for i in range(n) if i != j) for j in range(n)]
