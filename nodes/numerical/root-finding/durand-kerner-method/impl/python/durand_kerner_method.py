# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durand-kerner-method/. The authors are listed in prov/VNB2F0.jsonl.

"""Durand-Kerner (Weierstrass) iteration: all roots of a polynomial at once."""

import cmath
import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

U = 2.0 ** -53


@dataclass
class DurandKernerResult:
    roots: List[complex]
    iterations: int
    evaluations: int  # evaluations of p
    converged: bool
    history: List[List[complex]] = field(default_factory=list)


def horner(coeffs: Sequence[complex], z: complex):
    """Return p(z) and a running rounding bound 4 u mu (Higham, Algorithm 5.1, complex form).

    mu accumulates |z| mu + |p_k| over the Horner steps, so the bound tracks
    the sizes of the partial sums actually formed.
    """
    p = 0j
    mu = 0.0
    az = abs(z)
    for a in coeffs:
        p = p * z + a
        mu = mu * az + abs(p)
    return p, 4 * U * mu


def fujiwara_radius(coeffs: Sequence[complex]) -> float:
    """2 max |a_(n-k)/a_n|^(1/k): every root has modulus at most this."""
    n = len(coeffs) - 1
    lead = coeffs[0]
    r = 0.0
    for k in range(1, n + 1):
        c = abs(coeffs[k] / lead)
        if k == n:
            c /= 2
        if c > 0:
            r = max(r, c ** (1.0 / k))
    return 2 * r if r > 0 else 1.0


def start_points(coeffs: Sequence[complex]) -> List[complex]:
    """n points on a circle about the centroid c = -a_1/(n a_0) of the roots.

    The radius is 1.5 (|p(c)|/|a_0|)^(1/n), 1.5 times the geometric mean of
    the distances from c to the roots, capped by the Fujiwara bound; the
    angles are offset by 0.4 radians from the symmetric position.
    """
    n = len(coeffs) - 1
    c = -coeffs[1] / (n * coeffs[0])
    shifted = abs(horner(coeffs, c)[0] / coeffs[0]) ** (1.0 / n)
    r = shifted if shifted > 0 else 1.0
    r = min(1.5 * r, fujiwara_radius(coeffs) + abs(c))
    return [c + r * cmath.exp(1j * (2 * math.pi * k / n + 0.4)) for k in range(n)]


def durand_kerner(coeffs: Sequence[complex], tol: float = 1e-14, max_iter: int = 500,
                  start: Optional[Sequence[complex]] = None, keep_history: bool = False) -> DurandKernerResult:
    """All roots of p(z) = coeffs[0] z^n + ... + coeffs[n] by the Weierstrass correction.

    A root is frozen when |p(z)| is at the rounding floor of Horner's rule or
    its correction is at most tol |z|. The loop ends when all are frozen or
    after max_iter sweeps; each sweep evaluates p once at each active root.
    Raises ValueError on bad input, ArithmeticError on non-finite values or
    when two approximations coincide.
    """
    coeffs = [complex(a) for a in coeffs]
    if len(coeffs) < 2 or coeffs[0] == 0:
        raise ValueError("need degree >= 1 and a nonzero leading coefficient")
    if any(not (cmath.isfinite(a)) for a in coeffs):
        raise ArithmeticError("coefficients must be finite")
    n = len(coeffs) - 1
    lead = coeffs[0]
    if start is None:  # @line L1
        z = start_points(coeffs)
    else:
        z = [complex(s) for s in start]
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
            p, floor = horner(coeffs, z[i])  # @line L4
            evals += 1
            if abs(p) <= floor:
                active[i] = False
                continue
            d = lead  # @line L5
            for j in range(n):
                if j != i:
                    d *= z[i] - z[j]
            if d == 0:
                raise ArithmeticError("two approximations coincide")
            w = p / d  # @line L6
            new[i] = z[i] - w
            if not cmath.isfinite(new[i]):
                raise ArithmeticError("non-finite iterate")
            if abs(w) <= tol * abs(new[i]):  # @line L7
                active[i] = False
        z = new  # @line L8
        if keep_history:
            history.append(list(z))
        if not any(active):  # @line L9
            return DurandKernerResult(z, it, evals, True, history)
    return DurandKernerResult(z, max_iter, evals, False, history)  # @line L10
