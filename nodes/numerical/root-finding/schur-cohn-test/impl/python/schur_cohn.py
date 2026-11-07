# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schur-cohn-test/. The authors are listed in prov/AXFQZ4.jsonl.

"""The Schur-Cohn test: count the zeros of a polynomial inside a disc, exactly.

Coefficients are given from the constant term up: coeffs[i] is the
coefficient of z**i. They may be int, Fraction, float or complex; floats
and complex floats are converted exactly to rationals, so the count is
exact for the polynomial whose coefficients are the given machine numbers.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd
from typing import Any, List, Optional, Sequence, Tuple

GQ = Tuple[Fraction, Fraction]  # a Gaussian rational (real part, imaginary part)
ZERO: GQ = (Fraction(0), Fraction(0))


@dataclass
class SchurCohnResult:
    """The number of zeros in the open disc, or None, and the work done."""

    count: Optional[int]
    reason: str  # "count" or "singular" (a zero on the circle, or a degenerate step)
    degree: int
    steps: int  # number of Schur transforms computed
    deltas: List[Fraction] = field(default_factory=list)  # delta_1, delta_2, ...

    @property
    def converged(self) -> bool:
        return self.reason == "count"


def to_gq(v: Any) -> GQ:
    """Convert int, Fraction, float, complex or a pair to an exact Gaussian rational."""
    if isinstance(v, tuple):
        return (Fraction(v[0]), Fraction(v[1]))
    if isinstance(v, complex):
        return (Fraction(v.real), Fraction(v.imag))
    return (Fraction(v), Fraction(0))


def _mul(a: GQ, b: GQ) -> GQ:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _sub(a: GQ, b: GQ) -> GQ:
    return (a[0] - b[0], a[1] - b[1])


def _add(a: GQ, b: GQ) -> GQ:
    return (a[0] + b[0], a[1] + b[1])


def _conj(a: GQ) -> GQ:
    return (a[0], -a[1])


def _trim(p: List[GQ]) -> List[GQ]:
    while p and p[-1] == ZERO:
        p.pop()
    return p


def _primitive(p: List[GQ]) -> List[GQ]:
    """Divide by a positive rational so that the parts are coprime integers."""
    den = 1
    for c in p:
        for x in c:
            den = den * x.denominator // gcd(den, x.denominator)
    g = 0
    for c in p:
        for x in c:
            g = gcd(g, int(x * den))
    s = Fraction(den, g)
    return [(c[0] * s, c[1] * s) for c in p]


def taylor_shift_scale(coeffs: Sequence[Any], center: Any = 0, radius: Any = 1) -> List[GQ]:
    """Coefficients of q(w) = p(center + radius * w), exactly."""
    p = [to_gq(c) for c in coeffs]
    c = to_gq(center)
    r = Fraction(radius)
    n = len(p) - 1
    # Horner-style Taylor shift: after it, p holds the coefficients of p(c + w).
    for i in range(n):
        for k in range(n - 1, i - 1, -1):
            p[k] = _add(p[k], _mul(c, p[k + 1]))
    s = Fraction(1)
    for k in range(n + 1):
        p[k] = (p[k][0] * s, p[k][1] * s)
        s *= r
    return p


def schur_cohn(coeffs: Sequence[Any], center: Any = 0, radius: Any = 1) -> SchurCohnResult:
    """Count the zeros of p, with multiplicity, in the open disc |z - center| < radius."""
    if Fraction(radius) <= 0:
        raise ValueError("radius must be positive")
    p = _trim(taylor_shift_scale(coeffs, center, radius))
    if not p:  # @line L1
        raise ValueError("the zero polynomial has no finite zero count")
    n0 = len(p) - 1  # @line L2
    degrees: List[int] = []
    deltas: List[Fraction] = []
    while len(p) - 1 >= 1:  # @line L3
        n = len(p) - 1
        a0, an = p[0], p[n]
        pstar = [_conj(p[n - k]) for k in range(n + 1)]  # @line L4
        q = [_sub(_mul(_conj(a0), p[k]), _mul(an, pstar[k])) for k in range(n + 1)]  # @line L5
        delta = q[0][0]  # q(0) = |a0|^2 - |an|^2 is real
        deltas.append(delta)
        degrees.append(n)
        if delta == 0:  # @line L6
            return SchurCohnResult(None, "singular", n0, len(deltas), deltas)
        q = _trim(q)  # @line L7
        p = _primitive(q)  # the sign of q(0) and the zeros are unchanged
    k = 0  # @line L8
    for j in range(len(deltas) - 1, -1, -1):  # @line L9
        if deltas[j] < 0:
            k = degrees[j] - k
    return SchurCohnResult(k, "count", n0, len(deltas), deltas)  # @line L10


def is_schur_stable(coeffs: Sequence[Any]) -> bool:
    """True when every zero lies in the open unit disc (discrete-time stability)."""
    r = schur_cohn(coeffs)
    return r.converged and r.count == r.degree


def poly_from_roots(roots: Sequence[Any]) -> List[GQ]:
    """Exact coefficients, constant term first, of the monic polynomial with these roots."""
    p: List[GQ] = [(Fraction(1), Fraction(0))]
    for r in roots:
        z = to_gq(r)
        q = [ZERO] * (len(p) + 1)
        for i, c in enumerate(p):
            q[i + 1] = _add(q[i + 1], c)
            q[i] = _sub(q[i], _mul(z, c))
        p = q
    return p
