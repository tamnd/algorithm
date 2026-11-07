# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-polynomial-division/. The authors are listed in prov/X5VM5A.jsonl.

"""Fast division with remainder of polynomials, by Newton inversion of the reversed divisor.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first; the zero polynomial is []. Inputs may have zero entries at the
top; they are removed first. The coefficients may be int, Fraction, or any
ring element type with + - * and `/` for the inverse of a unit (for example a
Z/pZ class). The divisor's leading coefficient must be a unit; over Z this
means +1 or -1, so a monic divisor always works.

Costs are counted in ring operations. The multiplication is a parameter; the
default is Karatsuba multiplication, which works over every commutative ring
and has recursion depth O(log n).
"""

from __future__ import annotations

from typing import Any, Callable, List, Sequence, Tuple

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
    g: Poly = [_unit_inverse(f[0])]
    m = 1
    for m2 in precisions(n)[1:]:
        d = mul(list(f[:m2]), g)[:m2]
        while len(d) < m2:
            d.append(f[0] - f[0])
        t = [-c for c in d[m:m2]]
        c = mul(g, t)[: m2 - m]
        while len(c) < m2 - m:
            c.append(f[0] - f[0])
        g = g + c
        m = m2
    return g




def normalize(a: Sequence[Any]) -> Poly:
    """Return a copy of a without zero entries at the top."""
    out = list(a)
    while out and out[-1] == 0:
        out.pop()
    return out


def _pad(a: Poly, k: int, zero: Any) -> Poly:
    while len(a) < k:
        a.append(zero)
    return a


def reversed_inverse(b: Sequence[Any], k: int, mul: MulFn = karatsuba_mul) -> Poly:
    """Return the inverse of rev(b) modulo x^k, for reuse with many dividends."""
    b = normalize(b)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    return inverse(b[::-1], k, mul)


def divmod_fast(
    a: Sequence[Any],
    b: Sequence[Any],
    mul: MulFn = karatsuba_mul,
    rinv: Sequence[Any] = None,
) -> Tuple[Poly, Poly]:
    """Return (q, r) with a = q b + r and deg r < deg b, both normalized.

    Precondition: b is nonzero and lc(b) is a unit. If rinv is given, it must
    be the inverse of rev(b) modulo x^k for some k >= deg a - deg b + 1.
    Cost: at most 4 M(k) + M(m) + o(M(k)) + O(n) ring operations, with
    n = deg a, m = deg b and k = n - m + 1; M(k) + M(m) + O(n) with rinv.
    """
    a = normalize(a)  # @line L1
    b = normalize(b)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    n, m = len(a) - 1, len(b) - 1
    if n < m:  # @line L2
        return [], a
    zero = b[0] - b[0]
    k = n - m + 1  # @line L3
    if rinv is None:
        rinv = inverse(b[::-1], k, mul)  # @line L4
    elif len(rinv) < k:
        raise ValueError("the precomputed inverse is too short")
    ra = a[::-1][:k]  # @line L5
    rq = _pad(mul(ra, list(rinv[:k]))[:k], k, zero)  # @line L6
    q = rq[::-1]  # @line L7
    if m == 0:
        return normalize(q), []
    qb = _pad(mul(q[:m], b[:m])[:m], m, zero)  # @line L8
    r = [a[i] - qb[i] for i in range(m)]  # @line L9
    return normalize(q), normalize(r)  # @line L10


def divmod_schoolbook(a: Sequence[Any], b: Sequence[Any]) -> Tuple[Poly, Poly]:
    """Long division, the reference: Theta((n - m + 1) m) ring operations."""
    a = normalize(a)
    b = normalize(b)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    n, m = len(a) - 1, len(b) - 1
    if n < m:
        return [], a
    u = _unit_inverse(b[-1])
    r = list(a)
    q: Poly = [b[0] - b[0]] * (n - m + 1)
    for i in range(n - m, -1, -1):
        c = r[i + m] * u
        q[i] = c
        for j in range(m + 1):
            r[i + j] = r[i + j] - c * b[j]
    return normalize(q), normalize(r[:m])


if __name__ == "__main__":
    print(divmod_fast([6, 5, 4, 3, 2, 1], [1, 1, 1]))
