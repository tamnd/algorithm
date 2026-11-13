# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/analytic-signal/. The authors are listed in prov/F0XV5Y.jsonl.

"""The discrete analytic signal by the DFT method of Marple (1999).

Frequencies are in radians per sample. For an N-point real signal x with DFT X,
the analytic signal z has the DFT
    Z[0] = X[0], Z[k] = 2 X[k] for 0 < k < N/2, Z[N/2] = X[N/2] (N even),
    Z[k] = 0 for the negative frequencies N/2 < k < N.
Then Re z = x and Im z is the discrete Hilbert transform of x.
"""

import cmath
import math
from typing import Sequence


def dft(a: Sequence[complex], sign: int = -1) -> list[complex]:
    n = len(a)
    return [sum(a[j] * cmath.exp(sign * 2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def weights(n: int) -> list[int]:
    """1 at DC and at Nyquist (even n), 2 on the positive bins, 0 on the negative bins."""
    out = []
    for k in range(n):
        if k == 0 or 2 * k == n:
            out.append(1)
        elif 2 * k < n:
            out.append(2)
        else:
            out.append(0)
    return out


def analytic_signal(x: Sequence[float]) -> list[complex]:
    n = len(x)
    spec = [w * v for w, v in zip(weights(n), dft(x))]
    return [v / n for v in dft(spec, +1)]


def envelope(z: Sequence[complex]) -> list[float]:
    return [abs(v) for v in z]


def instantaneous_phase(z: Sequence[complex]) -> list[float]:
    """The unwrapped phase in radians: each step is moved into (-pi, pi]."""
    out = [cmath.phase(z[0])]
    for a, b in zip(z, z[1:]):
        step = cmath.phase(b / a)
        out.append(out[-1] + step)
    return out


def instantaneous_frequency(z: Sequence[complex]) -> list[float]:
    """The phase step between neighbouring samples, in radians per sample."""
    return [cmath.phase(b / a) for a, b in zip(z, z[1:])]
