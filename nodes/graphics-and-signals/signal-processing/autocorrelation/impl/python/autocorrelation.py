# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autocorrelation/. The authors are listed in prov/CHSTEW.jsonl.

"""Sample autocorrelation of a finite signal, by the defining sum and by the FFT.

A signal is a list x[0], ..., x[N - 1] of int, Fraction, float or complex
values. The lag k runs from 0 to max_lag; negative lags follow from
r[-k] = conj(r[k]).
"""

import cmath
from typing import Sequence


def _conj(v):
    return v.conjugate() if isinstance(v, complex) else v


def autocorrelation(x: Sequence, max_lag: int | None = None, scale: str = "biased") -> list:
    """Return r[0], ..., r[max_lag] with r[k] = c(k) * sum over n of x[n + k] conj(x[n]).

    scale "biased" uses c(k) = 1/N, "unbiased" uses c(k) = 1/(N - k) and
    "none" uses c(k) = 1 (the deterministic autocorrelation of a finite
    sequence). With int or Fraction input and scale "none" the result is
    exact; with "biased" or "unbiased" pass Fraction values to keep it exact.
    Cost: O(N K) operations for K = max_lag + 1 lags.
    """
    n = len(x)
    if n == 0:
        return []
    if max_lag is None:
        max_lag = n - 1
    if not 0 <= max_lag <= n - 1:
        raise ValueError("max_lag must be in [0, N - 1]")
    out = []
    for k in range(max_lag + 1):
        s = 0
        for j in range(n - k):
            s += x[j + k] * _conj(x[j])
        out.append(_scaled(s, k, n, scale))
    return out


def _scaled(s, k: int, n: int, scale: str):
    if scale == "none":
        return s
    if scale == "biased":
        return s / n
    if scale == "unbiased":
        return s / (n - k)
    raise ValueError("scale must be 'biased', 'unbiased' or 'none'")


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 iterative FFT. len(a) must be a power of two.

    The forward transform is A[m] = sum of a[n] e^(-2 pi i m n / L); the
    inverse uses e^(+2 pi i m n / L) and divides by L. Cost: O(L log L).
    """
    size = len(a)
    if size == 0 or size & (size - 1):
        raise ValueError("length must be a power of two")
    out = [complex(v) for v in a]
    j = 0
    for i in range(1, size):
        bit = size >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    sign = 1 if inverse else -1
    length = 2
    while length <= size:
        w_len = cmath.exp(sign * 2j * cmath.pi / length)
        half = length // 2
        for start in range(0, size, length):
            w = 1 + 0j
            for t in range(half):
                u = out[start + t]
                v = out[start + t + half] * w
                out[start + t] = u + v
                out[start + t + half] = u - v
                w *= w_len
        length <<= 1
    if inverse:
        out = [v / size for v in out]
    return out


def autocorrelation_fft(x: Sequence[complex], max_lag: int | None = None, scale: str = "biased") -> list[complex]:
    """The same values as autocorrelation, computed with the FFT.

    The signal is padded with zeros to a power of two L >= 2N - 1, so the
    circular correlation that the DFT gives has no wrap-around. Cost:
    O(N log N) operations. The result has rounding errors of order
    1e-15 times the energy of x.
    """
    n = len(x)
    if n == 0:
        return []
    if max_lag is None:
        max_lag = n - 1
    if not 0 <= max_lag <= n - 1:
        raise ValueError("max_lag must be in [0, N - 1]")
    size = 1
    while size < 2 * n - 1:
        size <<= 1
    spec = fft(list(x) + [0] * (size - n))
    power = [abs(v) ** 2 for v in spec]
    raw = fft(power, inverse=True)
    real_input = all(not isinstance(v, complex) for v in x)
    out = []
    for k in range(max_lag + 1):
        v = raw[k].real if real_input else raw[k]
        out.append(_scaled(v, k, n, scale))
    return out


def autocovariance(x: Sequence, max_lag: int | None = None, scale: str = "biased") -> list:
    """Autocorrelation of x minus its sample mean (the sample autocovariance)."""
    n = len(x)
    if n == 0:
        return []
    mean = sum(x) / n
    return autocorrelation([v - mean for v in x], max_lag, scale)


def toeplitz(r: Sequence) -> list[list]:
    """The Hermitian Toeplitz matrix R[i][j] = r[i - j], with r[-k] = conj(r[k])."""
    p = len(r)
    return [[r[i - j] if i >= j else _conj(r[j - i]) for j in range(p)] for i in range(p)]
