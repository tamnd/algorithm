# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-compensation/. The authors are listed in prov/4CW95Q.jsonl.

"""Iterative sampling density compensation (Pipe and Menon 1999).

Input: m k-space sample positions (tuples of floats in grid units, any
dimension) and a radial kernel C(r) that is zero for r >= width / 2. The
method looks for weights w > 0 with sum_j C(|k_i - k_j|) w_j = 1 at every
sample i, so that the weighted samples, convolved with C, give a flat
density. It starts from w = 1 and repeats the update
    w_i <- w_i / sum_j C(|k_i - k_j|) w_j.

Facts used by the tests (see proofs/correctness.md):
- every iterate is positive when C(0) > 0 and C >= 0;
- a positive w is a fixed point exactly when C w = 1;
- replacing C by c C (c > 0) divides every iterate after the first by c.
The paper gives no convergence proof, and none is claimed here.

Cost: O(m^2) to build the neighbour lists by brute force, then O(K m q)
for K iterations when each sample has at most q neighbours.
"""

import math
from typing import Callable, Sequence

Point = Sequence[float]


def bessel_i0(x: float) -> float:
    """The modified Bessel function I0 by its power series sum ((x/2)^(2k) / (k!)^2)."""
    term, total, k = 1.0, 1.0, 0
    q = (x / 2.0) ** 2
    while term > 1e-17 * total:
        k += 1
        term *= q / (k * k)
        total += term
    return total


def kaiser_bessel(width: float, beta: float) -> Callable[[float], float]:
    """C(r) = I0(beta sqrt(1 - (2 r / width)^2)) / I0(beta) for r < width / 2, else 0."""
    norm = bessel_i0(beta)

    def c(r: float) -> float:
        u = 2.0 * r / width
        if u >= 1.0:
            return 0.0
        return bessel_i0(beta * math.sqrt(1.0 - u * u)) / norm

    return c


def triangle(width: float) -> Callable[[float], float]:
    """C(r) = 1 - 2 r / width for r < width / 2, else 0."""

    def c(r: float) -> float:
        u = 2.0 * r / width
        return 1.0 - u if u < 1.0 else 0.0

    return c


def neighbours(points: Sequence[Point], kernel: Callable[[float], float], width: float) -> list[list[tuple[int, float]]]:
    """For each sample i, the pairs (j, C(|k_i - k_j|)) with |k_i - k_j| < width / 2."""
    m = len(points)
    half = width / 2.0
    out: list[list[tuple[int, float]]] = [[] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            r = math.dist(points[i], points[j])
            if r < half:
                v = kernel(r)
                if v != 0.0:
                    out[i].append((j, v))
    return out


def pipe_menon(
    points: Sequence[Point],
    kernel: Callable[[float], float],
    width: float,
    iters: int = 50,
) -> list[float]:
    """Density compensation weights by the Pipe-Menon fixed-point iteration."""
    if kernel(0.0) <= 0.0:
        raise ValueError("the kernel must be positive at 0")
    nb = neighbours(points, kernel, width)  # @line L1
    w = [1.0] * len(points)  # @line L2
    for _ in range(iters):  # @line L3
        d = [sum(c * w[j] for j, c in row) for row in nb]  # @line L4
        w = [wi / di for wi, di in zip(w, d)]  # @line L5
    return w  # @line L6


def kernel_matrix(points: Sequence[Point], kernel: Callable[[float], float]) -> list[list[float]]:
    """The dense m x m matrix C_ij = C(|k_i - k_j|)."""
    return [[kernel(math.dist(p, q)) for q in points] for p in points]


def residual(points: Sequence[Point], kernel: Callable[[float], float], w: Sequence[float]) -> float:
    """max_i |sum_j C_ij w_j - 1|."""
    c = kernel_matrix(points, kernel)
    return max(abs(sum(cij * wj for cij, wj in zip(row, w)) - 1.0) for row in c)


def radial_points(spokes: int, samples: int, kmax: float) -> list[tuple[float, float]]:
    """A radial trajectory: spokes through the center at angles pi s / spokes, samples per spoke.

    Sample q of a spoke sits at radius kmax (2 q - samples + 1) / samples, so
    no spoke has a sample at the exact center when samples is even.
    """
    pts = []
    for s in range(spokes):
        a = math.pi * s / spokes
        ca, sa = math.cos(a), math.sin(a)
        for q in range(samples):
            r = kmax * (2 * q - samples + 1) / samples
            pts.append((r * ca, r * sa))
    return pts
