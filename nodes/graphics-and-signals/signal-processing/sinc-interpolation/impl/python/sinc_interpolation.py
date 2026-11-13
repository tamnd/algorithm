# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinc-interpolation/. The authors are listed in prov/CYHRAN.jsonl.

"""Sinc interpolation: the Whittaker-Shannon series, truncated to the given samples.

Time is in seconds. samples[j] is the value at the time (start + j) * period,
where period = 1 / fs. Samples outside the given window are taken as zero.
"""

import math
from typing import Sequence


def sinc_interpolate(samples: Sequence[float], start: int, period: float, t: float) -> float:
    """Return the sum over j of samples[j] sinc(t / period - (start + j))."""
    if period <= 0:
        raise ValueError("period must be positive")
    u = t / period  # @line L1
    if u == math.floor(u) and start <= int(u) < start + len(samples):  # @line L2
        return float(samples[int(u) - start])
    s = 0.0  # @line L3
    for j, value in enumerate(samples):  # @line L4
        v = u - (start + j)  # @line L5
        s += value * math.sin(math.pi * v) / (math.pi * v)  # @line L6
    return s  # @line L7


def sinc_interpolate_one_sine(samples: Sequence[float], start: int, period: float, t: float) -> float:
    """The same sum with one sine per output point.

    sin(pi (u - n)) = (-1)^n sin(pi u), so the sum is
    (sin(pi u) / pi) times the sum of (-1)^n samples[n] / (u - n).
    """
    if period <= 0:
        raise ValueError("period must be positive")
    u = t / period
    if u == math.floor(u) and start <= int(u) < start + len(samples):
        return float(samples[int(u) - start])
    # reduce u modulo 2 so that sin(pi u) is accurate for large u
    s = 0.0
    for j, value in enumerate(samples):
        n = start + j
        term = value / (u - n)
        s += -term if n % 2 else term
    return math.sin(math.pi * math.fmod(u, 2.0)) / math.pi * s


def sinc_interpolate_many(samples: Sequence[float], start: int, period: float, times: Sequence[float]) -> list[float]:
    """Evaluate the series at each time; Theta(N M) for N samples and M times."""
    return [sinc_interpolate(samples, start, period, t) for t in times]
