# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aberth-ehrlich-method/. The authors are listed in prov/4VYZ43.jsonl.

"""Aberth-Ehrlich iteration: all roots of a polynomial at once, order 3 at simple roots."""

import cmath
import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

U = 2.0 ** -53


@dataclass
class AberthResult:
    roots: List[complex]
    iterations: int
    evaluations: int  # evaluations of p; p' is evaluated alongside, the same number of times
    converged: bool
    history: List[List[complex]] = field(default_factory=list)


def horner2(coeffs: Sequence[complex], z: complex):
    """Return p(z), p'(z) and a running rounding bound 4 u mu for p(z) (Higham, Section 5.1)."""
    p = 0j
    dp = 0j
    mu = 0.0
    az = abs(z)
    for a in coeffs:
        dp = dp * z + p
        p = p * z + a
        mu = mu * az + abs(p)
    return p, dp, 4 * U * mu


def start_points(coeffs: Sequence[complex]) -> List[complex]:
    """n points on a circle about c = -a_1/(n a_0), radius 1.5 (|p(c)|/|a_0|)^(1/n), angles offset by 0.4."""
    n = len(coeffs) - 1
    c = -coeffs[1] / (n * coeffs[0])
    r = abs(horner2(coeffs, c)[0] / coeffs[0]) ** (1.0 / n)
    r = 1.5 * r if r > 0 else 1.0
    return [c + r * cmath.exp(1j * (2 * math.pi * k / n + 0.4)) for k in range(n)]


def aberth(coeffs: Sequence[complex], tol: float = 1e-14, max_iter: int = 500,
           start: Optional[Sequence[complex]] = None, keep_history: bool = False) -> AberthResult:
    """All roots of p(z) = coeffs[0] z^n + ... + coeffs[n] by the Aberth correction.

    The correction is p/(p' - p S) with S = sum over j != i of 1/(z_i - z_j),
    the same as N/(1 - N S) with the Newton step N = p/p', but defined when
    p'(z_i) = 0. A root is frozen when |p(z_i)| is at the rounding floor of
    Horner's rule or its correction is at most tol |z_i|. Raises ValueError
    on bad input and ArithmeticError on non-finite values, coinciding
    approximations or a zero denominator.
    """
    coeffs = [complex(a) for a in coeffs]
    if len(coeffs) < 2 or coeffs[0] == 0:
        raise ValueError("need degree >= 1 and a nonzero leading coefficient")
    if any(not cmath.isfinite(a) for a in coeffs):
        raise ArithmeticError("coefficients must be finite")
    n = len(coeffs) - 1
    z = start_points(coeffs) if start is None else [complex(s) for s in start]  # @line L1
    if len(z) != n or len(set(z)) != n:
        raise ValueError("need n distinct starting points")
    active = [True] * n
    evals = 0
    history = [list(z)] if keep_history else []
    for it in range(1, max_iter + 1):  # @line L2
        new = list(z)
        for i in range(n):  # @line L3
            if not active[i]:
                continue
            p, dp, floor = horner2(coeffs, z[i])  # @line L4
            evals += 1
            if abs(p) <= floor:
                active[i] = False
                continue
            s = 0j  # @line L5
            for j in range(n):
                if j != i:
                    if z[i] == z[j]:
                        raise ArithmeticError("two approximations coincide")
                    s += 1 / (z[i] - z[j])
            den = dp - p * s  # @line L6
            if den == 0:
                raise ArithmeticError("zero denominator in the Aberth correction")
            w = p / den
            new[i] = z[i] - w
            if not cmath.isfinite(new[i]):
                raise ArithmeticError("non-finite iterate")
            if abs(w) <= tol * abs(new[i]):  # @line L7
                active[i] = False
        z = new  # @line L8
        if keep_history:
            history.append(list(z))
        if not any(active):  # @line L9
            return AberthResult(z, it, evals, True, history)
    return AberthResult(z, max_iter, evals, False, history)  # @line L10
