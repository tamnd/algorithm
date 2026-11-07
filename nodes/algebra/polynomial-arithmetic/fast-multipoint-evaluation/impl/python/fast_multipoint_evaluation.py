# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-multipoint-evaluation/. The authors are listed in prov/VW4WSE.jsonl.

"""Fast multipoint evaluation by remainders down the subproduct tree.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first; the zero polynomial is []. Coefficients and points may be int,
Fraction, or any ring element type with + - * (and `/` for the inverse of a
unit). Every divisor in the tree is monic, so no inverse is ever needed except
of 1, and the method works over every commutative ring, including Z.

Costs are counted in ring operations. The multiplication is a parameter; the
default is Karatsuba multiplication. The tree has ceil(log2 n) levels and all
loops are iterative, so there is no deep recursion.
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
    a = normalize(a)
    b = normalize(b)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    n, m = len(a) - 1, len(b) - 1
    if n < m:
        return [], a
    zero = b[0] - b[0]
    k = n - m + 1
    if rinv is None:
        rinv = inverse(b[::-1], k, mul)
    elif len(rinv) < k:
        raise ValueError("the precomputed inverse is too short")
    ra = a[::-1][:k]
    rq = _pad(mul(ra, list(rinv[:k]))[:k], k, zero)
    q = rq[::-1]
    if m == 0:
        return normalize(q), []
    qb = _pad(mul(q[:m], b[:m])[:m], m, zero)
    r = [a[i] - qb[i] for i in range(m)]
    return normalize(q), normalize(r)




def subproduct_tree(points: Sequence[Any], mul: MulFn = karatsuba_mul) -> List[List[Poly]]:
    """Return the levels of the subproduct tree, leaves first.

    Level 0 holds the monic polynomials x - u_i. Node k of level j + 1 is the
    product of nodes 2k and 2k + 1 of level j; a last node without a sibling
    is copied up unchanged. The last level has one node, prod (x - u_i).
    """
    one = None
    level: List[Poly] = []
    for u in points:
        one = u - u + 1
        level.append([-u, one])
    levels = [level]
    while len(level) > 1:
        nxt = []
        for k in range(0, len(level) - 1, 2):
            nxt.append(mul(level[k], level[k + 1]))
        if len(level) % 2 == 1:
            nxt.append(level[-1])
        levels.append(nxt)
        level = nxt
    return levels


def _rem(a: Poly, m: Poly, mul: MulFn) -> Poly:
    """Remainder of a modulo the monic m, by fast division."""
    if len(a) < len(m):
        return a
    return divmod_fast(a, m, mul)[1]


def evaluate(f: Sequence[Any], points: Sequence[Any], mul: MulFn = karatsuba_mul) -> List[Any]:
    """Return [f(u) for u in points], with O(M(n) log n) ring operations."""
    points = list(points)
    n = len(points)
    if n == 0:  # @line L1
        return []
    zero = points[0] - points[0]
    levels = subproduct_tree(points, mul)  # @line L2
    h = len(levels) - 1
    rems = [_rem(normalize(f), levels[h][0], mul)]  # @line L3
    for j in range(h - 1, -1, -1):  # @line L4
        nodes = levels[j]
        nxt = []  # @line L5
        for k, m in enumerate(nodes):  # @line L6
            nxt.append(_rem(rems[k // 2], m, mul))  # @line L7
        rems = nxt  # @line L8
    return [r[0] if r else zero for r in rems]  # @line L9


def evaluate_horner(f: Sequence[Any], points: Sequence[Any]) -> List[Any]:
    """Reference: Horner's rule at each point, n (deg f) multiplications each."""
    out = []
    for u in points:
        acc = u - u
        for c in reversed(list(f)):
            acc = acc * u + c
        out.append(acc)
    return out


if __name__ == "__main__":
    print(evaluate([1, -2, 0, 1], [0, 1, 2, 3]))
