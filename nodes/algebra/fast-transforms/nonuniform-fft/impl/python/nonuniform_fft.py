# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonuniform-fft/. The authors are listed in prov/KGXG3C.jsonl.

"""Nonuniform FFT of types 1 and 2 in one dimension, with a Gaussian kernel.

Type 1: X_k = sum_j c_j exp(-2*pi*i*k*t_j) for 0 <= k < n.
Type 2: y_j = sum_k f_k exp(-2*pi*i*k*t_j) for 0 <= j < m.
With sign=+1 the exponent has the opposite sign. In exact arithmetic the
error is at most eps * ||input||_1 in every output (see proofs/correctness.md).
"""

from __future__ import annotations

import cmath
import math
from typing import Sequence

TWO_PI = 2.0 * math.pi


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


def fft(a: list[complex]) -> list[complex]:
    """Iterative radix-2 FFT, A_r = sum_l a_l exp(-2*pi*i*l*r/N), N a power of two."""
    a = list(a)
    N = len(a)
    j = 0
    for i in range(1, N):
        bit = N >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= N:
        half = size // 2
        tw = [_unit(-r, size) for r in range(half)]
        for start in range(0, N, size):
            for r in range(half):
                u, v = a[start + r], tw[r] * a[start + r + half]
                a[start + r], a[start + r + half] = u + v, u - v
        size *= 2
    return a


def parameters(n: int, eps: float) -> tuple[int, int, float]:
    """Return the half-width M, the grid size N and the kernel parameter tau."""
    if not 0 < eps < 1:
        raise ValueError("eps must lie in (0, 1)")
    M = max(2, math.ceil(3.0 / TWO_PI * math.log(4.0 / eps)))
    N = 1
    while N < max(2 * n, 2 * M):
        N *= 2
    tau = math.pi * M / (N * (N - n / 2.0))
    return M, N, tau


def nufft1(t: Sequence[float], c: Sequence[complex], n: int, eps: float = 1e-12, sign: int = -1) -> list[complex]:
    """Type 1: X_k = sum_j c_j exp(sign*2*pi*i*k*t_j), 0 <= k < n."""
    if sign == 1:
        return [z.conjugate() for z in nufft1(t, [complex(v).conjugate() for v in c], n, eps)]
    if n < 1 or len(t) != len(c):
        raise ValueError("need n >= 1 and one weight per point")
    M, N, tau = parameters(n, eps)  # @line L1
    h, s = TWO_PI / N, n // 2
    v = [0j] * N  # @line L2
    for tj, cj in zip(t, c):  # @line L3
        u = tj % 1.0  # @line L4
        x = TWO_PI * u
        b = complex(cj) * cmath.exp(-TWO_PI * 1j * s * u)
        l0 = math.floor(x / h)
        for L in range(l0 - M + 1, l0 + M + 1):  # @line L5
            v[L % N] += b * math.exp(-((L * h - x) ** 2) / (4.0 * tau))
    V = fft(v)  # @line L6
    scale = math.sqrt(math.pi / tau) / N
    X = []
    for k in range(n):  # @line L7
        kappa = k - s  # @line L8
        X.append(scale * math.exp(tau * kappa * kappa) * V[kappa % N])
    return X  # @line L9


def nufft2(t: Sequence[float], f: Sequence[complex], eps: float = 1e-12, sign: int = -1) -> list[complex]:
    """Type 2: y_j = sum_k f_k exp(sign*2*pi*i*k*t_j); the transpose of type 1."""
    if sign == 1:
        return [z.conjugate() for z in nufft2(t, [complex(v).conjugate() for v in f], eps)]
    n = len(f)
    if n < 1:
        raise ValueError("need at least one frequency")
    M, N, tau = parameters(n, eps)
    h, s = TWO_PI / N, n // 2
    scale = math.sqrt(math.pi / tau) / N
    a = [0j] * N
    for k in range(n):  # deconvolve and place on the grid
        kappa = k - s
        a[kappa % N] += scale * math.exp(tau * kappa * kappa) * complex(f[k])
    U = fft(a)
    y = []
    for tj in t:  # interpolate with the same kernel
        u = tj % 1.0
        x = TWO_PI * u
        l0 = math.floor(x / h)
        acc = 0j
        for L in range(l0 - M + 1, l0 + M + 1):
            acc += U[L % N] * math.exp(-((L * h - x) ** 2) / (4.0 * tau))
        y.append(acc * cmath.exp(-TWO_PI * 1j * s * u))
    return y
