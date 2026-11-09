# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ellipsoid-method/. The authors are listed in prov/S8AASR.jsonl.

"""The central-cut ellipsoid method in floating point.

An ellipsoid is E(x, P) = {z : (z - x)^T P^-1 (z - x) <= 1} with P symmetric positive
definite. The code stores a factor J with P = J J^T, so that P stays positive definite
in spite of rounding. feasible_point looks for a point of {z : A z <= b}; minimize adds
cuts on the objective. The only access to the constraints is through a separation step,
so a caller can pass any separation oracle instead of the rows of A.
"""

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

Vector = list[float]
Matrix = list[list[float]]
Oracle = Callable[[Vector], Vector | None]  # None if x is feasible, else g with g^T z < g^T x for all feasible z


@dataclass
class Result:
    status: str  # "feasible" or "empty" (the volume fell below the bound)
    x: Vector = field(default_factory=list)
    iterations: int = 0
    centers: list[Vector] = field(default_factory=list)
    shapes: list[Matrix] = field(default_factory=list)  # the matrices P of the ellipsoids, if kept


def rows_oracle(a: Sequence[Sequence[float]], b: Sequence[float], tol: float = 0.0) -> Oracle:
    """Separation for A z <= b: return the first violated row a_i (a_i^T x > b_i + tol)."""

    def oracle(x: Vector) -> Vector | None:
        for row, bi in zip(a, b):
            if sum(r * v for r, v in zip(row, x)) > bi + tol:
                return [float(r) for r in row]
        return None

    return oracle


def iteration_bound(n: int, radius: float, inner: float) -> int:
    """Iterations after which the volume ratio (inner/radius)^n is passed: 2 (n + 1) n ln(radius / inner)."""
    return math.ceil(2 * (n + 1) * n * math.log(radius / inner))


def shape(J: Matrix) -> Matrix:
    """P = J J^T."""
    n = len(J)
    return [[sum(J[i][k] * J[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def cut(x: Vector, J: Matrix, g: Vector) -> tuple[Vector, Matrix]:
    """The least-volume ellipsoid containing E(x, J J^T) intersected with {z : g^T z <= g^T x}.

    With h = J^T g / |J^T g|, the vector bt = J h is P g / sqrt(g^T P g), the new center is
    x - bt / (n + 1), and the new factor is sqrt(n^2 / (n^2 - 1)) J (I - beta h h^T) with
    (1 - beta)^2 = (n - 1) / (n + 1), so that the new P is n^2/(n^2-1) (P - 2/(n+1) bt bt^T)."""
    n = len(x)
    h = [sum(J[k][i] * g[k] for k in range(n)) for i in range(n)]
    s = math.sqrt(sum(v * v for v in h))
    if s == 0.0:
        raise ArithmeticError("the ellipsoid is too thin for floating point")
    h = [v / s for v in h]
    bt = [sum(J[i][k] * h[k] for k in range(n)) for i in range(n)]  # @line L5
    if n == 1:  # an interval: keep the half that the cut allows
        return [x[0] - bt[0] / 2], [[J[0][0] / 2]]
    x2 = [x[i] - bt[i] / (n + 1) for i in range(n)]  # @line L6
    beta = 1 - math.sqrt((n - 1) / (n + 1))
    f = n / math.sqrt(n * n - 1.0)
    J2 = [[f * (J[i][j] - beta * bt[i] * h[j]) for j in range(n)] for i in range(n)]  # @line L7
    return x2, J2


def feasible_point(oracle: Oracle, n: int, radius: float, inner: float, keep: bool = False) -> Result:
    """Find z with oracle(z) is None, if the feasible set lies in the ball of the given radius
    around 0 and contains a ball of radius inner. Otherwise report "empty"."""
    x = [0.0] * n  # @line L1
    J = [[radius * (i == j) for j in range(n)] for i in range(n)]
    res = Result("empty")
    limit = iteration_bound(n, radius, inner)
    for k in range(limit + 1):  # @line L2
        if keep:
            res.centers.append(list(x))
            res.shapes.append(shape(J))
        g = oracle(x)
        if g is None:  # @line L3
            res.status, res.x, res.iterations = "feasible", x, k
            return res
        x, J = cut(x, J, g)  # @line L4: cut with the violated inequality g^T z <= g^T x
    res.iterations = limit  # @line L8: the volume is below that of the inner ball
    return res


def minimize(c: Sequence[float], oracle: Oracle, n: int, radius: float, iterations: int) -> Result:
    """Approximately minimize c^T z over the feasible set: a feasible center gives an objective cut.

    Returns the best feasible center found, or "empty" if no center was feasible."""
    x = [0.0] * n
    J = [[radius * (i == j) for j in range(n)] for i in range(n)]
    best = Result("empty")
    value = math.inf
    for k in range(iterations):
        g = oracle(x)
        if g is None:
            v = sum(ci * xi for ci, xi in zip(c, x))
            if v < value:
                best.status, best.x, value = "feasible", list(x), v
            g = [float(ci) for ci in c]  # keep only the points with c^T z <= c^T x
            if all(t == 0 for t in g):
                break
        try:
            x, J = cut(x, J, g)
        except ArithmeticError:
            break
        best.iterations = k + 1
    return best
