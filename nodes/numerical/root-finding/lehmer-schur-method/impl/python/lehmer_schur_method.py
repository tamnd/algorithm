# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lehmer-schur-method/. The authors are listed in prov/GXZ3FQ.jsonl.

"""The Lehmer-Schur method: locate a zero of a complex polynomial by
shrinking discs, deciding with the exact Schur-Cohn test whether each disc
contains a zero.

Coefficients are given from the constant term up. They may be int,
Fraction, float or complex, and are converted exactly to rationals. All
centres and radii are dyadic rationals, so every inclusion test is exact.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd
from typing import Any, List, Optional, Sequence, Tuple

GQ = Tuple[Fraction, Fraction]
ZERO: GQ = (Fraction(0), Fraction(0))

RHO = Fraction(13, 16)  # distance of the covering centres, in units of r
BETA = Fraction(7, 16)  # radius of the covering discs, in units of r
S = Fraction(181, 256)  # a dyadic value just below 1/sqrt(2)
DIRECTIONS: List[GQ] = [
    (Fraction(1), Fraction(0)), (S, S), (Fraction(0), Fraction(1)), (-S, S),
    (Fraction(-1), Fraction(0)), (-S, -S), (Fraction(0), Fraction(-1)), (S, -S),
]
PERTURB = [Fraction(1), Fraction(33, 32), Fraction(31, 32), Fraction(65, 64), Fraction(63, 64)]


@dataclass
class LehmerSchurResult:
    """The final disc (centre, radius), the zeros counted in it, and the work done."""

    center: Optional[complex]
    radius: Optional[Fraction]
    count: int  # zeros of p, with multiplicity, in the final open disc
    reason: str  # "converged", "no roots", "singular", "failure" or "kmax reached"
    iterations: int
    tests: int  # number of Schur-Cohn tests, including retries
    radii: List[Fraction] = field(default_factory=list)
    center_exact: Optional[GQ] = None

    @property
    def converged(self) -> bool:
        return self.reason == "converged"


def to_gq(v: Any) -> GQ:
    if isinstance(v, tuple):
        return (Fraction(v[0]), Fraction(v[1]))
    if isinstance(v, complex):
        return (Fraction(v.real), Fraction(v.imag))
    return (Fraction(v), Fraction(0))


def _mul(a: GQ, b: GQ) -> GQ:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _add(a: GQ, b: GQ) -> GQ:
    return (a[0] + b[0], a[1] + b[1])


def _sub(a: GQ, b: GQ) -> GQ:
    return (a[0] - b[0], a[1] - b[1])


def _conj(a: GQ) -> GQ:
    return (a[0], -a[1])


def _trim(p: List[GQ]) -> List[GQ]:
    while p and p[-1] == ZERO:
        p.pop()
    return p


def _primitive(p: List[GQ]) -> List[GQ]:
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


def shift_scale(p: Sequence[GQ], c: GQ, r: Fraction) -> List[GQ]:
    """Coefficients of p(c + r w), exactly."""
    q = list(p)
    n = len(q) - 1
    for i in range(n):
        for k in range(n - 1, i - 1, -1):
            q[k] = _add(q[k], _mul(c, q[k + 1]))
    s = Fraction(1)
    for k in range(n + 1):
        q[k] = (q[k][0] * s, q[k][1] * s)
        s *= r
    return q


def schur_cohn_count(p: Sequence[GQ]) -> Optional[int]:
    """Zeros of p in the open unit disc, or None when a Schur step is singular.

    The coefficients are scaled once to Gaussian integers; each transform is
    then done in integers and divided by the positive integer content.
    """
    p = _trim(_primitive(list(p)))
    a = [(int(c[0]), int(c[1])) for c in p]
    degrees, deltas = [], []
    while len(a) > 1:
        n = len(a) - 1
        (x0, y0), (xn, yn) = a[0], a[n]
        q = []
        for k in range(n + 1):
            u, v = a[k]
            w, t = a[n - k]  # p* has coefficient conj(a[n - k]) = (w, -t)
            # conj(a0) * a_k - a_n * conj(a_{n-k})
            q.append((x0 * u + y0 * v - (xn * w + yn * t), x0 * v - y0 * u - (yn * w - xn * t)))
        if q[0][0] == 0:
            return None
        degrees.append(n)
        deltas.append(q[0][0])
        while q and q[-1] == (0, 0):
            q.pop()
        g = 0
        for u, v in q:
            g = gcd(gcd(g, u), v)
        a = [(u // g, v // g) for u, v in q]
    k = 0
    for j in range(len(deltas) - 1, -1, -1):
        if deltas[j] < 0:
            k = degrees[j] - k
    return k


def _count(p: Sequence[GQ], c: GQ, r: Fraction, work: List[int]) -> Tuple[Optional[int], Fraction]:
    """Count zeros in D(c, r f) for the first factor f in PERTURB that gives a regular test."""
    for f in PERTURB:
        work[0] += 1
        k = schur_cohn_count(shift_scale(p, c, r * f))
        if k is not None:
            return k, r * f
    return None, r


def cauchy_radius(p: Sequence[GQ]) -> Fraction:
    """A power of 2 that is at least 1 + max |a_i / a_n|; every zero lies inside it."""
    an = p[-1]
    m2 = an[0] * an[0] + an[1] * an[1]
    best = Fraction(0)
    for c in p[:-1]:
        q = _mul(c, _conj(an))  # a_i / a_n = q / |a_n|^2
        best = max(best, (abs(q[0]) + abs(q[1])) / m2)  # |re| + |im| >= modulus
    b = Fraction(1)
    while b < 1 + best:
        b *= 2
    return b


def lehmer_schur(coeffs: Sequence[Any], tol: Any = Fraction(1, 2 ** 40),
                 max_iter: int = 400) -> LehmerSchurResult:
    """Find a disc of radius at most tol that contains a zero of p."""
    p = _trim([to_gq(a) for a in coeffs])
    if not p:
        raise ValueError("the zero polynomial")
    tol = Fraction(tol)
    if tol <= 0:
        raise ValueError("tol must be positive")
    if len(p) == 1:  # @line L1
        return LehmerSchurResult(None, None, 0, "no roots", 0, 0)
    c: GQ = ZERO
    r = cauchy_radius(p)
    work = [0]
    radii = [r]
    count = len(p) - 1
    for k in range(1, max_iter + 1):  # @line L2
        if r <= tol:  # @line L3
            return LehmerSchurResult(complex(c[0], c[1]), r, count, "converged", k - 1, work[0], radii, c)
        m, rh = _count(p, c, r / 2, work)  # @line L4
        if m is None:
            return LehmerSchurResult(complex(c[0], c[1]), r, count, "singular", k - 1, work[0], radii, c)
        if m >= 1:
            r, count = rh, m
            radii.append(r)
            continue
        inner = rh  # no zero in D(c, inner), so the zero is in the annulus inner <= |z - c| < r
        found = False
        for d in DIRECTIONS:  # @line L5
            cj = _add(c, (d[0] * RHO * r, d[1] * RHO * r))  # @line L6
            m, rj = _count(p, cj, BETA * r, work)
            if m is not None and m >= 1:
                c, r, count = cj, rj, m
                radii.append(r)
                found = True
                break
        if not found:  # @line L7
            return LehmerSchurResult(complex(c[0], c[1]), r, count, "failure", k, work[0], radii, c)
    return LehmerSchurResult(complex(c[0], c[1]), r, count, "kmax reached", max_iter, work[0], radii, c)  # @line L8


def poly_from_roots(roots: Sequence[Any]) -> List[GQ]:
    """Exact coefficients, constant term first, of the monic polynomial with these roots."""
    p: List[GQ] = [(Fraction(1), Fraction(0))]
    for z0 in roots:
        z = to_gq(z0)
        q = [ZERO] * (len(p) + 1)
        for i, a in enumerate(p):
            q[i + 1] = _add(q[i + 1], a)
            q[i] = _sub(q[i], _mul(z, a))
        p = q
    return p
