# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raised-cosine-filter/. The authors are listed in prov/QN0P95.jsonl.

"""The raised-cosine pulse h(t), its spectrum H(f) and the taps of a truncated FIR filter.

T is the symbol period and beta in [0, 1] the roll-off factor. sinc(x) = sin(pi x)/(pi x).
The pulse has h(0) = 1 and h(kT) = 0 for every integer k != 0.
"""

import math


def sinc(x: float) -> float:
    """sin(pi x)/(pi x), with sinc(0) = 1."""
    if x == 0:
        return 1.0
    return math.sin(math.pi * x) / (math.pi * x)


def rc_pulse(t: float, beta: float, period: float = 1.0) -> float:
    """The raised-cosine pulse at time t."""
    if not 0 <= beta <= 1:
        raise ValueError("beta must be in [0, 1]")
    u = t / period  # @line L1
    if beta > 0 and abs(abs(2 * beta * u) - 1) < 1e-12:  # @line L2
        return math.pi / 4 * sinc(1 / (2 * beta))  # @line L3
    return sinc(u) * math.cos(math.pi * beta * u) / (1 - (2 * beta * u) ** 2)  # @line L4


def rc_spectrum(f: float, beta: float, period: float = 1.0) -> float:
    """The raised-cosine spectrum H(f), equal to T on the flat part."""
    a = abs(f)
    lo = (1 - beta) / (2 * period)
    hi = (1 + beta) / (2 * period)
    if beta == 0 and a == lo:
        return period / 2  # the midpoint of the jump, so that the fold stays flat
    if a <= lo:
        return period
    if a > hi:
        return 0.0
    return period / 2 * (1 + math.cos(math.pi * period / beta * (a - lo)))


def rc_taps(beta: float, ls: int, span: int) -> list[float]:
    """h(n/ls) for n = -span*ls, ..., span*ls, with T = 1 and ls samples per symbol."""
    return [rc_pulse(n / ls, beta) for n in range(-span * ls, span * ls + 1)]  # @line L5
