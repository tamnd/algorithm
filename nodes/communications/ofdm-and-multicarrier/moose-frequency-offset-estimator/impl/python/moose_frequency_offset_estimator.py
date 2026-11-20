# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moose-frequency-offset-estimator/. The authors are listed in prov/6JQ8CA.jsonl.

"""Moose's estimator of the carrier frequency offset from two copies of one OFDM symbol.

The transmitter sends the same N samples twice. The second copy starts
N + G samples after the first (G = 0 if the copies follow each other, G = the
prefix length if each copy has its own prefix). A carrier offset epsilon, in
subcarrier spacings, turns subcarrier k of the second copy into
Y2[k] = e^(j 2 pi epsilon (N + G) / N) Y1[k] + noise. The estimate is

    C = sum over k of conj(Y1[k]) Y2[k]
    epsilon_hat = angle(C) N / (2 pi (N + G))

and its range is |epsilon| < N / (2 (N + G)). The page uses the unitary DFT,
so C is also sum over n of conj(y1[n]) y2[n] (Plancherel).
"""

import cmath
import math

import cbb


def correlation(y1: list[complex], y2: list[complex]) -> complex:
    """C = sum over k of conj(Y1[k]) Y2[k], from the two received copies in the time domain."""
    if len(y1) != len(y2) or not y1:
        raise ValueError("the two copies must have the same nonzero length")
    f1, f2 = cbb.udft(y1), cbb.udft(y2)  # @line L1
    return sum(a.conjugate() * b for a, b in zip(f1, f2))  # @line L2


def estimate(y1: list[complex], y2: list[complex], gap: int = 0) -> float:
    """epsilon_hat in subcarrier spacings. gap is G, the number of samples between the copies."""
    n = len(y1)
    c = correlation(y1, y2)
    return cmath.phase(c) * n / (2 * math.pi * (n + gap))  # @line L3


def estimate_time_domain(y1: list[complex], y2: list[complex], gap: int = 0) -> float:
    """The same estimate with C = sum over n of conj(y1[n]) y2[n], with no DFT."""
    n = len(y1)
    c = sum(a.conjugate() * b for a, b in zip(y1, y2))
    return cmath.phase(c) * n / (2 * math.pi * (n + gap))
