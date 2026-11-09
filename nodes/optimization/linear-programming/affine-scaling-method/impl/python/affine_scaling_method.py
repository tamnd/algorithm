# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-scaling-method/. The authors are listed in prov/CWE5Y6.jsonl.

"""The primal affine scaling method (Dikin's method) in floating point.

The program is in standard form: minimize c^T x subject to A x = b, x >= 0. The method
starts at an interior point x > 0 with A x = b. With X = diag(x), the dual estimate y
solves the weighted least squares problem min |X (c - A^T y)|, the reduced costs are
r = c - A^T y, and the step direction is d = -X^2 r. The step goes a fraction gamma of
the way to the boundary of x >= 0. The value c^T x falls at every step, by |X r|^2
times the step length.
"""

import math
from dataclasses import dataclass, field
from typing import Sequence

Vector = list[float]


@dataclass
class Result:
    status: str  # "optimal", "unbounded" or "limit"
    x: Vector
    y: Vector
    iterations: int
    values: list[float] = field(default_factory=list)  # c^T x at each iterate, the start first
    gap: float = math.inf  # x^T r = c^T x - b^T y when the stop test holds
    ray: Vector = field(default_factory=list)  # d >= 0 with A d = 0 and c^T d < 0, if unbounded


def dot(u: Sequence[float], v: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(u, v))


def weighted_projection(rows: list[Vector], v: Vector, tol: float = 1e-11) -> tuple[Vector, Vector]:
    """Return (p, y) with p = v - sum_k y_k rows[k] orthogonal to every row.

    Gram-Schmidt in two passes; the coefficients of each orthonormal vector over the
    rows are kept, so that y comes out at the same time. Dependent rows are skipped."""
    m = len(rows)
    basis: list[tuple[Vector, Vector]] = []
    for k, row in enumerate(rows):
        w, t = list(row), [0.0] * m
        t[k] = 1.0
        for _ in range(2):
            for q, tq in basis:
                d = dot(q, w)
                w = [a - d * b for a, b in zip(w, q)]
                t = [a - d * b for a, b in zip(t, tq)]
        s = math.sqrt(dot(w, w))
        if s > tol * max(1.0, math.sqrt(dot(row, row))):
            basis.append(([a / s for a in w], [a / s for a in t]))
    p, y = list(v), [0.0] * m
    for _ in range(2):
        for q, tq in basis:
            d = dot(q, p)
            p = [a - d * b for a, b in zip(p, q)]
            y = [a + d * b for a, b in zip(y, tq)]
    return p, y


def affine_scaling_method(
    a: Sequence[Sequence[float]],
    c: Sequence[float],
    x: Sequence[float],
    gamma: float = 2 / 3,
    eps: float = 1e-9,
    max_iter: int = 1000,
    ray_tol: float = 1e-12,
) -> Result:
    """Run from the interior point x (x > 0 and A x = b) until x^T r <= eps (1 + |c^T x|)
    with r >= -eps, where r = c - A^T y."""
    x = [float(v) for v in x]  # @line L1
    n = len(x)
    res = Result("limit", x, [], 0, [dot(c, x)])
    for k in range(max_iter):  # @line L2
        rows = [[aij * xj for aij, xj in zip(row, x)] for row in a]
        xr, y = weighted_projection(rows, [ci * xi for ci, xi in zip(c, x)])  # @line L3: X r with y
        r = [c[j] - sum(a[i][j] * y[i] for i in range(len(a))) for j in range(n)]  # @line L4
        gap = dot(x, r)
        if min(r) >= -eps and gap <= eps * (1 + abs(dot(c, x))):  # @line L5
            res.status, res.y, res.gap = "optimal", y, gap
            break
        d = [-xj * v for xj, v in zip(x, xr)]  # @line L6: d = -X^2 r
        # @line L7: if X r <= 0, then d >= 0, c^T d = -|X r|^2 < 0 and x + t d >= 0 for all t.
        # In floats the coordinates that tend to 0 keep tiny positive x_j r_j, so test X r <= ray_tol |X r|.
        if max(xr) <= ray_tol * math.sqrt(dot(xr, xr)):
            res.status, res.y, res.ray = "unbounded", y, d
            break
        step = gamma / max(v for v in xr)  # @line L8: max x_j r_j > 0; x_j + step d_j >= (1 - gamma) x_j
        x = [xj + step * dj for xj, dj in zip(x, d)]
        res.iterations = k + 1
        res.values.append(dot(c, x))
    res.x = x
    return res
