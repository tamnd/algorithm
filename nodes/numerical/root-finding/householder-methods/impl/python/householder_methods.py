# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/householder-methods/. The authors are listed in prov/M9RH7W.jsonl.

"""Householder's method of order d + 1: x <- x + d (1/f)^(d-1)(x) / (1/f)^(d)(x).

The derivatives of 1/f are never formed directly. With the Taylor
coefficients a_j = f^(j)(x) / j! the scaled coefficients
beta_n = f(x)^(n+1) (1/f)^(n)(x) / n! satisfy

    beta_0 = 1,   beta_n = -sum_{j=1..n} a_j a_0^(j-1) beta_(n-j),

which has no division, and the step is a_0 beta_(d-1) / beta_d.
d = 1 is Newton's method and d = 2 is Halley's method.

The code works with float, and also with decimal.Decimal or
fractions.Fraction when derivs returns such values.
"""

import math
from dataclasses import dataclass, field
from typing import Callable, List, Sequence


@dataclass
class HouseholderResult:
    root: object
    iterations: int
    evaluations: int  # calls of derivs; each call gives f, f', ..., f^(d)
    status: str  # "converged", "exact", "stalled", "zero-denominator", "max-iter"
    iterates: List[object] = field(default_factory=list)

    @property
    def converged(self) -> bool:
        return self.status in ("converged", "exact")


def _finite(v) -> bool:
    return not isinstance(v, float) or math.isfinite(v)


def householder_step(values: Sequence, d: int):
    """Return (a_0, beta_(d-1), beta_d) from f, f', ..., f^(d) at one point."""
    a = []
    fact = 1
    for j in range(d + 1):
        if j > 0:
            fact *= j
        a.append(values[j] / fact)
    beta = [1]
    for n in range(1, d + 1):
        acc = 0
        p = 1  # a_0^(j-1)
        for j in range(1, n + 1):
            acc += a[j] * p * beta[n - j]
            p *= a[0]
        beta.append(-acc)
    return a[0], beta[d - 1], beta[d]


def householder(derivs: Callable[[object], Sequence], x0, d: int = 2,
                tol=1e-14, max_iter: int = 100) -> HouseholderResult:
    """Run Householder's method of order d + 1 from x0.

    derivs(x) must return at least d + 1 values f(x), f'(x), ..., f^(d)(x).
    Stops with "converged" when the step is at most tol (1 + |x|), with
    "exact" when f(x) = 0, with "stalled" when the step is 0 although
    f(x) != 0, with "zero-denominator" when beta_d = 0, and with
    "max-iter" after max_iter steps. Raises ArithmeticError when a value
    or the step is not finite.
    """
    if d < 1:
        raise ValueError("d must be at least 1")
    x = x0
    iterates = [x]
    evals = 0
    for k in range(1, max_iter + 1):  # @line L1
        values = derivs(x)  # @line L2
        evals += 1
        if len(values) < d + 1:
            raise ValueError("derivs must return f, f', ..., f^(d)")
        if not all(_finite(v) for v in values[:d + 1]):
            raise ArithmeticError("non-finite value at x = %r" % (x,))
        if values[0] == 0:  # @line L3
            return HouseholderResult(x, k - 1, evals, "exact", iterates)
        a0, b_prev, b_d = householder_step(values, d)  # @line L4
        if b_d == 0:  # @line L5
            return HouseholderResult(x, k - 1, evals, "zero-denominator", iterates)
        s = a0 * b_prev / b_d  # @line L6
        if not _finite(s):
            raise ArithmeticError("non-finite step at x = %r" % (x,))
        if s == 0:
            return HouseholderResult(x, k - 1, evals, "stalled", iterates)
        x = x + s  # @line L7
        iterates.append(x)
        if abs(s) <= tol * (1 + abs(x)):  # @line L8
            return HouseholderResult(x, k, evals, "converged", iterates)
    return HouseholderResult(x, max_iter, evals, "max-iter", iterates)  # @line L9


def poly_derivs(coeffs: Sequence, d: int) -> Callable[[object], List]:
    """Return derivs(x) = [p(x), p'(x), ..., p^(d)(x)] for p with coefficients
    coeffs, highest degree first, by repeated Horner division."""
    cs = list(coeffs)

    def derivs(x):
        b = list(cs)
        out = []
        fact = 1
        for j in range(d + 1):
            if j > 0:
                fact *= j
            if len(b) == 0:
                out.append(0 * x)
                continue
            acc = 0 * x
            nb = []
            for c in b:
                acc = acc * x + c
                nb.append(acc)
            out.append(fact * nb[-1])  # j! times the j-th Taylor coefficient
            b = nb[:-1]
        return out

    return derivs
