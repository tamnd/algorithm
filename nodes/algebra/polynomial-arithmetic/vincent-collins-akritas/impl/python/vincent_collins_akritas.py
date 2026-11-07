# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vincent-collins-akritas/. The authors are listed in prov/S6W6AA.jsonl.
"""The Vincent-Collins-Akritas (Descartes) method for real root isolation.

Polynomials are lists of coefficients, lowest degree first; the zero
polynomial is []. The method works with ints only: Taylor shifts by 1,
multiplications by powers of two, and sign tests.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Sequence

Interval = tuple[Fraction, Fraction]


def _strip(a: list) -> list:
    while a and a[-1] == 0:
        a.pop()
    return a


def _taylor_shift(a: list[int], c: int) -> list[int]:
    """Return the coefficients of a(x + c), by the classical O(n^2) scheme."""
    a = list(a)
    n = len(a) - 1
    for i in range(n):
        for j in range(n - 1, i - 1, -1):
            a[j] += c * a[j + 1]
    return a


def _variations(a: Sequence[int]) -> int:
    """Number of sign changes in a, zeros ignored."""
    v, last = 0, 0
    for x in a:
        if x:
            if last and (x > 0) != (last > 0):
                v += 1
            last = x
    return v


def _descartes_test(a: list[int]) -> int:
    """Var of (x + 1)^n a(1 / (x + 1)): bounds the roots of a in (0, 1)."""
    return _variations(_taylor_shift(a[::-1], 1))


def _poly_rem(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    a = list(a)
    while len(a) >= len(b):
        q = a[-1] / b[-1]
        s = len(a) - len(b)
        for i, y in enumerate(b):
            a[s + i] -= q * y
        _strip(a)
    return a


def _poly_gcd(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    while b:
        a, b = b, _poly_rem(a, b)
    return a


def _poly_divexact(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    a = list(a)
    q = [Fraction(0)] * (len(a) - len(b) + 1)
    while len(a) >= len(b):
        t = a[-1] / b[-1]
        s = len(a) - len(b)
        q[s] = t
        for i, y in enumerate(b):
            a[s + i] -= t * y
        _strip(a)
    return q


def _to_primitive_int(a: Sequence[Fraction]) -> list[int]:
    den = 1
    for x in a:
        den = den * x.denominator // gcd(den, x.denominator)
    b = [int(x * den) for x in a]
    c = 0
    for x in b:
        c = gcd(c, x)
    if b[-1] < 0:
        c = -c
    return [x // c for x in b]


def _derivative(a: Sequence) -> list:
    return [i * a[i] for i in range(1, len(a))]


def square_free_part(f: Sequence[int | Fraction]) -> list[int]:
    """Primitive integer polynomial with the same distinct roots as f.

    Precondition: f is not the zero polynomial.
    Cost: O(n^2) operations on rationals, by Euclid's algorithm.
    """
    a = _strip([Fraction(x) for x in f])
    if not a:
        raise ValueError("the zero polynomial has no isolating intervals")
    if len(a) == 1:
        return [1]
    g = _poly_gcd(a, _strip(_derivative(a)))
    return _to_primitive_int(_poly_divexact(a, g))


def vca_isolate(f: Sequence[int]) -> list[Interval]:
    """Isolating intervals for the real roots of a square-free f in Z[x].

    Precondition: f has int coefficients, is not zero, and is square-free
    (no repeated complex root); leading zeros in the list are allowed.
    Returns a sorted list of pairs (lo, hi) of Fractions. A pair with
    lo < hi is an open interval holding exactly one root; a pair with
    lo == hi is an exact rational root. Distinct pairs are disjoint.
    Cost: O(n^3 (L + log n)) additions, shifts and sign tests, where L is
    the coefficient length, from the recursion tree bound of Eigenwillig,
    Sharma and Yap and O(n^2) work per node.
    """
    f = _strip([int(x) for x in f])
    if not f:
        raise ValueError("the zero polynomial has no isolating intervals")
    n = len(f) - 1
    if n == 0:
        return []
    if square_free_part(f) != _to_primitive_int([Fraction(x) for x in f]):
        raise ValueError("f must be square-free; use isolate_real_roots")
    bound = 1 + max(Fraction(abs(x), abs(f[n])) for x in f[:n])  # @line L1
    big = 1
    while big < bound:
        big *= 2
    scaled = [x * big**i for i, x in enumerate(f)]  # @line L2
    scaled = _taylor_shift(scaled, -1)
    a0 = [x << i for i, x in enumerate(scaled)]
    stack: list[tuple[list[int], int, int]] = [(a0, 0, 0)]  # @line L3
    out: list[Interval] = []
    width = 2 * big

    def ends(c: int, k: int) -> Interval:
        lo = Fraction(-big) + Fraction(c * width, 2**k)
        return lo, lo + Fraction(width, 2**k)

    while stack:  # @line L4
        a, c, k = stack.pop()  # @line L5
        v = _descartes_test(a)  # @line L6
        if v == 0:  # @line L7
            continue
        if v == 1:  # @line L8
            out.append(ends(c, k))
            continue
        left = [x << (n - i) for i, x in enumerate(a)]  # @line L9
        right = _taylor_shift(left, 1)
        if right[0] == 0:  # @line L10
            mid = ends(c, k)[0] + Fraction(width, 2 ** (k + 1))
            out.append((mid, mid))
        stack.append((right, 2 * c + 1, k + 1))  # @line L11
        stack.append((left, 2 * c, k + 1))
    out.sort()  # @line L12
    return out


def isolate_real_roots(f: Sequence[int | Fraction]) -> list[Interval]:
    """Isolating intervals for the distinct real roots of any nonzero f.

    Precondition: f is nonzero, with int or Fraction coefficients.
    Reduces f to its square-free part, then calls vca_isolate.
    Cost: O(n^2) rational operations for the reduction, plus vca_isolate.
    """
    return vca_isolate(square_free_part(f))
