# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/haar-wavelet-transform/. The authors are listed in prov/5B1Q93.jsonl.

import math
from fractions import Fraction
from typing import TypeVar

S = TypeVar("S", float, Fraction)

ORTHONORMAL = 1 / math.sqrt(2)
AVERAGES = Fraction(1, 2)


def _check_length(n: int) -> None:
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")


def haar(x: list[S], c: S) -> None:
    """Replace x by its full Haar transform, in place.

    Precondition: n = len(x) is a power of two. The scale c is 1/sqrt(2)
    for the orthonormal transform or 1/2 for the transform by averages.
    After the call, x[0] is the coarsest scaling coefficient and
    x[2**j + k] is the detail coefficient of level j and position k.
    Cost: 2n - 2 additions and 2n - 2 multiplications by c, Theta(n) time,
    and a buffer of n entries.
    """
    n = len(x)  # @line L1
    _check_length(n)
    t = [x[0]] * n
    m = n
    while m >= 2:  # @line L2
        h = m // 2
        for i in range(h):  # @line L3
            t[i] = c * (x[2 * i] + x[2 * i + 1])  # @line L4
            t[h + i] = c * (x[2 * i] - x[2 * i + 1])  # @line L5
        x[:m] = t[:m]  # @line L6
        m = h  # @line L7


def inverse_haar(y: list[S], c: S) -> None:
    """Undo haar(y, c), in place. Same precondition and cost as haar."""
    n = len(y)
    _check_length(n)
    t = [y[0]] * n
    two_c = 2 * c
    m = 2  # @line L8
    while m <= n:  # @line L9
        h = m // 2
        for i in range(h):  # @line L10
            t[2 * i] = (y[i] + y[h + i]) / two_c  # @line L11
            t[2 * i + 1] = (y[i] - y[h + i]) / two_c  # @line L12
        y[:m] = t[:m]  # @line L13
        m *= 2  # @line L14
