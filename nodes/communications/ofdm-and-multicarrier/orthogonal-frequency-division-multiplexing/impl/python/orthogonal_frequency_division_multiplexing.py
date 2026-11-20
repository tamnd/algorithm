# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-frequency-division-multiplexing/. The authors are listed in prov/2QCF2N.jsonl.

"""OFDM: inverse FFT and cyclic prefix at the transmitter, FFT and one tap per
subcarrier at the receiver.

The page uses the unitary DFT pair: x = F^H X and Y = F y, with
F[k, n] = e^(-j 2 pi k n / N) / sqrt(N). The channel frequency response is the
unnormalized DFT H[k] = sum over l of h[l] e^(-j 2 pi k l / N). If the prefix
length is at least L - 1 for a channel of L taps, the receiver sees
Y[k] = H[k] X[k] + W[k] on each subcarrier k.

fft is an iterative radix-2 FFT for a power of two N, and a direct sum
otherwise. It is here because OFDM costs O(N log N) per symbol only with it.
"""

import cmath
import math


def fft(x: list[complex], inverse: bool = False) -> list[complex]:
    """sum over n of x[n] e^(-+ j 2 pi k n / N), with no scale factor.

    The sign is minus for the forward transform and plus for inverse=True.
    """
    n = len(x)
    sign = 1.0 if inverse else -1.0
    if n == 0:
        return []
    if n & (n - 1):  # not a power of two: direct sum
        w = [cmath.exp(sign * 2j * math.pi * t / n) for t in range(n)]
        return [sum(x[t] * w[(k * t) % n] for t in range(n)) for k in range(n)]
    a = [complex(v) for v in x]
    j = 0
    for i in range(1, n):  # bit-reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        half = size // 2
        step = cmath.exp(sign * 2j * math.pi / size)
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(start, start + half):
                t = w * a[k + half]
                a[k + half] = a[k] - t
                a[k] = a[k] + t
                w *= step
        size *= 2
    return a


def ufft(x: list[complex]) -> list[complex]:
    """The unitary DFT F x."""
    s = 1.0 / math.sqrt(len(x))
    return [v * s for v in fft(x)]


def uifft(xf: list[complex]) -> list[complex]:
    """The unitary inverse DFT F^H X."""
    s = 1.0 / math.sqrt(len(xf))
    return [v * s for v in fft(xf, inverse=True)]


def modulate(xf: list[complex], ncp: int) -> list[complex]:
    """One OFDM symbol: N + ncp time samples for the N subcarrier symbols xf."""
    n = len(xf)
    if not 0 <= ncp <= n:
        raise ValueError("need 0 <= ncp <= N")
    x = uifft(xf)  # @line L1
    return x[n - ncp:] + x  # @line L2


def transmit(blocks: list[list[complex]], ncp: int) -> list[complex]:
    """The sample stream of several OFDM symbols, one after the other."""
    out: list[complex] = []
    for xf in blocks:
        out += modulate(xf, ncp)
    return out


def demodulate(r: list[complex], n: int, ncp: int) -> list[complex]:
    """Drop the prefix of one received symbol of N + ncp samples and take the FFT."""
    if len(r) < n + ncp:
        raise ValueError("need N + ncp samples")
    y = r[ncp:ncp + n]  # @line L3
    return ufft(y)  # @line L4


def channel_response(h: list[complex], n: int) -> list[complex]:
    """H[k] = sum over l of h[l] e^(-j 2 pi k l / N), the unnormalized DFT of the taps."""
    if len(h) > n:
        raise ValueError("more taps than subcarriers")
    return fft(list(h) + [0j] * (n - len(h)))  # @line L5


def equalize(yf: list[complex], hf: list[complex]) -> list[complex]:
    """The one-tap equalizer X[k] = Y[k] / H[k]."""
    return [y / hk for y, hk in zip(yf, hf)]  # @line L6


def receive(r: list[complex], h: list[complex], n: int, ncp: int, count: int) -> list[list[complex]]:
    """Demodulate and equalize count consecutive OFDM symbols of the stream r."""
    hf = channel_response(h, n)
    out = []
    for i in range(count):
        start = i * (n + ncp)
        out.append(equalize(demodulate(r[start:start + n + ncp], n, ncp), hf))
    return out
