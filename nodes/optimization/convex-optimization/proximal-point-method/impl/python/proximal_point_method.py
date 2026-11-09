# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proximal-point-method/. The authors are listed in prov/V8N3PJ.jsonl.

"""The proximal point method for a closed proper convex function f.

    x_{k+1} = prox_{lam f}(x_k) = argmin_z  f(z) + ||z - x_k||^2 / (2 lam).

The method only needs the proximal map of f, given as a function prox(v, lam). The vector
g_{k+1} = (x_k - x_{k+1}) / lam is a subgradient of f at x_{k+1}, so it certifies accuracy:
f(x_{k+1}) - f(x*) <= ||g_{k+1}|| ||x_{k+1} - x*||. If f has a minimizer x*, then
f(x_k) - f* <= ||x_0 - x*||^2 / (2 lam k) for every k >= 1 (Guler 1991).

Cost of one iteration: one evaluation of the proximal map. The helpers below give exact proximal
maps for a convex quadratic, a shifted l1 norm, and a linear function on a box. They work with
Fraction entries as well as with floats.
"""

from dataclasses import dataclass, field


@dataclass
class ProxResult:
    x: list
    iterates: list = field(default_factory=list)  # x_0, x_1, ..., x_k
    subgradients: list = field(default_factory=list)  # g_1, ..., g_k with g_j in the subdifferential at x_j


def proximal_point_method(prox, x0, lam, eps=0, max_iter=1000) -> ProxResult:
    """Run x <- prox(x, lam) until ||g|| <= eps or max_iter steps. eps = 0 asks for an exact fixed point."""
    x = list(x0)
    res = ProxResult(x, [x])
    for _ in range(max_iter):  # @line L1
        xn = prox(x, lam)  # @line L2
        g = [(a - b) / lam for a, b in zip(x, xn)]  # @line L3
        res.iterates.append(xn)
        res.subgradients.append(g)
        x = xn  # @line L4
        if sum(v * v for v in g) <= eps * eps:  # @line L5
            break
    res.x = x
    return res  # @line L6


def _solve(m, r):
    """Gaussian elimination with pivoting on the largest entry; exact for Fraction input."""
    k = len(r)
    a = [list(row) + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = max(range(col, k), key=lambda i: abs(a[i][col]))
        a[col], a[piv] = a[piv], a[col]
        for i in range(col + 1, k):
            f = a[i][col] / a[col][col]
            for j in range(col, k + 1):
                a[i][j] -= f * a[col][j]
    x = [0] * k
    for i in range(k - 1, -1, -1):
        x[i] = (a[i][k] - sum(a[i][j] * x[j] for j in range(i + 1, k))) / a[i][i]
    return x


def prox_quadratic(q, c):
    """prox of f(x) = x^T Q x / 2 + c^T x with Q positive semidefinite: solve (I + lam Q) z = v - lam c."""
    n = len(c)

    def prox(v, lam):
        m = [[(1 if i == j else 0) + lam * q[i][j] for j in range(n)] for i in range(n)]
        return _solve(m, [v[i] - lam * c[i] for i in range(n)])

    return prox


def prox_l1(a):
    """prox of f(x) = ||x - a||_1: move each coordinate toward a_i by at most lam."""

    def prox(v, lam):
        return [ai if abs(vi - ai) <= lam else (vi - lam if vi > ai else vi + lam) for vi, ai in zip(v, a)]

    return prox


def prox_box_linear(c, lo, hi):
    """prox of f(x) = c^T x on the box lo <= x <= hi: clip v - lam c to the box."""

    def prox(v, lam):
        return [min(max(vi - lam * ci, li), ui) for vi, ci, li, ui in zip(v, c, lo, hi)]

    return prox
