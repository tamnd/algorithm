# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hermite-reduction/. The authors are listed in prov/4X5MRR.jsonl.

"""Hermite reduction of a rational function over Q (Mack's linear version).

Polynomials are lists of Fractions, lowest degree first, with no trailing
zero; [] is the zero polynomial. A rational function is a pair (num, den).

hermite_reduce(A, D) returns (g, h) with A/D = g' + h, where g is a rational
function and h = a/d has a squarefree denominator d and deg a < deg d.

Cost model: operations in Q. With n = deg D, the method makes O(n) gcd and
extended gcd computations on polynomials of degree at most n, so it uses
O(n^2) field operations per level and O(n^3) in total with the classical
quadratic gcd here; with fast gcd it is O(M(n) log n) per level.
"""

from fractions import Fraction
from typing import List, Tuple

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
    return norm([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])  # type: ignore[misc]


def neg(a: Poly) -> Poly:
    return [-x for x in a]


def sub(a: Poly, b: Poly) -> Poly:
    return add(a, neg(b))


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
    """Quotient and remainder; b must be nonzero."""
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
    """Monic gcd by the Euclidean algorithm; gcd(0, 0) = 0."""
    while b:
        a, b = b, divmod_poly(a, b)[1]
    return monic(a)


def deriv(a: Poly) -> Poly:
    return norm([i * a[i] for i in range(1, len(a))])


def integrate_poly(a: Poly) -> Poly:
    return norm([Fraction(0)] + [a[i] / (i + 1) for i in range(len(a))])


def solve_diophantine(f: Poly, g: Poly, a: Poly) -> Tuple[Poly, Poly]:
    """(b, c) with b f + c g = a and deg b < deg g. Precondition: gcd(f, g) = 1."""
    r0, r1, s0, s1 = f, g, [Fraction(1)], []
    while r1:
        q, r = divmod_poly(r0, r1)
        r0, r1, s0, s1 = r1, r, s1, sub(s0, mul(q, s1))
    if deg(r0) != 0:
        raise ValueError("f and g are not coprime")
    s = [x / r0[0] for x in s0]  # s f = 1 (mod g)
    b = divmod_poly(mul(s, a), g)[1]
    c = exquo(sub(a, mul(b, f)), g)
    return b, c


def rat_add(x: RatFun, y: RatFun) -> RatFun:
    """Sum of two fractions, reduced, with a monic denominator."""
    n = add(mul(x[0], y[1]), mul(y[0], x[1]))
    d = mul(x[1], y[1])
    if not n:
        return [], [Fraction(1)]
    h = gcd(n, d)
    n, d = exquo(n, h), exquo(d, h)
    c = d[-1]
    return [v / c for v in n], [v / c for v in d]


def hermite_reduce(A: Poly, D: Poly) -> Tuple[RatFun, RatFun]:
    """Return (g, h) with A/D = g' + h, the denominator of h squarefree and h proper.

    Precondition: D is nonzero. Cost: O(deg D) gcds of degree at most deg D.
    """
    if not D:
        raise ZeroDivisionError("zero denominator")
    Pq, A = divmod_poly(A, D)  # @line L1
    g: RatFun = (integrate_poly(Pq), [Fraction(1)])
    Dm = gcd(D, deriv(D))  # @line L2
    Ds = exquo(D, Dm)
    while deg(Dm) > 0:  # @line L3
        Dm2 = gcd(Dm, deriv(Dm))  # @line L4
        Dms = exquo(Dm, Dm2)
        F = neg(exquo(mul(Ds, deriv(Dm)), Dm))
        B, C = solve_diophantine(F, Dms, A)  # @line L5
        A = sub(C, exquo(mul(deriv(B), Ds), Dms))  # @line L6
        g = rat_add(g, (B, Dm))  # @line L7
        Dm = Dm2  # @line L8
    return g, (A, Ds)  # @line L9
