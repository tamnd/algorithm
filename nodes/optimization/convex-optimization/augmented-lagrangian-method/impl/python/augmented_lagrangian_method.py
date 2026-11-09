# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/augmented-lagrangian-method/. The authors are listed in prov/27GRBM.jsonl.

"""The augmented Lagrangian method (method of multipliers) for an equality-constrained convex problem.

    minimize f(x)  subject to  A x = b.

The augmented Lagrangian is L_rho(x, y) = f(x) + y^T (A x - b) + (rho / 2) ||A x - b||^2.
One iteration minimizes L_rho over x for the current y, then sets y <- y + rho (A x - b).

The new x minimizes the ordinary Lagrangian f(x) + y^T (A x - b) at the new y, so the dual value
d(y) = f(x) + y^T (A x - b) is known exactly after each step. The y-sequence is the proximal point
method on -d, which gives, for each dual optimal y*,
    d* - d(y_k) <= ||y_0 - y*||^2 / (2 rho k)   and   ||A x_k - b|| <= ||y_0 - y*|| / (rho sqrt(k)).

Cost of one iteration: one minimization of L_rho. For a quadratic f(x) = x^T Q x / 2 + c^T x it is
one linear solve with Q + rho A^T A, which is the same matrix at every step.
"""

from dataclasses import dataclass, field


@dataclass
class ALMResult:
    x: list
    y: list
    steps: list = field(default_factory=list)  # (x_k, y_k, r_k) for k = 1, 2, ...


def augmented_lagrangian_method(argmin_aug, a, b, y0, rho, eps=0, max_iter=1000) -> ALMResult:
    """argmin_aug(y, rho) returns a minimizer over x of L_rho(x, y). Stops when ||A x - b|| <= eps."""
    y = list(y0)
    x = None
    res = ALMResult(x, y)
    for _ in range(max_iter):  # @line L1
        x = argmin_aug(y, rho)  # @line L2
        r = [sum(aij * xj for aij, xj in zip(row, x)) - bi for row, bi in zip(a, b)]  # @line L3
        y = [yi + rho * ri for yi, ri in zip(y, r)]  # @line L4
        res.steps.append((x, y, r))
        if sum(v * v for v in r) <= eps * eps:  # @line L5
            break
    res.x, res.y = x, y
    return res  # @line L6


def solve(m, r):
    """Gaussian elimination with pivoting on the largest entry; exact for Fraction input."""
    k = len(r)
    t = [list(row) + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = max(range(col, k), key=lambda i: abs(t[i][col]))
        if t[piv][col] == 0:
            raise ValueError("singular matrix")
        t[col], t[piv] = t[piv], t[col]
        for i in range(col + 1, k):
            f = t[i][col] / t[col][col]
            for j in range(col, k + 1):
                t[i][j] -= f * t[col][j]
    x = [0] * k
    for i in range(k - 1, -1, -1):
        x[i] = (t[i][k] - sum(t[i][j] * x[j] for j in range(i + 1, k))) / t[i][i]
    return x


def quadratic_argmin(q, c, a, b):
    """The x-step for f(x) = x^T Q x / 2 + c^T x: solve (Q + rho A^T A) x = -c - A^T y + rho A^T b."""
    n, m = len(c), len(b)

    def argmin_aug(y, rho):
        mat = [[q[i][j] + rho * sum(a[k][i] * a[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
        rhs = [-c[i] - sum(a[k][i] * (y[k] - rho * b[k]) for k in range(m)) for i in range(n)]
        return solve(mat, rhs)

    return argmin_aug
