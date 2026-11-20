# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/root-raised-cosine-filter/. The authors are listed in prov/TCPRM3.jsonl.

"""The root-raised-cosine pulse g(t) with unit energy, its truncated taps, and the pair g * g.

T is the symbol period and beta in [0, 1] the roll-off factor. The spectrum of g is the
square root of the raised-cosine spectrum, so g * g is the raised-cosine pulse.
"""

import math


def rrc_pulse(t: float, beta: float, period: float = 1.0) -> float:
    """The unit-energy root-raised-cosine pulse at time t."""
    if not 0 <= beta <= 1:
        raise ValueError("beta must be in [0, 1]")
    u = t / period  # @line L1
    if u == 0:  # @line L2
        return (1 - beta + 4 * beta / math.pi) / math.sqrt(period)
    if beta > 0 and abs(abs(4 * beta * u) - 1) < 1e-12:  # @line L3
        a = math.pi / (4 * beta)
        return beta / math.sqrt(2 * period) * ((1 + 2 / math.pi) * math.sin(a) + (1 - 2 / math.pi) * math.cos(a))
    num = math.sin(math.pi * (1 - beta) * u) + 4 * beta * u * math.cos(math.pi * (1 + beta) * u)  # @line L4
    return num / (math.sqrt(period) * math.pi * u * (1 - (4 * beta * u) ** 2))


def rrc_taps(beta: float, ls: int, span: int) -> list[float]:
    """The taps g(n/ls), n = -span*ls, ..., span*ls, for T = 1, scaled to unit energy."""
    g = [rrc_pulse(n / ls, beta) for n in range(-span * ls, span * ls + 1)]  # @line L5
    e = math.sqrt(sum(v * v for v in g))  # @line L6
    return [v / e for v in g]


def convolve(a: list[float], b: list[float]) -> list[float]:
    """The full linear convolution of two real sequences."""
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pair_at_symbols(g: list[float], ls: int) -> list[float]:
    """Samples of g * g at the center and at every ls samples from it."""
    r = convolve(g, g)  # @line L7
    c = (len(r) - 1) // 2  # @line L8
    return [r[c + k * ls] for k in range(-(c // ls), c // ls + 1)]  # @line L9
