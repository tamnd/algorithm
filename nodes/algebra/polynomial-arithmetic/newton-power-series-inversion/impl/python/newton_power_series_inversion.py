# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-power-series-inversion/. The authors are listed in prov/8P4715.jsonl.

"""Inversion of a power series by Newton iteration.

A power series f = f_0 + f_1 x + ... is given by a list [f_0, f_1, ...] of its
first coefficients, lowest degree first; missing coefficients are zero. The
coefficients may be int, Fraction, or any ring element type with + - * and
`/` for the inverse of the constant term (for example a Z/pZ class). The
result of inverse(f, n) is the list [g_0, ..., g_{n-1}] with f g = 1 mod x^n.

Costs are counted in ring operations. The multiplication is a parameter;
the default is Karatsuba multiplication, which works over every commutative
ring and has recursion depth O(log n).
"""

from __future__ import annotations

from typing import Any, Callable, List, Sequence

Poly = List[Any]
MulFn = Callable[[Sequence[Any], Sequence[Any]], Poly]

KARATSUBA_CUTOFF = 32


def schoolbook_mul(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """Return the full product of two coefficient lists, len(a) + len(b) - 1 entries."""
    if not a or not b:
        return []
    c: Poly = [a[0] - a[0]] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = c[i + j] + x * y
    return c


def _add(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """Return the coefficientwise sum of two lists of possibly different lengths."""
    if len(a) < len(b):
        a, b = b, a
    return [x + y for x, y in zip(a, b)] + list(a[len(b):])


def karatsuba_mul(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """Return the full product of two coefficient lists by Karatsuba's method.

    Works over every commutative ring. The recursion splits the longer operand
    in halves, so its depth is O(log(len(a) + len(b))).
    """
    if not a or not b:
        return []
    if len(a) < len(b):
        a, b = b, a
    if len(b) <= KARATSUBA_CUTOFF:
        return schoolbook_mul(a, b)
    zero = a[0] - a[0]
    h = len(a) // 2
    a0, a1 = list(a[:h]), list(a[h:])
    if len(b) <= h:
        # Unbalanced: b fits in the low half; multiply each half of a by b.
        lo = karatsuba_mul(a0, b)
        hi = karatsuba_mul(a1, b)
        c = [zero] * (len(a) + len(b) - 1)
        for i, v in enumerate(lo):
            c[i] = c[i] + v
        for i, v in enumerate(hi):
            c[i + h] = c[i + h] + v
        return c
    b0, b1 = list(b[:h]), list(b[h:])
    z0 = karatsuba_mul(a0, b0)
    z2 = karatsuba_mul(a1, b1)
    sa = _add(a0, a1)
    sb = _add(b0, b1)
    z1 = karatsuba_mul(sa, sb)
    for i, v in enumerate(z0):
        z1[i] = z1[i] - v
    for i, v in enumerate(z2):
        z1[i] = z1[i] - v
    c = [zero] * (len(a) + len(b) - 1)
    for i, v in enumerate(z0):
        c[i] = c[i] + v
    for i, v in enumerate(z1):
        if i + h < len(c):
            c[i + h] = c[i + h] + v
    for i, v in enumerate(z2):
        c[i + 2 * h] = c[i + 2 * h] + v
    return c


def _unit_inverse(c: Any) -> Any:
    """Return c^(-1), or raise ValueError if c is not a unit."""
    if isinstance(c, bool):
        raise TypeError("bool is not a ring element here")
    if isinstance(c, int):
        if c in (1, -1):
            return c
        raise ValueError("constant term is not a unit of Z")
    if c == 0:
        raise ValueError("constant term is zero")
    one = c - c + 1
    try:
        return one / c
    except ZeroDivisionError as exc:
        raise ValueError("constant term is not a unit") from exc


def precisions(n: int) -> List[int]:
    """Return the precisions 1 = k_s < ... < k_0 = n with k_(i+1) = ceil(k_i / 2)."""
    ks = [n]
    while ks[-1] > 1:
        ks.append((ks[-1] + 1) // 2)
    ks.reverse()
    return ks


def inverse(f: Sequence[Any], n: int, mul: MulFn = karatsuba_mul) -> Poly:
    """Return [g_0, ..., g_(n-1)] with f g = 1 mod x^n.

    Precondition: n >= 0, and f_0 is a unit of the coefficient ring.
    Cost: at most 3 M(n) + lower order terms ring operations, where M(n) is the
    cost of `mul` on inputs of length n.
    """
    if n <= 0:
        return []
    if not f:
        raise ValueError("the zero series has no inverse")
    g: Poly = [_unit_inverse(f[0])]  # @line L1
    m = 1  # @line L2
    for m2 in precisions(n)[1:]:  # @line L3
        d = mul(list(f[:m2]), g)[:m2]  # @line L4
        while len(d) < m2:
            d.append(f[0] - f[0])
        t = [-c for c in d[m:m2]]  # @line L5
        c = mul(g, t)[: m2 - m]  # @line L6
        while len(c) < m2 - m:
            c.append(f[0] - f[0])
        g = g + c  # @line L7
        m = m2
    return g  # @line L8


def divide_series(a: Sequence[Any], f: Sequence[Any], n: int, mul: MulFn = karatsuba_mul) -> Poly:
    """Return the first n coefficients of a / f, for f_0 a unit."""
    if n <= 0:
        return []
    g = inverse(f, n, mul)
    if not a:
        return [g[0] - g[0]] * n
    q = mul(list(a[:n]), g)[:n]
    while len(q) < n:
        q.append(g[0] - g[0])
    return q


def inverse_naive(f: Sequence[Any], n: int) -> Poly:
    """Return the inverse modulo x^n by the O(n^2) recurrence g_k = -f_0^(-1) sum f_j g_(k-j)."""
    if n <= 0:
        return []
    if not f:
        raise ValueError("the zero series has no inverse")
    u = _unit_inverse(f[0])
    g: Poly = [u]
    for k in range(1, n):
        s = f[0] - f[0]
        for j in range(1, min(k, len(f) - 1) + 1):
            s = s + f[j] * g[k - j]
        g.append(-(u * s))
    return g


if __name__ == "__main__":
    print(inverse([1, -1, -1], 8))
