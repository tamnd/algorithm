# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-domain-equalization/. The authors are listed in prov/8TF7E6.jsonl.

"""Single-carrier frequency-domain equalization (SC-FDE) with a cyclic prefix.

The transmitter sends blocks of N symbols, each with a cyclic prefix of P >= L-1
samples. After the prefix is removed, the channel acts on the block as a circular
convolution, y = h (*) x + w with w white CN(0, N0). The DFT (unnormalized,
X[k] = sum_n x[n] e^{-j 2 pi k n / N}) turns it into Y[k] = H[k] X[k] + W[k].
The equalizer is one tap per bin, W[k] = 1/H[k] (zero forcing) or
W[k] = conj(H[k]) / (|H[k]|^2 + N0/Es) (MMSE), followed by the inverse DFT.

The FFT here is the iterative radix-2 Cooley-Tukey algorithm; other sizes use
the direct DFT.
"""

import cmath
import math


def fft(x: list[complex], inverse: bool = False) -> list[complex]:
    """The unnormalized DFT of x (or the inverse DFT, with the 1/N factor)."""
    n = len(x)
    a = [complex(v) for v in x]
    sign = 1 if inverse else -1
    if n & (n - 1) or n == 0:
        out = [sum(a[t] * cmath.exp(sign * 2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]
    else:
        j = 0
        for i in range(1, n):  # bit reversal
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        size = 2
        while size <= n:
            w = cmath.exp(sign * 2j * math.pi / size)
            for start in range(0, n, size):
                wk = 1 + 0j
                for k in range(size // 2):
                    u, v = a[start + k], a[start + k + size // 2] * wk
                    a[start + k], a[start + k + size // 2] = u + v, u - v
                    wk *= w
            size *= 2
        out = a
    if inverse and n:
        out = [v / n for v in out]
    return out


def add_cyclic_prefix(x: list[complex], p: int) -> list[complex]:
    return list(x[len(x) - p:]) + list(x) if p else list(x)


def fde(r: list[complex], h: list[complex], n: int, p: int, n0: float | None = None, es: float = 1.0) -> list[complex]:
    """Equalize one received block r of n + p samples (prefix first).

    n0 = None gives zero forcing; otherwise the MMSE taps for noise CN(0, n0)
    and symbol energy es. Returns the n soft estimates of x.
    """
    if len(h) - 1 > p:
        raise ValueError("the cyclic prefix must hold at least L-1 samples")
    if len(r) != n + p:
        raise ValueError("r must hold n + p samples")
    y = r[p:]  # @line L1
    yf = fft(y)  # @line L2
    hf = fft(list(h) + [0j] * (n - len(h)))  # @line L3
    if n0 is None:
        w = [1 / v for v in hf]  # @line L4
    else:
        w = [v.conjugate() / (abs(v) ** 2 + n0 / es) for v in hf]  # @line L5
    return fft([a * b for a, b in zip(w, yf)], inverse=True)  # @line L6


def mmse_mse(h: list[complex], n: int, n0: float, es: float = 1.0) -> float:
    """The MSE per symbol of the MMSE-FDE: (1/N) sum_k N0 Es / (Es |H[k]|^2 + N0)."""
    hf = fft(list(h) + [0j] * (n - len(h)))
    return sum(n0 * es / (es * abs(v) ** 2 + n0) for v in hf) / n


def zf_mse(h: list[complex], n: int, n0: float) -> float:
    """The noise variance per symbol after the ZF-FDE: (1/N) sum_k N0 / |H[k]|^2."""
    hf = fft(list(h) + [0j] * (n - len(h)))
    return sum(n0 / abs(v) ** 2 for v in hf) / n


def channel(s: list[complex], h: list[complex], prev: list[complex] | None = None) -> list[complex]:
    """Linear convolution of the transmitted samples s with h, cut to len(s).

    prev holds the samples sent before s (the previous block), so that its tail
    falls into the prefix of s, as in a real stream.
    """
    prev = list(prev) if prev is not None else []
    full = prev + list(s)
    off = len(prev)
    return [sum(h[l] * full[off + k - l] for l in range(len(h)) if off + k - l >= 0) for k in range(len(s))]
