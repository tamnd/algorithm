# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsevals-theorem/. The authors are listed in prov/3S9P1H.jsonl.

"""The two sides of Parseval's theorem for the DTFT.

Frequencies are in radians per sample. A finite sequence x[0], x[1], ... is
zero outside the listed indices.
"""

import cmath
import math
from typing import Callable, Sequence


def energy(x: Sequence[complex]) -> float:
    """Return the time-domain energy, the sum of |x[n]|^2."""
    return sum(abs(v) ** 2 for v in x)


def inner(x: Sequence[complex], y: Sequence[complex]) -> complex:
    """Return the sum of x[n] times the conjugate of y[n]."""
    return sum(a * complex(b).conjugate() for a, b in zip(x, y))


def autocorrelation(x: Sequence[complex], d: int) -> complex:
    """Return r[d] = sum over n of x[n + d] times the conjugate of x[n].

    With integer or Fraction input the result is exact.
    """
    n = len(x)
    total = 0
    for j in range(max(0, -d), min(n, n - d)):
        total += x[j + d] * x[j].conjugate()
    return total


def dtft(x: Sequence[complex], omega: float) -> complex:
    """Return the direct sum X(e^(i omega)) = sum over n of x[n] e^(-i omega n)."""
    return sum(v * cmath.exp(-1j * omega * k) for k, v in enumerate(x))


def frequency_mean(g: Callable[[float], float], m: int) -> float:
    """Return (1/m) times the sum of g(2 pi k / m) for k = 0 .. m - 1.

    This is the trapezoidal rule for (1/(2 pi)) times the integral of a
    2 pi periodic function g over one period.
    """
    if m <= 0:
        raise ValueError("m must be positive")
    return sum(g(2 * math.pi * k / m) for k in range(m)) / m


def spectral_energy(x: Sequence[complex], m: int) -> float:
    """Return (1/m) times the sum of |X(e^(i 2 pi k / m))|^2.

    For m >= len(x) this equals (1/(2 pi)) times the integral of |X|^2.
    """
    return frequency_mean(lambda w: abs(dtft(x, w)) ** 2, m)
