# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wright-fisher-diffusion/. The authors are listed in prov/ET1T47.jsonl.
"""The diffusion approximation of the Wright-Fisher model, and the exact
chain to compare it with.

A diploid population of N individuals (2N copies). The genotypes AA, Aa and
aa have fitnesses 1 + s, 1 + h s and 1. Kimura's genic form 1 + 2 s_K,
1 + s_K, 1 is s = 2 s_K, h = 1/2.

Per generation, the change of the frequency x of A has, to first order in s
and 1/N, the mean M(x) = s x (1 - x) (h + (1 - 2h) x) and the variance
V(x) = x (1 - x) / (2N). Time is in generations in this module unless a
function says otherwise; the generator in units of 2N generations is
(1/2) x (1 - x) d^2/dx^2 + 2N M(x) d/dx.
"""

from __future__ import annotations

import math
from typing import List, Tuple


def moments(x: float, N: int, s: float = 0.0, h: float = 0.5) -> Tuple[float, float]:
    """(M(x), V(x)): the mean and variance of the change of x per generation."""
    m = s * x * (1 - x) * (h + (1 - 2 * h) * x)  # @line L1
    v = x * (1 - x) / (2 * N)  # @line L1
    return m, v


def generator_coefficients(x: float, N: int, s: float = 0.0, h: float = 0.5) -> Tuple[float, float]:
    """The drift and half the variance in units of 2N generations:
    (2N M(x), x (1 - x) / 2). They stay of order one when N s is fixed."""
    m, v = moments(x, N, s, h)
    return 2 * N * m, 2 * N * v / 2  # @line L2


def scale_density(y: float, N: int, s: float = 0.0, h: float = 0.5) -> float:
    """psi(y) = exp(-integral from 0 to y of 2 M / V) = exp(-4 N s (h y + (1 - 2h) y^2 / 2))."""
    return math.exp(-4 * N * s * (h * y + (1 - 2 * h) * y * y / 2))  # @line L4


def _grid(n: int) -> List[float]:
    return [i / n for i in range(n + 1)]


def _cumulative(f: List[float], n: int) -> List[float]:
    """Trapezoid integrals of f on [0, i/n], i = 0..n."""
    out = [0.0]
    for i in range(n):
        out.append(out[-1] + (f[i] + f[i + 1]) / (2 * n))
    return out


def fixation_probability(p: float, N: int, s: float = 0.0, h: float = 0.5, n: int = 4000) -> float:
    """u(p) solving (V/2) u'' + M u' = 0 with u(0) = 0 and u(1) = 1, so
    u(p) = int_0^p psi / int_0^1 psi, by the trapezoid rule with n cells
    (and Simpson's rule on the last partial cell)."""
    if not 0.0 <= p <= 1.0:
        raise ValueError("need 0 <= p <= 1")
    # Boundary values u(0) = 0 and u(1) = 1 of the backward equation.  # @line L3
    if s == 0:
        return p  # @line L3
    xs = _grid(n)
    psi = [scale_density(x, N, s, h) for x in xs]
    total = _cumulative(psi, n)[-1]  # @line L4
    k = int(p * n)
    part = _cumulative(psi[: k + 1], k)[-1] * (k / n) if k > 0 else 0.0
    a = k / n
    mid = scale_density((a + p) / 2, N, s, h)
    part += (p - a) / 6 * (scale_density(a, N, s, h) + 4 * mid + scale_density(p, N, s, h))
    return part / total  # @line L4


def kimura_genic(p: float, N: int, s_k: float) -> float:
    """Kimura's formula (1 - exp(-4 N s_K p)) / (1 - exp(-4 N s_K)) for the
    fitnesses 1 + 2 s_K, 1 + s_K, 1; p when s_K = 0."""
    if s_k == 0:
        return p
    return -math.expm1(-4 * N * s_k * p) / -math.expm1(-4 * N * s_k)


def absorption_time(p: float, N: int, s: float = 0.0, h: float = 0.5, n: int = 4000) -> float:
    """The mean time to loss or fixation, in generations:
    t(p) = int_0^1 G(p, y) dy with the Green function
      G(p, y) = 2 (1 - u(p)) S(y) / (V(y) psi(y))        for y <= p,
      G(p, y) = 2 u(p) (S(1) - S(y)) / (V(y) psi(y))     for y >  p,
    where S(y) = int_0^y psi. Midpoint rule on n cells."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    xs = _grid(n)
    psi = [scale_density(x, N, s, h) for x in xs]
    S = _cumulative(psi, n)
    u = fixation_probability(p, N, s, h, n)
    total = 0.0
    for i in range(n):
        y = (i + 0.5) / n
        Sy = (S[i] + S[i + 1]) / 2
        _, v = moments(y, N, s, h)
        ps = scale_density(y, N, s, h)
        if y <= p:
            g = 2 * (1 - u) * Sy / (v * ps)  # @line L5
        else:
            g = 2 * u * (S[n] - Sy) / (v * ps)  # @line L5
        total += g / n
    return total  # @line L5


def neutral_absorption_time(p: float, N: int) -> float:
    """-4N (p ln p + q ln q) generations."""
    q = 1 - p
    return -4 * N * ((p * math.log(p) if p > 0 else 0.0) + (q * math.log(q) if q > 0 else 0.0))


def exact_chain(two_n: int, s: float = 0.0, h: float = 0.5) -> Tuple[List[float], List[float]]:
    """Fixation probabilities and mean absorption times (generations) of the
    discrete Wright-Fisher chain with 2N copies, for each start 0..2N, by
    Gaussian elimination on (I - Q) [u t] = [r 1]."""
    size = two_n - 1
    rows = []
    for i in range(1, two_n):
        x = i / two_n
        q = 1 - x
        w_bar = x * x * (1 + s) + 2 * x * q * (1 + h * s) + q * q
        ps = x * (x * (1 + s) + q * (1 + h * s)) / w_bar
        pr = [math.comb(two_n, j) * ps ** j * (1 - ps) ** (two_n - j) for j in range(two_n + 1)]
        row = [(1.0 if i == j else 0.0) - pr[j] for j in range(1, two_n)]
        rows.append(row + [pr[two_n], 1.0])  # @line L6
    for c in range(size):
        piv = max(range(c, size), key=lambda r: abs(rows[r][c]))
        rows[c], rows[piv] = rows[piv], rows[c]
        for r in range(size):
            if r != c and rows[r][c] != 0.0:
                f = rows[r][c] / rows[c][c]
                for k in range(c, size + 2):
                    rows[r][k] -= f * rows[c][k]
    u = [0.0] + [rows[r][size] / rows[r][r] for r in range(size)] + [1.0]
    t = [0.0] + [rows[r][size + 1] / rows[r][r] for r in range(size)] + [0.0]
    return u, t  # @line L6
