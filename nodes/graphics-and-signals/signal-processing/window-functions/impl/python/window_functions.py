# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/window-functions/. The authors are listed in prov/YX4DES.jsonl.

"""Classic window functions and the measurement of their spectral figures.

A window of length N is a list w[0], ..., w[N - 1]. The periodic (DFT-even)
form uses the period N in the cosines and is the one used for spectral
analysis; the symmetric form uses N - 1 and is the one used for filter design.
Frequencies are in radians per sample; widths are given in DFT bins of
2 pi / N radians.
"""

import cmath
import math
from typing import Sequence


def _denominator(n: int, symmetric: bool) -> int:
    if n <= 0:
        raise ValueError("length must be positive")
    if symmetric:
        return max(n - 1, 1)
    return n


def cosine_sum(n: int, coeffs: Sequence[float], symmetric: bool = False) -> list[float]:
    """Return w[k] = sum over j of (-1)^j coeffs[j] cos(2 pi j k / D), D = N or N - 1."""
    d = _denominator(n, symmetric)
    return [sum((-1) ** j * a * math.cos(2 * math.pi * j * k / d) for j, a in enumerate(coeffs)) for k in range(n)]


def rectangular(n: int) -> list[float]:
    return [1.0] * n


def hann(n: int, symmetric: bool = False) -> list[float]:
    return cosine_sum(n, [0.5, 0.5], symmetric)


def hamming(n: int, symmetric: bool = False) -> list[float]:
    return cosine_sum(n, [0.54, 0.46], symmetric)


def blackman(n: int, symmetric: bool = False) -> list[float]:
    return cosine_sum(n, [0.42, 0.5, 0.08], symmetric)


def bessel_i0(x: float) -> float:
    """Modified Bessel function I0 by its power series, sum of ((x/2)^k / k!)^2."""
    total, term, k = 1.0, 1.0, 0
    while True:
        k += 1
        term *= (x / (2 * k)) ** 2
        total += term
        if term < 1e-17 * total:
            return total


def kaiser(n: int, beta: float) -> list[float]:
    """Symmetric Kaiser window I0(beta sqrt(1 - r^2)) / I0(beta), r from -1 to 1."""
    if n == 1:
        return [1.0]
    return [bessel_i0(beta * math.sqrt(max(0.0, 1 - (2 * k / (n - 1) - 1) ** 2))) / bessel_i0(beta) for k in range(n)]


def dtft_magnitude(w: Sequence[float], omega: float) -> float:
    """Return |W(e^(i omega))| by the direct sum."""
    return abs(sum(v * cmath.exp(-1j * omega * k) for k, v in enumerate(w)))


def coherent_gain(w: Sequence[float]) -> float:
    """Return the mean of the window, W(1) / N."""
    return sum(w) / len(w)


def enbw_bins(w: Sequence[float]) -> float:
    """Return the equivalent noise bandwidth N sum w^2 / (sum w)^2, in bins."""
    return len(w) * sum(v * v for v in w) / sum(w) ** 2


def measure(w: Sequence[float], oversample: int = 64) -> dict[str, float]:
    """Measure the main lobe and side lobes from a dense direct DTFT on [0, pi].

    Returns the first null (half-width of the main lobe, in bins), the -3 dB
    full width (in bins, refined by bisection), the peak side lobe level and
    the scalloping loss at half a bin (both in dB).
    """
    n = len(w)
    step = 2 * math.pi / (n * oversample)
    peak = dtft_magnitude(w, 0.0)
    count = n * oversample // 2 + 1
    mags = [dtft_magnitude(w, j * step) for j in range(count)]
    j = 1
    while j + 1 < count and mags[j + 1] < mags[j]:
        j += 1
    first_null = j / oversample
    side = max(mags[j:]) if j < count else 0.0
    target = peak / math.sqrt(2)
    lo, hi = 0.0, j * step
    for _ in range(60):
        mid = (lo + hi) / 2
        if dtft_magnitude(w, mid) > target:
            lo = mid
        else:
            hi = mid
    half_power = (lo + hi) / 2
    return {
        "first_null_bins": first_null,
        "bandwidth_3db_bins": 2 * half_power / (2 * math.pi / n),
        "peak_sidelobe_db": 20 * math.log10(side / peak) if side > 0 else -math.inf,
        "scalloping_db": 20 * math.log10(dtft_magnitude(w, math.pi / n) / peak),
    }
