# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-leakage/. The authors are listed in prov/SQWQYP.jsonl.

"""Spectral leakage of a sampled tone in the DFT, with and without a window.

A block holds N samples x[0..N-1]. Frequencies are given in cycles per block,
so a tone of c cycles has the normalized frequency 2 pi c / N radians per
sample and falls on DFT bin c when c is an integer.
"""

import cmath
import math
from typing import Sequence


def tone(n: int, cycles: float, amplitude: float = 1.0, phase: float = 0.0) -> list[float]:
    """Return amplitude * cos(2 pi cycles k / n + phase) for k = 0 .. n - 1."""
    return [amplitude * math.cos(2 * math.pi * cycles * k / n + phase) for k in range(n)]


def windowed(x: Sequence[float], w: Sequence[float]) -> list[float]:
    """Return the product x[k] w[k]."""
    return [a * b for a, b in zip(x, w)]


def dft(x: Sequence[complex]) -> list[complex]:
    """Return the DFT by the direct sum, X_k = sum of x[j] e^(-2 pi i j k / N)."""
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def hann(n: int) -> list[float]:
    """Periodic Hann window."""
    return [0.5 - 0.5 * math.cos(2 * math.pi * k / n) for k in range(n)]


def blackman(n: int) -> list[float]:
    """Periodic Blackman window."""
    return [0.42 - 0.5 * math.cos(2 * math.pi * k / n) + 0.08 * math.cos(4 * math.pi * k / n) for k in range(n)]


def far_leakage(x: Sequence[float], cycles: float, radius: float) -> float:
    """Return the fraction of the DFT energy in bins farther than radius from the tone.

    The distance of bin k from the tone is the smaller of |k - c| and
    |k - (N - c)|, so the mirror image of a real tone counts as near.
    """
    spectrum = dft(x)
    n = len(x)
    total = sum(abs(v) ** 2 for v in spectrum)
    far = sum(abs(v) ** 2 for k, v in enumerate(spectrum) if min(abs(k - cycles), abs(k - (n - cycles))) > radius)
    return far / total


def predicted_magnitude(n: int, cycles: float, k: int) -> float:
    """Closed form |X_k| for cos(2 pi cycles j / n) with the rectangular window.

    The cosine is two complex tones; each contributes half a Dirichlet kernel
    D(theta) = sum over j of e^(-i theta j) at theta = 2 pi (k -+ cycles) / n.
    """

    def dirichlet(theta: float) -> complex:
        s = math.sin(theta / 2)
        if abs(s) < 1e-14:
            return complex(n) * cmath.exp(-1j * theta * (n - 1) / 2)
        return cmath.exp(-1j * theta * (n - 1) / 2) * math.sin(n * theta / 2) / s

    return abs(0.5 * dirichlet(2 * math.pi * (k - cycles) / n) + 0.5 * dirichlet(2 * math.pi * (k + cycles) / n))
