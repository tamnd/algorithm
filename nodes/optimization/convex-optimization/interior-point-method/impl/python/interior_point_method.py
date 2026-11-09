# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interior-point-method/. The authors are listed in prov/MYGDGH.jsonl.

"""Short-step primal-dual path-following interior-point method for linear programming.

The program is in standard form:

    minimize c^T x  subject to  A x = b,  x >= 0,
    dual: maximize b^T y  subject to  A^T y + s = c,  s >= 0.

The start (x, y, s) must be strictly feasible (x > 0, s > 0, A x = b, A^T y + s = c) and lie in the
neighborhood N2(theta) = {||X S e - mu e|| <= theta mu} with theta = 0.4 and mu = x^T s / n.
Each iteration takes one full Newton step toward the point of the central path with
parameter sigma mu, sigma = 1 - 0.4 / sqrt(n). Then mu drops by the factor sigma exactly,
the iterates stay in N2(0.4), and the duality gap x^T s = n mu falls below eps after at most
ceil(sqrt(n) / 0.4 * ln(n mu_0 / eps)) iterations.

Cost of one iteration: form A D A^T with D = X S^-1 (O(m^2 n)) and solve it (O(m^3)).
"""

import math
from dataclasses import dataclass, field

THETA = 0.4


@dataclass
class IPMResult:
    x: list[float]
    y: list[float]
    s: list[float]
    gaps: list[float] = field(default_factory=list)  # x^T s before each iteration and at the end
    points: list[tuple[list[float], list[float]]] = field(default_factory=list)  # (x, s) at each gap
    iterations: int = 0


def _solve(m: list[list[float]], r: list[float]) -> list[float]:
    """Solve m z = r by Gaussian elimination with partial pivoting. m is square and nonsingular."""
    k = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = max(range(col, k), key=lambda i: abs(a[i][col]))
        a[col], a[piv] = a[piv], a[col]
        for i in range(col + 1, k):
            f = a[i][col] / a[col][col]
            if f:
                for j in range(col, k + 1):
                    a[i][j] -= f * a[col][j]
    z = [0.0] * k
    for i in range(k - 1, -1, -1):
        z[i] = (a[i][k] - sum(a[i][j] * z[j] for j in range(i + 1, k))) / a[i][i]
    return z


def interior_point_method(
    a: list[list[float]],
    x: list[float],
    y: list[float],
    s: list[float],
    eps: float = 1e-9,
    max_iter: int = 10000,
) -> IPMResult:
    """Run the short-step path-following method from a strictly feasible start in N2(0.4).

    Returns the last iterate, with x^T s <= eps. The vectors b and c are implied by the start:
    b = A x and c = A^T y + s.
    """
    m, n = len(a), len(x)
    x, y, s = list(map(float, x)), list(map(float, y)), list(map(float, s))
    sigma = 1.0 - THETA / math.sqrt(n)  # @line L1
    res = IPMResult(x, y, s)
    for _ in range(max_iter):
        gap = sum(xi * si for xi, si in zip(x, s))
        res.gaps.append(gap)
        res.points.append((x, s))
        mu = gap / n  # @line L3
        if gap <= eps:  # @line L4
            break
        r = [sigma * mu - x[i] * s[i] for i in range(n)]  # @line L5
        d = [x[i] / s[i] for i in range(n)]
        # normal equations: (A D A^T) dy = -A S^-1 r
        mat = [[sum(a[p][j] * d[j] * a[q][j] for j in range(n)) for q in range(m)] for p in range(m)]
        rhs = [-sum(a[p][j] * r[j] / s[j] for j in range(n)) for p in range(m)]
        dy = _solve(mat, rhs)  # @line L6
        ds = [-sum(a[p][j] * dy[p] for p in range(m)) for j in range(n)]  # @line L7
        dx = [(r[j] - x[j] * ds[j]) / s[j] for j in range(n)]  # @line L8
        x = [x[j] + dx[j] for j in range(n)]  # @line L9
        y = [y[p] + dy[p] for p in range(m)]
        s = [s[j] + ds[j] for j in range(n)]
        res.iterations += 1  # @line L2
    res.x, res.y, res.s = x, y, s
    return res


def iteration_bound(n: int, mu0: float, eps: float) -> int:
    """The proved bound on the number of iterations until n mu <= eps."""
    sigma = 1.0 - THETA / math.sqrt(n)
    if n * mu0 <= eps:
        return 0
    return math.ceil(math.log(n * mu0 / eps) / -math.log(sigma))
