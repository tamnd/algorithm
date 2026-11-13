# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sampling-theorem/. The authors are listed in prov/JHNYYV.jsonl.

"""Tools to check the sampling theorem on concrete signals.

Time is in seconds, frequencies in Hz, and the sampling rate fs in samples
per second. Sample n is taken at the time n / fs.
"""

import cmath
import math
from typing import Sequence


def sinc(u: float) -> float:
    """Return the normalized sinc, sin(pi u) / (pi u), with sinc(0) = 1."""
    if u == 0:
        return 1.0
    return math.sin(math.pi * u) / (math.pi * u)


def cardinal_series(samples: Sequence[float], start: int, fs: float, t: float) -> float:
    """Return the truncated series sum of x[n] sinc(fs t - n).

    samples[j] is the sample at the index n = start + j. The terms outside the
    given window are taken as zero.
    """
    u = fs * t
    if u == int(u) and start <= int(u) < start + len(samples):
        return float(samples[int(u) - start])
    return sum(v * sinc(u - (start + j)) for j, v in enumerate(samples))


def tone_amplitudes(freqs: Sequence[float], samples: Sequence[complex], fs: float) -> list[complex]:
    """Find a_k with sum over k of a_k exp(2 pi i f_k n / fs) = samples[n], n = 0 .. K - 1.

    K is the number of frequencies. The system is a Vandermonde system in the
    points z_k = exp(2 pi i f_k / fs); it has a unique solution exactly when
    these points are distinct, that is when no two frequencies differ by a
    multiple of fs. Raises ValueError when the system is singular.
    """
    k_count = len(freqs)
    if len(samples) < k_count:
        raise ValueError("need at least one sample per frequency")
    rows = [[cmath.exp(2j * math.pi * f * n / fs) for f in freqs] + [complex(samples[n])] for n in range(k_count)]
    for col in range(k_count):
        pivot = max(range(col, k_count), key=lambda r: abs(rows[r][col]))
        if abs(rows[pivot][col]) < 1e-9:
            raise ValueError("frequencies alias onto each other at this rate")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(col + 1, k_count):
            factor = rows[r][col] / rows[col][col]
            for c in range(col, k_count + 1):
                rows[r][c] -= factor * rows[col][c]
    out = [0j] * k_count
    for r in range(k_count - 1, -1, -1):
        acc = rows[r][k_count] - sum(rows[r][c] * out[c] for c in range(r + 1, k_count))
        out[r] = acc / rows[r][r]
    return out
