# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/broyden-method/. The authors are listed in prov/MK4APS.jsonl.

"""Broyden's (good) method for F(x) = 0 with F: R^n -> R^n.

Vectors are lists and matrices are lists of rows. The code uses only
+, -, *, / and abs on the entries, so it runs on floats and also on
fractions.Fraction (exact arithmetic) when F and B0 are exact.
"""

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence

Vector = List[float]
Matrix = List[List[float]]


@dataclass
class BroydenResult:
    x: Vector
    iterations: int
    evaluations: int  # evaluations of F, including those for a difference Jacobian
    status: str  # "converged", "exact", "singular", "max-iter"
    residual: float  # max-norm of F(x)
    steps: List[float] = field(default_factory=list)  # max-norms of the steps


def norm(v: Sequence) -> float:
    return max((abs(t) for t in v), default=0)


def _finite(v) -> bool:
    return not isinstance(v, float) or math.isfinite(v)


def solve(A: Matrix, b: Vector) -> Optional[Vector]:
    """Gaussian elimination with partial pivoting; None if A is singular."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f != 0:
                for j in range(c, n + 1):
                    M[r][j] -= f * M[c][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / M[i][i]
    return x


def difference_jacobian(F: Callable[[Vector], Vector], x: Vector, Fx: Vector) -> Matrix:
    """Forward differences with h_j = sqrt(eps) (1 + |x_j|); costs n evaluations."""
    n = len(x)
    J = [[0.0] * n for _ in range(n)]
    for j in range(n):
        h = math.sqrt(2.0 ** -52) * (1 + abs(x[j]))
        xh = list(x)
        xh[j] = x[j] + h
        h = xh[j] - x[j]  # the step actually taken
        Fh = F(xh)
        for i in range(n):
            J[i][j] = (Fh[i] - Fx[i]) / h
    return J


def broyden(F: Callable[[Vector], Vector], x0: Sequence, B0: Optional[Matrix] = None,
            tol: float = 1e-12, max_iter: int = 100) -> BroydenResult:
    """Broyden's good method.

    Stops with "converged" when the step s satisfies |s| <= tol (1 + |x|)
    in the max-norm, with "exact" when F(x) = 0, with "singular" when B is
    singular, and with "max-iter" after max_iter steps. B0 defaults to a
    forward difference Jacobian at x0. Raises ArithmeticError when F returns
    a value that is not finite.
    """
    x = list(x0)
    n = len(x)
    Fx = list(F(x))  # @line L1
    evals = 1
    if not all(_finite(t) for t in Fx):
        raise ArithmeticError("F(x0) is not finite")
    steps = []
    if norm(Fx) == 0:
        return BroydenResult(x, 0, evals, "exact", 0, steps)
    if B0 is None:
        B = difference_jacobian(F, x, Fx)
        evals += n
    else:
        B = [list(r) for r in B0]
    for k in range(1, max_iter + 1):  # @line L2
        if norm(Fx) == 0:  # @line L3
            return BroydenResult(x, k - 1, evals, "exact", 0, steps)
        s = solve(B, [-t for t in Fx])  # @line L4
        if s is None:
            return BroydenResult(x, k - 1, evals, "singular", norm(Fx), steps)
        x = [a + b for a, b in zip(x, s)]  # @line L5
        Fn = list(F(x))
        evals += 1
        if not all(_finite(t) for t in Fn):
            raise ArithmeticError("F(x) is not finite at x = %r" % (x,))
        y = [a - b for a, b in zip(Fn, Fx)]  # @line L6
        Bs = [sum(B[i][j] * s[j] for j in range(n)) for i in range(n)]
        ss = sum(t * t for t in s)
        for i in range(n):
            r = (y[i] - Bs[i]) / ss
            if r != 0:
                for j in range(n):
                    B[i][j] += r * s[j]
        Fx = Fn  # @line L7
        steps.append(norm(s))
        if norm(s) <= tol * (1 + norm(x)):  # @line L8
            return BroydenResult(x, k, evals, "converged", norm(Fx), steps)
    return BroydenResult(x, max_iter, evals, "max-iter", norm(Fx), steps)  # @line L9
