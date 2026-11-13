# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-shrinkage-thresholding/. The authors are listed in prov/XSY6C1.jsonl.

"""Iterative shrinkage-thresholding for the l1-regularised least squares problem

    minimize F(x) = 1/2 ||A x - y||^2 + lam ||x||_1.

Each step is a gradient step on the smooth part with step 1/L, followed by
soft thresholding at lam/L. L must be at least the largest eigenvalue of A^T A.
With int or Fraction data and a rational L, every iterate is exact.
"""

from fractions import Fraction


def soft_threshold(v, t):
    """The proximal map of t|.|: shrink v towards zero by t, and set it to zero inside [-t, t]."""
    if v > t:
        return v - t
    if v < -t:
        return v + t
    return v * 0


def matvec(A: list[list], x: list) -> list:
    return [sum((a * b for a, b in zip(row, x)), 0) for row in A]


def rmatvec(A: list[list], r: list) -> list:
    """A^T r."""
    return [sum((A[i][j] * r[i] for i in range(len(A))), 0) for j in range(len(A[0]))]


def objective(A: list[list], y: list, lam, x: list):
    r = [a - b for a, b in zip(matvec(A, x), y)]
    return sum((v * v for v in r), 0) / 2 + lam * sum((abs(v) for v in x), 0)


def ista_step(A: list[list], y: list, lam, L, x: list) -> list:
    r = [a - b for a, b in zip(matvec(A, x), y)]
    g = rmatvec(A, r)  # @line L3
    v = [xi - gi / L for xi, gi in zip(x, g)]  # @line L4
    return [soft_threshold(vi, lam / L) for vi in v]  # @line L5


def ista(A: list[list], y: list, lam, L, iters: int, x0: list | None = None) -> list[list]:
    """Run `iters` steps from x0 (zero by default). Returns the iterates x_0, ..., x_iters."""
    if L <= 0:
        raise ValueError("L must be positive")
    x = list(x0) if x0 is not None else [Fraction(0)] * len(A[0])  # @line L1
    xs = [x]
    for _ in range(iters):  # @line L2
        x = ista_step(A, y, lam, L, x)
        xs.append(x)
    return xs  # @line L6
