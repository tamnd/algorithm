# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-two-sum/. The authors are listed in prov/R9EM9Q.jsonl.

"""Fast2Sum (Dekker, 1971): the exact error of a binary64 addition in three operations."""

import math

E_MIN = -1022  # smallest exponent of a normal binary64 number


def exponent(x: float) -> int:
    """The exponent e of a finite float x, with 2^e <= |x| < 2^(e+1) for normal x.

    Subnormal numbers and zero get e = E_MIN, the exponent used for the
    spacing of the subnormal range. Cost: O(1).
    """
    if x == 0.0:
        return E_MIN
    return max(math.frexp(x)[1] - 1, E_MIN)


def precondition_holds(a: float, b: float) -> bool:
    """True when Fast2Sum is guaranteed exact for (a, b): both finite and exponent(a) >= exponent(b).

    A sufficient test that is easy to apply is |a| >= |b|. Cost: O(1).
    """
    return math.isfinite(a) and math.isfinite(b) and exponent(a) >= exponent(b)


def fast_two_sum(a: float, b: float) -> tuple[float, float]:
    """Return (s, t) with s = fl(a + b) and, under the precondition, a + b = s + t exactly.

    Precondition: a and b are finite, exponent(a) >= exponent(b) (for example
    |a| >= |b|), and a + b does not overflow. Arithmetic is binary64 with
    round to nearest, as Python floats are. Without the precondition the pair
    is still returned but t need not be the error. Cost: 3 floating-point
    operations, O(1) space.
    """
    s = a + b  # @line L1
    z = s - a  # @line L2
    t = b - z  # @line L3
    return s, t  # @line L4
