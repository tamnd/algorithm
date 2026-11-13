# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hilbert-transform/. The authors are listed in prov/MW0VT7.jsonl.

"""The discrete Hilbert transform of a periodic signal of period N, two ways.

Frequencies are in radians per sample; bin k of an N-point DFT is 2 pi k / N.
The multiplier is H[k] = -i for 0 < k < N/2, +i for N/2 < k < N, and 0 at k = 0
and k = N/2. The same operator is a circular convolution with the kernel
h[n] = (2/N) cot(pi n / N) for odd n and 0 for even n (N even).
"""

import cmath
import math
from typing import Sequence


def dft(a: Sequence[complex], sign: int = -1) -> list[complex]:
    n = len(a)
    return [sum(a[j] * cmath.exp(sign * 2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def multiplier(n: int) -> list[complex]:
    """-i sgn(k) on the DFT bins, with the bins 0 and n/2 set to 0."""
    out = []
    for k in range(n):
        if k == 0 or 2 * k == n:
            out.append(0j)
        elif 2 * k < n:
            out.append(-1j)
        else:
            out.append(1j)
    return out


def hilbert(x: Sequence[float]) -> list[float]:
    """Multiply the DFT by -i sgn(k) and transform back. O(N^2) here; an FFT makes it O(N log N)."""
    n = len(x)
    spec = [h * v for h, v in zip(multiplier(n), dft(x))]
    return [v.real / n for v in dft(spec, +1)]


def kernel(n: int) -> list[float]:
    """The periodic Hilbert kernel for even n: (2/n) cot(pi m / n) for odd m, 0 for even m."""
    if n % 2:
        raise ValueError("the closed form is for even n")
    return [2 / n / math.tan(math.pi * m / n) if m % 2 else 0.0 for m in range(n)]


def hilbert_by_convolution(x: Sequence[float]) -> list[float]:
    """The circular convolution of x with the kernel, the direct O(N^2) sum."""
    n = len(x)
    h = kernel(n)
    return [sum(h[m] * x[(i - m) % n] for m in range(n)) for i in range(n)]


def ideal_fir(half: int) -> list[float]:
    """Taps h[-half .. half] of the ideal discrete-time Hilbert transformer, 2/(pi n) for odd n, truncated."""
    return [2 / (math.pi * m) if m % 2 else 0.0 for m in range(-half, half + 1)]
