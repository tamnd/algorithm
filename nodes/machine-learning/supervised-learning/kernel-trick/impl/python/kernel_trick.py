# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-trick/. The authors are listed in prov/4044MK.jsonl.

"""The kernel trick: explicit feature maps, kernels, Gram matrices and closure rules.

A kernel k(x, z) equals an inner product phi(x) . phi(z) in a feature space.
This module builds the explicit feature map of the polynomial kernel and a
truncated feature map of the 1D Gaussian kernel, so that the identity can be
checked, and it gives tests of positive semidefiniteness for Gram matrices.
"""

import math
from fractions import Fraction
from typing import Callable, Optional, Sequence

Vec = Sequence[float]
Kernel = Callable[[Vec, Vec], float]


def dot(x: Vec, z: Vec) -> float:
    return sum(a * b for a, b in zip(x, z))


# ----- kernels ---------------------------------------------------------------


def polynomial_kernel(p: int, c: float = 1.0) -> Kernel:
    """k(x, z) = (x . z + c)^p with c >= 0 and an integer p >= 1."""
    return lambda x, z: (dot(x, z) + c) ** p


def gaussian_kernel(sigma: float) -> Kernel:
    """k(x, z) = exp(-|x - z|^2 / (2 sigma^2))."""
    return lambda x, z: math.exp(-sum((a - b) ** 2 for a, b in zip(x, z)) / (2 * sigma * sigma))


def kernel_sum(k1: Kernel, k2: Kernel) -> Kernel:
    return lambda x, z: k1(x, z) + k2(x, z)


def kernel_product(k1: Kernel, k2: Kernel) -> Kernel:
    return lambda x, z: k1(x, z) * k2(x, z)


def kernel_scale(a: float, k: Kernel) -> Kernel:
    if a < 0:
        raise ValueError("only a nonnegative scale keeps a kernel PSD")
    return lambda x, z: a * k(x, z)


def kernel_exp(k: Kernel) -> Kernel:
    """exp(k(x, z)), the limit of the partial sums of a power series with positive terms."""
    return lambda x, z: math.exp(k(x, z))


def kernel_warp(f: Callable[[Vec], float], k: Kernel) -> Kernel:
    """f(x) k(x, z) f(z) for any real function f."""
    return lambda x, z: f(x) * k(x, z) * f(z)


# ----- explicit feature maps -------------------------------------------------


