# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-method-for-systems/. The authors are listed in prov/EB6BTR.jsonl.

"""Newton's method for F(x) = 0 with F from R^n to R^n: solve J(x) s = -F(x), x <- x + s."""

import math
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence


@dataclass
class NewtonSystemResult:
    """The returned point, why the loop ended, and the work done."""

    x: List[Any]
    reason: str  # "root", "converged", "singular", "failure" or "kmax reached"
    iterations: int
    f_evals: int
    j_evals: int
    steps: List[Any] = field(default_factory=list)  # infinity norms of the steps

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "converged")


def _finite(v: Any) -> bool:
    return math.isfinite(float(v))


def norm_inf(v: Sequence[Any]) -> Any:
    return max((abs(t) for t in v), default=0)


def solve(a: Sequence[Sequence[Any]], b: Sequence[Any]) -> Optional[List[Any]]:
    """Solve a s = b by Gaussian elimination with partial pivoting.

    Returns None when a pivot is exactly zero, that is when the matrix is
    singular (exactly, for Fraction entries) or numerically singular to the
    point of a zero pivot. Cost: about 2n^3/3 multiplications.
    """
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            return None
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        for r in range(c + 1, n):
            t = m[r][c] / piv
            if t != 0:
                row_r, row_c = m[r], m[c]
                for j in range(c, n + 1):
                    row_r[j] -= t * row_c[j]
    s = [0] * n
    for i in range(n - 1, -1, -1):
        acc = m[i][n]
        for j in range(i + 1, n):
            acc -= m[i][j] * s[j]
        s[i] = acc / m[i][i]
    return s


def newton_system(F: Callable[[List[Any]], Sequence[Any]],
                  J: Callable[[List[Any]], Sequence[Sequence[Any]]],
                  x0: Sequence[Any], tol_abs: float = 0.0,
                  tol_rel: float = 2.0 ** -50,
                  max_iter: int = 100) -> NewtonSystemResult:
    """Run Newton's method on F from x0, with the Jacobian J.

    Works for float and fractions.Fraction entries. Precondition: tol_abs >= 0,
    tol_rel >= 0, not both zero, max_iter >= 1. Convergence is guaranteed
    only near a root where J is nonsingular and Lipschitz. Cost per pass: one
    call of F, one of J and one linear solve of O(n^3) operations.
    """
    x = list(x0)  # @line L1
    fe = je = 0
    steps: List[Any] = []
    for k in range(1, max_iter + 1):  # @line L2
        fx = list(F(x))  # @line L3
        fe += 1
        if all(t == 0 for t in fx):  # @line L4
            return NewtonSystemResult(x, "root", k, fe, je, steps)
        if not all(_finite(t) for t in fx):  # @line L5
            return NewtonSystemResult(x, "failure", k, fe, je, steps)
        a = J(x)  # @line L6
        je += 1
        if not all(_finite(t) for row in a for t in row):
            return NewtonSystemResult(x, "failure", k, fe, je, steps)
        s = solve(a, [-t for t in fx])  # @line L7
        if s is None or not all(_finite(t) for t in s):
            return NewtonSystemResult(x, "singular", k, fe, je, steps)
        x_new = [xi + si for xi, si in zip(x, s)]  # @line L8
        if not all(_finite(t) for t in x_new):  # @line L9
            return NewtonSystemResult(x, "failure", k, fe, je, steps)
        ns = norm_inf(s)
        steps.append(ns)
        if ns <= tol_abs + tol_rel * norm_inf(x_new):  # @line L10
            return NewtonSystemResult(x_new, "converged", k, fe, je, steps)
        x = x_new  # @line L11
    return NewtonSystemResult(x, "kmax reached", max_iter, fe, je, steps)  # @line L12


def forward_difference_jacobian(F: Callable[[List[float]], Sequence[float]],
                                h_rel: float = 2.0 ** -26):
    """Return a function x -> forward-difference Jacobian of F at x.

    Each call evaluates F n + 1 times; column j uses the step
    h_j = h_rel * max(|x_j|, 1), the square root of the unit roundoff by
    default. The counter attribute .calls counts the evaluations of F.
    """
    def jac(x: List[float]) -> List[List[float]]:
        n = len(x)
        f0 = list(F(x))
        jac.calls += 1
        cols = []
        for j in range(n):
            h = h_rel * max(abs(x[j]), 1.0)
            xp = list(x)
            xp[j] = x[j] + h
            h = xp[j] - x[j]
            fj = list(F(xp))
            jac.calls += 1
            cols.append([(fj[i] - f0[i]) / h for i in range(len(f0))])
        return [[cols[j][i] for j in range(n)] for i in range(len(f0))]

    jac.calls = 0
    return jac
