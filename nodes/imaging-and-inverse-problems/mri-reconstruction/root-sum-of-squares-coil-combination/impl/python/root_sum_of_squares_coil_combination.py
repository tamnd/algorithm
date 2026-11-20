# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/root-sum-of-squares-coil-combination/. The authors are listed in prov/4R76FY.jsonl.

"""Root-sum-of-squares (RSS) coil combination (Roemer et al. 1990).

Each coil k gives a complex image m_k. RSS combines them pixel by pixel:

    rss(p) = sqrt(sum_k |m_k(p)|^2).

With a noise covariance Psi between the coils (Psi = E[n n^H] for the noise
vector n of one pixel), the coils are first whitened with the Cholesky factor
Psi = L L^H: the combination is ||L^{-1} v|| = sqrt(v^H Psi^{-1} v), where v
is the vector of the coil values at one pixel.

optimal_combination is the combination of Roemer et al. with known coil
maps s: s^H Psi^{-1} v / (s^H Psi^{-1} s), an unbiased estimate of the
object with the least noise variance among the linear unbiased ones.
"""

import math
from typing import Optional, Sequence

from imgla import cho_solve, cholesky

Image = list[list[complex]]


def rss(coils: Sequence[Image]) -> list[list[float]]:
    """sqrt(sum_k |m_k|^2) at every pixel."""
    n1, n2 = len(coils[0]), len(coils[0][0])
    return [[math.sqrt(sum(abs(m[i][j]) ** 2 for m in coils)) for j in range(n2)] for i in range(n1)]


def _forward(low: list[list[complex]], v: list[complex]) -> list[complex]:
    """Solve L w = v for a lower triangular L."""
    w: list[complex] = []
    for i in range(len(v)):
        w.append((v[i] - sum(low[i][k] * w[k] for k in range(i))) / low[i][i])
    return w


def rss_prewhitened(coils: Sequence[Image], psi: Optional[Sequence[Sequence[complex]]] = None) -> list[list[float]]:
    """sqrt(v^H Psi^{-1} v) at every pixel; Psi = I gives the plain RSS."""
    c, n1, n2 = len(coils), len(coils[0]), len(coils[0][0])
    if psi is None:
        psi = [[1.0 if a == b else 0.0 for b in range(c)] for a in range(c)]
    low = cholesky(psi)  # @line L1
    out = [[0.0] * n2 for _ in range(n1)]
    for i in range(n1):  # @line L2
        for j in range(n2):
            v = [coils[k][i][j] for k in range(c)]  # @line L3
            w = _forward(low, v)  # @line L4
            out[i][j] = math.sqrt(sum(abs(x) ** 2 for x in w))  # @line L5
    return out  # @line L6


def optimal_combination(
    coils: Sequence[Image],
    maps: Sequence[Image],
    psi: Optional[Sequence[Sequence[complex]]] = None,
) -> Image:
    """s^H Psi^{-1} v / (s^H Psi^{-1} s) at every pixel (Roemer et al. 1990, with known maps)."""
    c, n1, n2 = len(coils), len(coils[0]), len(coils[0][0])
    if psi is None:
        psi = [[1.0 if a == b else 0.0 for b in range(c)] for a in range(c)]
    low = cholesky(psi)
    out = [[0j] * n2 for _ in range(n1)]
    for i in range(n1):
        for j in range(n2):
            s = [maps[k][i][j] for k in range(c)]
            v = [coils[k][i][j] for k in range(c)]
            u = cho_solve(low, s)  # Psi^{-1} s
            den = sum(a.conjugate() * b for a, b in zip(u, s)).real
            out[i][j] = sum(a.conjugate() * b for a, b in zip(u, v)) / den if den > 0 else 0j
    return out
