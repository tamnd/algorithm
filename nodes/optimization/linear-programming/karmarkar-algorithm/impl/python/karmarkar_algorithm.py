# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karmarkar-algorithm/. The authors are listed in prov/8T5Z9B.jsonl.

"""Karmarkar's projective algorithm in floating point.

The program is in Karmarkar's canonical form:

    minimize c^T x  subject to  A x = 0,  e^T x = 1,  x >= 0,

where A e = 0 (so the center e/n is feasible) and the optimal value is 0. Each step
maps the current point x to the center of the simplex with the projective map
y = X^-1 x / (e^T X^-1 x), takes a step of length alpha * r against the projected
cost in the ball of radius r = 1/sqrt(n(n-1)) inside the simplex, and maps back.
The potential n ln(c^T x) - sum ln x_j drops by at least 1/8 per step for alpha = 1/4.
"""

import math
from dataclasses import dataclass, field
from typing import Sequence

Vector = list[float]


@dataclass
class Result:
    # "optimal": c^T x <= eps c^T x0. "constant": c^T x has the same positive value on all the
    # feasible set, so the optimal value is not 0 and the input is not in canonical form.
    status: str
    x: Vector
    iterations: int
    values: list[float] = field(default_factory=list)  # c^T x after each step, the start first
    potentials: list[float] = field(default_factory=list)


def potential(c: Sequence[float], x: Sequence[float]) -> float:
    """Karmarkar's potential n ln(c^T x) - sum_j ln x_j."""
    return len(x) * math.log(sum(ci * xi for ci, xi in zip(c, x))) - sum(math.log(v) for v in x)


def project_out(rows: list[Vector], v: Vector, tol: float = 1e-12) -> Vector:
    """The projection of v onto the null space of the rows (Gram-Schmidt, two passes)."""
    basis: list[Vector] = []
    for row in rows:
        w = list(row)
        for _ in range(2):
            for q in basis:
                d = sum(a * b for a, b in zip(q, w))
                w = [a - d * b for a, b in zip(w, q)]
        s = math.sqrt(sum(a * a for a in w))
        if s > tol * max(1.0, math.sqrt(sum(a * a for a in row))):
            basis.append([a / s for a in w])
    p = list(v)
    for _ in range(2):
        for q in basis:
            d = sum(a * b for a, b in zip(q, p))
            p = [a - d * b for a, b in zip(p, q)]
    return p


def step_bound(n: int, eps: float, delta: float = 0.125) -> int:
    """Steps after which c^T x <= eps c^T x0 is sure: n ln(1/eps) / delta."""
    return math.ceil(n * math.log(1 / eps) / delta)


def karmarkar_algorithm(
    a: Sequence[Sequence[float]], c: Sequence[float], eps: float = 1e-8, alpha: float = 0.25
) -> Result:
    n = len(c)
    x = [1.0 / n] * n  # @line L1
    r = 1.0 / math.sqrt(n * (n - 1))
    start = sum(ci * xi for ci, xi in zip(c, x))
    res = Result("optimal", x, 0, [start], [potential(c, x)] if start > 0 else [])
    for k in range(step_bound(n, eps)):
        value = sum(ci * xi for ci, xi in zip(c, x))
        if value <= eps * start:  # @line L2
            break
        cbar = [ci * xi for ci, xi in zip(c, x)]  # @line L3: X c and B = [A X; e^T]
        rows = [[aij * xj for aij, xj in zip(row, x)] for row in a] + [[1.0] * n]
        p = project_out(rows, cbar)  # @line L4
        norm = math.sqrt(sum(v * v for v in p))
        if norm <= 1e-15 * math.sqrt(sum(v * v for v in cbar)):  # @line L5
            res.status = "constant"
            break
        y = [1.0 / n - alpha * r * v / norm for v in p]  # @line L6
        s = sum(xj * yj for xj, yj in zip(x, y))
        x = [xj * yj / s for xj, yj in zip(x, y)]  # @line L7
        res.iterations = k + 1
        res.values.append(sum(ci * xi for ci, xi in zip(c, x)))
        res.potentials.append(potential(c, x))
    res.x = x  # @line L8
    return res
