# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sc-fdma/. The authors are listed in prov/1A5ZQW.jsonl.

"""SC-FDMA (DFT-spread OFDM): transmitter, receiver and the PAPR measurement.

A user with M data symbols takes their unitary M-point DFT, places the M
values on M of the N subcarriers (a block of adjacent subcarriers, localized,
or every Q-th subcarrier, interleaved, with Q = N / M), takes the unitary
N-point inverse DFT and adds a cyclic prefix. The receiver removes the prefix,
takes the N-point DFT, picks the M subcarriers, equalizes each with one tap
and takes the M-point inverse DFT. The FFT is a radix-2 FFT, so M, N and the
oversampling factor must be powers of two.
"""

import cmath
import math
from typing import Optional, Sequence


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


def udft(x: Sequence[complex]) -> list[complex]:
    """The unitary DFT F x, with F[k, n] = e^(-j 2 pi k n / n_len) / sqrt(n_len)."""
    s = 1.0 / math.sqrt(len(x))
    return [v * s for v in fft(x)]


def uidft(X: Sequence[complex]) -> list[complex]:
    """The unitary inverse DFT F^H X."""
    s = 1.0 / math.sqrt(len(X))
    return [v * s for v in fft(X, inverse=True)]


def subcarriers(m: int, n: int, mapping: str, offset: int = 0) -> list[int]:
    """The N-point subcarrier indices of the M DFT outputs."""
    if n % m:
        raise ValueError("M must divide N")
    if mapping == "localized":
        return [(offset + i) % n for i in range(m)]
    if mapping == "interleaved":
        q = n // m
        return [(offset + q * i) % n for i in range(m)]
    raise ValueError("mapping must be localized or interleaved")


def transmit(d: Sequence[complex], n: int, mapping: str, offset: int = 0, cp: int = 0) -> list[complex]:
    """One SC-FDMA symbol with its cyclic prefix."""
    D = udft(d)  # @line L1
    X = [0j] * n  # @line L2
    for v, k in zip(D, subcarriers(len(d), n, mapping, offset)):
        X[k] = v
    x = uidft(X)  # @line L3
    return x[n - cp:] + x if cp else x  # @line L4


def receive(
    r: Sequence[complex], m: int, n: int, mapping: str, offset: int = 0, cp: int = 0,
    h: Optional[Sequence[complex]] = None, noise_var: float = 0.0,
) -> list[complex]:
    """Recover the M data symbols with one-tap MMSE equalization (zero forcing when noise_var = 0).

    h is the channel impulse response, at most cp + 1 taps long.
    """
    Y = udft(list(r[cp: cp + n]))  # @line L5
    hk = fft(list(h) + [0j] * (n - len(h))) if h is not None else [1 + 0j] * n
    Z = []
    for k in subcarriers(m, n, mapping, offset):  # @line L6
        Z.append(hk[k].conjugate() * Y[k] / (abs(hk[k]) ** 2 + noise_var))
    return uidft(Z)  # @line L7


def channel(x: Sequence[complex], h: Sequence[complex]) -> list[complex]:
    """Linear convolution with h, cut to the length of x."""
    return [sum(h[l] * x[t - l] for l in range(len(h)) if t - l >= 0) for t in range(len(x))]


def oversampled(d: Sequence[complex], n: int, mapping: str, offset: int = 0, L: int = 4) -> list[complex]:
    """The SC-FDMA symbol (no prefix) oversampled by L, zeros in the middle of the spectrum, scaled by sqrt(L)."""
    X = [0j] * n
    for v, k in zip(udft(d), subcarriers(len(d), n, mapping, offset)):
        X[k] = v
    z = [0j] * (L * n)
    z[: n // 2] = X[: n // 2]
    z[L * n - n + n // 2:] = X[n // 2:]
    s = 1.0 / math.sqrt(n)
    return [v * s for v in fft(z, inverse=True)]


def papr(x: Sequence[complex]) -> float:
    """max |x[m]|^2 over the time average of |x[m]|^2."""
    p = [abs(v) ** 2 for v in x]
    return max(p) / (sum(p) / len(p))
