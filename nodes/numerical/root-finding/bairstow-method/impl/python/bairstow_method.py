# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bairstow-method/. The authors are listed in prov/J2HSDJ.jsonl.

"""Bairstow's method: Newton's method on the remainder of p modulo x^2 - u x - v.

Coefficients are real and listed highest degree first: a[0] x^n + ... + a[n].
"""

import cmath
import math
import random
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple


@dataclass
class FactorResult:
    u: float
    v: float
    quotient: List[float]  # b_0, ..., b_(n-2): p = (x^2 - u x - v) q + remainder
    iterations: int
    evaluations: int  # passes of the double synthetic division
    status: str  # "converged", "exact", "singular", "max-iter"
    # "converged": the step test held, or the remainder is below its rounding floor


@dataclass
class RootsResult:
    roots: List[complex]
    factors: List[Tuple[float, float]] = field(default_factory=list)
    evaluations: int = 0
    restarts: int = 0
    status: str = "converged"  # or "failed"


def divide(a: Sequence[float], u: float, v: float) -> List[float]:
    """b_k = a_k + u b_(k-1) + v b_(k-2): p = (x^2 - u x - v)(b_0 x^(n-2) + ... + b_(n-2)) + b_(n-1)(x - u) + b_n."""
    b = []
    b1 = b2 = 0.0
    for ak in a:
        bk = ak + u * b1 + v * b2
        b.append(bk)
        b1, b2 = bk, b1
    return b


def remainder_floor(a: Sequence[float], u: float, v: float) -> Tuple[float, float]:
    """Running bounds gamma * mu_k for the rounding in b_(n-1) and b_n, with
    mu_k = |a_k| + |u| mu_(k-1) + |v| mu_(k-2) and gamma = 4 (n + 1) 2^-53."""
    m1 = m2 = 0.0
    mus = []
    for ak in a:
        mk = abs(ak) + abs(u) * m1 + abs(v) * m2
        mus.append(mk)
        m1, m2 = mk, m1
    gamma = 4 * len(a) * 2.0 ** -53
    return gamma * mus[-2], gamma * mus[-1]


def quadratic_roots(u: float, v: float) -> List[complex]:
    """Roots of x^2 - u x - v, computed without cancellation."""
    disc = u * u + 4 * v
    if disc >= 0:
        x1 = (u + math.copysign(math.sqrt(disc), u)) / 2
        x2 = -v / x1 if x1 != 0 else 0.0
        return [complex(x1), complex(x2)]
    im = math.sqrt(-disc) / 2
    return [complex(u / 2, im), complex(u / 2, -im)]


def find_factor(a: Sequence[float], u: float, v: float, tol: float = 1e-14,
                max_iter: int = 100) -> FactorResult:
    """Newton's method on (b_(n-1), b_n) as functions of (u, v). Needs deg p >= 3."""
    n = len(a) - 1
    if n < 3:
        raise ValueError("find_factor needs degree at least 3")
    evals = 0
    for k in range(1, max_iter + 1):  # @line L1
        b = divide(a, u, v)  # @line L2
        evals += 1
        if b[n - 1] == 0 and b[n] == 0:  # @line L3
            return FactorResult(u, v, b[:n - 1], k - 1, evals, "exact")
        f1, f0 = remainder_floor(a, u, v)
        if abs(b[n - 1]) <= f1 and abs(b[n]) <= f0:
            return FactorResult(u, v, b[:n - 1], k - 1, evals, "converged")
        c = divide(b[:n], u, v)  # @line L4
        det = c[n - 2] * c[n - 2] - c[n - 1] * c[n - 3]  # @line L5
        if det == 0 or not math.isfinite(det):
            return FactorResult(u, v, b[:n - 1], k - 1, evals, "singular")
        du = (b[n] * c[n - 3] - b[n - 1] * c[n - 2]) / det  # @line L6
        dv = (b[n - 1] * c[n - 1] - b[n] * c[n - 2]) / det
        u, v = u + du, v + dv  # @line L7
        if not (math.isfinite(u) and math.isfinite(v)):
            return FactorResult(u, v, b[:n - 1], k, evals, "singular")
        if abs(du) + abs(dv) <= tol * (1 + abs(u) + abs(v)):  # @line L8
            b = divide(a, u, v)
            evals += 1
            return FactorResult(u, v, b[:n - 1], k, evals, "converged")
    b = divide(a, u, v)
    return FactorResult(u, v, b[:n - 1], max_iter, evals + 1, "max-iter")  # @line L9


def cauchy_radius(a: Sequence[float]) -> float:
    return 1 + max(abs(x / a[0]) for x in a[1:])


def bairstow_roots(coeffs: Sequence[float], tol: float = 1e-14, max_iter: int = 100,
                   max_restarts: int = 30, seed: int = 1) -> RootsResult:
    """All roots of a real polynomial by Bairstow's method with deflation.

    The first start is Lin's (u, v) = (-a_(n-1)/a_(n-2), -a_n/a_(n-2)); a
    failed factor search restarts from pseudo-random starts inside the
    Cauchy radius, at most max_restarts times per factor.
    """
    a = [float(x) for x in coeffs]
    if not all(math.isfinite(x) for x in a):
        raise ValueError("coefficients must be finite")
    while a and a[0] == 0:
        a.pop(0)
    if len(a) == 0:
        raise ValueError("the zero polynomial has every number as a root")
    rng = random.Random(seed)
    out = RootsResult([])
    while len(a) - 1 >= 3:  # @line L10
        n = len(a) - 1
        if a[n - 2] != 0:
            u, v = -a[n - 1] / a[n - 2], -a[n] / a[n - 2]
        else:
            u, v = 0.0, 0.0
        r = cauchy_radius(a)
        for attempt in range(max_restarts + 1):
            res = find_factor(a, u, v, tol, max_iter)
            out.evaluations += res.evaluations
            if res.status in ("converged", "exact"):
                break
            out.restarts += 1
            z = cmath.rect(r * rng.random(), math.pi * rng.random())
            u, v = 2 * z.real, -abs(z) ** 2
        else:
            out.status = "failed"
            return out
        out.factors.append((res.u, res.v))
        out.roots.extend(quadratic_roots(res.u, res.v))  # @line L11
        a = res.quotient  # @line L12
    if len(a) == 3:  # @line L13
        out.roots.extend(quadratic_roots(-a[1] / a[0], -a[2] / a[0]))
    elif len(a) == 2:
        out.roots.append(complex(-a[1] / a[0]))
    return out
