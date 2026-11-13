# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiener-khinchin-theorem/. The authors are listed in prov/QHCYJX.jsonl.

"""Both sides of the finite Wiener-Khinchin identity, computed separately.

Left side: the periodogram P(w) = |sum of x[n] e^(-iwn)|^2 / N.
Right side: the Fourier sum of the biased sample autocorrelation,
sum over |k| < N of r[k] e^(-iwk). The frequency w is in radians per sample.
"""

import cmath
from typing import Callable, Sequence


def _conj(v):
    return v.conjugate() if isinstance(v, complex) else v


def biased_autocorrelation(x: Sequence) -> list:
    """r[0], ..., r[N - 1] with r[k] = (1/N) sum of x[n + k] conj(x[n]). Cost: O(N^2)."""
    n = len(x)
    return [sum(x[j + k] * _conj(x[j]) for j in range(n - k)) / n for k in range(n)]


def laurent_square(x: Sequence) -> list:
    """Coefficients of X(z) conj(X)(1/z) / N, from z^-(N-1) to z^(N-1).

    X(z) = sum of x[n] z^(-n). The product is computed term by term, so with
    int or Fraction input it is exact. Entry N - 1 + k is the coefficient of z^(-k).
    """
    n = len(x)
    out = [0] * (2 * n - 1)
    for m in range(n):
        for j in range(n):
            out[n - 1 + (m - j)] += x[m] * _conj(x[j])
    return [v / n for v in out]


def periodogram_at(x: Sequence[complex], w: float) -> float:
    """|sum of x[n] e^(-iwn)|^2 / N, by the direct sum. Cost: O(N)."""
    s = sum(v * cmath.exp(-1j * w * k) for k, v in enumerate(x))
    return abs(s) ** 2 / len(x)


def correlogram_at(r: Sequence[complex], w: float) -> float:
    """sum over |k| < len(r) of r[k] e^(-iwk), with r[-k] = conj(r[k]). Cost: O(len(r))."""
    total = complex(r[0])
    for k in range(1, len(r)):
        total += r[k] * cmath.exp(-1j * w * k) + _conj(r[k]) * cmath.exp(1j * w * k)
    return total.real


def dft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """The direct DFT of any length L, in O(L^2). The inverse divides by L."""
    size = len(a)
    sign = 1 if inverse else -1
    out = []
    for m in range(size):
        s = 0j
        for k, v in enumerate(a):
            s += v * cmath.exp(sign * 2j * cmath.pi * m * k / size)
        out.append(s / size if inverse else s)
    return out


def periodogram_dft(x: Sequence[complex], size: int) -> list[float]:
    """P at w_m = 2 pi m / size for m = 0, ..., size - 1, with x padded to size >= N."""
    n = len(x)
    if size < n:
        raise ValueError("size must be at least N")
    spec = dft(list(x) + [0] * (size - n))
    return [abs(v) ** 2 / n for v in spec]


def lags_from_periodogram(x: Sequence[complex], size: int) -> list[complex]:
    """The inverse DFT of the sampled periodogram, entries 0 to size - 1.

    For size >= 2N - 1 entry k is r[k] for 0 <= k < N and entry size - k is
    r[-k]. For a smaller size the lags k and k - size add up (time aliasing).
    """
    return dft(periodogram_dft(x, size), inverse=True)


def folded_autocorrelation(x: Sequence, size: int) -> list:
    """The biased autocorrelation wrapped onto size slots: slot j holds the sum of r[k] over k = j mod size."""
    n = len(x)
    r = biased_autocorrelation(x)
    out = [0] * size
    for k in range(-(n - 1), n):
        out[k % size] += r[k] if k >= 0 else _conj(r[-k])
    return out


def expected_periodogram(r: Callable[[int], complex], n: int, w: float) -> float:
    """E[P_N(w)] = sum over |k| < n of (1 - |k|/n) r(k) e^(-iwk) for a WSS process with autocorrelation r."""
    total = complex(r(0))
    for k in range(1, n):
        weight = 1 - k / n
        total += weight * (r(k) * cmath.exp(-1j * w * k) + _conj(r(k)) * cmath.exp(1j * w * k))
    return total.real
