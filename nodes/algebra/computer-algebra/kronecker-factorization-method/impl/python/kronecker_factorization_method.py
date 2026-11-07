# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kronecker-factorization-method/. The authors are listed in prov/9JH5VC.jsonl.

"""Kronecker's method: factor a primitive polynomial in Z[x] into irreducibles.

A polynomial is a list of integers [a_0, ..., a_d], lowest degree first, with a
nonzero last entry. The method is exponential in the degree and is meant for
small inputs and for teaching.
"""

from fractions import Fraction
from itertools import product
from math import gcd
from typing import List, Optional

Poly = List[int]


def evaluate(f: Poly, a: int) -> int:
    v = 0
    for c in reversed(f):
        v = v * a + c
    return v


def divisors(n: int) -> List[int]:
    """The positive divisors of n != 0, by trial division."""
    n = abs(n)
    small, large = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i * i != n:
                large.append(n // i)
        i += 1
    return small + large[::-1]


def exact_quotient(f: Poly, g: Poly) -> Optional[Poly]:
    """f / g if g divides f in Z[x], else None."""
    r = list(f)
    q = [0] * (len(f) - len(g) + 1)
    for s in range(len(f) - len(g), -1, -1):
        c, m = divmod(r[s + len(g) - 1], g[-1])
        if m:
            return None
        q[s] = c
        for i, b in enumerate(g):
            r[s + i] -= c * b
    return q if not any(r) else None


def interpolate(points: List[int], values: List[int]) -> Optional[Poly]:
    """The polynomial of degree < len(points) through the points, if it is in Z[x]."""
    n = len(points)
    coeffs = [Fraction(0)] * n
    for i in range(n):
        basis = [Fraction(1)]  # prod_{j != i} (x - a_j) / (a_i - a_j)
        for j in range(n):
            if j != i:
                den = points[i] - points[j]
                nxt = [Fraction(0)] * (len(basis) + 1)
                for k, c in enumerate(basis):
                    nxt[k] -= c * points[j] / den
                    nxt[k + 1] += c / den
                basis = nxt
        for k in range(n):
            coeffs[k] += values[i] * basis[k]
    if any(c.denominator != 1 for c in coeffs):
        return None
    g = [int(c) for c in coeffs]
    while g and g[-1] == 0:
        g.pop()
    return g


def choose_points(f: Poly, count: int) -> List[int]:
    """count integers with f(a) != 0, preferring values with few divisors."""
    cands = []
    a = 0
    while len(cands) < 2 * len(f) + count:
        for b in ((a,) if a == 0 else (a, -a)):
            if evaluate(f, b) != 0:
                cands.append(b)
        a += 1
    cands.sort(key=lambda b: (len(divisors(evaluate(f, b))), abs(b)))
    return cands[:count]


def find_factor(f: Poly, e: int) -> Optional[Poly]:
    """A factor of f of degree exactly e, or None if there is none."""
    pts = choose_points(f, e + 1)  # @line L3
    divs = [divisors(evaluate(f, a)) for a in pts]  # @line L4
    choices = [divs[0]] + [d + [-x for x in d] for d in divs[1:]]  # g(a_0) > 0
    for vals in product(*choices):  # @line L5
        g = interpolate(pts, list(vals))  # @line L6
        if g is not None and len(g) == e + 1:  # @line L7
            q = exact_quotient(f, g)
            if q is not None:
                return [-c for c in g] if g[-1] < 0 else g
    return None


def kronecker_factor(f: Poly) -> List[Poly]:
    """The irreducible factors of a primitive f with positive leading coefficient.

    The product of the returned factors is f. Each factor has a positive
    leading coefficient. Constants give the empty list.
    """
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    if not f:
        raise ValueError("f must be nonzero")
    c = 0
    for a in f:
        c = gcd(c, a)
    if c != 1 or f[-1] < 0:
        raise ValueError("f must be primitive with a positive leading coefficient")
    factors: List[Poly] = []
    e = 1  # @line L1
    while 2 * e <= len(f) - 1:  # @line L2
        g = find_factor(f, e)
        if g is None:
            e += 1  # @line L9
        else:
            factors.append(g)  # @line L8
            f = exact_quotient(f, g)
    if len(f) > 1:
        factors.append(f)  # @line L10
    return factors  # @line L11
