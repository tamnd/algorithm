# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pseudo-division/. The authors are listed in prov/XBNRYF.jsonl.
"""Pseudo-division of polynomials over a commutative ring, without inversions.

Polynomials are coefficient lists, lowest degree first; the zero polynomial is
[]. Coefficients may be of any type with +, -, * and == 0 that models a
commutative ring, for example int, Fraction or a class for Z/pZ.
"""

from __future__ import annotations

from typing import Any, Sequence


def _strip(a: Sequence[Any]) -> list[Any]:
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def pseudo_divmod(f: Sequence[Any], g: Sequence[Any]) -> tuple[list[Any], list[Any]]:
    """Return (q, r) with lc(g)^(m - n + 1) f = q g + r and deg r < n.

    Precondition: g is not the zero polynomial; m = deg f and n = deg g. If
    m < n, the result is (0, f). No inversion is used. Cost, with d = m - n:
    at most (d + 1)(2n) + d(d + 1)/2 + 2d multiplications and (d + 1) n
    subtractions in the ring, which is O((d + 1) m).
    """
    f, g = _strip(f), _strip(g)
    if not g:  # @line L1
        raise ZeroDivisionError("pseudo-division by the zero polynomial")
    m, n = len(f) - 1, len(g) - 1
    if m < n:  # @line L2
        return [], f
    lead = g[n]  # @line L3
    r = list(f)
    d = m - n
    t = [lead * 0] * (d + 1)
    for k in range(d, -1, -1):  # @line L4
        t[k] = r[n + k]  # @line L5
        for j in range(n + k):  # @line L6
            r[j] = lead * r[j]
        for j in range(n):  # @line L7
            r[j + k] = r[j + k] - t[k] * g[j]
        r[n + k] = lead * 0  # @line L8
    q = [t[0]]  # @line L9
    power = None
    for k in range(1, d + 1):
        power = lead if power is None else power * lead
        q.append(t[k] * power)
    return _strip(q), _strip(r[:n])  # @line L10
