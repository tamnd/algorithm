# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bibo-stability/. The authors are listed in prov/WPRRG6.jsonl.

"""BIBO stability of a causal filter with a rational transfer function.

The filter is H(z) = B(z) / A(z) with B(z) = sum b_k z^(-k) and
A(z) = sum a_k z^(-k), a0 != 0, causal (the region of convergence is
outside the largest pole). Coefficients are int or Fraction, so every
step is exact.

is_stable first cancels the common factors of B and A (a polynomial gcd
over the rationals), then runs the Schur-Cohn step-down test on what is
left of A. The test answers "all poles strictly inside the unit circle"
without finding the poles.
"""

from fractions import Fraction
from typing import Sequence


def _trim(p: list) -> list:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def poly_divmod(n: Sequence, d: Sequence) -> tuple[list, list]:
    """Division of polynomials in w = z^(-1); index k holds the coefficient of w^k."""
    n = _trim([Fraction(v) for v in n])
    d = _trim([Fraction(v) for v in d])
    if d == [0]:
        raise ZeroDivisionError("division by the zero polynomial")
    q = [Fraction(0)] * max(1, len(n) - len(d) + 1)
    r = n[:]
    while len(r) >= len(d) and r != [0]:
        shift = len(r) - len(d)
        c = r[-1] / d[-1]
        q[shift] = c
        for i, v in enumerate(d):
            r[i + shift] -= c * v
        r.pop()
        r = _trim(r) if r else [Fraction(0)]
    return _trim(q), r


def poly_gcd(p: Sequence, q: Sequence) -> list:
    """Monic gcd by Euclid's algorithm over the rationals."""
    a = _trim([Fraction(v) for v in p])
    b = _trim([Fraction(v) for v in q])
    while b != [0]:
        a, b = b, poly_divmod(a, b)[1]
    lead = a[-1]
    return [v / lead for v in a]


def cancel(b: Sequence, a: Sequence) -> tuple[list, list]:
    """Remove the common factors of B and A. The result has a0 = 1."""
    g = poly_gcd(b, a)
    b2 = poly_divmod(b, g)[0]
    a2 = poly_divmod(a, g)[0]
    a0 = a2[0]
    return [v / a0 for v in b2], [v / a0 for v in a2]


def reflection_coefficients(a: Sequence) -> list:
    """Schur-Cohn step-down. Returns k_p, k_(p-1), ... until a step meets |k| >= 1.

    With a normalised to a0 = 1, k_p = a_p and the next polynomial is
    a'_m = (a_m - k_p a_(p-m)) / (1 - k_p^2) for m = 0..p-1.
    The poles z with z^p A(z) = 0 are all inside the unit circle if and
    only if every |k_m| < 1.
    """
    a = _trim([Fraction(v) for v in a])
    a = [v / a[0] for v in a]
    ks = []
    while len(a) > 1:
        p = len(a) - 1
        k = a[p]
        ks.append(k)
        if abs(k) >= 1:
            break
        a = [(a[m] - k * a[p - m]) / (1 - k * k) for m in range(p)]
    return ks


def is_stable(b: Sequence, a: Sequence) -> bool:
    """True if and only if the causal filter B/A is BIBO stable."""
    _, a2 = cancel(b, a)
    return all(abs(k) < 1 for k in reflection_coefficients(a2))


def lfilter(b: Sequence, a: Sequence, x: Sequence) -> list:
    """The difference equation with initial rest, exact on Fractions."""
    y: list = []
    for n in range(len(x)):
        acc = sum(b[k] * x[n - k] for k in range(len(b)) if n - k >= 0)
        acc -= sum(a[k] * y[n - k] for k in range(1, len(a)) if n - k >= 0)
        y.append(Fraction(acc) / a[0])
    return y


def impulse_response(b: Sequence, a: Sequence, count: int) -> list:
    return lfilter(b, a, [1] + [0] * (count - 1))
