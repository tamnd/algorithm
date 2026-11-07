# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polynomial-extended-euclidean-algorithm/. The authors are listed in prov/HMRZF4.jsonl.

"""The extended Euclidean algorithm for polynomials over a field.

A polynomial is a list of coefficients, lowest degree first: [a0, a1, ..., an].
The zero polynomial is []. The coefficients must be elements of a field, for
example Fraction or an element of Z/pZ, with +, -, *, == 0 and 1 / a.
"""

from typing import Any, Sequence

Poly = list[Any]


def _strip(a: Sequence[Any]) -> Poly:
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


def _divmod(f: Poly, g: Poly) -> tuple[Poly, Poly]:
    """Long division of f by the nonzero, stripped g."""
    m, n = len(f) - 1, len(g) - 1
    if m < n:
        return [], f
    u = _inverse(g[n])
    r = list(f)
    q: Poly = [None] * (m - n + 1)
    for k in range(m - n, -1, -1):
        c = r[n + k] * u
        q[k] = c
        for j in range(n):
            r[j + k] = r[j + k] - c * g[j]
        r[n + k] = c - c
    return _strip(q), _strip(r[:n])


def _sub_mul(a: Poly, q: Poly, b: Poly) -> Poly:
    """Return a - q * b, by the schoolbook product."""
    c: Poly = [0] * max(len(a), len(q) + len(b) - 1)
    for i, x in enumerate(a):
        c[i] = x
    for i, x in enumerate(q):
        for j, y in enumerate(b):
            c[i + j] = c[i + j] - x * y
    return _strip(c)


def polynomial_xgcd(f: Sequence[Any], g: Sequence[Any]) -> tuple[Poly, Poly, Poly]:
    """Return (h, s, t) with s*f + t*g = h, where h is the monic gcd of f and g.

    For f = g = 0 it returns ([], [1], []). If f and g are nonzero and h is
    neither the monic f nor the monic g, then deg s < deg g - deg h and
    deg t < deg f - deg h.
    Precondition: the coefficients lie in a field.
    Cost: O(deg f * deg g + deg f + deg g) field operations, and at most
    deg g + 2 inversions when deg f >= deg g.
    """
    r0, s0, t0 = _strip(f), [1], []  # @line L1
    r1, s1, t1 = _strip(g), [], [1]
    while r1:  # @line L2
        q, r = _divmod(r0, r1)  # @line L3
        r0, s0, t0, r1, s1, t1 = r1, s1, t1, r, _sub_mul(s0, q, s1), _sub_mul(t0, q, t1)  # @line L4
    if not r0:  # @line L5
        return [], s0, t0
    u = _inverse(r0[-1])  # @line L6
    return [c * u for c in r0], [c * u for c in s0], [c * u for c in t0]  # @line L7
