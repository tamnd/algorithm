# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subresultant-gcd/. The authors are listed in prov/DB9KV8.jsonl.
"""The subresultant gcd algorithm and the subresultant remainder sequence.

Polynomials are coefficient lists, lowest degree first; the zero polynomial is
[]. subresultant_gcd works over Z (int coefficients). subresultant_prs works
over any integral domain whose elements support +, -, *, == 0 and an exact
division: int (checked floor division), Fraction, or a field class with /.
"""

from __future__ import annotations

from math import gcd
from typing import Any, Sequence


def _strip(a: Sequence[Any]) -> list[Any]:
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _exact_div(a: Any, b: Any) -> Any:
    """a / b when b divides a exactly in the coefficient domain."""
    if isinstance(a, int) and isinstance(b, int):
        q, r = divmod(a, b)
        if r != 0:
            raise ArithmeticError("division is not exact")
        return q
    return a / b


def _prem(f: list[Any], g: list[Any]) -> list[Any]:
    """Pseudo-remainder: lc(g)^(deg f - deg g + 1) f mod g, deg f >= deg g >= 0."""
    m, n = len(f) - 1, len(g) - 1
    lead = g[n]
    r = list(f)
    for k in range(m - n, -1, -1):
        t = r[n + k]
        for j in range(n + k):
            r[j] = lead * r[j]
        for j in range(n):
            r[j + k] = r[j + k] - t * g[j]
        r[n + k] = lead * 0
    return _strip(r[:n])


def _content(a: Sequence[int]) -> int:
    c = 0
    for x in a:
        c = gcd(c, x)
        if c == 1:
            break
    return c


def _pp(a: Sequence[int]) -> list[int]:
    """The primitive part with a positive leading coefficient."""
    c = _content(a)
    if a[-1] < 0:
        c = -c
    return [x // c for x in a]


def subresultant_gcd(f: Sequence[int], g: Sequence[int]) -> list[int]:
    """The gcd of f and g in Z[x], with a positive leading coefficient.

    Precondition: integer coefficients. gcd(0, 0) = 0. Cost, for m = max
    degree: O(m^2) operations on integers. The members of the sequence are
    subresultants up to sign, so their coefficients obey the Hadamard bound
    and have O(m (L + log m)) digits for inputs with L-digit coefficients.
    """
    f, g = _strip(f), _strip(g)
    if len(f) < len(g):  # @line L1
        f, g = g, f
    if not g:  # @line L2
        return [-x for x in f] if f and f[-1] < 0 else f
    c = gcd(_content(f), _content(g))  # @line L3
    a, b = _pp(f), _pp(g)
    gam, h = 1, 1
    while True:  # @line L4
        delta = len(a) - len(b)  # @line L5
        r = _prem(a, b)  # @line L6
        if not r:  # @line L7
            return [c * x for x in _pp(b)]
        if len(r) == 1:  # @line L8
            return [c]
        a = b  # @line L9
        divisor = gam * h**delta
        b = [_exact_div(x, divisor) for x in r]
        gam = a[-1]  # @line L10
        if delta >= 1:
            h = _exact_div(gam**delta, h ** (delta - 1))


def subresultant_prs(f: Sequence[Any], g: Sequence[Any]) -> list[list[Any]]:
    """The subresultant remainder sequence [f, g, R_3, ..., R_k] of f and g.

    Precondition: deg f >= deg g >= 0, coefficients in an integral domain with
    exact division. Each R_i is the pseudo-remainder of the two members before
    it, divided exactly by gamma * h^delta; up to sign R_i is the subresultant
    of index deg R_(i-1) - 1. The last member is a gcd up to a constant.
    Cost: O(m^2) ring operations and exact divisions for m = deg f.
    """
    a, b = _strip(f), _strip(g)
    if not b or len(a) < len(b):
        raise ValueError("need deg f >= deg g >= 0")
    seq = [a, b]
    gam, h = a[-1] * 0 + 1, a[-1] * 0 + 1
    while True:
        delta = len(a) - len(b)
        r = _prem(a, b)
        if not r:
            return seq
        divisor = gam * _power(h, delta)
        a, b = b, [_exact_div(x, divisor) for x in r]
        seq.append(b)
        if len(b) == 1:
            return seq
        gam = a[-1]
        if delta >= 1:
            h = _exact_div(_power(gam, delta), _power(h, delta - 1))


def _power(x: Any, e: int) -> Any:
    """x^e for e >= 0 by repeated multiplication."""
    out = x * 0 + 1
    for _ in range(e):
        out = out * x
    return out
