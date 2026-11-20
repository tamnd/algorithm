# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preamble-correlation-detection/. The authors are listed in prov/31P2YC.jsonl.

"""Preamble correlation detection with a threshold on the normalized correlation.

The input is a stream of complex symbols y[0..] at one sample per symbol and a
known preamble s[0..L-1]. For each start n the detector forms

    c(n) = sum_i conj(s[i]) y[n + i],   E(n) = sum_i |y[n + i]|^2,
    rho(n) = |c(n)|^2 / (E_s E(n)),     E_s = sum_i |s[i]|^2.

By the Cauchy-Schwarz inequality 0 <= rho(n) <= 1, with rho(n) = 1 exactly when
y[n..n+L-1] is a complex multiple of s. rho does not change when y is scaled by
any nonzero complex number, so it needs neither the carrier phase nor the gain
nor the noise level. The detector declares the first n with rho(n) >= lambda,
then moves to the largest rho in the next L - 1 starts.

On noise alone, y i.i.d. CN(0, sigma^2), P(rho(n) >= lambda) = (1 - lambda)^(L - 1)
for each n, for every sigma.
"""

import cmath
import math
from typing import Optional, Sequence


def threshold_for_pfa(pfa: float, length: int) -> float:
    """lambda with (1 - lambda)^(L - 1) = pfa, the false alarm rate per start on noise alone."""
    return 1.0 - pfa ** (1.0 / (length - 1))


def normalized_correlation(y: Sequence[complex], s: Sequence[complex]) -> list[float]:
    """rho(n) for n = 0, ..., len(y) - L, with a running sum for E(n)."""
    length = len(s)
    es = sum(abs(v) ** 2 for v in s)
    energy = sum(abs(v) ** 2 for v in y[:length])  # @line L1
    out: list[float] = []
    for n in range(len(y) - length + 1):  # @line L2
        if n > 0:
            energy += abs(y[n + length - 1]) ** 2 - abs(y[n - 1]) ** 2  # @line L3
        c = sum(s[i].conjugate() * y[n + i] for i in range(length))  # @line L4
        out.append(abs(c) ** 2 / (es * energy) if energy > 0 else 0.0)  # @line L5
    return out


def detect(
    y: Sequence[complex], s: Sequence[complex], lam: float
) -> Optional[tuple[int, float, complex]]:
    """The first preamble start whose rho passes lam, refined to the peak.

    Return (n, rho(n), gain) with the complex gain estimate c(n) / E_s, or None.
    """
    rho = normalized_correlation(y, s)
    length = len(s)
    for n, r in enumerate(rho):  # @line L6
        if r >= lam:  # @line L7
            window = range(n, min(n + length, len(rho)))
            best = max(window, key=lambda k: rho[k])  # @line L8
            es = sum(abs(v) ** 2 for v in s)
            c = sum(s[i].conjugate() * y[best + i] for i in range(length))
            return best, rho[best], c / es  # @line L9
    return None  # @line L10


def phase_of(gain: complex) -> float:
    """The carrier phase estimate arg(c(n)), in (-pi, pi]."""
    return cmath.phase(gain)


def recompute_energy(y: Sequence[complex], n: int, length: int) -> float:
    """E(n) by a direct sum, to check or to reset the running sum."""
    return math.fsum(abs(v) ** 2 for v in y[n:n + length])
