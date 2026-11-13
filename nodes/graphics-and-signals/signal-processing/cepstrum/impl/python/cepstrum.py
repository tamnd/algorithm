# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cepstrum/. The authors are listed in prov/YRJ2PT.jsonl.

"""The real cepstrum c = IDFT(log |DFT x|) of a finite signal.

The index n of c is the quefrency, in samples. An echo x[n] = s[n] + a s[n - d]
multiplies the spectrum by 1 + a e^(-i w d), so it adds
    log |1 + a e^(-i w d)| = sum_{k >= 1} (-1)^(k+1) a^k cos(k w d) / k    (|a| < 1)
to log |X|, and that term puts peaks at the quefrencies d, 2d, 3d, ...
"""

import cmath
import math
from typing import Sequence


def fft(a: Sequence[complex], sign: int = -1) -> list[complex]:
    """Radix-2 FFT; the length must be a power of two. sign=+1 gives the unnormalized inverse."""
    n = len(a)
    if n == 1:
        return [complex(a[0])]
    if n % 2:
        raise ValueError("length must be a power of two")
    even = fft(a[0::2], sign)
    odd = fft(a[1::2], sign)
    out = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(sign * 2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + n // 2] = even[k] - t
    return out


def dft(a: Sequence[complex], sign: int = -1) -> list[complex]:
    n = len(a)
    return [sum(a[j] * cmath.exp(sign * 2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def real_cepstrum(x: Sequence[float]) -> list[float]:
    """Fails with ValueError if a DFT bin is exactly zero, where the log is not defined."""
    n = len(x)
    spec = fft(list(x))
    if any(v == 0 for v in spec):
        raise ValueError("a spectral zero has no logarithm")
    logmag = [complex(math.log(abs(v))) for v in spec]
    return [v.real / n for v in fft(logmag, +1)]


def echo_cepstrum(n: int, delay: int, a: float, terms: int = 200) -> list[float]:
    """The closed form of the real cepstrum of delta[m] + a delta[m - delay] on n points, |a| < 1."""
    out = [0.0] * n
    for k in range(1, terms + 1):
        v = (-1) ** (k + 1) * a**k / (2 * k)
        out[(k * delay) % n] += v
        out[(-k * delay) % n] += v
    return out


def circular_echo(s: Sequence[float], delay: int, a: float) -> list[float]:
    n = len(s)
    return [s[i] + a * s[(i - delay) % n] for i in range(n)]


def peak_quefrency(c: Sequence[float], low: int, high: int) -> int:
    """The quefrency in low .. high - 1 with the largest cepstral value."""
    return max(range(low, high), key=lambda q: c[q])