def _compositions(total: int, parts: int):
    """All tuples of `parts` nonnegative integers with the given sum."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total, -1, -1):
        for rest in _compositions(total - first, parts - 1):
            yield (first,) + rest


def polynomial_features(x: Vec, p: int, c: float = 1.0) -> list[float]:
    """phi(x) with phi(x) . phi(z) = (x . z + c)^p.

    By the multinomial theorem, (c + sum_j x_j z_j)^p is the sum over
    exponents (k_0, k_1, ..., k_d) with sum p of
    multinomial(p; k) c^k_0 prod_j (x_j z_j)^k_j. Each term is the product of
    one coordinate for x and the same coordinate for z. With c = 0 only the
    terms with k_0 = 0 remain, so the map has binom(d + p - 1, p)
    coordinates; with c > 0 it has binom(d + p, p).
    """
    d = len(x)
    out = []
    for k in _compositions(p, d + 1):
        if c == 0 and k[0] > 0:
            continue
        coef = math.factorial(p) // math.prod(math.factorial(kj) for kj in k)
        v = math.sqrt(coef) * (math.sqrt(c) ** k[0] if k[0] else 1.0)
        for j in range(d):
            v *= x[j] ** k[j + 1]
        out.append(v)
    return out


def gaussian_features_1d(x: float, sigma: float, m: int) -> list[float]:
    """The first m coordinates of a feature map of the 1D Gaussian kernel.

    exp(-(x - z)^2 / 2s^2) = exp(-x^2/2s^2) exp(-z^2/2s^2) sum_k (xz/s^2)^k / k!,
    so phi_k(x) = exp(-x^2/2s^2) x^k / (s^k sqrt(k!)) for k = 0, 1, 2, ...
    Every coordinate is needed: the feature space is infinite dimensional.
    """
    g = math.exp(-x * x / (2 * sigma * sigma))
    return [g * (x / sigma) ** k / math.sqrt(math.factorial(k)) for k in range(m)]


# ----- Gram matrices and PSD tests -------------------------------------------


def gram(xs: Sequence[Vec], k: Kernel) -> list[list[float]]:
    return [[k(a, b) for b in xs] for a in xs]


def cholesky_pivots(m: Sequence[Sequence[float]], shift: float = 0.0) -> Optional[list[float]]:
    """Return the pivots of the Cholesky factorization of m + shift I, or None.

    None means that a pivot was not positive, so m + shift I is not positive
    definite. A symmetric m is PSD if and only if m + s I is positive definite
    for every s > 0.
    """
    n = len(m)
    a = [[m[i][j] + (shift if i == j else 0.0) for j in range(n)] for i in range(n)]
    pivots = []
    for j in range(n):
        s = a[j][j] - sum(a[j][t] * a[j][t] for t in range(j))
        if s <= 0:
            return None
        r = math.sqrt(s)
        a[j][j] = r
        pivots.append(s)
        for i in range(j + 1, n):
            a[i][j] = (a[i][j] - sum(a[i][t] * a[j][t] for t in range(j))) / r
    return pivots


def is_psd(m: Sequence[Sequence[float]], tol: float = 1e-9) -> bool:
    """Floating point test: m + tol * (1 + max|m_ii|) I has a Cholesky factor."""
    scale = 1.0 + max((abs(m[i][i]) for i in range(len(m))), default=0.0)
    return cholesky_pivots(m, tol * scale) is not None


def is_psd_exact(m: Sequence[Sequence[Fraction]]) -> bool:
    """Exact test for a symmetric rational matrix by symmetric elimination.

    At each step the first diagonal entry must be >= 0. If it is 0, its whole
    row must be 0 (a PSD matrix with a zero diagonal entry has a zero row);
    the row and column are then dropped. If it is positive, take the Schur
    complement, which is PSD if and only if the matrix is.
    """
    a = [[Fraction(v) for v in row] for row in m]
    while a:
        p = a[0][0]
        if p < 0:
            return False
        if p == 0:
            if any(v != 0 for v in a[0]):
                return False
            a = [row[1:] for row in a[1:]]
            continue
        a = [[a[i][j] - a[i][0] * a[0][j] / p for j in range(1, len(a))] for i in range(1, len(a))]
    return True


def rank_exact(m: Sequence[Sequence[Fraction]]) -> int:
    a = [[Fraction(v) for v in row] for row in m]
    rank = 0
    cols = len(a[0]) if a else 0
    for c in range(cols):
        p = next((r for r in range(rank, len(a)) if a[r][c] != 0), None)
        if p is None:
            continue
        a[rank], a[p] = a[p], a[rank]
        for r in range(len(a)):
            if r != rank and a[r][c] != 0:
                f = a[r][c] / a[rank][c]
                a[r] = [u - f * v for u, v in zip(a[r], a[rank])]
        rank += 1
    return rank


# ----- the template applied: a kernelized perceptron -------------------------


def kernel_perceptron(
    xs: Sequence[Vec], ys: Sequence[int], k: Kernel, max_epochs: int = 100
) -> tuple[list[int], bool]:
    """The dual perceptron: w = sum_i a_i y_i phi(x_i) is never formed.

    Returns the mistake counts a_i and whether a pass made no mistake.
    """
    n = len(xs)  # @line L1 (the dual form: f(x) = sum_j a_j y_j phi(x_j) . phi(x))
    gm = gram(xs, k)  # @line L3 (the Gram matrix replaces every x_i . x_j)
    a = [0] * n
    for _ in range(max_epochs):  # @line L4 (the solver is the perceptron)
        clean = True
        for i in range(n):
            f = sum(a[j] * ys[j] * gm[j][i] for j in range(n))  # @line L2
            if ys[i] * f <= 0:
                a[i] += 1
                clean = False
        if clean:
            return a, True
    return a, False


def kernel_predict(xs: Sequence[Vec], ys: Sequence[int], a: Sequence[int], k: Kernel, x: Vec) -> int:
    f = sum(a[j] * ys[j] * k(xs[j], x) for j in range(len(xs)))  # @line L5
    return 1 if f > 0 else -1
