# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polynomial-long-division/. The authors are listed in prov/0Q78BZ.jsonl.

"""Polynomial long division with remainder.

A polynomial is a list of coefficients, lowest degree first: [a0, a1, ..., an].
The zero polynomial is []. The coefficients can be int, Fraction, or any type
with +, -, *, == 0 and 1 / a for a unit a (for example an element of Z/pZ).
"""

from typing import Any, Sequence


def _strip(a: Sequence[Any]) -> list[Any]:
    """Return a copy of a without zero coefficients at the top."""
    b = list(a)
    while b and b[-1] == 0:
        b.pop()
    return b


def _unit_inverse(a: Any) -> Any:
    """Return the inverse of the unit a. For an int, only 1 and -1 are units."""
    if a == 1 or a == -1:
        return a  # a * a = 1, and a keeps its type
    if isinstance(a, int):
        raise ValueError("the leading coefficient of the divisor is not a unit")
    return 1 / a


def polynomial_long_division(f: Sequence[Any], g: Sequence[Any]) -> tuple[list[Any], list[Any]]:
    """Return (q, r) with f = q*g + r and deg r < deg g.

    Precondition: g is not zero and its leading coefficient is a unit of the
    coefficient ring (every nonzero element over a field; 1 or -1 over Z).
    Cost: at most (2n + 1)(m - n + 1) ring operations and one inversion, for
    m = deg f and n = deg g.
    """
    f = _strip(f)  # @line L1
    g = _strip(g)
    if not g:
        raise ZeroDivisionError("division by the zero polynomial")
    m, n = len(f) - 1, len(g) - 1
    if m < n:  # @line L2
        return [], f
    u = _unit_inverse(g[n])  # @line L3
    r = list(f)  # @line L4
    q: list[Any] = [None] * (m - n + 1)
    for k in range(m - n, -1, -1):  # @line L5
        c = r[n + k] * u  # @line L6
        q[k] = c  # @line L7
        for j in range(n):  # @line L8
            r[j + k] = r[j + k] - c * g[j]  # @line L9
        r[n + k] = c - c  # @line L10: the top term cancels, since c * g[n] = r[n + k]
    return _strip(q), _strip(r[:n])  # @line L11
