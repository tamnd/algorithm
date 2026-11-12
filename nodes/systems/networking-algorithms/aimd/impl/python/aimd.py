# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aimd/. The authors are listed in prov/378JCS.jsonl.

"""Additive increase, multiplicative decrease in the synchronous model of
Chiu and Jain (1989): n users share one resource of capacity c, and after
each step all users get the same binary feedback, overload or not.

Rates may be Fractions, so that the traces are exact.
"""

from fractions import Fraction
from typing import Sequence

Number = int | Fraction


def linear_step(x: Sequence[Number], c: Number, inc: tuple[Number, Number], dec: tuple[Number, Number]) -> list[Number]:
    """One step of a linear control x <- a + b x.

    inc = (a_I, b_I) is used when the total load is at most c;
    dec = (a_D, b_D) when the total load is above c. Rates stay >= 0.
    """
    a, b = dec if sum(x) > c else inc
    return [max(a + b * xi, 0) for xi in x]


def aimd(x0: Sequence[Number], c: Number, a: Number, b: Number, steps: int) -> list[list[Number]]:
    """Run AIMD for the given number of steps; return the trace of rates.

    a > 0 is the additive increase, 0 < b < 1 the multiplicative decrease.
    The trace has steps + 1 vectors, the first is x0. Cost O(n * steps).
    """
    if not (a > 0 and 0 < b < 1):
        raise ValueError("need a > 0 and 0 < b < 1")
    x = list(x0)
    trace = [list(x)]
    for _ in range(steps):  # @line L1
        y = sum(x) > c  # @line L2
        for i in range(len(x)):  # @line L3
            if not y:  # @line L4
                x[i] = x[i] + a
            else:  # @line L5
                x[i] = b * x[i]
        trace.append(list(x))  # @line L6
    return trace


def jain_index(x: Sequence[Number]) -> Fraction:
    """Fairness index (sum x)^2 / (n sum x^2) of Chiu and Jain; 1 means equal."""
    s = sum(Fraction(v) for v in x)
    q = sum(Fraction(v) ** 2 for v in x)
    return s * s / (len(x) * q)
