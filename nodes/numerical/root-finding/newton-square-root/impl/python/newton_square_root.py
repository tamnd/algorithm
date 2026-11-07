# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-square-root/. The authors are listed in prov/MBGG7T.jsonl.

"""Newton's method for the square root (Heron's method), with range reduction."""

import math
from dataclasses import dataclass
from typing import Any, List


@dataclass
class SqrtResult:
    """The computed square root, why the loop ended, and the work done."""

    root: float
    reason: str  # "exact input", "converged", "kmax reached" or "invalid"
    iterations: int
    divisions: int


def newton_sqrt(a: float, max_iter: int = 60) -> SqrtResult:
    """Square root of a float by Newton's method x <- (x + m/x)/2.

    Precondition: a is a float. Negative numbers and NaN give "invalid";
    0, -0.0 and +inf are returned unchanged. The argument is reduced
    exactly to a = m * 4^e with 1/2 <= m < 2, the iteration runs on m from
    x = (1 + m)/2 and stops as soon as an iterate fails to decrease. The
    result is within one unit in the last place of the true root. Cost:
    one division per pass, at most 6 passes for binary64.
    """
    if math.isnan(a) or a < 0:  # @line L1
        return SqrtResult(math.nan, "invalid", 0, 0)
    if a == 0 or math.isinf(a):
        return SqrtResult(a, "exact input", 0, 0)
    f, big_e = math.frexp(a)  # @line L2
    if big_e % 2 == 0:
        m, e = f, big_e // 2
    else:
        m, e = 2 * f, (big_e - 1) // 2
    x = (1 + m) / 2  # @line L3
    for k in range(1, max_iter + 1):  # @line L4
        y = (x + m / x) / 2  # @line L5
        if y >= x:  # @line L6
            return SqrtResult(math.ldexp(x, e), "converged", k, k)
        x = y  # @line L7
    return SqrtResult(math.ldexp(x, e), "kmax reached", max_iter, max_iter)  # @line L8


def heron_iterates(a: Any, x0: Any, n: int) -> List[Any]:
    """The first n Newton iterates x <- (x + a/x)/2 from x0 > 0, in any field type.

    Works with Fraction (exact) and Decimal (current context). Cost: n divisions.
    """
    xs = [x0]
    x = x0
    for _ in range(n):
        x = (x + a / x) / 2
        xs.append(x)
    return xs
