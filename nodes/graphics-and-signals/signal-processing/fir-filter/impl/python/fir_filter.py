# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fir-filter/. The authors are listed in prov/A2Z6XD.jsonl.

"""A direct form FIR filter with a circular delay line, its frequency response,
and the four linear phase types.

Frequencies are in radians per sample, omega in [-pi, pi]. A filter of order M
has the M + 1 coefficients h[0], ..., h[M].
"""

import cmath
import math
from typing import Sequence


def fir_filter(h: Sequence, x: Sequence) -> list:
    """Return y[n] = sum over k of h[k] x[n - k], for n = 0 .. len(x) - 1.

    The state starts at zero, so x[n] = 0 for n < 0. The values may be int,
    float, complex or Fraction; the output has the type of the products.
    """
    taps = len(h)
    if taps == 0:
        raise ValueError("the filter needs at least one coefficient")
    buf = [0] * taps  # @line L1: the delay line, all zero
    pos = 0
    y = []
    for v in x:  # @line L2
        buf[pos] = v  # @line L3: the newest input goes over the oldest one
        acc = h[0] * buf[pos]  # @line L4
        idx = pos
        for k in range(1, taps):  # @line L5
            idx = idx - 1 if idx > 0 else taps - 1  # @line L6: buf[idx] = x[n - k]
            acc += h[k] * buf[idx]  # @line L7
        y.append(acc)  # @line L8
        pos = pos + 1 if pos + 1 < taps else 0  # @line L9
    return y


def frequency_response(h: Sequence, omega: float) -> complex:
    """Return H(e^(i omega)) = sum over k of h[k] e^(-i omega k)."""
    return sum(complex(c) * cmath.exp(-1j * omega * k) for k, c in enumerate(h))


def linear_phase_type(h: Sequence) -> int:
    """Return 1, 2, 3 or 4 for the four linear phase types, and 0 for none.

    Type 1: symmetric, odd length. Type 2: symmetric, even length.
    Type 3: antisymmetric, odd length. Type 4: antisymmetric, even length.
    """
    m = len(h) - 1
    if all(h[k] == h[m - k] for k in range(len(h))):
        return 1 if m % 2 == 0 else 2
    if all(h[k] == -h[m - k] for k in range(len(h))):
        return 3 if m % 2 == 0 else 4
    return 0


def amplitude(h: Sequence, omega: float) -> float:
    """Return the real amplitude A(omega) of a linear phase filter.

    For types 1 and 2, H(e^(i omega)) = e^(-i omega M / 2) A(omega).
    For types 3 and 4, H(e^(i omega)) = i e^(-i omega M / 2) A(omega).
    """
    t = linear_phase_type(h)
    m = len(h) - 1
    if t in (1, 2):
        return sum(float(c) * math.cos(omega * (m / 2 - k)) for k, c in enumerate(h))
    if t in (3, 4):
        return sum(float(c) * math.sin(omega * (m / 2 - k)) for k, c in enumerate(h))
    raise ValueError("the filter does not have linear phase")


def l1_gain(h: Sequence) -> float:
    """Return sum of |h[k]|, the largest factor by which the filter can grow a bounded input."""
    return sum(abs(c) for c in h)
