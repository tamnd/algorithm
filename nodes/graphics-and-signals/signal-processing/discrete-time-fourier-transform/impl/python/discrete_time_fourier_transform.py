# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-time-fourier-transform/. The authors are listed in prov/0QHXWM.jsonl.

"""The discrete-time Fourier transform of a finite sequence, by the direct sum.

Frequencies are in radians per sample. The sequence x[0], x[1], ... is placed
at the times start, start + 1, ...
"""

import cmath
import math
from typing import Sequence


def dtft(x: Sequence[complex], omega: float, start: int = 0) -> complex:
    """Return X(e^(i omega)) = sum over n of x[n] e^(-i omega n)."""
    total = 0j
    for k, v in enumerate(x):
        total += v * cmath.exp(-1j * omega * (start + k))
    return total


def dtft_at_bins(x: Sequence[complex], m: int, start: int = 0) -> list[complex]:
    """Return the DTFT at the m frequencies 2 pi k / m, for k = 0 .. m - 1."""
    if m <= 0:
        raise ValueError("m must be positive")
    return [dtft(x, 2 * math.pi * k / m, start) for k in range(m)]


def dirichlet(length: int, omega: float) -> complex:
    """Closed form of the DTFT of the box x[n] = 1 for 0 <= n < length."""
    if length <= 0:
        return 0j
    half = math.sin(omega / 2)
    if abs(half) < 1e-12:
        # omega is (close to) a multiple of 2 pi, where every term of the sum is 1
        return complex(length)
    return cmath.exp(-1j * omega * (length - 1) / 2) * math.sin(length * omega / 2) / half


def inverse_from_bins(values: Sequence[complex], n: int) -> complex:
    """Return (1/m) sum over k of X(e^(i 2 pi k / m)) e^(i 2 pi k n / m).

    This is the trapezoidal rule for the inverse DTFT integral. It is exact
    for a sequence supported on m consecutive times that contain n.
    """
    m = len(values)
    return sum(values[k] * cmath.exp(2j * math.pi * k * n / m) for k in range(m)) / m


def fold(x: Sequence[complex], n: int) -> list[complex]:
    """Return the length-n periodization: y[j] = sum over r of x[j + r n]."""
    if n <= 0:
        raise ValueError("n must be positive")
    y = [0j] * n
    for k, v in enumerate(x):
        y[k % n] += v
    return y
