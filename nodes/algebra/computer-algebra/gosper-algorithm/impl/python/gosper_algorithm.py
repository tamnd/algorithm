# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gosper-algorithm/. The authors are listed in prov/CAVQHD.jsonl.

"""Gosper's algorithm for indefinite hypergeometric summation over Q.

A hypergeometric term t(n) is given by its ratio r(n) = t(n+1)/t(n) as a pair
(num, den) of polynomials. Polynomials are lists of Fractions, lowest degree
first, with no trailing zero; [] is the zero polynomial.

gosper(num, den) returns a rational function y = (p, q) such that
z(n) = y(n) t(n) satisfies z(n+1) - z(n) = t(n), or None if t has no
hypergeometric antidifference.

Cost model: operations in Q. With d the larger degree of num and den, H the
bound on integer root differences used for the Gosper form, and D the degree
bound for the polynomial x, the cost is O(H d^2) for the form (gcds of degree
at most d) plus O((d + D)^3) for the linear system. H and D are integers read
off the input, so the bound is pseudo-polynomial in the bit size.
"""

from fractions import Fraction
from typing import List, Optional, Tuple

Poly = List[Fraction]
RatFun = Tuple[Poly, Poly]


def norm(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def P(*cs: object) -> Poly:
    """Polynomial from coefficients, lowest degree first."""
    return norm([Fraction(c) for c in cs])  # type: ignore[arg-type]


def deg(a: Poly) -> int:
    return len(a) - 1


def add(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return norm([(a[i] if i < len(a) else Fraction(0)) + (b[i] if i < len(b) else Fraction(0)) for i in range(n)])


def scale(a: Poly, c: Fraction) -> Poly:
    return norm([c * x for x in a])


def sub(a: Poly, b: Poly) -> Poly:
    return add(a, scale(b, Fraction(-1)))


def mul(a: Poly, b: Poly) -> Poly:
    if not a or not b:
        return []
    c = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return norm(c)


def divmod_poly(a: Poly, b: Poly) -> Tuple[Poly, Poly]:
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    r = list(a)
    q = [Fraction(0)] * max(len(a) - len(b) + 1, 0)
    inv = 1 / b[-1]
    for k in range(len(a) - len(b), -1, -1):
        t = r[k + len(b) - 1] * inv
        q[k] = t
        if t:
            for j, y in enumerate(b):
                r[k + j] -= t * y
    return norm(q), norm(r[: len(b) - 1])


def exquo(a: Poly, b: Poly) -> Poly:
    q, r = divmod_poly(a, b)
    if r:
        raise ArithmeticError("division is not exact")
    return q


def monic(a: Poly) -> Poly:
    return [x / a[-1] for x in a] if a else []


def gcd(a: Poly, b: Poly) -> Poly:
    while b:
        a, b = b, divmod_poly(a, b)[1]
    return monic(a)


def shift(a: Poly, s: int) -> Poly:
    """a(n + s), by Horner's rule with the linear polynomial n + s."""
    out: Poly = []
    lin = P(s, 1)
    for c in reversed(a):
        out = add(mul(out, lin), [c] if c else [])
    return out


def root_bound(a: Poly) -> int:
    """An integer bound on the absolute values of the complex roots of a (Fujiwara):
    |z| <= 2 max_i |a_(d-i) / a_d|^(1/i), with the term for i = d halved."""
    d = deg(a)
    best = 0
    for i in range(1, d + 1):
        c = abs(a[d - i] / a[d])
        if i == d:
            c = c / 2
        if c == 0:
            continue
        r = max(int(float(c) ** (1.0 / i)) - 1, 0)
        while Fraction(r) ** i < c:  # smallest integer r with r^i >= c
            r += 1
        best = max(best, r)
    return 2 * best


def solve_linear(cols: List[Poly], rhs: Poly) -> Optional[List[Fraction]]:
    """A solution v of sum_j v_j cols[j] = rhs, or None. Gaussian elimination over Q."""
    rows = max([len(c) for c in cols] + [len(rhs)])
    m = len(cols)
    A = [[(cols[j][i] if i < len(cols[j]) else Fraction(0)) for j in range(m)]
         + [rhs[i] if i < len(rhs) else Fraction(0)] for i in range(rows)]
    piv: List[int] = []
    r = 0
    for c in range(m):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [v * inv for v in A[r]]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [u - f * v for u, v in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    if any(A[i][m] != 0 for i in range(r, rows)):
        return None
    v = [Fraction(0)] * m
    for i, c in enumerate(piv):
        v[c] = A[i][m]
    return v


def degree_bound(a: Poly, B: Poly, c: Poly) -> int:
    """Largest possible degree of a polynomial x with a(n) x(n+1) - B(n) x(n) = c(n)."""
    d1, d2 = deg(a), deg(B)
    if d1 != d2:
        return deg(c) - max(d1, d2)
    if a[-1] != B[-1]:
        return deg(c) - d1
    e = deg(c) - d1 + 1
    al = a[-2] if d1 >= 1 else Fraction(0)
    be = B[-2] if d2 >= 1 else Fraction(0)
    d0 = (be - al) / a[-1]
    if d0.denominator == 1 and d0 >= 0:
        e = max(e, int(d0))
    return e


def gosper(num: Poly, den: Poly) -> Optional[RatFun]:
    """Antidifference of the term t with t(n+1)/t(n) = num/den, as y = z/t.

    Precondition: num and den nonzero polynomials over Q. Returns (p, q) with
    (p/q)(n+1) * num(n)/den(n) - (p/q)(n) = 1, or None if no rational y exists.
    Cost: O(H d^2 + (d + D)^3) operations in Q, see the module docstring.
    """
    if not num or not den:
        raise ValueError("the ratio must be a nonzero rational function")
    a = scale(monic(num), num[-1] / den[-1])  # @line L1
    b = monic(den)
    c = P(1)
    H = root_bound(num) + root_bound(den)  # every integer root difference is at most H
    for h in range(H + 1):  # @line L2
        while True:
            g = gcd(a, shift(b, h))  # @line L3
            if deg(g) <= 0:
                break
            a = exquo(a, g)  # @line L4
            b = exquo(b, shift(g, -h))
            for i in range(1, h + 1):
                c = mul(c, shift(g, -i))
    B = shift(b, -1)  # @line L5
    D = degree_bound(a, B, c)
    if D < 0:  # @line L6
        return None
    cols = []
    for j in range(D + 1):  # @line L7
        e = P(*([0] * j + [1]))
        cols.append(sub(mul(a, shift(e, 1)), mul(B, e)))
    v = solve_linear(cols, c)
    if v is None:  # @line L8
        return None
    x = P(*v)
    p, q = mul(B, x), c  # @line L9
    g = gcd(p, q)
    p, q = exquo(p, g), exquo(q, g)
    return scale(p, 1 / q[-1]), monic(q)
