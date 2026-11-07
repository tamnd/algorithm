# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laguerre-method/. The authors are listed in prov/K13QF2.jsonl.

"""Laguerre's method for one root of a polynomial, and all roots with deflation."""

import cmath
import math
from dataclasses import dataclass
from typing import List, Sequence

U = 2.0 ** -53  # unit roundoff of binary64


@dataclass
class LaguerreResult:
    """The returned point, why the loop ended, and the work done."""

    root: complex
    reason: str  # "root", "residual", "converged", "failure" or "kmax reached"
    iterations: int
    evaluations: int  # Horner sweeps, each giving p, p' and p''

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "residual", "converged")


def horner2(coeffs: Sequence[complex], x: complex):
    """Return p(x), p'(x), p''(x) and sum |a_j| |x|^j in one sweep.

    coeffs lists a_n, ..., a_0 from the leading coefficient down.
    """
    p = coeffs[0]
    d = dd = 0
    s = abs(coeffs[0])
    ax = abs(x)
    for c in coeffs[1:]:
        dd = dd * x + d
        d = d * x + p
        p = p * x + c
        s = s * ax + abs(c)
    return p, d, 2 * dd, s


def _finite(v) -> bool:
    return cmath.isfinite(complex(v))


def laguerre(coeffs: Sequence[complex], x0: complex, tol_abs: float = 0.0,
             tol_rel: float = 2.0 ** -50, max_iter: int = 100) -> LaguerreResult:
    """Run Laguerre's method on the polynomial with coefficients a_n..a_0.

    Precondition: degree n >= 1 and a_n != 0; tol_abs >= 0, tol_rel >= 0;
    max_iter >= 1. Cost per pass: one Horner sweep of about 3n complex
    multiply-adds and one complex square root.
    """
    n = len(coeffs) - 1
    if n < 1 or coeffs[0] == 0:
        raise ValueError("need a polynomial of degree at least 1")
    x = complex(x0)  # @line L1
    for k in range(1, max_iter + 1):  # @line L2
        p, d1, d2, s = horner2(coeffs, x)  # @line L3
        if p == 0:  # @line L4
            return LaguerreResult(x, "root", k, k)
        if not (_finite(p) and _finite(d1) and _finite(d2)):
            return LaguerreResult(x, "failure", k, k)
        if abs(p) <= 8 * n * U * s:  # @line L5
            return LaguerreResult(x, "residual", k, k)
        g = d1 / p  # @line L6
        h = g * g - d2 / p
        r = cmath.sqrt((n - 1) * (n * h - g * g))  # @line L7
        dp, dm = g + r, g - r  # @line L8
        den = dp if abs(dp) >= abs(dm) else dm
        if not _finite(den):
            return LaguerreResult(x, "failure", k, k)
        if den == 0:  # @line L9
            # p' = p'' = 0 here: take a fixed-size step in a varying direction
            a = (1 + abs(x)) * cmath.exp(1j * k)
        else:
            a = n / den  # @line L10
        x_new = x - a
        if not _finite(x_new):
            return LaguerreResult(x, "failure", k, k)
        if abs(a) <= tol_abs + tol_rel * abs(x_new):  # @line L11
            return LaguerreResult(x_new, "converged", k, k)
        x = x_new
    return LaguerreResult(x, "kmax reached", max_iter, max_iter)  # @line L12


def deflate(coeffs: Sequence[complex], z: complex) -> List[complex]:
    """Divide by (x - z) with synthetic division and drop the remainder."""
    out = [coeffs[0]]
    for c in coeffs[1:-1]:
        out.append(out[-1] * z + c)
    return out


def laguerre_all_roots(coeffs: Sequence[complex], polish: bool = True,
                       max_iter: int = 100) -> List[complex]:
    """All n roots: Laguerre from 0 on the deflated polynomials, then polish.

    Each root found on a deflated polynomial is refined by a few Laguerre
    steps on the original polynomial, which removes most of the error that
    deflation introduces. Cost: O(n^2) per sweep of passes over all roots.
    """
    coeffs = [complex(c) for c in coeffs]
    work = list(coeffs)
    roots = []
    while len(work) > 1:
        r = laguerre(work, 0.0, max_iter=max_iter)
        z = r.root
        if polish:
            z = laguerre(coeffs, z, max_iter=10).root
        roots.append(z)
        work = deflate(work, z)
    return roots
