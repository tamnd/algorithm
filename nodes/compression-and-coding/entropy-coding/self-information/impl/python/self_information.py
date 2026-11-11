# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-information/. The authors are listed in prov/10AS4N.jsonl.
"""Self-information I(x) = -log p(x), and the ideal code length of a message."""

from fractions import Fraction
from math import ceil, log, log2
from typing import Hashable, Mapping, Sequence


def self_information(p: float, base: float = 2.0) -> float:
    """I = -log p for an outcome of probability p, 0 < p <= 1. In bits for base 2."""
    if not 0 < p <= 1:
        raise ValueError("p must be in (0, 1]")
    return -log(p, base)


def message_information(msg: Sequence[Hashable], model: Mapping[Hashable, float]) -> float:
    """The sum of I(x) over the symbols of a message under a memoryless model, in bits."""
    return sum(self_information(model[x]) for x in msg)


def arithmetic_interval(msg: Sequence[Hashable], model: Mapping[Hashable, Fraction]) -> tuple[Fraction, Fraction]:
    """The final interval [low, low + width) of exact arithmetic coding of msg under a memoryless model.

    The symbols take the subintervals of [0, 1) in the order of the keys of the model.
    """
    if sum(model.values()) != 1:
        raise ValueError("the model does not sum to 1")
    cum: dict = {}
    acc = Fraction(0)
    for sym, q in model.items():
        cum[sym] = acc
        acc += q
    low, width = Fraction(0), Fraction(1)
    for x in msg:
        low += width * cum[x]
        width *= model[x]
    return low, width


def ideal_length(width: Fraction) -> float:
    """-log2 of an interval width: the ideal code length of the message, in bits."""
    return log2(width.denominator) - log2(width.numerator)


def shortest_dyadic_inside(low: Fraction, width: Fraction) -> str:
    """The shortest bit string b such that [0.b, 0.b + 2^-|b|) lies inside [low, low + width).

    This is the output of an exact arithmetic coder that stops as soon as the bits
    already sent fix the interval of the message.
    """
    high = low + width
    k = 0
    while True:
        scale = 1 << k
        m = ceil(low * scale)  # the first multiple of 2^-k at or after low
        if Fraction(m + 1, scale) <= high:
            return format(m, "b").zfill(k) if k > 0 else ""
        k += 1
