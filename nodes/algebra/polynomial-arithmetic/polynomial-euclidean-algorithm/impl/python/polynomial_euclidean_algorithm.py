# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polynomial-euclidean-algorithm/. The authors are listed in prov/EBMDJ7.jsonl.

"""Euclid's algorithm for the gcd of two polynomials over a field.

A polynomial is a list of coefficients, lowest degree first: [a0, a1, ..., an].
The zero polynomial is []. The coefficients must be elements of a field, for
example Fraction or an element of Z/pZ, with +, -, *, == 0 and 1 / a.
"""

from typing import Any, Sequence


def _strip(a: Sequence[Any]) -> list[Any]:
    """Return a copy of a without zero coefficients at the top."""
    b = list(a)
    while b and b[-1] == 0:
        b.pop()
    return b


def _inverse(a: Any) -> Any:
    """Return 1 / a for a nonzero field element a; 1 and -1 keep their type."""
    if a == 1 or a == -1:
        return a
    if isinstance(a, int):
        raise ValueError("int coefficients: use Fraction or a finite field type")
    return 1 / a


def _rem(f: list[Any], g: list[Any]) -> list[Any]:
    """Remainder of f by the nonzero, stripped g, by long division."""
    n = len(g) - 1
    if len(f) - 1 < n:
        return f
    u = _inverse(g[n])
    r = list(f)
    for k in range(len(f) - 1 - n, -1, -1):
        c = r[n + k] * u
        for j in range(n):
            r[j + k] = r[j + k] - c * g[j]
        r[n + k] = c - c
    return _strip(r[:n])


def polynomial_gcd(f: Sequence[Any], g: Sequence[Any]) -> list[Any]:
    """Return the monic gcd of f and g, or [] when f = g = 0.

    Precondition: the coefficients lie in a field.
    Cost: for deg f = m >= deg g = n, at most (2n + 1)(m + n + 1) + n + 1
    field operations and n + 2 inversions.
    """
    r0, r1 = _strip(f), _strip(g)  # @line L1
    while r1:  # @line L2
        r0, r1 = r1, _rem(r0, r1)  # @line L3
    if not r0:  # @line L4
        return []
    u = _inverse(r0[-1])  # @line L5
    return [c * u for c in r0]  # @line L6
