# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luise-reggiannini-estimator/. The authors are listed in prov/6HGD52.jsonl.

"""The Luise and Reggiannini (L and R) frequency estimator.

For z[k] = A e^(j(2 pi nu k + phi)) + w[k], k = 0, ..., N-1 (the received
samples with the known data removed), compute the sample autocorrelations

  R(m) = 1/(N - m) sum_{k=m}^{N-1} z[k] conj(z[k-m]),  m = 1, ..., L,

and estimate the normalized frequency nu (cycles per sample) as

  nu_hat = arg(sum_{m=1}^{L} R(m)) / (pi (L + 1)).

Without noise this is exact for |nu| < 1/(L + 1), which is the range of the
estimator. L is the design parameter: L = N/2 gives a variance close to the
Cramer-Rao bound, and a smaller L gives a wider range.
"""

import cmath
import math
from typing import Sequence


def autocorrelation(z: Sequence[complex], m: int) -> complex:
    """R(m) = 1/(N - m) sum_{k=m}^{N-1} z[k] conj(z[k-m])."""
    n = len(z)
    return sum(z[k] * z[k - m].conjugate() for k in range(m, n)) / (n - m)


def lr_estimate(z: Sequence[complex], big_l: int) -> float:
    """The L and R estimate of nu, in cycles per sample, in (-1/(L+1), 1/(L+1)]."""
    n = len(z)  # @line L1
    if not 1 <= big_l <= n - 1:
        raise ValueError("need 1 <= L <= N - 1")
    s = 0j  # @line L2
    for m in range(1, big_l + 1):  # @line L3
        s += autocorrelation(z, m)  # @line L4
    return cmath.phase(s) / (math.pi * (big_l + 1))  # @line L5


def crb_nu(n: int, snr: float) -> float:
    """The Cramer-Rao bound on the variance of nu_hat: 6 / ((2 pi)^2 SNR N (N^2 - 1))."""
    return 6.0 / ((2.0 * math.pi) ** 2 * snr * n * (n * n - 1))
