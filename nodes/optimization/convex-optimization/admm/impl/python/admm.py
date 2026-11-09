# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/admm/. The authors are listed in prov/N7GCD0.jsonl.

"""The alternating direction method of multipliers (ADMM), scaled form.

    minimize f(x) + g(z)  subject to  A x + B z = c.

With the scaled multiplier u = y / rho, one iteration is

    x <- argmin_x f(x) + (rho/2) ||A x + B z - c + u||^2
    z <- argmin_z g(z) + (rho/2) ||A x + B z - c + u||^2
    u <- u + (A x + B z - c).

The primal residual is r = A x + B z - c and the dual residual is s = rho A^T B (z - z_old).
For closed proper convex f and g with a saddle point (x*, z*, y*), the averages of the first K
iterates satisfy |f + g - p*| = O(1/K) and ||A x + B z - c|| = O(1/K), and
V_k = ||y_k - y*||^2 / rho + rho ||B (z_k - z*)||^2 does not increase.

Cost of one iteration: one x-minimization, one z-minimization and O(size of A and B) for the
residuals and the update.
"""

from dataclasses import dataclass, field


@dataclass
class ADMMResult:
    x: list
    z: list
    y: list
    steps: list = field(default_factory=list)  # (x_k, z_k, u_k, r_k) for k = 1, 2, ...


def matvec(m, v):
    return [sum(p * q for p, q in zip(row, v)) for row in m]


def admm(x_step, z_step, a, b, c, z0, u0, rho, eps=0, max_iter=1000) -> ADMMResult:
    """x_step(z, u, rho) and z_step(x, u, rho) solve the two subproblems. Stops when ||r||, ||s|| <= eps."""
    z, u = list(z0), list(u0)
    x = None
    res = ADMMResult(x, z, [rho * ui for ui in u])
    for _ in range(max_iter):  # @line L1
        x = x_step(z, u, rho)  # @line L2
        z_old = z  # @line L3
        z = z_step(x, u, rho)  # @line L4
        r = [p + q - ci for p, q, ci in zip(matvec(a, x), matvec(b, z), c)]  # @line L5
        u = [ui + ri for ui, ri in zip(u, r)]  # @line L6
        bdz = matvec(b, [p - q for p, q in zip(z, z_old)])
        s = [rho * sum(a[i][j] * bdz[i] for i in range(len(a))) for j in range(len(x))]  # @line L7
        res.steps.append((x, z, u, r))
        if sum(v * v for v in r) <= eps * eps and sum(v * v for v in s) <= eps * eps:  # @line L8
            break
    res.x, res.z, res.y = x, z, [rho * ui for ui in u]
    return res  # @line L9


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


def box_qp_steps(p, q, lo, hi):
    """Splitting of min x^T P x / 2 + q^T x s.t. lo <= x <= hi as f(x) + g(z), x - z = 0 (A = I, B = -I, c = 0)."""
    n = len(q)

    def x_step(z, u, rho):  # (P + rho I) x = -q + rho (z - u)
        mat = [[p[i][j] + (rho if i == j else 0) for j in range(n)] for i in range(n)]
        return solve(mat, [-q[i] + rho * (z[i] - u[i]) for i in range(n)])

    def z_step(x, u, rho):  # projection of x + u onto the box
        return [min(max(xi + ui, l), h) for xi, ui, l, h in zip(x, u, lo, hi)]

    return x_step, z_step


def standard_lp_steps(a, b, c):
    """Splitting of min c^T x s.t. A x = b, x >= 0 as f(x) = c^T x + [A x = b], g(z) = [z >= 0], x - z = 0."""
    m, n = len(b), len(c)

    def x_step(z, u, rho):  # [rho I  A^T; A  0] [x; w] = [rho (z - u) - c; b]
        mat = [[(rho if i == j else 0) for j in range(n)] + [a[k][i] for k in range(m)] for i in range(n)]
        mat += [list(a[k]) + [0] * m for k in range(m)]
        return solve(mat, [rho * (z[i] - u[i]) - c[i] for i in range(n)] + list(b))[:n]

    def z_step(x, u, rho):  # projection of x + u onto the nonnegative orthant
        return [max(xi + ui, 0) for xi, ui in zip(x, u)]

    return x_step, z_step
