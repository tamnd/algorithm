# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peak-to-average-power-ratio/. The authors are listed in prov/Z633YX.jsonl.

"""The peak-to-average power ratio (PAPR) of an OFDM symbol, measured with oversampling.

The OFDM symbol is x = F^H X with the unitary DFT pair. The oversampled symbol
puts (L - 1) N zeros in the middle of X, so that the indices k >= N/2 stay the
negative frequencies, and takes an inverse FFT of size L N scaled by sqrt(L).
Then x_L[L n] equals the Nyquist-rate sample x[n], and the mean power of x_L
equals the mean of |X[k]|^2. The FFT is a radix-2 Cooley-Tukey FFT, so N and L
must be powers of two.
"""

import cmath
import math
from typing import Sequence


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT with no scale factor: sum_n a[n] e^(-+ j 2 pi k n / n_len)."""
    n = len(a)
    if n == 0 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    out = [complex(v) for v in a]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    sign = 1 if inverse else -1
    size = 2
    while size <= n:
        half = size // 2
        tw = [cmath.exp(sign * 2j * math.pi * k / size) for k in range(half)]
        for s in range(0, n, size):
            for k in range(half):
                u = out[s + k]
                v = out[s + k + half] * tw[k]
                out[s + k] = u + v
                out[s + k + half] = u - v
        size *= 2
    return out


def ofdm_oversampled(X: Sequence[complex], L: int = 4) -> list[complex]:
    """The OFDM symbol F^H X sampled L times per Nyquist interval."""
    n = len(X)
    if n < 2 or L < 1:
        raise ValueError("need N >= 2 and L >= 1")
    z = [0j] * (L * n)  # @line L1
    for k in range(n // 2):
        z[k] = complex(X[k])
    for k in range(n // 2, n):
        z[L * n - n + k] = complex(X[k])
    s = math.sqrt(L) / math.sqrt(L * n)
    return [v * s for v in fft(z, inverse=True)]  # @line L2


def papr(x: Sequence[complex], mean_power: float | None = None) -> float:
    """max |x[n]|^2 divided by the mean power.

    The mean power is the time average of |x[n]|^2 unless mean_power gives the
    ensemble mean E|x[n]|^2. For constant-modulus subcarrier symbols the two are equal.
    """
    p = [abs(v) ** 2 for v in x]
    peak = max(p)  # @line L3
    mean = sum(p) / len(p) if mean_power is None else mean_power
    return peak / mean  # @line L4


def papr_db(x: Sequence[complex], mean_power: float | None = None) -> float:
    """The PAPR in dB."""
    return 10.0 * math.log10(papr(x, mean_power))


def ccdf_rule(gamma: float, n: int) -> float:
    """The rule P(PAPR > gamma) = 1 - (1 - e^-gamma)^N for gamma as a linear ratio."""
    return 1.0 - (1.0 - math.exp(-gamma)) ** n
