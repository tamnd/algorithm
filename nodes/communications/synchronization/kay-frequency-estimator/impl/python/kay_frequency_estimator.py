# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kay-frequency-estimator/. The authors are listed in prov/9RD1BP.jsonl.

"""Kay's weighted phase averager for the frequency of one complex tone.

For r[t] = A e^(j(omega t + phi)) + w[t], t = 0, ..., N-1, the phase
differences arg(r[t+1] conj(r[t])) are omega plus noise. At high SNR that
noise is a moving-average process, and the best linear unbiased weights are

  w_t = 6 (t + 1) (N - 1 - t) / (N (N^2 - 1)),  t = 0, ..., N-2,

a parabola that sums to 1. The estimate is omega_hat = sum_t w_t arg(r[t+1] conj(r[t]))
in radians per sample, for |omega| < pi. Its variance reaches the Cramer-Rao
bound 6 / (SNR N (N^2 - 1)) above a threshold SNR.
"""

import cmath
from typing import Sequence


def kay_weights(n: int) -> list[float]:
    """The N - 1 Kay weights 6 (t+1)(N-1-t) / (N (N^2 - 1))."""
    if n < 2:
        raise ValueError("need at least two samples")
    return [6.0 * (t + 1) * (n - 1 - t) / (n * (n * n - 1)) for t in range(n - 1)]


def kay_estimate(r: Sequence[complex]) -> float:
    """The frequency estimate in radians per sample, a weighted mean of angles in (-pi, pi]."""
    n = len(r)  # @line L1
    w = kay_weights(n)  # @line L1
    omega = 0.0  # @line L2
    for t in range(n - 1):  # @line L3
        d = cmath.phase(r[t + 1] * r[t].conjugate())  # @line L4
        omega += w[t] * d  # @line L5
    return omega  # @line L6


def crb(n: int, snr: float) -> float:
    """The Cramer-Rao bound on the variance of an unbiased estimate of omega (rad^2 per sample^2)."""
    return 6.0 / (snr * n * (n * n - 1))
