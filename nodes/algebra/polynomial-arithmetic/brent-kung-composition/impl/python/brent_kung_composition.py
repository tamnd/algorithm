# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-kung-composition/. The authors are listed in prov/48QJRY.jsonl.

"""Brent-Kung modular composition: f(g) mod h by baby steps and giant steps.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first; the zero polynomial is []. Coefficients may be int, Fraction, or
any ring element type with + - * (and `/` for the inverse of a unit). The
leading coefficient of h must be a unit, so over Z it must be 1 or -1.

With N = len(f) and k = ceil(sqrt(N)), the algorithm forms the baby steps
g^0, ..., g^k mod h, gets every block F_j(g) mod h from one matrix product
of an m x k matrix by a k x n matrix, and joins the blocks by Horner's rule
in g^k mod h. That is about 2 sqrt(N) products modulo h, plus the matrix
product, which this file does by the schoolbook method. Costs are counted in
ring operations. All loops are iterative.
"""

from __future__ import annotations

from math import isqrt
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


def block_size(N: int) -> int:
    """Return ceil(sqrt(N)) for N >= 1."""
    k = isqrt(N)
    return k if k * k == N else k + 1


class _Modulus:
    """Reduction modulo a fixed h, with the inverse of rev(h) computed once."""

    def __init__(self, h: Sequence[Any], mul: MulFn) -> None:
        self.h = normalize(h)
        if not self.h:
            raise ZeroDivisionError("modulus is the zero polynomial")
        self.n = len(self.h) - 1
        self.mul = mul
        self.rinv = reversed_inverse(self.h, max(self.n, 1), mul) if self.n >= 1 else None
        self.count = 0

    def reduce(self, a: Sequence[Any]) -> Poly:
        a = normalize(a)
        if len(a) <= self.n:
            return a
        if self.n == 0:
            return []
        k = len(a) - self.n
        rinv = self.rinv if k <= len(self.rinv) else None
        return divmod_fast(a, self.h, self.mul, rinv)[1]

    def mulmod(self, a: Sequence[Any], b: Sequence[Any]) -> Poly:
        self.count += 1
        return self.reduce(self.mul(list(a), list(b)))


def mat_mul(a: List[List[Any]], b: List[List[Any]], zero: Any) -> List[List[Any]]:
    """Schoolbook product of an r x s matrix by an s x t matrix."""
    t = len(b[0]) if b else 0
    out = []
    for row in a:
        acc = [zero] * t
        for i, c in enumerate(row):
            if c == 0:
                continue
            bi = b[i]
            for j in range(t):
                acc[j] = acc[j] + c * bi[j]
        out.append(acc)
    return out


def compose_mod(
    f: Sequence[Any],
    g: Sequence[Any],
    h: Sequence[Any],
    mul: MulFn = karatsuba_mul,
    stats: dict = None,
) -> Poly:
    """Return f(g) mod h, normalized.

    Precondition: h is nonzero with a unit leading coefficient.
    Cost: about 2 sqrt(N) products modulo h and an m x k by k x n matrix
    product, with N = len(f), k = ceil(sqrt(N)), m = ceil(N / k), n = deg h.
    """
    md = _Modulus(h, mul)
    n = md.n
    f = normalize(f)
    if n == 0 or not f:
        return []
    zero = md.h[0] - md.h[0]
    one = zero + 1
    g = md.reduce(g)
    N = len(f)
    k = block_size(N)  # @line L1
    m = -(-N // k)
    G: List[Poly] = [[one], g]  # @line L2
    for _ in range(2, min(k, N - 1) + 1):  # @line L3
        G.append(md.mulmod(G[-1], g))
    A = [[f[j * k + i] if j * k + i < N else zero for i in range(k)] for j in range(m)]  # @line L4
    B = [_pad(list(G[i]), n, zero) if i < len(G) else [zero] * n for i in range(k)]  # @line L5
    C = mat_mul(A, B, zero)  # @line L6
    s = C[m - 1]  # @line L7
    for j in range(m - 2, -1, -1):  # @line L8
        s = _add(md.mulmod(s, G[k]), C[j])  # @line L9
    if stats is not None:
        stats["mulmod"] = md.count
        stats["k"], stats["m"] = k, m
    return normalize(s)  # @line L10


def compose_mod_horner(f: Sequence[Any], g: Sequence[Any], h: Sequence[Any]) -> Poly:
    """Reference: Horner's rule modulo h with schoolbook arithmetic."""
    h = normalize(h)
    if not h:
        raise ZeroDivisionError("modulus is the zero polynomial")
    f = normalize(f)
    n = len(h) - 1
    if n == 0 or not f:
        return []
    inv = _unit_inverse(h[-1])

    def rem(a: Poly) -> Poly:
        a = list(a)
        for d in range(len(a) - 1, n - 1, -1):
            c = a[d] * inv
            if c != 0:
                for i in range(n + 1):
                    a[d - n + i] = a[d - n + i] - c * h[i]
        return normalize(a[:n])

    s: Poly = []
    for c in reversed(f):
        s = rem(_add(schoolbook_mul(s, g), [c]))
    return s


if __name__ == "__main__":
    st = {}
    f, g, h = [1, 2, 3, 4], [0, 1, 1], [-2, 0, 0, 0, 1]
    print(compose_mod(f, g, h, stats=st), st, compose_mod_horner(f, g, h))
